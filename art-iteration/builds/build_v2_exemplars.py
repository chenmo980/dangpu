# -*- coding: utf-8 -*-
"""v2 构建器：对标原作风格（真1x 24-32px、AA软边、#292234描边、中性体+彩色点缀）
方法：64x64 超采样绘制 → BOX 降采样到 32x32（自然AA）→ alpha 5档量化 → RGB 调色板锁定 → 内侧描边
产出：pixel-art/pawnshop-icons/v2/  + 对比表（原作 | v2 | v1）
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = r'C:\测试工作区\probably-stolen-study'
OUT = os.path.join(ROOT, 'pixel-art', 'pawnshop-icons', 'v2')
os.makedirs(OUT, exist_ok=True)
SS = 64          # 超采样画布
TRUE = 32        # 真像素尺寸
OUTLINE = (41, 34, 52, 255)          # #292234
ALPHA_LEVELS = (0, 72, 132, 200, 255)

# 调色板（原作中性银灰族 + 原作金/红 + 中国色辅）
PAL = {
    'hl':  (213, 210, 184, 255),   # d5d2b8 亮
    'hi':  (196, 196, 176, 255),   # c4c4b0
    'mid': (168, 174, 165, 255),   # a8aea5
    'lo':  (136, 148, 138, 255),   # 88948a
    'lo2': (121, 116, 110, 255),   # 79746e
    'dk':  (95, 104, 104, 255),    # 5f6868
    'dk2': (68, 70, 76, 255),      # 44464c 暗
    'gold_l': (224, 208, 155, 255),# e0d09b
    'gold':  (204, 185, 135, 255), # ccb987
    'gold_d': (186, 137, 83, 255), # ba8953
    'red':   (156, 55, 56, 255),   # 9c3738
    'red_l': (192, 160, 164, 255), # c0a0a4
    'paper': (213, 210, 184, 255), # 同 hl
    'teal':  (69, 145, 139, 255),  # 45918b
    # 木质/棕色族（皮货/烟杆用，防止深棕被锁到红色）
    'wood_hl': (166, 128, 88, 255),
    'wood_l':  (140, 101, 64, 255),
    'wood':    (92, 58, 33, 255),
    'wood_d':  (74, 48, 28, 255),
}
PAL_LIST = list(PAL.values())

def nearest(c):
    """把任意 RGBA 颜色锁到调色板最近色"""
    if c[3] == 0:
        return (0, 0, 0, 0)
    best = min(PAL_LIST, key=lambda p: (p[0]-c[0])**2 + (p[1]-c[1])**2 + (p[2]-c[2])**2)
    return (best[0], best[1], best[2], c[3])

# ---------- 64px 超采样绘制（每物品一个函数） ----------
def draw_ingot(d, w=52, h=30, y_base=56, yuanbao=False):
    """银锭：左上受光、底 1/3 压暗、金色戳记"""
    x0 = (SS - w) // 2
    body_lo, body_mid, body_hi = PAL['lo'], PAL['mid'], PAL['hi']
    dark = PAL['dk']
    # 底座（马蹄）
    d.ellipse([x0, y_base - h, x0 + w, y_base], fill=body_mid)
    # 顶面亮
    d.ellipse([x0 + 3, y_base - h + 2, x0 + w - 3, y_base - h + 14], fill=body_hi)
    # 底 1/3 压暗（接地）
    d.ellipse([x0, y_base - h // 2 + 2, x0 + w, y_base], fill=dark)
    d.ellipse([x0 + 2, y_base - h // 2 + 2, x0 + w - 2, y_base - 3], fill=body_lo)
    # 顶突
    cw = w // 2
    d.ellipse([x0 + cw - 13, y_base - h - 12, x0 + cw + 13, y_base - h + 6], fill=body_mid)
    d.ellipse([x0 + cw - 10, y_base - h - 10, x0 + cw + 10, y_base - h + 2], fill=body_hi)
    d.ellipse([x0 + cw - 6, y_base - h - 8, x0 + cw + 2, y_base - h - 1], fill=(230, 232, 224, 255))
    # 戳记（金色）
    if yuanbao:
        d.ellipse([x0 + cw - 8, y_base - h - 6, x0 + cw + 8, y_base - h + 4], fill=PAL['gold'])
        d.ellipse([x0 + cw - 5, y_base - h - 4, x0 + cw + 5, y_base - h + 2], fill=PAL['gold_l'])
        d.ellipse([x0 + 6, y_base - 12, x0 + 14, y_base - 6], fill=PAL['gold'])
        d.ellipse([x0 + w - 14, y_base - 12, x0 + w - 6, y_base - 6], fill=PAL['gold'])
    else:
        d.ellipse([x0 + 5, y_base - 14, x0 + 13, y_base - 7], fill=PAL['gold'])
        d.ellipse([x0 + 7, y_base - 12, x0 + 11, y_base - 8], fill=PAL['gold_l'])

def draw_bracelet(d):
    """银镯：环面 ramp + 左上高光弧 + 内侧投影"""
    cx, cy, r = SS // 2, 32, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAL['lo'])
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], fill=PAL['hi'])
    d.ellipse([cx - r + 9, cy - r + 9, cx + r - 9, cy + r - 9], fill=(0, 0, 0, 0))
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 300, fill=(230, 232, 224, 255), width=3)  # 左上高光弧
    d.arc([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], 0, 120, fill=PAL['dk'], width=3)  # 右下内影

def draw_lock(d):
    """长命锁：圆盾+顶环+红穗+标签面板"""
    d.ellipse([26, 4, 38, 16], outline=PAL['lo'], width=4)             # 顶环
    d.ellipse([16, 18, 48, 50], fill=PAL['mid'])                       # 盾
    d.ellipse([19, 21, 45, 47], fill=PAL['hi'])
    d.ellipse([21, 23, 43, 45], fill=PAL['mid'])
    d.ellipse([26, 28, 38, 40], fill=PAL['hl'])                        # 中心面板
    d.rectangle([29, 31, 35, 37], fill=PAL['red'])                     # 面板色带
    d.rectangle([18, 50, 24, 62], fill=PAL['red'])                     # 穗
    d.rectangle([40, 50, 46, 62], fill=PAL['red'])
    d.rectangle([19, 51, 23, 61], fill=PAL['red_l'])
    d.rectangle([41, 51, 45, 61], fill=PAL['red_l'])

def draw_teapot(d):
    """银壶：壶身+嘴+提梁+盖"""
    d.ellipse([14, 26, 50, 58], fill=PAL['lo'])
    d.ellipse([16, 28, 48, 56], fill=PAL['mid'])
    d.ellipse([18, 30, 44, 46], fill=PAL['hi'])
    d.ellipse([15, 44, 49, 58], fill=PAL['lo2'])                       # 底部压暗
    d.rectangle([26, 16, 38, 28], fill=PAL['mid'])                     # 颈
    d.ellipse([24, 10, 40, 20], fill=PAL['hi'])                        # 盖
    d.ellipse([29, 6, 35, 12], fill=PAL['gold'])                       # 盖钮
    d.polygon([(48, 32), (60, 24), (60, 34), (50, 38)], fill=PAL['mid'])  # 嘴
    d.arc([6, 14, 30, 38], 200, 80, fill=PAL['lo2'], width=4)          # 提梁
    d.rectangle([24, 34, 40, 44], fill=PAL['paper'])                   # 标签面板
    d.rectangle([24, 34, 40, 37], fill=PAL['teal'])                    # 标签色带

def draw_foxpelt(d):
    """狐皮：摊开的皮张，头贴上、四肢放射、毛边 AA、底色狐红 ramp"""
    fur_l, fur_m, fur_d = (196, 122, 74, 255), (168, 98, 58, 255), (129, 82, 51, 255)
    d.ellipse([10, 18, 54, 46], fill=fur_m)                            # 体
    d.ellipse([14, 21, 50, 43], fill=fur_l)
    d.ellipse([22, 6, 42, 22], fill=fur_m)                             # 头贴上摊平
    d.ellipse([25, 9, 39, 19], fill=fur_l)
    d.polygon([(20, 8), (25, 2), (28, 10)], fill=fur_d)                # 左耳
    d.polygon([(36, 10), (39, 2), (44, 8)], fill=fur_d)                # 右耳
    for (x0, y0, x1, y1) in [(14, 44, 6, 58), (24, 46, 20, 60), (42, 46, 46, 60), (52, 44, 58, 58)]:
        d.line([x0, y0, x1, y1], fill=fur_d, width=6)                  # 四肢（短粗）
        d.line([(x0+x1)//2, y0, (x0+x1)//2 + 1, y1], fill=fur_m, width=3)
    d.ellipse([0, 20, 10, 34], fill=fur_d)                             # 尾
    d.ellipse([1, 22, 8, 32], fill=fur_l)
    d.arc([12, 20, 52, 44], 180, 360, fill=(222, 150, 100, 255), width=2)  # 背脊高光

BUILDERS = {
    'ingot_small':  lambda d: draw_ingot(d, w=36, h=22, y_base=58),
    'ingot_mid':    lambda d: draw_ingot(d, w=48, h=27, y_base=57),
    'ingot_large':  lambda d: draw_ingot(s_wide(d), w=58, h=32, y_base=56),
    'yuanbao':      lambda d: draw_ingot(d, w=52, h=28, y_base=57, yuanbao=True),
    'bracelet_silver': draw_bracelet,
    'lock_silver':  draw_lock,
    'teapot_silver': draw_teapot,
    'fox_pelt':     draw_foxpelt,
}

def s_wide(d):  # 宽银锭占位（保持签名一致）
    return d

# ---------- 降采样 + 量化 + 描边 ----------
def process(img):
    small = img.resize((TRUE, TRUE), Image.BOX)
    px = small.load()
    # alpha 量化 + RGB 锁定
    for y in range(TRUE):
        for x in range(TRUE):
            r, g, b, a = px[x, y]
            if a < 18:
                px[x, y] = (0, 0, 0, 0); continue
            a2 = min(ALPHA_LEVELS, key=lambda v: abs(v - a))
            r2, g2, b2, _ = nearest((r, g, b, 255))
            px[x, y] = (r2, g2, b2, a2)
    # 内侧描边：不透明且四邻有透明的像素 → 描边色（保 AA alpha）
    edge = []
    for y in range(TRUE):
        for x in range(TRUE):
            r, g, b, a = px[x, y]
            if a == 0: continue
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < TRUE and 0 <= ny < TRUE:
                    if px[nx, ny][3] == 0:
                        edge.append((x, y, a)); break
                else:
                    edge.append((x, y, a)); break
    for x, y, a in edge:
        r, g, b, _ = px[x, y]
        px[x, y] = (OUTLINE[0], OUTLINE[1], OUTLINE[2], a)
    return small

def main():
    results = {}
    for name, fn in BUILDERS.items():
        big = Image.new('RGBA', (SS, SS), (0, 0, 0, 0))
        fn(ImageDraw.Draw(big))
        results[name] = process(big)
        results[name].save(os.path.join(OUT, f'{name}.png'))
    # 对比表：原作参考 | v2 新版 | v1 旧版
    font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 14)
    atlas = Image.open(os.path.join(ROOT, 'analysis', 'items_medical_atlas.png')).convert('RGBA')
    # 原作参考裁块（药瓶群）
    ref = atlas.crop((400, 300, 470, 380)).resize((210, 240), Image.NEAREST)
    names = list(BUILDERS.keys())
    rows = len(names)
    ROW = 136  # 容纳 @4x 128px 显示
    sheet = Image.new('RGBA', (620, rows * ROW + 260), (35, 37, 43, 255))
    d2 = ImageDraw.Draw(sheet)
    sheet.paste(ref, (6, 8))
    d2.text((6, 252), '原作参考(药瓶)', fill=(200, 195, 175, 255), font=font)
    for i, name in enumerate(names):
        y = 8 + i * ROW
        d2.text((240, y + 2), 'v2 ' + name, fill=(160, 210, 170, 255), font=font)
        big = results[name].resize((64, 64), Image.NEAREST)
        sheet.paste(big, (236, y + 22), big)
        old_path = os.path.join(ROOT, 'pixel-art', 'pawnshop-icons', f'{name}.png')
        if os.path.exists(old_path):
            old = Image.open(old_path).convert('RGBA').resize((64, 64), Image.NEAREST)
            d2.text((320, y + 2), 'v1 旧版', fill=(210, 160, 150, 255), font=font)
            sheet.paste(old, (316, y + 22), old)
        d2.text((404, y + 2), 'v2 @4x', fill=(150, 170, 210, 255), font=font)
        disp = results[name].resize((128, 128), Image.NEAREST)
        sheet.paste(disp, (400, y + 4), disp)
    sheet.save(os.path.join(OUT, 'compare_v2_v1_ref.png'))
    print('v2 exemplars OK ->', OUT)

if __name__ == '__main__':
    main()
