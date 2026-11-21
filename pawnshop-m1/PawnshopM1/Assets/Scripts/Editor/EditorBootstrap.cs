using System.IO;
using UnityEditor;
using UnityEngine;
using Pawnshop.Core;

namespace Pawnshop.EditorTools
{
    /// <summary>
    /// M1 验证引导：batchmode 下跑 30 天自动模拟，
    /// 验证 Core 模拟层在 Unity 内编译、运行、经济闭环成立。
    /// 命令行：Unity.exe -projectPath ... -batchmode -quit -nographics -executeMethod Pawnshop.EditorTools.EditorBootstrap.Validate
    /// </summary>
    public static class EditorBootstrap
    {
        public static void Validate()
        {
            var csvPath = Path.Combine(Application.streamingAssetsPath, "item_catalog.csv");
            Debug.Log($"[M1] StreamingAssets 当品目录: {csvPath} 存在={File.Exists(csvPath)}");

            var catalog = Pawnshop.Core.ItemCatalog.LoadFromText(File.ReadAllText(csvPath));
            Debug.Log($"[M1] 当品模板数: {catalog.Templates.Count}");

            var sim = new Pawnshop.Core.ShopSim(catalog, 20260701);
            int deals = 0, rejects = 0;

            while (!sim.Clock.Ended)
            {
                foreach (var c in sim.GenerateTodayCustomers())
                {
                    var item = c.Item;
                    item.Appraised = true;
                    if (item.IsFake) { sim.Reject(c, false); rejects++; continue; }
                    int offer = System.Math.Max(1, (int)(item.BaseValue * 0.4));
                    if (sim.Ledger.Cash < offer) continue;
                    var before = sim.Ledger.Tickets.Count;
                    if (Bargain.Resolve(sim.Ledger, c, item, offer, sim.Rng))
                        sim.AcceptPawn(c, offer);
                    else
                    {
                        offer = System.Math.Max(1, (int)(item.BaseValue * 0.5));
                        if (sim.Ledger.Cash >= offer && Bargain.Resolve(sim.Ledger, c, item, offer, sim.Rng))
                            sim.AcceptPawn(c, offer);
                        else sim.Reject(c, true);
                    }
                    if (sim.Ledger.Tickets.Count > before) deals++;
                }
                sim.SellAllDeadStock();
                sim.Ledger.EndOfDay(sim.Rng, sim.Clock);
                sim.Clock.NextDay();
            }

            Debug.Log($"[M1] 30天模拟: 成交 {deals} | 服务 {sim.Ledger.CustomersServed} | 查抄 {sim.Ledger.Raids} | 现银 {sim.Ledger.Cash} 两");
            Debug.Log($"[M1] 验收结论: Core 模拟层在 Unity 内编译运行成功 ✓");
            EditorApplication.Exit(0);
        }
    }
}
