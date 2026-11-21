using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Pawnshop.Core
{
    /// <summary>当品目录：加载 item_catalog.csv（120 件），M0.9 与 Unity 通用</summary>
    public class ItemCatalog
    {
        public List<ItemTemplate> Templates = new List<ItemTemplate>();
        private static readonly char[] Slash = { '/' };

        /// <summary>桌面/编辑器：从路径加载</summary>
        public static ItemCatalog Load(string csvPath)
        {
            return LoadFromText(File.ReadAllText(csvPath));
        }

        /// <summary>Unity：从 TextAsset.text 加载</summary>
        public static ItemCatalog LoadFromText(string csvContent)
        {
            var cat = new ItemCatalog();
            foreach (var line in csvContent.Split('\n'))
            {
                var clean = line.TrimEnd('\r');
                if (string.IsNullOrWhiteSpace(clean) || clean.StartsWith("identifier,")) continue;
                var parts = clean.Split(',');
                if (parts.Length < 8) continue;
                var shape = parts[7].Split('x');
                int.TryParse(shape[0], out var sw);
                int.TryParse(shape[1], out var sh);
                cat.Templates.Add(new ItemTemplate
                {
                    Identifier = parts[0],
                    Name = parts[1],
                    Category = parts[2],
                    ValueLow = int.Parse(parts[3]),
                    ValueHigh = int.Parse(parts[4]),
                    Flaws = parts[5].Split(Slash, StringSplitOptions.RemoveEmptyEntries),
                    Tags = parts[6].Split(Slash, StringSplitOptions.RemoveEmptyEntries),
                    Shape = (sw, sh),
                });
            }
            return cat;
        }

        /// <summary>随机抽一件模板（低值品出现率更高，符合街面客流）</summary>
        public ItemTemplate PickWeighted(Random rng)
        {
            var weights = Templates.Select(t => Math.Max(1, 1000 / ((t.ValueLow + t.ValueHigh) / 2 + 10))).ToArray();
            var total = weights.Sum();
            var roll = rng.Next(total);
            for (int i = 0; i < Templates.Count; i++)
            {
                roll -= weights[i];
                if (roll < 0) return Templates[i];
            }
            return Templates[Templates.Count - 1];
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
                UniqueId = rng.Next(1, int.MaxValue) * 1000000L + rng.Next(1, 1000000),
            };
            if (t.Flaws.Length > 0 && rng.NextDouble() < 0.30)
            {
                var n = rng.Next(1, Math.Min(2, t.Flaws.Length) + 1);
                piece.HiddenFlaws = t.Flaws.OrderBy(_ => rng.Next()).Take(n).ToList();
            }
            if (piece.IsFake && t.Flaws.Length > 0)
                piece.HiddenFlaws.Add("疑似赝品");
            return piece;
        }
    }
}
