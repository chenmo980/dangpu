# 《掌眼·当铺》美术资产与工程交接手册（AI / 开发者接手指南）

> **交接定位**：本 `asset/` 目录已归档《掌眼·当铺》（晚清北方州城高柜台当铺，玩法对标《深空当铺 / Probably Stolen》）的 **完整商业级高清美术资产库**：140/140 全量高清当品、8 派系三表情透明立绘（常规/愤怒/满意）、主标题封面 + 甲乙丙丁 4 张结局插画卡、日/夜/雪/雨 4 种正交窗外天气场景、10 张高清瑕疵贴片、8 个高清掌眼工具/暗箱图标，以及 11 件晚清像素 UI 与事件贴图套件。

## 一、目录结构总览（全量商业级高清）

| 路径 | 内容说明 | 用途 |
| ----- | ----- | ----- |
| `asset/scenes/` | **主标题封面**（`title_screen_cover_hd.png`）+ **日/夜/雪夜/阴雨 4 套正交窗外古巷**（`bg_alley_*`）+ **日/夜镂空木窗前景**（`fg_interior_*`，1376×768） | 主菜单封面、主场景 4 层渲染与天气切换 |
| `asset/endings/` | **甲/乙/丙/丁 4 档结局插画卡**（`ending_grade_a/b/c/d.png`） | 对接 T8 结局结算单评级展示 |
| `asset/characters/` | **全部 8 派系三表情透明半身立绘**：常规（`portraits_256/128`）+ 愤怒/惊慌（`portraits_angry_256/128`）+ 满意/喜悦（`portraits_happy_256/128`）+ **64×64 海捕文书头像**（`headshots_64/`） | 窗外客人交互、收当/压价/识破赝品/求购客情绪闭环 |
| `asset/items_hd_*_20/` | **7 大类共 140 件商业级高清多格 PNG**（兵器违禁 / 银器 / 玉器 / 瓷器 / 皮货 / 字画 / 钟表，均含 `hd_64px_per_cell/` 与 `native_32px_per_cell/` 双规格） | 高清桌面鉴宝、博古架陈列、桌下多格收纳 |
| `asset/items_adapted_120/` | 兼容旧路径的 120 件 `(W×32)×(H×32)` 透明 PNG（已 100% 同步替换为最新商业级高清版） | 零改路径直接生效 |
| `asset/overlays_and_tools/` | **10 张高清透明瑕疵贴片**（`flaw_overlays/`，128×128）+ **8 个高清掌眼工具与桌下暗箱图标**（`tools_facilities/`，128×128） | 放大镜验货瑕疵叠加、掌眼工具栏、桌下暗箱开关 |
| `asset/ui_kit/` | **晚清像素 UI 与事件套件（11 件透明 PNG）**：当票宣纸底纹、紫檀九宫格木框、胡桃木匾额按钮、黄铜放大镜光标、朱砂方/圆印章、红绳铜钱串、2 帧柔光油灯火苗、**官府查抄封条**（`event_yamen_seal_strip.png`）、**求购客心愿气泡框**（`event_buyer_bubble.png`） | 弹窗、按钮、盖章、油灯闪烁、查抄封条与 T1 求购客心愿提示 |
| `asset/configs/` | `all_140_hd_manifest.json`、`factions_manifest.json`、`endings_manifest.json`、`ui_kit_manifest.json`、`scene_layout_flat.json`、`grid_layout_spec.json` 及 7 份分品类 manifest | 引擎一键加载与坐标对齐 |
| `asset/docs/` | `item_catalog_140_grid.csv`（140 件全量多格规范表）、设施规划与提示词规范 | 数值与网格尺寸唯一事实源 |
| `asset/previews/` | 17 张全品类/三表情/结局/UI/天气透窗实机总览验收图 | 快速核对全库视觉标准 |

## 二、核心渲染层级与网格坐标规范

1. **Layer 0（窗外背景）**：`scenes/bg_alley_hd_day.png`（日）/ `bg_alley_flat_night_hd.png`（夜）/ `bg_alley_hd_snow.png`（雪夜）/ `bg_alley_hd_rain.png`（阴雨）。
2. **Layer 1（窗外客人）**：`characters/portraits_256/`（常规）、`portraits_angry_256/`（压价/识破赝品）、`portraits_happy_256/`（满意成交/求购客心仪成交），底部对齐窗台 `y = 410`。
3. **Layer 2（正交前景）**：`scenes/fg_interior_hd_day.png` 或 `fg_interior_flat_night_hd.png`（中央木窗镂空 `x=[505, 881], y=[134, 410]`）。
4. **Layer 3（交互与 UI）**：桌面 `28×3` 网格（`x=32, y=444`）、桌下 `14×5` 库房网格（`x=446, y=582`）、瑕疵 Overlay、油灯 2 帧火苗、求购心愿气泡与查抄封条。

## 三、视觉硬约束

* **统一描边色**：`#292234`（暗紫墨内侧描边，严禁纯黑 `#000000`）。
* **12 色中国传统色板**：朱砂 `#C3272B`、胭脂 `#9D2933`、藤黄 `#FFB61E`、秋香 `#D9B611`、月白 `#D6ECF0`、黛蓝 `#425066`、玄青 `#3D3B4F`、黛绿 `#2B4A3D`、紫檀 `#4C2A20`、胡桃 `#8C5B3F`、纸黄 `#E8D7B0`、银灰 `#B8BCC8`。