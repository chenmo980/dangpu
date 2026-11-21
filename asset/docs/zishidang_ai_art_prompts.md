# 《子时当：阴阳当铺》AI 批量美术出图提示词模板库

适配模型：Flux.1 Dev / SDXL + ComfyUI 批量工作流（同样可用于 Midjourney / 即梦等平台前期定调）。
视觉基调：**中式暗黑民俗版画 × 志怪厚涂**（低饱和墨黑底色、暖朱砂与古铜金点缀、微青绿验煞光晕、宣纸颗粒质感）。

---

## 一、全局风格锚点（所有出图必须固定挂载）

为了防止几百张资产画风漂移，把下面两段设为 ComfyUI 的全局公共节点，所有道具与立绘均通过字符串拼接复用。

### 1. 正向风格锚点（`STYLE_ANCHOR`）

```text
Chinese dark folklore game art, moody ink-wash and painterly woodblock illustration style, muted desaturated earthy palette with subtle cinnabar red and antique brass accents, dramatic chiaroscuro rim lighting, aged rice-paper grain texture, crisp silhouette, high-craft indie game asset, 2D hand-painted brushwork
```

### 2. 通用负向词（`NEGATIVE_PROMPT`，SDXL / 支持负向词的管线必填）

```text
photorealistic, 3D render, blender, plastic sheen, anime cel-shading, neon cyberpunk, oversaturated, modern objects, text, calligraphy, Chinese characters, watermark, signature, frame, border, multiple views, cluttered background, blurry edges, deformed hands, extra fingers
```

> **提示**：如果使用 Flux.1 Dev（原生不依赖负向词），直接把 `no text, no readable characters, no watermark, clean isolated silhouette` 拼在正向词末尾即可。

---

## 二、模板 1：批量货品与法宝（Props & Artifacts）

### 核心规则
- **锁定视角**：统一用 `centered isolated icon, slight three-quarter top-down view`（微俯视 3/4 视角），确保摆在柜台和暗格里透视一致。
- **锁定纯色底**：必须使用 `solid flat pure dark charcoal background (#101216)` 或 `solid flat neutral grey background (#808080)`，方便后续 Python 脚本一键抠图且边缘不发白。
- **不直接生成文字**：任何符箓、玉佩、古籍都明确写 `abstract mystical strokes, no readable text`，真假铭文留到引擎层叠加或人工/局部重绘处理。

### 提示词模板

```text
[STYLE_ANCHOR], single mystical antique game item: {ITEM_NAME}, made of {MATERIAL}, showing {AGE_AND_WEAR}, {LIGHTING_DETAIL}, centered composition with generous margin, slight three-quarter top-down view, isolated object on a solid flat uniform #808080 neutral grey background, no cast shadow on background, no text, no readable characters, no watermark
```

### 批量跑图变量示例（可直接存成 CSV 喂给 ComfyUI 批处理节点）

| 资产 ID | `{ITEM_NAME}` | `{MATERIAL}` | `{AGE_AND_WEAR}` | `{LIGHTING_DETAIL}` |
| :--- | :--- | :--- | :--- | :--- |
| `prop_jade_01` | carved dragon-phoenix jade pendant | pale celadon mutton-fat jade with red silk tassel | fine hairline crack and earthy tomb patina | faint eerie jade-green inner glow |
| `prop_mirror_01` | octagonal bronze Bagua exorcism mirror | oxidized dark bronze | verdigris rust along the engraved rim | subtle cold moonlight reflection on polished center |
| `prop_bell_01` | Taoist soul-summoning handbell | blackened cast brass with carved peach-wood handle | worn patina from decades of use | warm amber oil-lamp rim light |
| `prop_urn_01` | sealed funerary spirit jar | cracked stoneware pottery wrapped in yellow paper strips | dried cinnabar wax seal and soot stains | dim ominous red underlight |

---

## 三、模板 2：半身顾客立绘 & 画皮破绽（Customer Portraits）

### 核心规则
- **构图锁死**：搭配 ControlNet（OpenPose / Depth 通用半身剪影模板），把所有 NPC 的头顶位置、肩宽和视线高度锁死在窗框中轴线上，换角色不跳帧。
- **表情与真身用 Img2Img 派生**：先生成 1 张中性平静立绘（`base`），再对面部/眼部/阴影区域做局部重绘，生成“惊慌/阴笑”与“八卦镜中的画皮破绽图”。

### 1. 基础立绘模板（`base`）

