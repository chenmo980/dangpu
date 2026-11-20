# -*- coding: utf-8 -*-
"""第1轮：银器 cup/bowl/censer/chopsticks v2 化
复用 build_v2_exemplars 的已验证管线（超采样→BOX降采样→alpha/调色板量化→内侧描边）
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, TRUE, SS
from PIL import Image, ImageDraw, ImageFont

def draw_cup(d):
    """银盏：小而深，敞口，圈足，内壁暗"""
    d.ellipse([14, 22, 50, 36], fill=PAL['dk2'])            # 口沿内壁（暗）
    d.ellipse([16, 24, 48, 35], fill=PAL['dk'])             # 内壁亮一点
    d.ellipse([12, 24, 52, 38], fill=PAL['mid'])            # 口沿环
    d.ellipse([14, 25, 50, 36], fill=PAL['dk2'])            # 再挖出内口
    d.ellipse([16, 26, 48, 36], fill=PAL['dk'])
    d.arc([12, 24, 52, 38], 160, 300, fill=PAL['hl'], width=3)   # 左上沿高光
    d.chord([15, 30, 49, 56], 10, 170, fill=PAL['mid'])     # 杯身（与沿同宽连贯）
    d.ellipse([15, 42, 49, 56], fill=PAL['lo2'])            # 底 1/3 压暗
    d.ellipse([17, 30, 28, 38], fill=PAL['hi'])             # 左上外壁高光
    d.rectangle([25, 55, 39, 60], fill=PAL['lo'])           # 圈足
    d.ellipse([22, 58, 42, 63], fill=PAL['dk'])             # 足底
    d.arc([25, 55, 39, 62], 180, 360, fill=PAL['gold_d'], width=2)  # 足金线

def draw_bowl(d):
    """银碗：宽而浅，敞口，大圈足"""
    d.ellipse([8, 26, 56, 42], fill=PAL['dk2'])             # 碗口
    d.ellipse([10, 27, 54, 41], fill=PAL['dk'])             # 内壁
    d.ellipse([6, 26, 58, 44], fill=PAL['mid'])             # 沿
    d.ellipse([8, 27, 56, 42], fill=PAL['dk2'])
    d.ellipse([10, 28, 54, 41], fill=PAL['dk'])
    d.arc([6, 26, 58, 44], 170, 320, fill=PAL['hl'], width=3)   # 沿高光
    d.chord([10, 32, 54, 57], 15, 165, fill=PAL['mid'])     # 碗身（与沿衔接）
    d.ellipse([10, 45, 54, 57], fill=PAL['lo2'])            # 底 1/3 压暗
    d.ellipse([13, 32, 26, 40], fill=PAL['hi'])             # 外壁左上高光
    d.ellipse([22, 56, 42, 63], fill=PAL['lo'])             # 圈足
    d.ellipse([24, 58, 40, 63], fill=PAL['dk2'])
    d.arc([24, 58, 40, 64], 180, 360, fill=PAL['gold_d'], width=2)

def draw_censer(d):
    """小银炉：双立耳、宽扁身、三足、金色弦纹"""
    d.arc([6, 10, 26, 32], 210, 90, fill=PAL['lo2'], width=6)    # 左立耳（粗短）
    d.arc([38, 10, 58, 32], 90, 330, fill=PAL['lo2'], width=6)   # 右立耳
    d.arc([7, 11, 25, 31], 210, 80, fill=PAL['mid'], width=3)
    d.arc([39, 11, 57, 31], 100, 330, fill=PAL['mid'], width=3)
    d.ellipse([16, 26, 48, 36], fill=PAL['dk2'])            # 炉口
    d.ellipse([18, 27, 46, 35], fill=PAL['dk'])
    d.ellipse([13, 25, 51, 40], fill=PAL['mid'])            # 口沿
    d.ellipse([15, 26, 49, 38], fill=PAL['dk2'])
    d.ellipse([17, 27, 47, 36], fill=PAL['dk'])
    d.chord([12, 30, 52, 56], 20, 160, fill=PAL['mid'])     # 炉身
    d.ellipse([12, 46, 52, 56], fill=PAL['lo2'])            # 底部压暗
    d.ellipse([16, 32, 28, 40], fill=PAL['hi'])             # 左上高光
    d.rectangle([12, 36, 52, 39], fill=PAL['gold'])         # 金弦纹（紧贴口沿）
    d.rectangle([12, 36, 52, 37], fill=PAL['gold_l'])
    for lx in (18, 30, 42):                                  # 三足
        d.ellipse([lx - 3, 54, lx + 3, 62], fill=PAL['lo'])
        d.ellipse([lx - 2, 55, lx + 2, 60], fill=PAL['lo2'])

def draw_chopsticks(d):
    """银箸一对：斜置拉开间距，束头单箍，尾端渐细"""
    for (x0, y0, x1, y1) in [(14, 6, 32, 58), (28, 4, 46, 56)]:
        d.line([x0, y0, x1, y1], fill=PAL['dk'], width=5)
        d.line([x0 + 1, y0, x1 + 1, y1], fill=PAL['mid'], width=3)
        d.line([x0 + 2, y0 + 1, x1 + 2, y1], fill=PAL['hi'], width=1)
        d.line([x0 + 3, y0 + 2, x1 + 3, y1 - 2], fill=PAL['hl'], width=1)  # 棱高光
        d.line([x1 - 1, y1 - 2, x1 + 2, y1 + 1], fill=PAL['lo'], width=3)  # 尾端渐细
    d.rectangle([12, 14, 42, 18], fill=PAL['gold'])          # 束头单箍（横跨两根）
    d.rectangle([12, 14, 42, 15], fill=PAL['gold_l'])
    d.rectangle([38, 46, 50, 49], fill=PAL['gold_d'])        # 中段细箍
    d.rectangle([38, 46, 50, 47], fill=PAL['gold'])

BUILDERS = {
    'cup_silver': draw_cup,
    'bowl_silver': draw_bowl,
    'censer_silver': draw_censer,
    'chopsticks_silver': draw_chopsticks,
}

def main():
    results = {}
    for name, fn in BUILDERS.items():
        big = Image.new('RGBA', (SS, SS), (0, 0, 0, 0))
        fn(ImageDraw.Draw(big))
        results[name] = process(big)
        results[name].save(os.path.join(OUT, f'{name}.png'))
    # 三联对比：v2 新版 | v1 旧版 | 原作参考
    font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 14)
    atlas = Image.open(r'C:\测试工作区\probably-stolen-study\analysis\items_medical_atlas.png').convert('RGBA')
    ref = atlas.crop((400, 300, 470, 380)).resize((210, 240), Image.NEAREST)
    names = list(BUILDERS.keys())
    ROW = 136
    sheet = Image.new('RGBA', (620, rows_h := (rows := len(names)) * ROW + 260), (35, 37, 43, 255))
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
    sheet.save(os.path.join(OUT, 'compare_r2.png'))
    print('r2 OK:', names)

if __name__ == '__main__':
    main()
