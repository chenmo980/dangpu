# 美术迭代状态（无人值守接力文件）
> 每轮开始先读本文件，结束前必须更新本文件并删除 LOCK。
> 截止：2026-11-20 07:00（到点由时间闸调用 CronPauseSelf）

## 目标与标尺
- 质量对标：`analysis\items_medical_atlas.png`（原作真资产）。已学习：study 卡片 `~/.zcode/skills/pixel-art-studio/references/learned/001-pawnshop-original.md`，调色板 `PALETTES['pawnshop_ref']`
- 风格要点：真 1x 24-32px、中性主体+彩色点缀、左上受光、底 1/3 压暗、#292234 内侧描边、AA 软边、几乎无抖动、标签面板细节
- 单调规则：新版 ≥ 旧版才覆盖；否则保留旧版换方向；连续 2 次不达标→记教训跳下一项

## v2 标准配方（已验证，新代码必须照抄此管线）
代码范本：`art-iteration\builds\build_v2_exemplars.py`
1. 64×64 超采样 PIL 绘制（左上高光/底部压暗/金戳/标签面板）
2. BOX 降采样到 32×32 → 自然 AA
3. alpha 量化 5 档 (0,72,132,200,255)；RGB 锁定到 PAL 表（脚本内）
4. 内侧描边 #292234（不透明且邻透明像素，保留 AA alpha）
5. 产出 `pixel-art\pawnshop-icons\v2\<id>.png`（32px 真 1x）
6. 评审用三联对比图：v2 | v1 | 原作裁块，必须亲自 Read 查看

