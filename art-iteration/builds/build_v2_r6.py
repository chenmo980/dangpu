# -*- coding: utf-8 -*-
"""第5轮(自动化)：皮货 tiger/horse/cow/rabbit_bundle v2 化"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, OUT, SS
from build_v2_r5 import FURS, draw_pelt_v2
from PIL import Image, ImageDraw, ImageFont

# 补充色族
FURS['tiger'] = [(217, 142, 43, 255), (186, 110, 34, 255), (140, 78, 26, 255), (232, 190, 130, 255)]
FURS['horse'] = [(122, 82, 51, 255), (101, 66, 40, 255), (74, 48, 28, 255), (166, 128, 88, 255)]
FURS['cow']   = [(229, 224, 213, 255), (203, 196, 182, 255), (74, 58, 48, 255), (240, 236, 226, 255)]
FURS['rabbit']= [(169, 162, 155, 255), (148, 140, 132, 255), (120, 112, 104, 255), (200, 194, 186, 255)]

def draw_tiger(d):
    """虎皮：橙底黑横纹（宽条纹、随机错位）、方头、直尾"""
    draw_pelt_v2(d, 'tiger', tail='straight', head_shape='square')
    # 宽黑纹（体部 5 道，错位）
    for i, sy in enumerate(range(20, 42, 5)):
        off = (i % 2) * 4
        d.line([16 + off, sy, 46 - off, sy + 1], fill=(60, 42, 26, 255), width=3)
        d.line([16 + off, sy + 1, 46 - off, sy + 2], fill=(48, 34, 22, 255), width=1)
    d.line([24, 18, 22, 44], fill=(60, 42, 26, 255), width=3)   # 中线纹
    d.line([40, 18, 42, 44], fill=(60, 42, 26, 255), width=3)   # 侧线纹

def draw_horse(d):
    """马皮：大张棕色皮，长头（马头轮廓），蹄形腿端"""
    draw_pelt_v2(d, 'horse', tail='straight', head_shape='square', ears='up')
    d.ellipse([36, 4, 50, 14], fill=FURS['horse'][2])           # 长口鼻
    d.ellipse([38, 6, 47, 12], fill=FURS['horse'][0])
    for (x0, y0, x1, y1) in [(8, 54, 6, 60), (20, 56, 18, 61), (44, 56, 46, 61), (56, 54, 58, 60)]:
        d.ellipse([x1 - 3, y1 - 2, x1 + 4, y1 + 3], fill=FURS['horse'][2])  # 蹄端

def draw_cow(d):
    """牛皮：白底黑斑大张皮"""
    draw_pelt_v2(d, 'cow', tail='straight', head_shape='square')
    for (bx, by, bw, bh) in [(18, 24, 12, 10), (36, 22, 10, 8), (28, 32, 14, 10), (16, 34, 8, 8)]:
        d.ellipse([bx, by, bx + bw, by + bh], fill=(74, 58, 48, 255))
        d.ellipse([bx + 2, by + 2, bx + bw - 2, by + bh - 1], fill=(52, 40, 33, 255))

def draw_rabbit_bundle(d):
    """兔皮一捆：三张小皮叠卷+束绳"""
    l, m, dk, hi = FURS['rabbit']
    d.ellipse([8, 20, 40, 48], fill=m)                          # 底卷
    d.ellipse([10, 22, 38, 46], fill=l)
    d.ellipse([18, 14, 48, 40], fill=m)                         # 上卷
    d.ellipse([20, 16, 46, 38], fill=l)
    d.ellipse([26, 10, 52, 34], fill=m)                         # 顶卷
    d.ellipse([28, 12, 50, 32], fill=l)
    for (ex, ey) in [(26, 12), (24, 20), (30, 28)]:             # 露出的耳朵尖
        d.polygon([(ex, ey), (ex + 6, ey - 6), (ex + 8, ey + 2)], fill=dk)
    d.line([10, 32, 50, 36], fill=(139, 94, 62, 255), width=3)  # 束绳
    d.line([10, 31, 50, 35], fill=(166, 128, 88, 255), width=1)
    d.ellipse([27, 30, 35, 38], fill=(117, 78, 48, 255))        # 绳结
    d.arc([14, 24, 44, 44], 180, 360, fill=hi, width=2)         # 顶部受光

BUILDERS = {
    'tiger_pelt': draw_tiger,
    'horse_hide': draw_horse,
    'cow_hide': draw_cow,
    'rabbit_bundle': draw_rabbit_bundle,
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
        old_path = os.path.join(r'C:\测试工作区\probably-stolen-study\pixel-art\pawnshop-icons', f'{name}.png')
        if os.path.exists(old_path):
            old = Image.open(old_path).convert('RGBA').resize((64, 64), Image.NEAREST)
            d2.text((320, y + 2), 'v1 旧版', fill=(210, 160, 150, 255), font=font)
            sheet.paste(old, (316, y + 22), old)
        d2.text((404, y + 2), 'v2 @4x', fill=(150, 170, 210, 255), font=font)
        disp = results[name].resize((128, 128), Image.NEAREST)
        sheet.paste(disp, (400, y + 4), disp)
    sheet.save(os.path.join(OUT, 'compare_r6.png'))
    print('r6 OK:', names)

if __name__ == '__main__':
    main()
