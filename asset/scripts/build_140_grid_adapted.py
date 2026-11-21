#!/usr/bin/env python3
"""
《掌眼·当铺》全部 140 件当品真实多格网格适配（(W*32)x(H*32)）+ 高清平铺主场景容量实机验证脚本
- 修复仓库 item_catalog.csv 缺失的 2 条 shape（山水立轴->1x3, 玉如意->2x1）
- 将仓库 120 件已有 v2 当品全部按真实 (W, H) 适配到 (W*32)x(H*32) 多格画布（零拉伸变形 + 锐化描边）
- 将第 2 天 20 件兵器/违禁品按真实多格比例（1x1 / 2x1 / 1x2 / 3x1 / 2x2）在 3x 超采样画布高细节重绘
- 结合升级版高清木纹平铺主场景，输出 14x5=70 格桌下库房 + 20x3 桌面验货区的实机拼格验收图
"""
import csv
import json
from pathlib import Path
import zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path("/working_dir/c_9dc48f286509629e")
GEN_DIR = ROOT / "user_uploaded_files/ttl=63d/tool_generated"
REPO_CSV = ROOT / "artifacts/dangpu_repo/pawnshop-m0/Pawnshop.M0/item_catalog.csv"
REPO_V2 = ROOT / "artifacts/dangpu_repo/pixel-art/pawnshop-icons/v2"
STARTER = ROOT / "artifacts/file_generation/ttl=63d/intermediate/starter_pack"
STAGE = ROOT / "artifacts/file_generation/ttl=63d/intermediate/grid_140_pack"
OUT_DIR = ROOT / "artifacts/file_generation/ttl=63d/output"

(STAGE / "sprites_140").mkdir(parents=True, exist_ok=True)
(STAGE / "scene_hd_flat").mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

HD_DAY_SRC = GEN_DIR / "watermarked_img_2838075442864672134.jpg"
CELL = 32
OUTLINE = (41, 34, 52, 255)
ALPHA_LEVELS = (0, 72, 132, 200, 255)

PAL = {
    "hl": (232, 228, 204, 255),
    "hi": (206, 205, 186, 255),
    "mid": (168, 174, 165, 255),
    "lo": (132, 142, 136, 255),
    "lo2": (110, 106, 102, 255),
    "dk": (84, 92, 96, 255),
    "dk2": (56, 58, 66, 255),
    "gold_hl": (248, 232, 172, 255),
    "gold_l": (224, 202, 138, 255),
    "gold": (196, 166, 104, 255),
    "gold_d": (156, 112, 62, 255),
    "red_l": (206, 92, 86, 255),
    "red": (164, 52, 52, 255),
    "red_d": (112, 30, 34, 255),
    "paper": (222, 214, 184, 255),
    "teal_l": (96, 172, 162, 255),
    "teal": (64, 136, 128, 255),
    "teal_d": (38, 68, 60, 255),
    "wood_hl": (176, 134, 92, 255),
    "wood_l": (140, 98, 62, 255),
    "wood": (94, 60, 36, 255),
    "wood_d": (64, 40, 24, 255),
    "ink": (41, 34, 52, 255),
}
PAL_LIST = list(PAL.values())


def parse_shape(s: str) -> tuple[int, int]:
    parts = s.lower().strip().split("x")
    return int(parts[0]), int(parts[1])


def quantize_alpha(a: int) -> int:
    return min(ALPHA_LEVELS, key=lambda lv: abs(lv - a))


