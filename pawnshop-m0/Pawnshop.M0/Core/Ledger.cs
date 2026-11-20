namespace Pawnshop.Core;

/// <summary>账本：银钱/罪证值/威望/声望 + 库存 + 当票簿</summary>
public class Ledger
{
    public int Cash = 200;                        // 开局本银（设计文档 §5）
    public int Evidence;                          // 赃证值 0~100
    public int Prestige = 10;                     // 朝奉威望
    public int EyeSkill = 1;                      // 掌眼等级（M0 固定 1）
    public int RentPerMonth = 8;                  // 房租 8 两/月
    public const int RentPerMonthConst = 8;

    public List<PawnTicket> Tickets = new();      // 当票簿
    public List<GameItem> DeadStock = new();      // 死当库存（可转卖）
    public int CustomersServed, DealsWon, BargainsLost, Raids;

    public bool Bankrupt => Cash < 0 && DeadStock.Count == 0 && Tickets.Count == 0;

    /// <summary>净身价（结算用）</summary>
    public int NetWorth(Random rng)
    {
        int stock = DeadStock.Sum(i => i.DeadSaleValue(rng));
        int tickets = Tickets.Where(t => !t.IsDead).Sum(t => t.Item.BaseValue / 2);
        return Cash + stock + tickets;
    }

    public void AddEvidence(int delta)
    {
        Evidence = Math.Clamp(Evidence + delta, 0, 100);
    }

    /// <summary>每日结算：罪证自然衰减 -1（风声过了）</summary>
    public string EndOfDay(Random rng, Clock clock)
    {
        var msgs = new List<string>();
        AddEvidence(-1);
        // 月初交租
        if (clock.IsRentDue)
        {
            Cash -= RentPerMonthConst;
            msgs.Add($"月初交房租 {RentPerMonthConst} 两（余 {Cash} 两）。");
        }
        // 当票到期 → 死当入库
        foreach (var t in Tickets.Where(t => !t.IsDead && clock.Day > t.DueDay).ToList())
        {
            t.IsDead = true;
            DeadStock.Add(t.Item);
            Tickets.Remove(t);
            msgs.Add($"一票当期已过（{t.Item.Template.Name}），依规死当归铺，上柜转卖。");
        }
        return string.Join("\n", msgs);
    }
}

/// <summary>当票：活当（收当立票 → 月息二分 → 到期死当）</summary>
public class PawnTicket
{
    public GameItem Item;
    public int PawnPrice;           // 已付当价
    public int DueDay;              // 到期日
    public const double MonthlyInterest = 0.20;   // 单利二分

    public bool IsDead;
    public bool Redeemed;

    /// <summary>赎回应收 = 当价 + 当价×二分利（按天折算月）</summary>
    public int RedeemAmount(int today)
    {
        var months = Math.Max(1, (int)Math.Ceiling((today - IssuedDay) / 10.0));
        return PawnPrice + (int)Math.Ceiling(PawnPrice * MonthlyInterest * months);
    }

    public int IssuedDay;
}