```text
[STYLE_ANCHOR], waist-up front-facing portrait of {CHARACTER_ARCHETYPE}, wearing {COSTUME_DETAIL}, {EXPRESSION_AND_POSE}, standing behind a dark antique wooden pawnshop window, lit from below by a faint green-tinted oil lamp and dim red lantern glow from behind, centered head and shoulders, solid dark ink-black background (#0E1013), no text, no watermark
```

### 2. 变量示例

| 角色 ID | `{CHARACTER_ARCHETYPE}` | `{COSTUME_DETAIL}` | `{EXPRESSION_AND_POSE}` |
| :--- | :--- | :--- | :--- |
| `npc_scholar_01` | pale exhausted late-Qing young scholar with dark circles under eyes | frayed indigo linen robe with mud-stained collar | nervous sideways glance, clutching collar tightly |
| `npc_tomb_01` | scarred middle-aged tomb raider with missing earlobe | patched dark oilskin cloak and hemp rope over shoulder | shrewd half-smile, squinting eyes |
| `npc_bride_01` | eerie silent woman in traditional red wedding veil | faded crimson embroidered bridal robe with tarnished silver hairpin | head tilted unnaturally slightly left, unblinking gaze |

### 3. 铜镜倒影 / 画皮真身派生模板（Inpainting，Denoise `0.50–0.65`）

在 `base` 立绘基础上，仅涂抹脸部、脖颈或肩后阴影区域，执行局部重绘：

```text
[STYLE_ANCHOR], distorted reflection in an antique bronze mirror, subtle folklore horror reveal: {HORROR_CLUE}, greenish oxidized bronze mirror tint, misty vignette edges, keeping the exact same silhouette and clothing folds, no text
```

- `{HORROR_CLUE}` 常用破绽词库：
  - `hollow pitch-black eye sockets with faint pale smoke drifting out`（空洞黑眼眶冒阴烟）
  - `faint pale stitching seams along the jawline and neck like sewn paper skin`（下颌与颈部纸皮缝合线）
  - `silhouette of a gaunt fox-spirit skull faintly overlaid behind the human face`（人面后浮现瘦削狐妖骨影）

---

## 四、模板 3：假货与煞气破绽局部重绘（Inpainting Flaws）

**核心原则**：同款物品的“真品”与“假货/带煞气版”绝对不要重新文生图，否则外形变化太大，玩家无法通过观察细节鉴宝。正确做法是**以真品 PNG 为底图，用 Mask 涂抹局部（占总面积 10%–25%），Denoise 设为 `0.35–0.52`**。

| 破绽类型 | Mask 涂抹区域 | Inpainting 提示词（拼接 `STYLE_ANCHOR`） | 推荐 Denoise |
| :--- | :--- | :--- | :--- |
| **高仿做旧假货** | 底部印款、边缘漆面或接缝处 | `crude modern brass glue seam, uneven chemical acid faux-patina stain, slightly misaligned engraving, subtle forgery flaw` | `0.38` |
| **盗墓带煞冥器** | 器物纹理缝隙或玉石内部 | `dried dark crimson bloodstains trapped inside fine cracks, faint clinging pale ghost-hair filaments, eerie cold ash residue` | `0.45` |
| **邪修附灵凶物** | 器物中心或缠绕外圈 | `faint glowing dark vermilion curse veins pulsing beneath the surface, subtle wisps of black-green miasma smoke` | `0.50` |
| **障眼法骗当货** | 局部边角（验煞灯照射下显现） | `peeling golden lacquer revealing cheap rotting gray wood underneath, crumbling paper-mache core exposed at the corner` | `0.42` |

---

## 五、20–30 张自训专属画风 LoRA 实操建议

如果打算用 1 个项目专属 LoRA 彻底锁死画风，建议训练集按以下比例准备（共 25–30 张，先精修到完全统一再开训）：

- **12 张货品道具**：覆盖玉器、青铜、纸符、木器、陶瓷 5 种核心材质，确保模型学会你的材质笔触。
- **8 张半身人物**：覆盖老少男女与不同服饰质感，统一暗部色温和脸部比例。
- **5 张环境/工具局部**：木柜台纹理、红灯笼夜景、青绿油灯光晕、算盘与铜镜特写。
- **训练要点**：使用唯一触发词（如 `zsd_folklore_style`），学习率偏保守、轮数适中（避免过拟合导致只能画出训练集里的那几件物品），打标时把物体内容写细、把风格词留给触发词承载。
