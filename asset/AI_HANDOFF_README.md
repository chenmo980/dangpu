# 《掌眼·当铺》×《典当春秋》全量美术与剧本融合交接手册（v3.0）

> **交接定位**：本 `asset/` 目录已完成《掌眼·当铺》（正交实体柜台玩法与商业级像素美术）与《典当春秋》（全五章 1898–1900 晚清历史剧本、210 件物品、14 条人情链、6 大结局）的**美术与数据双向融合**。接手编程 AI 可直接读取 `asset/script_data/` 下的 4 份结构化 JSON 与 `asset/configs/all_160_hd_manifest.json`，零门槛把第一章（清明 10 天教学旬）及全五章内容接入 `prototype/index.html` 或 Unity `pawnshop-m1`。

## 一、最新融合资产总览

| 路径 | 内容说明 | 用途 |
|---|---|---|
| `asset/items_hd_*_20/`（8 大类共 **160 件**） | 原有 7 大类 140 件 + **新增 `items_hd_story_20/`（20 件《典当春秋》专属主线物证与民生道具）**，均含 `hd_64px_per_cell/` 与 `native_32px_per_cell/` | 全量 210 件剧本物品均已一对一映射到这 160 件高清素材 |
| `asset/characters/` | **8 派系 × 3 表情（常规/愤怒/满意）** + **新增 `named_portraits_256/128/`（8 位核心具名剧情角色：小顺子、蒙面人沈墨、胡二爷、福公公、小菊仙、钱掌柜、王婆、慧明和尚）** + 64×64 海捕头像 | 固定剧情客调用专属立绘，随机客调用 8 派系三表情立绘 |
| `asset/scenes/` | 主标题封面 + **日 / 夜 / 雪夜 / 阴雨 / 新增庚子战火（`bg_alley_hd_war.png`）** 5 套正交窗外古巷 + 日/夜镂空木窗前景 | 五章节令季节与战乱氛围精准切换（清明→端午→中秋→腊月→庚子） |
| `asset/endings/` | **完整 6 张结局插画卡**：`ending_grade_a/b/c/d.png` + **新增 `ending_yishi.png`（义士）与 `ending_heishi.png`（黑市枭雄）** | 完整覆盖《典当春秋》全部 6 大历史结局 |
| `asset/overlays_and_tools/` | 10 张高清瑕疵贴片（128×128）+ 8 个高清掌眼工具与暗箱图标（128×128） | 放大镜验货瑕疵叠加与工具栏交互 |
| `asset/ui_kit/` | 11 件晚清像素 UI 与事件套件（当票宣纸、九宫格木框、匾额按钮、放大镜光标、朱砂方/圆印章、红绳铜钱、2 帧油灯火苗、官府查抄封条、求购客心愿气泡） | 弹窗、盖章、油灯动效与事件反馈 |
| `asset/script_data/` | **新增 4 份工程级融合 JSON**：`story_items_210_mapped.json`（210 件剧本物品→160 HD 贴图自动映射）、`chapters_schedule_5.json`（五章排程与全客人立绘映射）、`chapter1_playable_script.json`（第一章清明可玩对话树）、`endings_6_rules.json`（6 大结局优先级判定表） | 程序直接读取，无需再手解析 Excel / Markdown |
| `asset/configs/` | `all_160_hd_manifest.json`（含兼容旧版 `all_140_hd_manifest.json`）、`named_characters_manifest.json`、`factions_manifest.json`、`endings_manifest.json`、`ui_kit_manifest.json`、`scene_layout_flat.json`、`grid_layout_spec.json` | 引擎资产索引与坐标对齐 |

## 二、编程 AI 快速接入指南（推荐 M2 垂直切片顺序）

1. **接入 160 件全量图库**：将图标加载源从 `all_140_hd_manifest.json` 切换为 `all_160_hd_manifest.json`（完全向下兼容）。
2. **跑通第一章·清明（10 天教学旬）**：读取 `script_data/chapters_schedule_5.json`（`chapters[0]`）、`script_data/story_items_210_mapped.json` 与 `script_data/chapter1_playable_script.json`——开场签 300 两借据 → 王婆棉袍教行话 → 油头少年假金镯教试金石 → 蒙面人沈墨留 `story_wooden_box_locked`（`2×2` 不可开木匣，占桌下库房格子）。
3. **接入 5 季节场景与 6 结局**：按 `chapters_schedule_5.json` 中的 `default_bg` 自动切换五章窗外景（第五章启用 `bg_alley_hd_war.png`），终局按 `script_data/endings_6_rules.json` 顺序判定并展示对应插画卡。