def nearest_pal(c):
    if c[3] == 0:
        return (0, 0, 0, 0)
    best = min(PAL_LIST, key=lambda p: (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 + (p[2] - c[2]) ** 2)
    return (best[0], best[1], best[2], c[3])


def finalize_multicell(hi_img: Image.Image, gw: int, gh: int) -> Image.Image:
    """将 3x 超采样高细节图降采样为 (gw*32)x(gh*32)，锁色并加 #292234 锐利内侧描边。"""
    tw, th = gw * CELL, gh * CELL
    small = hi_img.resize((tw, th), Image.Resampling.BOX)
    px = small.load()
    for y in range(th):
        for x in range(tw):
            r, g, b, a = px[x, y]
            qa = quantize_alpha(a)
            px[x, y] = (0, 0, 0, 0) if qa == 0 else nearest_pal((r, g, b, qa))

    out = small.copy()
    opx = out.load()
    for y in range(th):
        for x in range(tw):
            if px[x, y][3] >= 132:
                for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ny, nx = y + dy, x + dx
                    if not (0 <= nx < tw and 0 <= ny < th) or px[nx, ny][3] == 0:
                        opx[x, y] = (OUTLINE[0], OUTLINE[1], OUTLINE[2], px[x, y][3])
                        break
    return out


def adapt_existing_120_sprite(src_path: Path, gw: int, gh: int) -> Image.Image:
    """
    将仓库现有 32x32 图标无拉伸适配到 (gw*32)x(gh*32) 多格画布：
    - 1x1 原样保留 32x32 零损
    - 非 1x1 裁切紧致边界，按整数/清晰像素比等比缩放居中，并保留自然视觉留白与微弱底影
    """
    im = Image.open(src_path).convert("RGBA")
    if gw == 1 and gh == 1:
        return im

    tw, th = gw * CELL, gh * CELL
    bbox = im.getbbox()
    if not bbox:
        return Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    crop = im.crop(bbox)
    cw, ch = crop.size

    # 允许最多 1.25x 温和比例适配 + 优先保持等比不畸变
    pad_w = max(4, int(tw * 0.08))
    pad_h = max(4, int(th * 0.08))
    avail_w = tw - pad_w * 2
    avail_h = th - pad_h * 2

    scale = min(avail_w / cw, avail_h / ch)
    # 针对 2x1 / 1x2 / 3x1 / 1x3 长条物，在长轴方向给予适度舒展（上限 1.28x 避免明显拉扁）
    nw = max(1, int(round(cw * scale)))
    nh = max(1, int(round(ch * scale)))
    if gw > gh and nw < avail_w * 0.72:
        nw = min(avail_w, int(round(nw * 1.22)))
    elif gh > gw and nh < avail_h * 0.72:
        nh = min(avail_h, int(round(nh * 1.22)))

    # 使用 NEAREST 保持真像素锐利边缘
    resized = crop.resize((nw, nh), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ox = (tw - nw) // 2
    oy = (th - nh) // 2

    # 在底部添加 2px 轻柔接地阴影增强真实立体感
    shadow = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([ox + 3, oy + nh - 4, ox + nw - 3, min(th - 1, oy + nh + 2)], fill=(20, 16, 26, 95))
    canvas.alpha_composite(shadow)
    canvas.paste(resized, (ox, oy), resized)
    return canvas


# ==================== 20 件多格高清兵器/违禁品绘制（3x 超采样，按 WxH 动态尺寸） ====================
def new_hi(gw: int, gh: int):
    w, h = gw * 96, gh * 96
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im), w, h


def draw_yanling_dao_3x1(d, w, h):
    # 3x1 雁翎腰刀（宽 288 x 高 96）：舒展弯刀刃 + 血槽 + 铜盘护手 + 缠布刀柄 + 朱砂刀穗
    d.polygon([(78, 56), (226, 30), (274, 24), (254, 48), (82, 68)], fill=PAL["lo"])
    d.polygon([(80, 54), (226, 30), (270, 26), (234, 40), (82, 60)], fill=PAL["hl"])  # 刀背高光
    d.line([(96, 56), (222, 36)], fill=PAL["dk"], width=4)  # 血槽
    d.rounded_rectangle([68, 36, 86, 76], 6, fill=PAL["gold_d"])  # 铜护手
    d.rounded_rectangle([71, 39, 82, 72], 4, fill=PAL["gold_hl"])
    d.polygon([(20, 62), (70, 50), (70, 64), (24, 74)], fill=PAL["wood_d"])  # 刀柄
    for x in range(28, 66, 9):
        d.line([(x, 58), (x + 4, 69)], fill=PAL["wood_hl"], width=3)  # 缠绳纹理
    d.ellipse([12, 60, 26, 74], fill=PAL["gold"])
    d.polygon([(14, 72), (6, 88), (22, 88)], fill=PAL["red"])  # 刀穗
    d.line([(12, 76), (12, 86)], fill=PAL["red_l"], width=2)


def draw_iron_flute_2x1(d, w, h):
    # 2x1 铁笛暗器（192 x 96）
    d.rounded_rectangle([24, 38, 174, 58], 6, fill=PAL["dk2"])
    d.rounded_rectangle([26, 40, 172, 47], 4, fill=PAL["mid"])
    for x in (58, 76, 94, 112, 130, 148):
        d.ellipse([x - 4, 44, x + 4, 52], fill=PAL["ink"])
    for x in (34, 158):
        d.rectangle([x, 36, x + 8, 60], fill=PAL["gold"])
        d.rectangle([x + 2, 38, x + 6, 48], fill=PAL["gold_hl"])
    d.polygon([(24, 52), (10, 74), (28, 76)], fill=PAL["red"])


def draw_bronze_dagger_2x1(d, w, h):
    d.polygon([(74, 48), (168, 34), (180, 48), (168, 62)], fill=PAL["lo"])
    d.polygon([(76, 48), (168, 36), (176, 48)], fill=PAL["hl"])
    d.ellipse([108, 42, 132, 56], fill=PAL["teal"])  # 青铜绿锈斑
    d.rectangle([62, 30, 76, 66], fill=PAL["gold_d"])
    d.rectangle([65, 32, 72, 50], fill=PAL["gold_hl"])
    d.rounded_rectangle([18, 40, 64, 56], 5, fill=PAL["wood"])
    d.rounded_rectangle([20, 42, 62, 47], 3, fill=PAL["wood_hl"])


def draw_flintlock_2x1(d, w, h):
    # 2x1 洋造燧发短枪（192 x 96）
    d.rectangle([58, 28, 178, 44], fill=PAL["dk"])
    d.rectangle([60, 29, 176, 35], fill=PAL["hl"])  # 枪管高光
    d.polygon([(18, 78), (46, 40), (118, 40), (108, 54), (48, 84)], fill=PAL["wood_d"])
    d.polygon([(24, 74), (48, 42), (114, 42), (104, 50), (48, 76)], fill=PAL["wood_hl"])
    d.rectangle([78, 18, 92, 34], fill=PAL["gold"])  # 黄铜击锤
    d.rectangle([136, 38, 146, 48], fill=PAL["gold_d"])
    d.arc([68, 46, 98, 70], 0, 180, fill=PAL["gold"], width=5)


def draw_revolver_2x1(d, w, h):
    d.rectangle([80, 22, 176, 38], fill=PAL["dk2"])
    d.rectangle([82, 23, 174, 29], fill=PAL["hi"])
    d.rounded_rectangle([62, 34, 100, 60], 6, fill=PAL["dk"])  # 弹巢
    for x in (70, 80, 90):
        d.line([(x, 36), (x, 58)], fill=PAL["hl"], width=3)
    d.polygon([(22, 82), (44, 44), (68, 48), (50, 86)], fill=PAL["wood"])
    d.polygon([(28, 78), (46, 48), (62, 50), (48, 80)], fill=PAL["wood_hl"])
    d.arc([74, 54, 102, 74], 0, 180, fill=PAL["mid"], width=5)


def draw_flying_knife_1x2(d, w, h):
    # 1x2 柳叶飞刀三柄竖排（96 x 192）
    for ox, oy in ((-18, 10), (0, 0), (18, -10)):
        cx = 48 + ox
        d.polygon([(cx, 22 + oy), (cx + 12, 92 + oy), (cx, 104 + oy), (cx - 12, 92 + oy)], fill=PAL["mid"])
        d.polygon([(cx, 26 + oy), (cx, 100 + oy), (cx - 10, 90 + oy)], fill=PAL["hl"])
        d.rectangle([cx - 6, 104 + oy, cx + 6, 152 + oy], fill=PAL["red"])
        d.ellipse([cx - 8, 150 + oy, cx + 8, 166 + oy], outline=PAL["gold"], width=4)


def draw_brass_knuckle_1x1(d, w, h):
    d.rounded_rectangle([12, 30, 84, 68], 14, fill=PAL["gold_d"])
    d.rounded_rectangle([14, 32, 82, 56], 12, fill=PAL["gold_hl"])
    for cx in (24, 40, 56, 72):
        d.ellipse([cx - 6, 39, cx + 6, 51], fill=(0, 0, 0, 0))
    d.rectangle([20, 62, 76, 72], fill=PAL["gold"])


def draw_iron_whip_3x1(d, w, h):
    pts = [(26, 30), (88, 66), (146, 28), (206, 66), (254, 42)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=PAL["dk2"], width=12)
        d.line([pts[i], pts[i + 1]], fill=PAL["hi"], width=4)
    for x, y in pts:
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=PAL["gold"])
        d.ellipse([x - 4, y - 4, x + 2, y + 2], fill=PAL["gold_hl"])
    d.polygon([(254, 42), (278, 30), (278, 56)], fill=PAL["red"])