## 🏁 里程碑：原目录 40 件当品全部 v2 化完成（r8，03:22）
- ✅ v2 = 40/40（银器 20 + 皮货 20，与 item_catalog.csv 一一对应）→ `pixel-art\pawnshop-icons\v2\`
- ⚠️ 命名修正记录：horse_pelt→horse_hide、cow_pelt→cow_hide（build_v2_r6.py 的 BUILDERS key 已同步修正）
- v2 累计接触表：`pixel-art\pawnshop-icons\v2\contact_sheet_v2.png`（40 件）
- 对比证据：`compare_v2_v1_ref.png`、`compare_r2~r8.png`
- 新增工作（不占原 40 件配额）：新品类字画/瓷器/钟表/玉器各 20 件

## 🏁 里程碑 2：瓷器 20/20 完成（r15，05:07）——v2 累计 80 件
## 🏁 最终交付完成（r20 续轮，06:10）
- **v2 图库 = 120/120**（银器20 + 皮货20 + 字画20 + 瓷器20 + 钟表20 + 玉器20），与 item_catalog.csv 120 行一一对应
- **总图集**：`pixel-art\pawnshop-icons\v2\pawnshop-atlas-120.png`（410×342）+ `pawnshop-atlas-120.json`（Unity 切片参数：cell 34px/offset 2）
- **最终接触表**：`pixel-art\pawnshop-icons\v2\contact_sheet_v2.png`（120 件 @4x）
- 管线配方沉淀：`art-iteration\builds\`（r2 最初的 exemplars → r5-r20 各品类参数化模板）
- 教训全文累积在下方——新增物品颜色前必须检查 PAL 覆盖

## Backlog（全部完成 ✅）
1. ~~银器 20 件~~ ✅ r0-r4
2. ~~皮货 20 件~~ ✅ r0/r5-r7
3. ~~皮具 5 件 + crown~~ ✅ r8
4. ~~字画 20 件~~ ✅ r9-r12
5. ~~瓷器 20 件~~ ✅ r13-r15
6. ~~钟表 20 件~~ ✅ r16-r19（缺 clock_wall_round 裂变体，非必需）
7. ~~玉器 20 件~~ ✅ r18-r19续
8. ~~全量 atlas + Unity JSON + 最终接触表~~ ✅ 06:10

## 后续轮次任务（07:00 前的打磨选项）
按优先级：
1. ~~弱项打磨：scroll_flowers 鸟形（v2.1 头喙眼尾羽爪）、cicada_jade_han 汉八刀蝉（v2.1 斜削大翅+刀痕）~~ ✅ r19 完成
2. ~~浅色背景可读性验证（月白底 4 件抽查）~~ ✅ r19 完成（light-bg-check.png）
3. ~~CSV↔图集一致性核对~~ ✅ r19 完成（art-iteration\consistency-report.txt：120↔120 全对齐）
4. ~~浅背景抽查第 2 组 12 件~~ ✅ r20 完成（light-bg-check2.png，16/16 全通过，无返工项）
5. ~~浅背景抽查第 3 组 3 件（如意/郎红/印谱）~~ ✅ r21 完成（light-bg-check3.png）
## ✅ 全部任务完成（r21，06:52）
- 三组浅背景抽检累计 19/19 通过，零返工项
- 120 件图库 + 图集/JSON + 数据目录 + 一致性报告 + 风格守则 + 教训库 = 完整交付
- 07:00 下一轮将命中时间闸 → CronPauseSelf 自动停机
- 若需继续迭代：直接修改 STATE.md 的 Backlog 并重启自动化即可，管线与配方全部沉淀在 builds/

## 🎮 M0.5 浏览器原型（r21 续，06:5x）
- `prototype\index.html`：可玩的《掌眼·当铺》网页版（120 件真像素图 + 完整经济循环）
- 系统已验证：客流(派系→赃物一致性)/掌眼/磨价概率/立票/赎当利滚利/死当转卖/赃证+查抄/房租/30天结算
- 启动方式：① 双击 index.html（file:// 下 <img> 相对路径可用）② 或 `python -m http.server 8765`（在 probably-stolen-study 目录）后开 http://localhost:8765/prototype/index.html
- 已知简化：无存档、掌眼固定 1 级、赎当随机、查抄简化

## 教训（累积）

## 🎮 M0.5 浏览器原型（r21 续，06:5x）
- `prototype\index.html`：可玩的《掌眼·当铺》网页版（120 件真像素图 + 完整经济循环）
- 系统已验证：客流(派系→赃物一致性)/掌眼/磨价概率/立票/赎当利滚利/死当转卖/赃证+查抄/房租/30天结算
- 启动方式：① 双击 index.html（file:// 下 <img> 相对路径可用）② 或 `python -m http.server 8765`（在 probably-stolen-study 目录）后开 http://localhost:8765/prototype/index.html
- 已知简化：无存档、掌眼固定 1 级、赎当随机、查抄简化

## 教训（累积）
- v1 失败根因：48px 稀疏硬边 + noise 假质感 + 纯黑描边 —— 风格与原作(软边AA小尺寸)错位
- 超采样降采样法能自然产出原作式 AA；不要手画 AA
- 对比图行高必须 ≥ 4x 显示尺寸(136px)，否则重叠
- 原作裁块参考：atlas (400,300)-(470,380) 是药瓶群；更多区域坐标待补
- 【r2】32px 下"弦纹横带"易把器物切成两段——装饰带必须紧贴结构转折处，且≤3px 高
- 【r2】双件并列物（筷子）暗色底会把两根糊在一起——间距 ≥6px 起画
- 【r3】细描边圆环(顶环/钩环) outline width≥4 且下缘必须埋入主体，否则降采样后断裂成悬空点
- 【r3】ImageDraw 与 pixelstudio Sprite API 不同：无 px()/only= 参数——纯 PIL 构建脚本里用 d.point()/去掉 only
- 【r4】长杆类道具（烟袋）杆宽 ≤4px + 金箍 3px 细环，粗了变船桨
- 【r4】背光/光环弧 width ≤3 且开口 ≥30°，全环包裹会读作相框
- 【r5】⚠️ 调色板锁定表必须覆盖全色相族——缺棕色导致深棕被锁成红。已加 wood 族，新增物品颜色前先检查 PAL 覆盖
- 【r5】皮张腿"短粗放射"(宽6、长14)才像皮张，细长腿读作蜘蛛/昆虫
- 【r6】浅色皮（牛皮白底）的腿要加深色边缘或改深色，否则白腿在浅背景消失

## 约定
- 锁：art-iteration\LOCK 存在=上一轮未结束，本轮跳过
- 每轮产出后：更新本文件 + 删除 LOCK + 简短总结
