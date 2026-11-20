namespace Pawnshop.Core;

/// <summary>回合时钟：M0 用天数制（30 天验收），月 = 10 天（设计文档 §2）</summary>
public class Clock
{
    public const int TotalDays = 30;
    public const int DaysPerMonth = 10;
    public int Day { get; private set; } = 1;

    public bool Ended => Day > TotalDays;
    public int Month => (Day - 1) / DaysPerMonth + 1;
    public int DayOfMonth => (Day - 1) % DaysPerMonth + 1;
    public bool IsRentDue => DayOfMonth == 1 && Day > 1;   // 每月初交租

    public void NextDay() => Day++;

    public string Formatted => $"开业第{Day}天（{Month}月{DayOfMonth}日）";
}