def draw_crossbow_2x1(d, w, h):
    d.arc([110, 10, 174, 86], 250, 110, fill=PAL["wood_d"], width=10)
    d.line([(134, 14), (134, 82)], fill=PAL["hl"], width=3)
    d.rounded_rectangle([20, 40, 166, 56], 4, fill=PAL["wood"])
    d.rounded_rectangle([22, 42, 164, 47], 2, fill=PAL["wood_hl"])
    d.polygon([(180, 48), (156, 38), (156, 58)], fill=PAL["hl"])
    d.rectangle([76, 36, 94, 60], fill=PAL["gold"])


def draw_military_token_1x1(d, w, h):
    d.ellipse([38, 8, 58, 24], outline=PAL["red"], width=5)
    d.rounded_rectangle([24, 24, 72, 78], 8, fill=PAL["gold_d"])
    d.rounded_rectangle([28, 28, 68, 74], 6, fill=PAL["gold_hl"])
    d.rectangle([34, 34, 62, 68], fill=PAL["wood_d"])
    d.rectangle([40, 40, 56, 62], fill=PAL["red"])
    d.polygon([(44, 78), (52, 78), (48, 92)], fill=PAL["red"])


def draw_opium_pipe_3x1(d, w, h):
    # 3x1 象牙鸦片烟枪（288 x 96）
    d.line([(20, 56), (266, 40)], fill=PAL["wood_d"], width=14)
    d.line([(22, 52), (264, 37)], fill=PAL["wood_hl"], width=5)
    d.rounded_rectangle([240, 32, 276, 48], 6, fill=PAL["hl"])  # 象牙嘴
    d.ellipse([136, 20, 174, 52], fill=PAL["red_d"])  # 红铜烟斗
    d.ellipse([140, 22, 170, 44], fill=PAL["gold"])
    d.ellipse([148, 28, 162, 38], fill=PAL["ink"])
    d.rectangle([62, 44, 74, 62], fill=PAL["gold_l"])


