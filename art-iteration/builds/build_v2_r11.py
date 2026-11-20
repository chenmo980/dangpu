# -*- coding: utf-8 -*-
"""第10轮(自动化)：字画第 3 批 scroll_broken/scroll_spring/album_thumbed/fan_broken/painting_horses/calligraphy_seal"""
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
TEAL   = (69, 145, 139, 255)
TEAL_D = (47, 117, 111, 255)
RED    = (156, 55, 56, 255)
GOLD   = (186, 137, 83, 255)
GOLD_L = (224, 208, 155, 255)

def draw_scroll_broken(d):
    """残卷断轴：断裂错位+缺角+霉斑"""
    d.rounded_rectangle([20, 2, 44, 7], 2, fill=ROD_D)              # 上轴头（暗=旧）
    d.rectangle([16, 7, 46, 26], fill=PAPER_D)                      # 上半段（脏）
    d.polygon([(40, 22), (46, 22), (46, 30), (42, 26)], fill=(0, 0, 0, 0))  # 缺角
    d.line([16, 26, 46, 26], fill=INK, width=2)                     # 断口
    d.rectangle([20, 28, 44, 48], fill=PAPER_D)                     # 下半段（错位）
    d.rectangle([24, 30, 40, 46], fill=PAPER)                       # 残画心
    for (mx, my) in [(22, 32), (38, 30), (26, 42), (40, 44)]:        # 霉斑
        d.ellipse([mx, my, mx + 3, my + 3], fill=(120, 112, 92, 255))
    d.ellipse([20, 48, 44, 54], fill=ROD_D)                         # 下轴头
    d.line([16, 7, 46, 7], fill=INK_L, width=1)

def draw_scroll_spring(d):
    """春景横披：横向+柳枝+燕子+远山"""
    d.rounded_rectangle([4, 6, 20, 10], 2, fill=ROD)                # 左轴头
    d.rounded_rectangle([44, 6, 60, 10], 2, fill=ROD)               # 右轴头
    d.rectangle([6, 10, 58, 46], fill=PAPER)
    d.rectangle([6, 10, 58, 13], fill=PAPER_L)
    d.polygon([(10, 42), (22, 30), (34, 42)], fill=TEAL)            # 远山
    d.polygon([(28, 42), (42, 32), (54, 42)], fill=TEAL_D)
    d.arc([12, 16, 30, 34], 250, 40, fill=(140, 170, 100, 255), width=2)  # 柳枝
    d.arc([14, 18, 32, 36], 250, 40, fill=(140, 170, 100, 255), width=1)
    d.polygon([(30, 22), (35, 19), (37, 24)], fill=INK)             # 燕子 1
    d.polygon([(38, 18), (43, 15), (45, 20)], fill=INK)             # 燕子 2
    d.line([8, 44, 56, 44], fill=INK_L, width=1)                    # 水纹
    d.rectangle([48, 14, 53, 19], fill=RED)
    d.rectangle([6, 46, 58, 50], fill=PAPER_D)

def draw_album_thumbed(d):
    """油渍册页：歪斜叠页+油渍晕+缺页角"""
    d.rounded_rectangle([12, 16, 54, 54], 3, fill=PAPER_D)
    d.polygon([(14, 18), (52, 16), (50, 52), (16, 54)], fill=PAPER)  # 歪斜页
    d.polygon([(16, 20), (48, 18), (46, 50), (18, 52)], fill=PAPER_L)
    d.ellipse([24, 26, 40, 42], fill=(196, 178, 130, 255))           # 油渍晕
    d.ellipse([28, 30, 36, 38], fill=(178, 158, 108, 255))
    d.polygon([(52, 18), (52, 30), (42, 18)], fill=(0, 0, 0, 0))     # 缺角
    d.line([16, 22, 46, 20], fill=INK_L, width=1)                    # 字痕
    d.rectangle([42, 44, 47, 49], fill=RED)
    d.line([20, 52, 46, 50], fill=INK, width=1)                      # 折痕

