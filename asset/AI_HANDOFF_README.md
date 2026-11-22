# 《掌眼·当铺》美术资产与工程交接手册（AI / 开发者接手指南）

> **交接定位**：本 `asset/` 目录已归档《掌眼·当铺》（晚清北方州城高柜台当铺，玩法对标《深空当铺 / Probably Stolen》）的 **全量商业级高清美术资产（140/140 当品 100% 高清满配 + 8 派系双表情立绘 + 日夜双层正交场景 + 晚清像素 UI 套件）**、配置文件、数据表与自动化切片/抠图脚本。任何接手 AI（ZCode / Cursor / Claude Code / Gemini）可直接读取 `asset/configs/all_140_hd_manifest.json` 等配置开展程序实装。

## 一、目录结构总览（已全部达商业级高清标准）

| 路径 | 内容说明 | 用途 |
| ----- | ----- | ----- |
| `asset/scenes/` | **正面平铺（零斜角正交）日/夜双层主场景**（`bg_alley_*` 后景 + `fg_interior_*` 镂空木窗前景，1376×768 高清及 640×360 / 320×180） | Unity / HTML 主场景 4 层渲染 |
| `asset/characters/` | **全部 8 派系晚清像素透明半身立绘（双表情）**：常规 `portraits_256/`、`portraits_128/` + **愤怒/惊慌变体 `portraits_angry_256/`、`portraits_angry_128/`** + **64×64 海捕文书头像**（`headshots_64/`） | 窗外客人交互、识破赝品/压价情绪切换、左墙通缉令 |
| `asset/items_hd_20/` | **兵器/违禁品 20 件**商业级高清多格 PNG（`hd_64px_per_cell/` + `native_32px_per_cell/`） | 高清桌面鉴宝、桌下网格收纳 |
| `asset/items_hd_silver_20/` | **银器 20 件**商业级高清多格 PNG（双规格） | 同上 |
| `asset/items_hd_jade_20/` | **玉器 20 件**商业级高清多格 PNG（双规格） | 同上 |
| `asset/items_hd_porcelain_20/` | **瓷器 20 件**商业级高清多格 PNG（双规格） | 同上 |
| `asset/items_hd_fur_20/` | **皮货 20 件**商业级高清多格 PNG（双规格） | 同上 |
| `asset/items_hd_painting_20/` | **字画 20 件**商业级高清多格 PNG（双规格） | 同上 |
| `asset/items_hd_clock_20/` | **钟表与西洋仪器 20 件**商业级高清多格 PNG（双规格） | 同上 |
| `asset/items_adapted_120/` | 兼容旧路径的 120 件 `(W×32)×(H×32)` 透明 PNG（**已 100% 同步替换为上述商业级高清原生版**） | 零改路径直接享受全库高清升级 |
| `asset/ui_kit/` | **晚清像素 UI 套件（9 件透明 PNG）**：当票宣纸底纹、紫檀铜角九宫格木框、胡桃木匾额按钮底、黄铜放大镜光标、朱砂方形印章框、朱砂圆形官印、红绳铜钱串、**油灯动态火苗 2 帧（`f1`/`f2` 含柔化暖光晕）** | 当票弹窗、9-Slice 对话框、按钮、盖章与油灯闪烁动效 |
| `asset/overlays_and_tools/` | **10 张通用透明瑕疵贴片**（`flaw_overlays/`）+ **8 个掌眼工具与桌下暗箱图标**（`tools_facilities/`） | 动态叠加真假瑕疵、桌下藏赃交互 |
| `asset/configs/` | **`all_140_hd_manifest.json`（140 件全量总索引）**、`ui_kit_manifest.json`、`factions_manifest.json`、`scene_layout_flat.json`、`grid_layout_spec.json` 及 7 份分品类 manifest | 引擎一键加载全部资产与 UI 坐标对齐 |
| `asset/docs/` | `item_catalog_140_grid.csv`（140 件全量多格规范表）、设施规划与提示词规范 | 数值与网格尺寸唯一事实源 |
| `asset/scripts/` | 连通域精切、BFS 洪泛抠图、多格适配、统一色温 Python 脚本 | 后续扩充新 DLC 当品直接复用 |
| `asset/previews/` | 12 张实机合成与全品类/UI/双表情总览验收图 | 快速肉眼核对视觉标准 |

