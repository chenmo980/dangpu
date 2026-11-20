using Pawnshop.Core;

// 《掌眼·当铺》M0 原型 —— 控制台可玩循环
// 用法：PawnshopM0.exe          交互模式
//       PawnshopM0.exe --sim 30 --seed 7   自动模拟 30 天（平衡性验证）

Console.OutputEncoding = System.Text.Encoding.UTF8;
Console.Title = "掌眼·当铺 M0";

var csv = Path.Combine(AppContext.BaseDirectory, "item_catalog.csv");
if (!File.Exists(csv)) csv = Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "item_catalog.csv");
var catalog = ItemCatalog.Load(csv);

int? seed = null;
var simDays = 0;
for (int i = 0; i < args.Length; i++)
{
    if (args[i] == "--sim" && i + 1 < args.Length) simDays = int.Parse(args[i + 1]);
    if (args[i] == "--seed" && i + 1 < args.Length) seed = int.Parse(args[i + 1]);
}

var sim = new ShopSim(catalog, seed);

if (simDays > 0) { RunAutoSim(sim, simDays); return; }
RunInteractive(sim);

// ---------------- 交互模式 ----------------
void RunInteractive(ShopSim sim)
{
    Console.WriteLine("════════════════════════════════════");
    Console.WriteLine("        掌 眼 · 当 铺   M0 原型");
    Console.WriteLine("  高柜台前坐下，你就是新来的朝奉。");
    Console.WriteLine("════════════════════════════════════");
    Console.WriteLine("（目标：30 天后净身价最高；赃证值满 100 会被官差查铺）");

    while (!sim.Clock.Ended && !sim.Ledger.Bankrupt)
    {
        Console.WriteLine();
        Console.WriteLine($"─── {sim.Clock.Formatted} ──────────────────────");
        Console.WriteLine($"本银 {sim.Ledger.Cash} 两 | 罪证 {sim.Ledger.Evidence}/100 | 威望 {sim.Ledger.Prestige} | 死当 {sim.Ledger.DeadStock.Count} 件 | 当票 {sim.Ledger.Tickets.Count} 张");

        // 赎当事件
        var redeem = sim.TryRedeems();
        if (redeem.Length > 0) Console.WriteLine(redeem);

        // 查抄判定
        var raid = sim.RaidCheck();
        if (raid != null) { Console.WriteLine(raid); }

        if (sim.Clock.Ended || sim.Ledger.Bankrupt) break;

        var customers = sim.GenerateTodayCustomers();
        Console.WriteLine($"今日上门 {customers.Count} 位客人。");

        foreach (var c in customers)
        {
            Console.WriteLine();
            Console.WriteLine($"◆ {c.Faction}「{c.Name}」呈上一件：{c.Item.Template.Name}（{c.Item.Template.Category}，要价 {c.AskPrice} 两）");
            bool handled = false;
            while (!handled)
            {
                Console.Write("  [1]瞄一眼 [2]掌眼细验 [3]出估值五成 [4]出估值四成 [5]出估值三成 [6]拒收 [7]卖死当 [8]看库房 [9]提前打烊 > ");
                var key = Console.ReadLine()?.Trim();
                if (key == null) { handled = true; goto EndDay; }   // 输入流结束（EOF）→ 打烊
                switch (key)
                {
                    case "1":
                        Console.WriteLine($"  目测成色尚可，你估摸公允值 {c.Item.BaseValue} 两上下。{(c.SuspiciousShown ? "神色可疑。" : "")}");
                        break;
                    case "2":
                        Console.WriteLine(Indent(sim.Appraise(c)));
                        break;
                    case "3": case "4": case "5":
                    {
                        double f = key == "3" ? 0.5 : key == "4" ? 0.4 : 0.3;
                        var offer = Math.Max(1, (int)(c.Item.BaseValue * f));
                        if (sim.Ledger.Cash < offer) { Console.WriteLine("  本银不够，出不了这个价。"); break; }
                        if (Bargain.Resolve(sim.Ledger, c, c.Item, offer, sim.Rng))
                            Console.WriteLine(Indent(sim.AcceptPawn(c, offer)));
                        else
                            Console.WriteLine(Indent(sim.Reject(c, true)));
                        handled = true;
                        break;
                    }
                    case "6":
                        Console.WriteLine(Indent(sim.Reject(c, false)));
                        handled = true;
                        break;
                    case "7": SellDeadMenu(sim); break;
                    case "8":
                        Console.WriteLine($"  库房死当 {sim.Ledger.DeadStock.Count} 件：");
                        for (int i = 0; i < sim.Ledger.DeadStock.Count; i++)
                        {
                            var it = sim.Ledger.DeadStock[i];
                            Console.WriteLine($"   [{i + 1}] {it.Template.Name}（估值 {it.BaseValue} 两，{(it.IsFake ? "假" : "真")}，可得约 {it.DeadSaleValue(sim.Rng)} 两）");
                        }
                        break;
                    case "9": handled = true; goto EndDay;
                    default: Console.WriteLine("  （输入 1-9）"); break;
                }
            }
        }
    EndDay:
        var eod = sim.Ledger.EndOfDay(sim.Rng, sim.Clock);
        if (eod.Length > 0) Console.WriteLine("· 打烊 ——\n" + Indent(eod));
        sim.Clock.NextDay();
    }

    // 结算
    Console.WriteLine();
    Console.WriteLine("═══════════════ 三十日结算 ═══════════════");
    Console.WriteLine(sim.Ledger.Bankrupt
        ? "铺子倒了——本银亏空，货也光了。（FAIL）"
        : $"净身价 {sim.Ledger.NetWorth(sim.Rng)} 两 | 现银 {sim.Ledger.Cash} 两 | 服务客人 {sim.Ledger.CustomersServed} | 成交 {sim.Ledger.DealsWon} | 查抄 {sim.Ledger.Raids} 次");
    Console.WriteLine("（M0 原型验收：能完整跑完 30 天即达标）");
}