def draw_fan_broken(d):
    """残破折扇：扇骨折断错位+面撕+缺边"""
    d.polygon([(28, 58), (18, 14), (24, 12), (38, 54)], fill=PAPER_D)
    d.polygon([(28, 58), (24, 12), (30, 10), (42, 50)], fill=PAPER)
    d.polygon([(28, 58), (30, 10), (34, 8), (40, 46)], fill=PAPER_L)
    d.polygon([(30, 10), (34, 8), (36, 12)], fill=(0, 0, 0, 0))      # 缺边
    d.line([24, 12, 20, 16], fill=ROD_D, width=3)                    # 断骨翘起
    d.line([36, 20, 44, 24], fill=PAPER_D, width=3)                  # 撕裂面
    d.line([34, 22, 40, 28], fill=(0, 0, 0, 0), width=2)             # 撕口
    for (x0, y0, x1, y1) in [(22, 12, 32, 55), (30, 9, 38, 52)]:
        d.line([x0, y0, x1, y1], fill=ROD_D, width=1)
    d.ellipse([25, 54, 33, 62], fill=ROD)
    d.ellipse([27, 56, 31, 60], fill=GOLD)

def draw_horses(d):
    """百马图卷：横卷+三马剪影群"""
    d.rounded_rectangle([6, 12, 22, 18], 2, fill=ROD)               # 左轴头
    d.rounded_rectangle([42, 12, 58, 18], 2, fill=ROD)              # 右轴头
    d.rectangle([6, 18, 58, 44], fill=PAPER)
    d.rectangle([6, 18, 58, 21], fill=PAPER_L)
    # 马 1（棕，站）
    d.ellipse([10, 30, 24, 40], fill=(176, 138, 90, 255))
    d.ellipse([8, 26, 16, 34], fill=(154, 116, 70, 255))
    d.line([12, 40, 11, 46], fill=(120, 88, 52, 255), width=2)
    d.line([20, 40, 21, 46], fill=(120, 88, 52, 255), width=2)
    d.line([24, 32, 29, 26], fill=(120, 88, 52, 255), width=2)      # 尾
    # 马 2（青，卧）
    d.ellipse([30, 34, 46, 42], fill=TEAL)
    d.ellipse([44, 30, 52, 38], fill=TEAL_D)
    d.line([46, 38, 50, 42], fill=TEAL_D, width=2)
    # 马 3（黑，小马）
    d.ellipse([36, 24, 46, 32], fill=INK_L)
    d.ellipse([34, 21, 40, 27], fill=INK_L)
    d.rectangle([50, 22, 54, 26], fill=RED)
    d.line([6, 44, 58, 44], fill=INK_L, width=1)
    d.rectangle([6, 44, 58, 48], fill=PAPER_D)

def draw_seal_book(d):
    """名家印谱：蓝布函套+打开页红印泥方阵"""
    d.rounded_rectangle([10, 10, 54, 54], 4, fill=(47, 74, 111, 255))  # 函套
    d.rounded_rectangle([13, 13, 51, 51], 3, fill=(63, 92, 133, 255))
    d.rounded_rectangle([16, 16, 48, 42], 2, fill=PAPER)            # 打开印谱页
    d.rounded_rectangle([16, 16, 48, 20], 2, fill=PAPER_L)
    for gy in (22, 30, 38):                                          # 印拓方阵
        for gx in (20, 28, 36):
            d.ellipse([gx, gy, gx + 6, gy + 6], fill=RED)
            d.ellipse([gx + 1, gy + 1, gx + 5, gy + 5], fill=(192, 100, 96, 255))
            d.rectangle([gx + 2, gy + 2, gx + 4, gy + 4], fill=PAPER)  # 印文白
    d.rectangle([30, 44, 40, 52], fill=PAPER)                       # 题签
    ink_rows = [(32, 46), (33, 49)]
    for (ix, iy) in ink_rows:
        d.line([ix, iy, ix + 6, iy], fill=INK, width=1)
    d.rectangle([17, 17, 21, 21], fill=PAL['gold_d'])               # 函套角饰

BUILDERS = {
    'scroll_broken': draw_scroll_broken,
    'scroll_spring': draw_scroll_spring,
    'album_thumbed': draw_album_thumbed,
    'fan_broken': draw_fan_broken,
    'painting_horses': draw_horses,
    'calligraphy_seal': draw_seal_book,
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
    sheet.save(os.path.join(OUT, 'compare_r11.png'))
    print('r11 OK:', names)

if __name__ == '__main__':
    main()
