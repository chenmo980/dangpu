namespace Pawnshop.Core;

/// <summary>一日经营编排：客流→逐客交互（由 UI 层驱动）→ 打烊结算</summary>
public class ShopSim
{
    public readonly ItemCatalog Catalog;
    public readonly Ledger Ledger;
    public readonly Clock Clock = new();
    public readonly Random Rng;
    public int DailyRentWarned;

    public ShopSim(ItemCatalog catalog, int? seed = null)
    {
        Catalog = catalog;
        Rng = seed.HasValue ? new Random(seed.Value) : new Random();
        Ledger = new Ledger();
    }

    public List<Customer> GenerateTodayCustomers()
    {
        var n = 4 + Rng.Next(3);                       // 4-6 客/日
        var list = new List<Customer>();
        for (int i = 0; i < n; i++)
            list.Add(Customer.Generate(Catalog, Ledger, Rng));
        return list;
    }

    /// <summary>收当成交：付磨价、立票；赃物加罪证</summary>
    public string AcceptPawn(Customer c, int price)
    {
        price = Math.Min(price, c.AskPrice);
        Ledger.Cash -= price;
        var due = Clock.Day + Rng.Next(10, 25);         // 10~24 天内到期（覆盖 30 天局）
        Ledger.Tickets.Add(new PawnTicket
        {
            Item = c.Item,
            PawnPrice = price,
            IssuedDay = Clock.Day,
            DueDay = due,
        });
        Ledger.CustomersServed++;
        Ledger.DealsWon++;
        var msgs = new List<string> { $"成交！付当价 {price} 两，立票（当期至第 {due} 天，月息二分）。" };
        if (c.Item.IsStolen)
        {
            var w = c.Item.Template.EvidenceWeight;
            Ledger.AddEvidence(w);
            msgs.Add($"（此物来路不明，赃证值 +{w}，现 {Ledger.Evidence}/100）");
        }
        if (c.Item.IsFake)
            msgs.Add("（你并未看出这物件有问题——除非掌眼。）");
        return string.Join("\n", msgs);
    }

    /// <summary>拒收：小额声望损失（磨价失败连带）</summary>
    public string Reject(Customer c, bool afterBargainFail)
    {
        Ledger.BargainsLost++;
        if (afterBargainFail && Rng.NextDouble() < 0.3)
        {
            Ledger.Prestige = Math.Max(0, Ledger.Prestige - 1);
            return "客人甩袖而去，街坊看着不太好看。（威望 -1）";
        }
        return "客人收起物件，出门去了。";
    }

    /// <summary>掌眼：揭示瑕疵+辨伪（耗时 1 炷香，M0 简化为无资源消耗，纯信息）</summary>
    public string Appraise(Customer c)
    {
        c.Item.Appraised = true;
        var msgs = new List<string> { "你上手细看——" };
        var detectFake = 0.4 + Ledger.EyeSkill * 0.1;
        if (c.Item.IsFake && Rng.NextDouble() < detectFake)
        {
            msgs.Add("手感不对，分量偏轻——这物件怕是假的！");
            foreach (var f in c.Item.HiddenFlaws.Where(f => f == "疑似赝品").ToList())
            {
                c.Item.HiddenFlaws.Remove(f);
                c.Item.KnownFlaws.Add(f);
            }
        }
        foreach (var f in c.Item.HiddenFlaws.Where(f => f != "疑似赝品").ToList())
        {
            c.Item.HiddenFlaws.Remove(f);
            c.Item.KnownFlaws.Add(f);
            msgs.Add($"看出瑕疵：{f}。");
        }
        if (c.Item.IsStolen && Rng.NextDouble() < 0.5 + Ledger.Prestige / 40.0)
        {
            c.SuspiciousShown = true;
            msgs.Add("来路含糊，问了几句眼神就躲——多半是销赃的。");
        }
        if (msgs.Count == 1) msgs.Add("没看出大问题，成色尚可。");
        return string.Join("\n", msgs);
    }

    /// <summary>死当转卖</summary>
    public string SellDead(GameItem item)
    {
        var price = item.DeadSaleValue(Rng);
        Ledger.DeadStock.Remove(item);
        Ledger.Cash += price;
        return $"死当 {item.Template.Name} 上柜转卖，得 {price} 两。";
    }

    /// <summary>赎当（客人在到期前来赎：我们赚利息）</summary>
    public string TryRedeems()
    {
        var msgs = new List<string>();
        foreach (var t in Ledger.Tickets.Where(t => !t.IsDead && !t.Redeemed).ToList())
        {
            // 到期前 30%~70% 概率客人来赎
            var dueIn = t.DueDay - Clock.Day;
            if (Clock.Day - t.IssuedDay < 3) continue;            // 最短持有 3 天
            if (dueIn <= 0 || Rng.NextDouble() > 0.30) continue;  // 每日 30% 来赎
            var amount = t.RedeemAmount(Clock.Day);
            Ledger.Cash += amount;
            Ledger.Tickets.Remove(t);
            t.Redeemed = true;
            msgs.Add($"有客来赎 {t.Item.Template.Name}，收当价加利 {amount} 两，货出库。");
        }
        return string.Join("\n", msgs.Where(m => m.Length > 0));
    }

    /// <summary>官差查抄判定（赃证 ≥100 → 查抄）</summary>
    public string RaidCheck()
    {
        if (Ledger.Evidence < 100) return null;
        Ledger.Raids++;
        var fine = Math.Min(Ledger.Cash, 50);
        Ledger.Cash -= fine;
        var confiscated = Ledger.DeadStock.RemoveAll(i => i.IsStolen);
        var stolenTickets = Ledger.Tickets.RemoveAll(t => t.Item.IsStolen);
        Ledger.AddEvidence(-70);                        // 查抄后风声大减
        Ledger.Prestige = Math.Max(0, Ledger.Prestige - 2);
        return $"⚠ 官差查铺！赃证值满 100——\n罚银 {fine} 两，{(confiscated + stolenTickets)} 件来路不明之物尽数充公。（赃证值降至 {Ledger.Evidence}，威望 -2）";
    }
}
