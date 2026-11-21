using System;
using System.Collections.Generic;
using System.Linq;

namespace Pawnshop.Core
{

/// <summary>当品模板（来自 item_catalog.csv）</summary>
public class ItemTemplate
{
    public string Identifier;
    public string Name;
    public string Category;
    public int ValueLow;
    public int ValueHigh;
    public string[] Flaws;      // 可出现瑕疵
    public string[] Tags;
    public (int W, int H) Shape;

    /// <summary>品类赃证权重（兵器>银器>字画…，设计文档 4.4）</summary>
    public int EvidenceWeight
    {
        get
        {
            if (Tags.Contains("weapon_item")) return 20;
            if (Tags.Contains("precious_item")) return Tags.Contains("jade_item") ? 15 : 10;
            if (Tags.Contains("rare_item")) return 12;
            return 6;
        }
    }
}

/// <summary>一件当品实例（模板 + 真伪 + 瑕疵）</summary>
public class GameItem
{
    public ItemTemplate Template;
    public bool IsFake;                     // 赝品（真/假双状态）
    public bool IsStolen;                   // 来路不明
    public List<string> HiddenFlaws = new();  // 未被掌眼发现的瑕疵
    public List<string> KnownFlaws = new();   // 已被掌眼发现的瑕疵
    public bool Appraised;                  // 是否已上手验过
    public long UniqueId;

    /// <summary>公允估值（真品基准）</summary>
    public int BaseValue;

    /// <summary>死当转卖可得价（假品折价 35%）</summary>
    public int DeadSaleValue(Random rng)
    {
        var baseV = IsFake ? (int)(BaseValue * 0.35) : BaseValue;
        var f = 0.6 + rng.NextDouble() * 0.3;   // 0.6~0.9
        return Math.Max(1, (int)(baseV * f));
    }
}
}
