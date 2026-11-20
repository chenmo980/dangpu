# M1 Unity 竖切 · 接入指南

> 目标版本：Unity 2021.3.45f2（与对标原作同版本，LTS）
> 前置：`../design doc`（中国当铺版-设计文档.md）§7 技术方案

## 一、工程初始化

1. Unity Hub → 新建项目：**2D (Built-in Render Pipeline)** 模板，命名为 `PawnshopM1`
2. Player Settings → Company: `Questing`（占位），Product: `PawnshopM1`
3. Edit → Project Settings → TextMesh Pro → Import TMP Essentials

## 二、接入核心模拟层

1. 把 `Assets/Scripts/` 下全部 .cs 拷进工程 `Assets/Scripts/Core/`
2. 把 `../art-tools/item_catalog.csv` 拖到 `Assets/StreamingAssets/`
3. 初始化（任一 MonoBehaviour 的 Awake）：

```csharp
var catalog = ItemCatalogUnityBridge.LoadFromText(
    ((TextAsset)Resources.Load("item_catalog")).text);   // 或 StreamingAssets 读取
var sim = new ShopSim(catalog, seed: null);
```

## 三、图集接入

1. `pawnshop-atlas-120.png` 拖入 `Assets/Sprites/`
2. Texture Type = Sprite (2D and UI)，Mesh Type = Full Rect，
   Grid Sprite Editor：Cell 34×34，Offset (2,2)（对应 JSON）
3. 单件 sprite 名 = identifier（与 item_catalog.csv 一致）

## 四、柜台场景结构（对照 mockup）

```
Scene: Counter
├─ Camera (正交, 背景色 玄青 #3D3B4F)
├─ Background（墙面/匾额「掌眼當」/灯笼 —— 参考 art-demo/高柜台构图mockup.png）
├─ Counter（柜面横条 #A9764F）
├─ CustomerAnchor（客人 sprite 走入目标点）
├─ UI Canvas (Screen Space Overlay, 1920×1080)
│  ├─ HUD（日期/本银/罪证条/威望/行情）
│  ├─ ItemPanel（icon + 名称 + 要价 + 掌眼结果）
│  ├─ ActionBar（掌眼/出价×3/拒收/卖死当/打烊）
│  └─ EndOfDayPanel（打烊结算，对照 endDay() 返回消息）
└─ GameMaster（MonoBehaviour，持有 ShopSim 并驱动 UI）
```

## 五、接线要点

- `ShopSim` 全部公开方法返回**可显示字符串**，UI 层零逻辑
- 每次交互后调 `hud()` 等价：读 `Ledger` 字段刷新 HUD
- 走入演出：Canvas Group alpha + 位置 tween（DOTween 或 Coroutine）
- 存档：M1 先用 PlayerPrefs/JSON；对象图序列化器按设计文档 §2 后置

## 六、验收（对照设计文档 M1）

陌生玩家不看说明能完成 3 天经营 = 竖切达标。
