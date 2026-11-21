# 《掌眼·当铺》美术资产与工程交接手册（AI / 开发者接手指南）

> **交接定位**：本 `asset/` 目录已归档《掌眼·当铺》（晚清北方州城高柜台当铺，玩法对标《深空当铺 / Probably Stolen》）的 **Demo 级全套定稿美术、配置文件、数据表与自动化切片/抠图脚本**。任何接手 AI（ZCode / Cursor / Claude Code / Gemini）可直接把本目录放入 `chenmo980/dangpu` 仓库根目录下开展程序实装或后续批次扩图。

## 一、目录结构总览

| 路径 | 内容说明 | 用途 | 
| ----- | ----- | ----- | 
| `asset/scenes/` | **正面平铺（零斜角正交）日/夜双层主场景**（`bg_alley_*` 后景 + `fg_interior_*` 镂空木窗前景，1376×768 高清及 640×360 / 320×180） | Unity / HTML 主场景 3 层渲染 | 
| `asset/characters/` | **全部 8 派系晚清像素透明半身立绘**（`portraits_256/`、`portraits_128/`）+ **64×64 海捕文书头像**（`headshots_64/`） | 窗外客人交互、左墙通缉令 | 
| `asset/items_hd_20/` | **20 件商业级高清多格兵器/违禁品**（`hd_64px_per_cell/` 与 `native_32px_per_cell/` 双规格，已按真实 `GridShape` 旋正铺满） | 高清桌面鉴宝、桌下网格收纳 | 
| `asset/items_adapted_120/` | 仓库原有 120 件当品的 `(W×32)×(H×32)` 多格适配版透明 PNG | 零拉伸兼容多格网格系统 | 
| `asset/overlays_and_tools/` | **10 张通用透明瑕疵贴片**（`flaw_overlays/`）+ **8 个掌眼工具与桌下暗箱图标**（`tools_facilities/`） | 动态叠加真假瑕疵、桌下藏赃交互 | 
| `asset/configs/` | `scene_layout_flat.json`、`grid_layout_spec.json`、`factions_manifest.json`、`hd_20_manifest.json` | 引擎 UI 坐标对齐与资产加载索引 | 
| `asset/docs/` | `item_catalog_140_grid.csv`（140 件全量多格规范表，已修补原表缺失的 `scroll_landscape=1x3` 与 `ruyi_jade=2x1`）、设施规划与提示词规范 | 数值与后续扩图唯一事实源 | 
| `asset/scripts/` | 连通域精切、BFS 洪泛抠图、多格适配、统一色温 4 个 Python 脚本 | 接手 AI 批量升级剩余 120 件当品直接复用 | 
| `asset/previews/` | 4 张实机合成与总览验收图 | 快速肉眼核对视觉标准 | 

## 二、核心渲染层级与网格坐标规范（程序实装必读）

### 1. 主场景 4 层叠加顺序（基准分辨率 `1376×768`，与原版《深空当铺》同向：由内向外）

1. **Layer 0**：`scenes/bg_alley_hd_day.png`（日景）或 `scenes/bg_alley_flat_night_hd.png`（夜景）— 窗外古巷。

2. **Layer 1**：`characters/portraits_256/npc_*.png` — 客人面朝屏幕站在窗外（左右入场动画自动被 Layer 2 木窗框裁切，底部对齐窗台 `y = 410`）。

3. **Layer 2**：`scenes/fg_interior_hd_day.png` / `fg_interior_flat_night_hd.png` — 中央木窗精确镂空（`x=[505, 881], y=[134, 410]`）的正面平铺店内前景。

4. **Layer 3**：交互网格物品（博古架 / 桌面 / 桌下库房）+ 瑕疵 Overlay 贴片 + 动态 UI 文字（房租木牌、海捕文书、当票）。

### 2. 已验证的网格参数（见 `configs/grid_layout_spec.json`）

* **基准单格**：原生 `32×32px`，在 `1376×768` 高清画布上按 **`34×34px/格`** 渲染：

  * **桌面验货网格**：`x=32, y=444`，**`28×3 = 84 格`**（完整覆盖窗框至算盘左侧）。

  * **桌下中区库房网格**：`x=446, y=582`，**`14×5 = 70 格`**（对标原版 `12×6 = 72 格`，`1×3` 立轴与 `2×2` 皮货均可直放无需强制旋转）。

* **瑕疵贴片叠加规则**：从 `overlays_and_tools/flaw_overlays/` 取对应透明 PNG，按底层当品的 Alpha 通道作为 Mask 叠加（避免瑕疵超出物品轮廓）。

## 三、视觉与色板硬约束（后续扩图不得破坏）

* **统一描边色**：`#292234`（暗紫墨内侧描边，严禁纯黑 `#000000`）。

* **12 色中国传统色板**：朱砂 `#C3272B`、胭脂 `#9D2933`、藤黄 `#FFB61E`、秋香 `#D9B611`、月白 `#D6ECF0`、黛蓝 `#425066`、玄青 `#3D3B4F`、黛绿 `#2B4A3D`、紫檀 `#4C2A20`、胡桃 `#8C5B3F`、纸黄 `#E8D7B0`、银灰 `#B8BCC8`。

* **人物与道具标准**：所有新资产均以 `scenes/bg_alley_hd_day.png` 或 `characters/portraits_256/npc_prodigal_256.png` 作为风格参考图，固定 `#808080` 纯灰底生成后再用 `scripts/` 内的 BFS 洪泛抠图处理（绝不可用全局色键，否则会误抠银器/金属灰）。

## 四、接手 AI 的下一步待办清单（按优先级）

1. **【P0 · 立即实装】将 `asset/` 接入 `prototype/index.html` 与 `pawnshop-m1` Unity 工程**

   * 读取 `configs/scene_layout_flat.json` 与 `configs/grid_layout_spec.json`，把网页原型里的纯色块替换为真实日/夜双层主景、8 派系透明立绘，并接入 `28×3` 桌面与 `14×5` 桌下可拖放网格。

2. **【P1 · 品质升级，可选】用“2×5 精品总表”分批替换原有 120 件程序化当品**

   * **已验证最高效管线**：1 次 AI 生图出一张 `16:9` 的 `2×5` 精灵总表（`#808080` 纯灰底，10 件商业级像素道具） → 直接运行 `scripts/slice_hd_20_items.py` 里的连通域分离 + 自动旋正铺满多格逻辑。

   * 升级全部 120 件仅需 **12 次生图调用**（按银器 2 张、皮货 2 张、字画 2 张、瓷器 2 张、钟表 2 张、玉器 2 张分批推进即可）。

3. **【P2 · 正式版打磨，可选】补充角色情绪与轻量动效**

   * 8 派系角色各补 1 张“愤怒/惊慌”表情变体（以现有 `portraits_256/` 为参考图做局部重绘）；

   * 右侧油灯 2 帧火苗微动 + 窗外灯笼微光 Shader + 当票九宫格边框切图。