static string Indent(string s) => "  " + s.Replace("\n", "\n  ");

void SellDeadMenu(ShopSim sim)
{
    if (sim.Ledger.DeadStock.Count == 0) { Console.WriteLine("  死当库房空着。"); return; }
    for (int i = 0; i < sim.Ledger.DeadStock.Count; i++)
    {
        var it = sim.Ledger.DeadStock[i];
        Console.WriteLine($"   [{i + 1}] {it.Template.Name}（估值 {it.BaseValue} 两，{(it.IsFake ? "假" : "真")}，可得约 {it.DeadSaleValue(sim.Rng)} 两）");
    }
    Console.Write("   卖几号？（回车返回）> ");
    var k = Console.ReadLine()?.Trim();
    if (int.TryParse(k, out var idx) && idx >= 1 && idx <= sim.Ledger.DeadStock.Count)
        Console.WriteLine(Indent(sim.SellDead(sim.Ledger.DeadStock[idx - 1])));
}

// ---------------- 自动模拟（平衡性验证） ----------------
void RunAutoSim(ShopSim sim, int days)
{
    Console.WriteLine($"[自动模拟] {days} 天，seed={ (sim.Rng.GetHashCode() & 0xffff) }");
    while (!sim.Clock.Ended)
    {
        var redeem = sim.TryRedeems();
        var raid = sim.RaidCheck();
        if (raid != null) Console.WriteLine(raid);
        foreach (var c in sim.GenerateTodayCustomers())
        {
            // 简单 AI：先掌眼；验出假货→拒；罪证高时拒赃物；出估值四成，失败加到五成
            Console.WriteLine(sim.Appraise(c));
            if (c.Item.Appraised && c.Item.KnownFlaws.Any(f => f.Contains("假"))) { Console.WriteLine(sim.Reject(c, false)); continue; }
            if (c.Item.IsStolen && sim.Ledger.Evidence >= 70) { Console.WriteLine(sim.Reject(c, false)); continue; }
            var offer = Math.Max(1, (int)(c.Item.BaseValue * 0.4));
            if (sim.Ledger.Cash < offer) continue;
            if (Bargain.Resolve(sim.Ledger, c, c.Item, offer, sim.Rng)) Console.WriteLine(sim.AcceptPawn(c, offer));
            else
            {
                offer = Math.Max(1, (int)(c.Item.BaseValue * 0.5));
                if (sim.Ledger.Cash >= offer && Bargain.Resolve(sim.Ledger, c, c.Item, offer, sim.Rng)) Console.WriteLine(sim.AcceptPawn(c, offer));
                else Console.WriteLine(sim.Reject(c, true));
            }
        }
        var eod = sim.Ledger.EndOfDay(sim.Rng, sim.Clock);
        if (eod.Length > 0) Console.WriteLine(eod);
        // 自动卖死当
        foreach (var it in sim.Ledger.DeadStock.ToList())
            Console.WriteLine(sim.SellDead(it));
        Console.WriteLine($"-- 第{sim.Clock.Day}天末：现银 {sim.Ledger.Cash} 两，罪证 {sim.Ledger.Evidence}，死当 {sim.Ledger.DeadStock.Count}，当票 {sim.Ledger.Tickets.Count}");
        sim.Clock.NextDay();
        if (sim.Clock.Day > days) break;
    }
    Console.WriteLine($"[模拟结束] 净身价 {sim.Ledger.NetWorth(sim.Rng)} 两 | 现银 {sim.Ledger.Cash} | 服务 {sim.Ledger.CustomersServed} | 成交 {sim.Ledger.DealsWon} | 查抄 {sim.Ledger.Raids}");
}