def draw_opium_lamp_1x2(d, w, h):
    d.ellipse([20, 140, 76, 174], fill=PAL["gold_d"])
    d.ellipse([24, 136, 72, 160], fill=PAL["gold_hl"])
    d.polygon([(26, 142), (34, 44), (62, 44), (70, 142)], fill=PAL["mid"])
    d.polygon([(32, 138), (38, 48), (58, 48), (64, 138)], fill=PAL["hl"])
    d.ellipse([40, 82, 56, 118], fill=PAL["red"])
    d.ellipse([43, 88, 53, 110], fill=PAL["gold_hl"])
    d.rectangle([30, 32, 66, 48], fill=PAL["gold"])


def draw_opium_paste_1x1(d, w, h):
    d.ellipse([14, 30, 82, 78], fill=PAL["dk2"])
    d.ellipse([18, 24, 78, 62], fill=PAL["dk"])
    d.ellipse([24, 28, 72, 56], fill=PAL["wood_d"])
    d.rectangle([32, 34, 64, 50], fill=PAL["red"])
    d.rectangle([38, 38, 58, 46], fill=PAL["gold_hl"])


def draw_salt_bag_2x2(d, w, h):
    # 2x2 私盐大麻袋（192 x 192）
    d.ellipse([28, 60, 164, 176], fill=PAL["wood"])
    d.ellipse([36, 66, 156, 164], fill=PAL["wood_hl"])
    for y in range(88, 156, 18):
        d.arc([44, y, 148, y + 26], 10, 170, fill=PAL["wood_l"], width=4)
    d.rectangle([62, 46, 130, 68], fill=PAL["red"])  # 粗麻绳结
    d.polygon([(46, 48), (68, 18), (124, 18), (146, 48)], fill=PAL["paper"])
    d.ellipse([60, 22, 132, 52], fill=PAL["hl"])  # 溢出白盐晶


def draw_fake_banknote_2x1(d, w, h):
    d.rectangle([16, 18, 176, 78], fill=PAL["paper"])
    d.rectangle([24, 24, 168, 72], outline=PAL["dk2"], width=5)
    d.rectangle([32, 32, 78, 64], fill=PAL["teal"])
    d.ellipse([108, 30, 148, 66], fill=PAL["red"])  # 大朱砂假印
    d.line([(86, 38), (102, 38)], fill=PAL["ink"], width=4)
    d.line([(86, 52), (102, 52)], fill=PAL["ink"], width=4)


def draw_fake_seal_1x1(d, w, h):
    d.rectangle([22, 48, 74, 80], fill=PAL["gold_d"])
    d.rectangle([26, 50, 70, 72], fill=PAL["gold_hl"])
    d.rectangle([22, 74, 74, 84], fill=PAL["red"])
    d.ellipse([32, 18, 64, 50], fill=PAL["gold"])
    d.ellipse([38, 24, 58, 42], fill=PAL["gold_hl"])


def draw_tomb_figurine_1x2(d, w, h):
    d.ellipse([30, 18, 66, 58], fill=PAL["lo"])
    d.ellipse([34, 22, 60, 50], fill=PAL["hl"])
    d.polygon([(20, 174), (28, 60), (68, 60), (76, 174)], fill=PAL["lo2"])
    d.polygon([(28, 170), (34, 66), (62, 66), (68, 170)], fill=PAL["mid"])
    d.rectangle([32, 82, 64, 114], fill=PAL["red"])
    d.rectangle([34, 132, 62, 158], fill=PAL["teal_d"])


def draw_coin_sword_1x2(d, w, h):
    d.line([(48, 16), (48, 176)], fill=PAL["red"], width=8)
    for y in range(24, 156, 18):
        d.ellipse([36, y - 9, 60, y + 9], fill=PAL["gold_d"])
        d.ellipse([40, y - 6, 56, y + 6], fill=PAL["gold_hl"])
        d.rectangle([46, y - 2, 50, y + 2], fill=PAL["ink"])
    d.rectangle([20, 132, 76, 146], fill=PAL["gold"])
    d.polygon([(40, 168), (56, 168), (48, 186)], fill=PAL["red"])


