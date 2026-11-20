# -*- coding: utf-8 -*-
"""第11轮(自动化)：字画收官 2 件 scroll_imperial(御题诗轴)/painting_orchid(兰谱四条)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

PAPER_L = (232, 224, 196, 255)
PAPER  = (213, 210, 184, 255)
PAPER_D = (186, 178, 148, 255)
INK    = (68, 70, 76, 255)
INK_L  = (95, 104, 104, 255)
ROD    = (92, 58, 33, 255)
ROD_D  = (74, 48, 28, 255)
RED    = (156, 55, 56, 255)
GOLD   = (186, 137, 83, 255)
GOLD_L = (224, 208, 155, 255)
YELLOW = (217, 182, 80, 255)   # 黄绫
TEAL   = (69, 145, 139, 255)

def draw_imperial(d):
    """御题诗轴：黄绫天地头+墨字+双玺印金框"""
    d.rounded_rectangle([18, 2, 46, 8], 3, fill=ROD)                # 上轴头
    d.ellipse([15, 1, 21, 9], fill=GOLD); d.ellipse([43, 1, 49, 9], fill=GOLD)  # 轴头镀金
    d.rectangle([14, 8, 50, 15], fill=YELLOW)                       # 天头（黄绫）
    d.rectangle([14, 15, 50, 50], fill=PAPER)                       # 画心
    d.rectangle([14, 15, 50, 18], fill=PAPER_L)
    for gy in (20, 28, 36):                                          # 御题大字
        d.rectangle([21, gy, 43, gy + 6], fill=INK)
        d.rectangle([23, gy + 1, 41, gy + 5], fill=INK_L)
        d.rectangle([25, gy + 2, 31, gy + 4], fill=INK)
    d.rectangle([16, 18, 22, 24], fill=RED)                         # 御玺 1（大）
    d.rectangle([17, 19, 21, 23], fill=(192, 100, 96, 255))
    d.rectangle([42, 44, 48, 50], fill=RED)                         # 御玺 2
    d.rectangle([43, 45, 47, 49], fill=(192, 100, 96, 255))
    d.rectangle([14, 50, 50, 54], fill=YELLOW)                      # 地头黄绫
    d.rounded_rectangle([18, 54, 46, 60], 3, fill=ROD)
    d.ellipse([15, 53, 21, 61], fill=GOLD); d.ellipse([43, 53, 49, 61], fill=GOLD)
    d.line([14, 15, 50, 15], fill=GOLD, width=1)                    # 绫金边
    d.line([14, 50, 50, 50], fill=GOLD, width=1)

def draw_orchid(d):
    """兰谱四条：四窄条并排（间距≥4px），每条兰叶弧+小花"""
    for i, cx in enumerate((6, 20, 34, 48)):
        d.rectangle([cx, 4, cx + 11, 58], fill=PAPER)
        d.rectangle([cx, 4, cx + 11, 7], fill=PAPER_L)
        d.rounded_rectangle([cx, 2, cx + 11, 6], 2, fill=ROD)       # 上杆
        d.rounded_rectangle([cx, 56, cx + 11, 60], 2, fill=ROD)     # 下杆
        # 兰叶（弧线 3 条，长短交替）
        d.arc([cx + 1, 14, cx + 11, 34], 250, 40, fill=INK, width=2)
        d.arc([cx + 2, 22, cx + 12, 44], 250, 40, fill=INK, width=1)
        d.arc([cx, 30, cx + 10, 52], 250, 40, fill=INK_L, width=1)
        # 兰花
        d.ellipse([cx + 3, 12 + i * 2, cx + 8, 17 + i * 2], fill=TEAL if i % 2 else (192, 100, 96, 255))
        d.point([(cx + 5, 14 + i * 2)], fill=PAPER_L)
        d.rectangle([cx + 8, 50, cx + 10, 54], fill=RED)            # 落款印

BUILDERS = {
    'scroll_imperial': draw_imperial,
    'painting_orchid': draw_orchid,
}

def main():
    results = {}
    for name, fn in BUILDERS.items():
        big = Image.new('RGBA', (SS, SS), (0, 0, 0, 0))
        fn(ImageDraw.Draw(big))
        results[name] = process(big)
        results[name].save(os.path.join(OUT, f'{name}.png'))
    font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 14)
    atlas = Image.open(r'C:\测试工作区\probably-stolen-study\analysis\items_medical_atlas.png').convert('RGBA')
    ref = atlas.crop((400, 300, 470, 380)).resize((210, 240), Image.NEAREST)
    ROW = 136
    names = list(BUILDERS.keys())
    sheet = Image.new('RGBA', (620, len(names) * ROW + 260), (35, 37, 43, 255))
    d2 = ImageDraw.Draw(sheet)
    sheet.paste(ref, (6, 8))
    d2.text((6, 252), '原作参考(风格)', fill=(200, 195, 175, 255), font=font)
    for i, name in enumerate(names):
        y = 8 + i * ROW
        d2.text((240, y + 2), 'v2 ' + name, fill=(160, 210, 170, 255), font=font)
        big = results[name].resize((64, 64), Image.NEAREST)
        sheet.paste(big, (236, y + 22), big)
        d2.text((404, y + 2), 'v2 @4x', fill=(150, 170, 210, 255), font=font)
        disp = results[name].resize((128, 128), Image.NEAREST)
        sheet.paste(disp, (400, y + 4), disp)
    sheet.save(os.path.join(OUT, 'compare_r12.png'))
    print('r12 OK:', names)

if __name__ == '__main__':
    main()
