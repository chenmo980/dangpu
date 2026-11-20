namespace Pawnshop.Core;

/// <summary>磨价：纯概率判定（设计文档 §4.3，公式为改造起点）</summary>
public static class Bargain
{
    /// <summary>
    /// 出价成交概率（%）：
    /// 60 + 威望/4 + 验出瑕疵加成20 + 出价诚意 - 要价差额惩罚
    /// </summary>
    public static int AcceptChance(Ledger ledger, Customer c, GameItem item, int offer)
    {
        var ask = c.AskPrice;
        // 出价诚意：offer/ask 的比值映射 -40~+25
        double sincerity = (double)offer / Math.Max(1, ask);
        int sincerityPts = sincerity >= 0.55 ? 25
                         : sincerity >= 0.45 ? 10
                         : sincerity >= 0.35 ? -5
                         : -40;
        int chance = 60
                   + ledger.Prestige / 4
                   + (item.Appraised && item.KnownFlaws.Count > 0 ? 20 : 0)  // 掌眼依据
                   + sincerityPts
                   - (c.Faction == "绿林朋友" ? 15 : 0)                     // 绿林难磨
                   + (c.Faction == "败家子弟" ? 10 : 0);                    // 败家好磨
        return Math.Clamp(chance, 5, 95);
    }

    /// <summary>判定一次磨价（true=成交）</summary>
    public static bool Resolve(Ledger ledger, Customer c, GameItem item, int offer, Random rng)
    {
        var chance = AcceptChance(ledger, c, item, offer);
        return rng.Next(100) < chance;
    }
}

/// <summary>上门客人</summary>
public class Customer
{
    public string Name;
    public string Faction;
    public GameItem Item;
    public int AskPrice;            // 客人要价（当价口径）
    public bool SuspiciousShown;    // 是否已向玩家透露可疑

    public static readonly string[] Factions =
        { "街坊小民", "败家子弟", "绿林朋友", "官面衙门", "古玩行家", "洋行买办", "当行同行", "女眷", "行脚商" };

    private static readonly string[] Surnames = { "王", "李", "张", "赵", "钱", "孙", "周", "吴", "郑", "冯" };
    private static readonly string[] Given = { "二", "三", "四", "老蔫", "瘸子", "秀才", "掌柜", "娘子", "老刀", "顺子" };

    public static Customer Generate(ItemCatalog catalog, Ledger ledger, Random rng)
    {
        var faction = Factions[rng.Next(Factions.Length)];
        // 各派系行为差异（M0 简化：绿林必赃、官眷女眷必净）
        bool stolen = faction switch
        {
            "绿林朋友" => true,
            "官面衙门" => false,
            "女眷" => false,
            _ => rng.NextDouble() < 0.30,
        };
        var t = catalog.PickWeighted(rng);
        var item = catalog.MakePiece(t, rng, stolen, fakeChance: 0.15);
        // 可疑度：赃物 + 派系可疑 → 玩家可从神态看出端倪（威望越高越准）
        var askBase = item.BaseValue * (0.8 + rng.NextDouble() * 0.4);   // 要价 = 估值的 0.8~1.2
        return new Customer
        {
            Name = Surnames[rng.Next(Surnames.Length)] + Given[rng.Next(Given.Length)],
            Faction = faction,
            Item = item,
            AskPrice = Math.Max(1, (int)askBase),
            SuspiciousShown = false,
        };
    }
}