def draw_cinnabar_bottle_1x1(d, w, h):
    d.ellipse([24, 36, 72, 84], fill=PAL["teal_d"])
    d.ellipse([28, 40, 66, 78], fill=PAL["teal_l"])
    d.rectangle([38, 20, 58, 38], fill=PAL["teal"])
    d.rectangle([35, 14, 61, 24], fill=PAL["red"])
    d.rectangle([34, 50, 62, 70], fill=PAL["paper"])
    d.line([(39, 54), (57, 66)], fill=PAL["red"], width=4)
    d.line([(57, 54), (39, 66)], fill=PAL["red"], width=4)


def draw_gunpowder_jar_2x2(d, w, h):
    d.ellipse([32, 56, 160, 174], fill=PAL["dk2"])
    d.ellipse([40, 64, 148, 162], fill=PAL["dk"])
    d.ellipse([54, 72, 116, 110], fill=PAL["lo"])  # 高光面
    d.rectangle([66, 40, 126, 62], fill=PAL["gold_l"])
    d.rectangle([60, 92, 132, 134], fill=PAL["red"])
    d.rectangle([74, 104, 118, 122], fill=PAL["gold_hl"])
    d.arc([96, 12, 152, 56], 180, 360, fill=PAL["paper"], width=6)
    d.ellipse([142, 26, 158, 42], fill=PAL["red_l"])


NEW_20_SPECS = [
    ("weapon_yanling_dao", "雁翎腰刀", "兵器", 45, 90, "卷刃/血槽锈/假钢", "weapon_item", "3x1", draw_yanling_dao_3x1),
    ("weapon_iron_flute", "铁笛暗器", "兵器", 32, 65, "管裂/金箍松", "weapon_item", "2x1", draw_iron_flute_2x1),
    ("weapon_bronze_dagger", "青铜短匕", "兵器", 38, 75, "断尖/绿锈蚀刃", "weapon_item", "2x1", draw_bronze_dagger_2x1),
    ("weapon_flintlock", "洋造燧发枪", "兵器", 95, 180, "撞针卡死/枪托裂", "weapon_item", "2x1", draw_flintlock_2x1),
    ("weapon_revolver", "洋行转轮枪", "兵器", 140, 260, "弹巢卡滞/膛线磨", "weapon_item", "2x1", draw_revolver_2x1),
    ("weapon_flying_knife", "柳叶飞刀", "兵器", 28, 55, "缺一柄/刃卷", "weapon_item", "1x2", draw_flying_knife_1x2),
    ("weapon_brass_knuckle", "铁莲花指虎", "兵器", 22, 42, "铜锈/变形", "weapon_item", "1x1", draw_brass_knuckle_1x1),
    ("weapon_iron_whip", "九节铁鞭", "兵器", 50, 95, "环扣锈死/缺红缨", "weapon_item", "3x1", draw_iron_whip_3x1),
    ("weapon_crossbow_mini", "袖箭机弩", "兵器", 68, 130, "弦松/机括卡顿", "weapon_item", "2x1", draw_crossbow_2x1),
    ("weapon_military_token", "官造兵符", "兵器", 120, 220, "仿刻/字迹糊", "weapon_item precious_item", "1x1", draw_military_token_1x1),
    ("contra_opium_pipe", "象牙烟枪", "违禁", 85, 160, "假象牙/烟斗堵", "contraband_item", "3x1", draw_opium_pipe_3x1),
    ("contra_opium_lamp", "玻璃烟灯", "违禁", 40, 75, "灯罩裂/油漏", "contraband_item", "1x2", draw_opium_lamp_1x2),
    ("contra_opium_paste", "土膏烟盒", "违禁", 65, 120, "掺杂/封条破", "contraband_item", "1x1", draw_opium_paste_1x1),
    ("contra_salt_bag", "私盐麻袋", "违禁", 30, 58, "受潮结块/破口", "contraband_item", "2x2", draw_salt_bag_2x2),
    ("contra_fake_banknote", "假官银票", "违禁", 55, 110, "纸质劣/印泥晕", "contraband_item", "2x1", draw_fake_banknote_2x1),
    ("contra_fake_seal", "私刻官印", "违禁", 110, 210, "篆文错/边角磕", "contraband_item", "1x1", draw_fake_seal_1x1),
    ("contra_tomb_figurine", "盗墓彩陶俑", "违禁", 90, 175, "断颈粘合/彩釉脱", "contraband_item rare_item", "1x2", draw_tomb_figurine_1x2),
    ("contra_coin_sword", "镇煞古钱剑", "违禁", 48, 92, "散绳/杂假钱", "contraband_item", "1x2", draw_coin_sword_1x2),
    ("contra_cinnabar_bottle", "黑市鹤顶红", "违禁", 75, 140, "蜡封破/受潮", "contraband_item", "1x1", draw_cinnabar_bottle_1x1),
    ("contra_gunpowder_jar", "走私火药坛", "违禁", 60, 115, "引线潮/坛裂", "contraband_item", "2x2", draw_gunpowder_jar_2x2),
]


