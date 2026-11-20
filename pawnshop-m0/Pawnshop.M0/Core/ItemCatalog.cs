namespace Pawnshop.Core;

/// <summary>当品目录：加载 item_catalog.csv（120 件）</summary>
public class ItemCatalog
{
    public List<ItemTemplate> Templates = new();
    private static readonly char[] Slash = { '/' };

    public static ItemCatalog Load(string csvPath)
    {
        var cat = new ItemCatalog();
        foreach (var line in File.ReadAllLines(csvPath))
        {
            if (string.IsNullOrWhiteSpace(line) || line.StartsWith("identifier,")) continue;
            var parts = line.Split(',');
            if (parts.Length < 8) continue;
            var shape = parts[7].Split('x');
            cat.Templates.Add(new ItemTemplate
            {
                Identifier = parts[0],
                Name       = parts[1],
                Category   = parts[2],
                ValueLow   = int.Parse(parts[3]),
                ValueHigh  = int.Parse(parts[4]),
                Flaws      = parts[5].Split(Slash, StringSplitOptions.RemoveEmptyEntries),
                Tags       = parts[6].Split(Slash, StringSplitOptions.RemoveEmptyEntries),
                Shape      = (int.Parse(shape[0]), int.Parse(shape[1])),
            });
        }
        return cat;
    }

    /// <summary>随机抽一件模板（低值品出现率更高，符合街面客流）</summary>
    public ItemTemplate PickWeighted(Random rng)
    {
        // 权重 = 1000 / 平均估值（估值越低越常见），最低 1
        var weights = Templates.Select(t => Math.Max(1, 1000 / ((t.ValueLow + t.ValueHigh) / 2 + 10))).ToArray();
        var total = weights.Sum();
        var roll = rng.Next(total);
        for (int i = 0; i < Templates.Count; i++)
        {
            roll -= weights[i];
            if (roll < 0) return Templates[i];
        }
        return Templates[^1];
    }

    /// <summary>生成一件实例</summary>
    public GameItem MakePiece(ItemTemplate t, Random rng, bool stolen, double fakeChance)
    {
        var baseValue = rng.Next(t.ValueLow, t.ValueHigh + 1);
        var piece = new GameItem
        {
            Template = t,
            BaseValue = baseValue,
            IsFake = rng.NextDouble() < fakeChance,
            IsStolen = stolen,
            UniqueId = rng.NextInt64(1, long.MaxValue - 1),
        };
        // 瑕疵：30% 概率带 1-2 项
        if (t.Flaws.Length > 0 && rng.NextDouble() < 0.30)
        {
            var n = rng.Next(1, Math.Min(2, t.Flaws.Length) + 1);
            piece.HiddenFlaws = t.Flaws.OrderBy(_ => rng.Next()).Take(n).ToList();
        }
        if (piece.IsFake && t.Flaws.Length > 0)
            piece.HiddenFlaws.Add("疑似赝品");                     // 赝品必有暗瑕
        return piece;
    }
}
