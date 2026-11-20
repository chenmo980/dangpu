using System.Collections.Generic;
using System.Linq;

namespace Pawnshop.Core
{
    /// <summary>
    /// M1 Unity 平移说明：
    /// 1. 把 Core/ 下全部 .cs 拷进 Assets/Scripts/Core/（无 Unity 依赖，纯 C#）
    /// 2. item_catalog.csv 放入 Assets/StreamingAssets/ 或拖成 TextAsset
    /// 3. UI 层（uGUI）调用 ShopSim 的公开方法，读返回的字符串渲染
    /// 4. 图集 pawnshop-atlas-120.png 按 JSON 切片（cell 34px / offset 2px）
    /// </summary>
    public static class ItemCatalogUnityBridge
    {
        /// <summary>Unity 入口：从 TextAsset.text 解析目录</summary>
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
                    Flaws = parts[5].Split('/'),
                    Tags = parts[6].Split('/'),
                    Shape = (sw, sh),
                });
            }
            return cat;
        }
    }
}