def load_cjk_font(size: int):
    for p in [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main():
    # 1. 处理仓库原有 120 件当品 -> 多格适配 + 修复 2 条缺失 shape
    merged_rows = []
    adapted_map = {}  # id -> (Image, gw, gh, name)

    with open(REPO_CSV, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            ident = r["identifier"].strip()
            name = r["name"].strip()
            shape = (r.get("shape") or "").strip()
            if not shape:
                if ident == "scroll_landscape":
                    shape = "1x3"
                elif ident == "ruyi_jade":
                    shape = "2x1"
                else:
                    shape = "1x1"
            gw, gh = parse_shape(shape)
            src_png = REPO_V2 / f"{ident}.png"
            if src_png.exists():
                sp = adapt_existing_120_sprite(src_png, gw, gh)
                sp.save(STAGE / "sprites_140" / f"{ident}.png", optimize=True)
                adapted_map[ident] = (sp, gw, gh, name)
            merged_rows.append({
                "identifier": ident,
                "name": name,
                "category": r["category"].strip(),
                "value_low": r["value_low"].strip(),
                "value_high": r["value_high"].strip(),
                "flaws": r["flaws"].strip(),
                "tags": r["tags"].strip(),
                "shape": f"{gw}x{gh}",
                "pixel_size": f"{gw*CELL}x{gh*CELL}",
            })

    # 2. 生成 20 件高清多格兵器/违禁品
    for ident, name, cat, vlow, vhigh, flaws, tags, shape, fn in NEW_20_SPECS:
        gw, gh = parse_shape(shape)
        hi, d, w, h = new_hi(gw, gh)
        fn(d, w, h)
        sp = finalize_multicell(hi, gw, gh)
        sp.save(STAGE / "sprites_140" / f"{ident}.png", optimize=True)
        adapted_map[ident] = (sp, gw, gh, name)
        merged_rows.append({
            "identifier": ident, "name": name, "category": cat,
            "value_low": str(vlow), "value_high": str(vhigh),
            "flaws": flaws, "tags": tags, "shape": shape,
            "pixel_size": f"{gw*CELL}x{gh*CELL}",
        })

    # 写入合并后的 140 件规范 CSV
    csv_out = STAGE / "item_catalog_140_grid.csv"
    with open(csv_out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["identifier", "name", "category", "value_low", "value_high", "flaws", "tags", "shape", "pixel_size"])
        w.writeheader()
        w.writerows(merged_rows)

    # 3. 切分升级版高清木纹平铺场景（保留在 scene_hd_flat）
    hd_day = Image.open(HD_DAY_SRC).convert("RGBA")
    wx1, wy1, wx2, wy2 = 505, 134, 410, 410  # 精确检测窗框开口
    band = np.asarray(hd_day.convert("RGB"))[200:360, :, :].astype(np.float32)
    col_mean = band.mean(axis=(0, 2))
    col_r, col_b = band[..., 0].mean(axis=0), band[..., 2].mean(axis=0)
    xs = np.where((col_mean > 95.0) & (col_b >= col_r - 12.0) & (np.arange(len(col_mean)) > 480) & (np.arange(len(col_mean)) < 900))[0]
    wx1, wx2, wy1, wy2 = int(xs.min()), int(xs.max()) + 1, 134, 410

    fg_arr = np.asarray(hd_day).copy()
    fg_arr[wy1:wy2, wx1:wx2, 3] = 0
    fg_hd_day = Image.fromarray(fg_arr, mode="RGBA")
    hd_day.save(STAGE / "scene_hd_flat/bg_alley_hd_day.png", optimize=True)
    fg_hd_day.save(STAGE / "scene_hd_flat/fg_interior_hd_day.png", optimize=True)

    # 4. 制作“高清平铺场景 + 14x5=70 格桌下库房 + 20x3 桌面多格拼格实机验证图”
    # 画布：1376 x 1140（上 768 为 1:1 原尺寸高清实机场景，下 372 为多格兵器/违禁品清晰度展示）
    comp = hd_day.copy()
    npc_yamen = Image.open(STARTER / "npc_yamen_256.png").convert("RGBA").resize((276, 276), Image.Resampling.NEAREST)
    comp.paste(npc_yamen, ((wx1 + wx2) // 2 - 138, wy2 - 266), npc_yamen)
    comp.alpha_composite(fg_hd_day)

    d = ImageDraw.Draw(comp)
    f_plaque = load_cjk_font(24)
    d.text((112, 86), "初五 · 距交租 3 日", fill=(232, 215, 176, 255), font=f_plaque)

    # 单格显示尺寸 = 34px（对标原版 12x6=72 格的紧凑手感！）
    # 桌面验货网格：20列 x 3行（x=36..716? 放宽到 24列 x 3行：x=44..860, y=432..534）
    GRID_C = 34
    DESK_X0, DESK_Y0 = 32, 444
    DESK_COLS, DESK_ROWS = 28, 3

    # 绘制极轻的半透明桌面网格辅助线（仅验收可见）
    overlay = Image.new("RGBA", comp.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for r_i in range(DESK_ROWS):
        for c_i in range(DESK_COLS):
            rx = DESK_X0 + c_i * GRID_C
            ry = DESK_Y0 + r_i * GRID_C
            od.rectangle([rx, ry, rx + GRID_C - 2, ry + GRID_C - 2], fill=(20, 16, 24, 38), outline=(232, 215, 176, 55), width=1)

    # 桌下中区库房网格：14列 x 5行 = 70 格（直接对标原版 12x6 = 72 格！）
    STOR_X0, STOR_Y0 = 446, 582
    STOR_COLS, STOR_ROWS = 14, 5
    for r_i in range(STOR_ROWS):
        for c_i in range(STOR_COLS):
            rx = STOR_X0 + c_i * GRID_C
            ry = STOR_Y0 + r_i * GRID_C
            od.rectangle([rx, ry, rx + GRID_C - 2, ry + GRID_C - 2], fill=(18, 16, 26, 155), outline=(112, 86, 68, 180), width=1)

    comp.alpha_composite(overlay)

    def place_on_grid(item_id: str, gx0: int, gy0: int, col: int, row: int):
        if item_id not in adapted_map:
            return
        sp, gw, gh, _ = adapted_map[item_id]
        tw, th = gw * GRID_C - 2, gh * GRID_C - 2
        scaled = sp.resize((tw, th), Image.Resampling.NEAREST)
        comp.paste(scaled, (gx0 + col * GRID_C, gy0 + row * GRID_C), scaled)

    # 在 24x3 桌面同时摊开多种真实多格物品（含 3x1 雁翎刀、3x2 百马图、2x2 狐皮、1x3 山水立轴、2x1 燧发枪等！）
    desk_placements = [
        ("weapon_yanling_dao", 1, 1),   # 3x1
        ("weapon_flintlock", 5, 1),     # 2x1
        ("ingot_large", 8, 1),          # 1x1
        ("painting_horses", 10, 0),     # 3x2
        ("fox_pelt", 14, 0),            # 2x2
        ("scroll_landscape", 17, 0),    # 1x3 (3格高也能完整放下!)
        ("contra_opium_pipe", 19, 1),   # 3x1
        ("contra_fake_seal", 23, 1),    # 1x1
        ("weapon_bronze_dagger", 25, 1),# 2x1
        ("yuanbao", 26, 2),             # 1x1
        ("teapot_silver", 5, 2),        # 2x1
        ("bowl_wucai", 8, 2),           # 1x1
    ]
    for iid, c_i, r_i in desk_placements:
        place_on_grid(iid, DESK_X0, DESK_Y0, c_i, r_i)

    # 在 14x5 = 70 格桌下库房塞入各种多格库存（演示俄罗斯方块式高密度收纳！）
    stor_placements = [
        ("scroll_flowers", 0, 0),       # 1x3
        ("clock_tallcase", 1, 0),       # 1x3
        ("contra_salt_bag", 2, 0),      # 2x2
        ("contra_gunpowder_jar", 4, 0), # 2x2
        ("tiger_pelt", 6, 0),           # 2x2
        ("weapon_iron_whip", 8, 0),     # 3x1
        ("contra_fake_banknote", 11, 0),# 2x1
        ("yuanbao", 13, 0),             # 1x1
        ("weapon_revolver", 8, 1),      # 2x1
        ("weapon_crossbow_mini", 10, 1),# 2x1
        ("contra_tomb_figurine", 12, 1),# 1x2
        ("contra_coin_sword", 13, 1),   # 1x2
        ("ruyi_jade", 2, 2),            # 2x1
        ("pipe_silver", 4, 2),          # 2x1
        ("sable_pelt", 6, 2),           # 2x1
        ("weapon_flying_knife", 8, 2),  # 1x2
        ("contra_opium_lamp", 9, 2),    # 1x2
        ("bracelet_silver", 10, 2),     # 1x1
        ("contra_cinnabar_bottle", 11, 2), # 1x1
        ("contra_opium_paste", 0, 3),   # 1x1
        ("weapon_military_token", 1, 3),# 1x1
        ("wolf_pelt", 2, 3),            # 2x2
        ("vase_bq_meiping", 4, 3),      # 1x2
        ("buddha_silver", 5, 3),        # 1x2
        ("weapon_bronze_dagger", 6, 3), # 2x1
        ("weapon_brass_knuckle", 10, 3),# 1x1
        ("seal_jade", 11, 3),           # 1x1
    ]
    for iid, c_i, r_i in stor_placements:
        place_on_grid(iid, STOR_X0, STOR_Y0, c_i, r_i)

    # 拼装总预览图：上 1376x768 实机，下 380px 清晰度对比与尺寸说明条
    total = Image.new("RGBA", (1376, 1148), (18, 20, 26, 255))
    total.paste(comp, (0, 0))
    td = ImageDraw.Draw(total)
    fh = load_cjk_font(22)
    fs = load_cjk_font(15)

    td.line([(0, 768), (1376, 768)], fill=(140, 91, 63, 255), width=3)
    td.text((28, 782), "多格真实比例精灵抽检（3×1 雁翎刀 / 3×1 烟枪 / 2×1 燧发枪与转轮枪 / 2×2 火药坛与私盐袋 / 1×2 陶俑与古钱剑）", fill=(255, 182, 30, 255), font=fh)

    showcase_ids = [
        ("weapon_yanling_dao", "雁翎腰刀 3×1"),
        ("contra_opium_pipe", "象牙烟枪 3×1"),
        ("weapon_flintlock", "燧发枪 2×1"),
        ("weapon_revolver", "转轮枪 2×1"),
        ("contra_salt_bag", "私盐袋 2×2"),
        ("contra_gunpowder_jar", "火药坛 2×2"),
        ("contra_tomb_figurine", "彩陶俑 1×2"),
        ("contra_coin_sword", "古钱剑 1×2"),
    ]
    cx = 28
    for iid, lbl in showcase_ids:
        sp, gw, gh, _ = adapted_map[iid]
        # 按 2x 像素放大展示真实长宽比
        bw, bh = gw * 64, gh * 64
        # 限制高度不超过 144px 居中排布
        scale_disp = min(1.0, 144 / bh)
        dw, dh = int(bw * scale_disp), int(bh * scale_disp)
        box_w = max(dw + 16, 108)
        td.rectangle([cx, 822, cx + box_w, 982], fill=(41, 34, 52, 255), outline=(140, 91, 63, 255), width=1)
        big = sp.resize((dw, dh), Image.Resampling.NEAREST)
        total.paste(big, (cx + (box_w - dw) // 2, 822 + (160 - dh) // 2), big)
        td.text((cx + 4, 990), lbl, fill=(232, 215, 176, 255), font=fs)
        cx += box_w + 14

    # 底部原版容量对照条
    td.rectangle([28, 1032, 1348, 1126], fill=(28, 30, 38, 255), outline=(82, 183, 136, 255), width=2)
    td.text((48, 1044), "网格容量对标原版《深空当铺》实测结果：", fill=(82, 183, 136, 255), font=fh)
    td.text((48, 1080), "• 桌下库房：原版 12×6 = 72 格  vs  本作平铺凹槽 14×5 = 70 格（34px/格），1×3 立轴与 2×2 皮货均无需强制旋转即可直放。", fill=(214, 236, 240, 255), font=fs)
    td.text((48, 1102), "• 桌面验货：本作 28×3 = 84 格全幅台面（完整覆盖窗框至算盘左侧），可同时摊开 3×2 百马图 + 3×1 腰刀 + 2×2 狐皮 + 多件小银器；全部 140 件已完成 (W×32)×(H×32) 适配。", fill=(214, 236, 240, 255), font=fs)

    preview_path = OUT_DIR / "zhangyan_grid_adapted_preview.png"
    total.convert("RGB").save(preview_path, optimize=True)

    # 导出网格配置 JSON
    grid_cfg = {
        "base_resolution": [1376, 768],
        "cell_px_native": 32,
        "cell_px_on_hd_canvas": GRID_C,
        "desktop_grid": {"x": DESK_X0, "y": DESK_Y0, "cols": DESK_COLS, "rows": DESK_ROWS, "capacity": DESK_COLS * DESK_ROWS},
        "under_desk_storage_grid": {"x": STOR_X0, "y": STOR_Y0, "cols": STOR_COLS, "rows": STOR_ROWS, "capacity": STOR_COLS * STOR_ROWS},
        "total_adapted_items": len(adapted_map),
        "csv_fixes": {"scroll_landscape": "1x3", "ruyi_jade": "2x1"},
    }
    (STAGE / "grid_layout_spec.json").write_text(json.dumps(grid_cfg, ensure_ascii=False, indent=2), encoding="utf-8")

    # 打包全部 140 件多格资产 + 高清场景 ZIP
    zip_path = OUT_DIR / "zhangyan_140_grid_adapted_pack.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(STAGE.rglob("*")):
            if p.is_file():
                zf.write(p, arcname=str(p.relative_to(STAGE)))
        zf.write(preview_path, arcname="zhangyan_grid_adapted_preview.png")

    print("PREVIEW:", preview_path)
    print("ZIP:", zip_path)
    print("ADAPTED COUNT:", len(adapted_map))


if __name__ == "__main__":
    main()
