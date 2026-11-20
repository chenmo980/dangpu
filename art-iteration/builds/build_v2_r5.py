# -*- coding: utf-8 -*-
"""第4轮(自动化)：皮货 sable/wolf/deer/sheep v2 化（狐皮配方参数化）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, OUT, SS
from PIL import Image, ImageDraw, ImageFont

FURS = {
    'sable':  [(139, 94, 62, 255), (117, 78, 48, 255), (95, 62, 38, 255), (139, 94, 62, 255)],   # 貂：深棕
    'wolf':   [(142, 144, 153, 255), (121, 116, 110, 255), (95, 92, 86, 255), (68, 70, 76, 255)],# 狼：灰
    'deer':   [(176, 138, 90, 255), (154, 116, 70, 255), (120, 88, 52, 255), (213, 187, 140, 255)],# 鹿：棕黄
    'sheep':  [(232, 215, 176, 255), (213, 194, 150, 255), (186, 165, 118, 255), (240, 230, 200, 255)],# 羊：奶油
}

def draw_pelt_v2(d, fur='sable', big=True, ears='up', tail='bushy', spots=None, head_shape='round'):
    """摊开皮张参数化：体+贴边头+放射腿+尾；light 0=亮色 3=暗色"""
    l, m, dk, hi = FURS[fur]
    # 体（大椭圆摊平）
    d.ellipse([10, 18, 54, 44], fill=dk)
    d.ellipse([13, 20, 51, 42], fill=m)
    d.ellipse([15, 22, 49, 40], fill=l)
    # 头贴上边
    if head_shape == 'round':
        d.ellipse([22, 6, 42, 22], fill=dk)
        d.ellipse([25, 8, 39, 19], fill=m)
        d.ellipse([27, 9, 37, 16], fill=l)
    else:  # 方头（狼）
        d.rounded_rectangle([21, 6, 43, 20], 4, fill=dk)
        d.rounded_rectangle([24, 8, 40, 17], 3, fill=m)
        d.rounded_rectangle([26, 9, 38, 15], 2, fill=l)
    # 鼻端
    d.ellipse([29, 12, 35, 17], fill=dk)
    # 耳
    if ears == 'up':
        d.polygon([(18, 8), (22, 1), (26, 9)], fill=dk)
        d.polygon([(38, 9), (42, 1), (46, 8)], fill=dk)
        d.polygon([(20, 8), (22, 4), (24, 9)], fill=m)
        d.polygon([(40, 8), (42, 4), (44, 9)], fill=m)
    elif ears == 'round':
        d.ellipse([17, 3, 27, 12], fill=dk); d.ellipse([19, 5, 25, 10], fill=m)
        d.ellipse([37, 3, 47, 12], fill=dk); d.ellipse([39, 5, 45, 10], fill=m)
    # 四腿短粗放射（防蜘蛛腿）
    for (x0, y0, x1, y1) in [(14, 42, 8, 54), (24, 44, 20, 56), (40, 44, 44, 56), (50, 42, 56, 54)]:
        d.line([x0, y0, x1, y1], fill=dk, width=6)
        d.line([(x0 + x1) // 2, y0, (x0 + x1) // 2 + 1, y1], fill=m, width=3)
    # 尾
    if tail == 'bushy':
        d.ellipse([0, 18, 12, 34], fill=dk)
        d.ellipse([2, 20, 10, 32], fill=m)
        d.ellipse([3, 22, 8, 30], fill=l)
    elif tail == 'straight':
        d.line([2, 24, 12, 30], fill=dk, width=5)
        d.line([2, 23, 12, 28], fill=m, width=2)
    # 斑点（梅花鹿）
    if spots:
        for (sx, sy) in [(18, 26), (26, 24), (34, 27), (42, 24), (22, 33), (32, 32), (40, 34), (28, 37)]:
            d.ellipse([sx, sy, sx + 4, sy + 3], fill=hi)
            d.point([(sx + 1, sy + 1)], fill=l)
    # 背脊高光
    d.arc([14, 18, 50, 40], 180, 360, fill=hi, width=2)

def draw_sheep_fleece(d):
    """羊皮：剪下的卷毛毯——圆角方毯+波浪毛边+卷毛弧纹"""
    l, m, dk, hi = FURS['sheep']
    d.rounded_rectangle([8, 12, 56, 52], 12, fill=m)
    d.rounded_rectangle([11, 15, 53, 49], 10, fill=l)
    # 波浪毛边（外圈小圆弧）
    for gx in (12, 24, 36, 48):
        d.arc([gx - 3, 6, gx + 7, 16], 180, 360, fill=dk, width=3)
        d.arc([gx - 3, 48, gx + 7, 58], 0, 180, fill=dk, width=3)
    for gy in (16, 28, 40):
        d.arc([2, gy, 12, gy + 10], 90, 270, fill=dk, width=3)
        d.arc([52, gy, 62, gy + 10], 270, 90, fill=dk, width=3)
    # 卷毛弧纹（S 小弧阵列）
    for gy in (20, 30, 40):
        for gx in (18, 30, 42):
            d.arc([gx, gy, gx + 8, gy + 7], 60, 300, fill=dk, width=2)
            d.arc([gx + 2, gy + 1, gx + 8, gy + 6], 180, 340, fill=hi, width=1)
    d.ellipse([14, 16, 26, 26], fill=hi)   # 左上受光

BUILDERS = {
    'sable_pelt':  lambda d: draw_pelt_v2(d, 'sable', tail='bushy', head_shape='round'),
    'wolf_pelt':   lambda d: draw_pelt_v2(d, 'wolf', tail='straight', head_shape='square'),
    'deer_pelt':   lambda d: draw_pelt_v2(d, 'deer', tail='straight', spots=True, ears='round'),
    'sheep_pelt':  draw_sheep_fleece,
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
    sheet.save(os.path.join(OUT, 'compare_r5.png'))
    print('r5 OK:', names)

if __name__ == '__main__':
    main()