## 二、核心渲染层级与网格坐标规范（程序实装必读）

### 1. 主场景 4 层叠加顺序（基准分辨率 `1376×768`，由内向外正交视角）

1. **Layer 0**：`scenes/bg_alley_hd_day.png`（日景）或 `scenes/bg_alley_flat_night_hd.png`（夜景）— 窗外古巷。
2. **Layer 1**：`characters/portraits_256/npc_*.png`（常规）或 `characters/portraits_angry_256/npc_*_angry_256.png`（识破赝品/压价/拒收触发）— 客人面朝屏幕站在窗外，底部对齐窗台 `y = 410`。
3. **Layer 2**：`scenes/fg_interior_hd_day.png` / `fg_interior_flat_night_hd.png` — 中央木窗精确镂空（`x=[505, 881], y=[134, 410]`）的正面平铺店内前景。
4. **Layer 3**：交互网格物品（博古架 / 桌面 / 桌下库房）+ 瑕疵 Overlay 贴片 + `ui_kit/` 动态 UI（油灯 2 帧火苗、当票宣纸与朱砂印章、房租木牌、海捕文书）。

### 2. 已验证的网格参数（见 `configs/grid_layout_spec.json`）

* **基准单格**：原生 `32×32px`（高清 `64×64px`），在 `1376×768` 画布上按 **`34×34px/格`** 渲染：
  * **桌面验货网格**：`x=32, y=444`，**`28×3 = 84 格`**（完整覆盖窗框至算盘左侧）。
  * **桌下中区库房网格**：`x=446, y=582`，**`14×5 = 70 格`**（`1×3` 立轴与 `2×2` 皮货均可直放无需强制旋转）。
* **瑕疵贴片叠加规则**：从 `overlays_and_tools/flaw_overlays/` 取对应透明 PNG，按底层当品的 Alpha 通道作为 Mask 叠加（避免瑕疵超出物品轮廓）。

## 三、视觉与色板硬约束（后续扩图不得破坏）

* **统一描边色**：`#292234`（暗紫墨内侧描边，严禁纯黑 `#000000`）。
* **12 色中国传统色板**：朱砂 `#C3272B`、胭脂 `#9D2933`、藤黄 `#FFB61E`、秋香 `#D9B611`、月白 `#D6ECF0`、黛蓝 `#425066`、玄青 `#3D3B4F`、黛绿 `#2B4A3D`、紫檀 `#4C2A20`、胡桃 `#8C5B3F`、纸黄 `#E8D7B0`、银灰 `#B8BCC8`。
* **抠图规范**：固定 `#808080` 纯灰底生成后，使用 BFS 洪泛抠图处理（封闭镂空如玉镯、怀表、铜钱孔与印章框启用 `clear_holes=True`）。

## 四、程序接手立即可做清单

1. **一键接入全部 140 件 HD 当品**：直接遍历 `asset/configs/all_140_hd_manifest.json`，将 `hd_path` 绑定至 `pawnshop-m1` / `prototype/index.html` 的桌面鉴宝与博古架/库房渲染。
2. **接入 8 派系情绪反馈**：在压价过低、识破赝品或拒收赃物时，将客人立绘切换为 `factions_manifest.json` 中的 `sprite_angry_256`。
3. **接入晚清像素 UI 套件**：读取 `asset/configs/ui_kit_manifest.json`，将当票弹窗替换为 `ui_pawn_ticket_paper.png` + `ui_stamp_square_frame.png` / `ui_stamp_round_seal.png`，并在右侧油灯位循环播放 `ui_lamp_flame_f1.png` / `ui_lamp_flame_f2.png`（4–6 FPS）。