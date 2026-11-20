# -*- coding: utf-8 -*-
"""第15轮(自动化)：钟表第 1 批 6 件 clock_tallcase/watch_pocket_gold/watch_pocket_silver/
clock_wall_round/compass_marine/astrolabe
clock v2 配方：表盘圆+刻度点+指针两针+外壳金属/木 ramp+玻璃高光
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

ROD  = (92, 58, 33, 255)
ROD_D = (74, 48, 28, 255)
ROD_L = (140, 101, 64, 255)
SIL_L = (213, 210, 184, 255)
SIL = (168, 174, 165, 255)
SIL_D = (121, 116, 110, 255)
INK = (68, 70, 76, 255)
INK_L = (95, 104, 104, 255)
GOLD = (186, 137, 83, 255)
GOLD_L = (224, 208, 155, 255)
RED = (156, 55, 56, 255)
TEAL = (69, 145, 139, 255)

def clock_face(d, cx, cy, r, hands=True):
    """表盘：刻度 12 点+指针"""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SIL_L)
    d.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], fill=(240, 236, 226, 255))
    import math
    for i in range(12):
        ang = math.radians(i * 30)
        tx = cx + (r - 3) * math.sin(ang)
        ty = cy - (r - 3) * math.cos(ang)
        d.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=INK)
    if hands:
        import math as m
        ha = m.radians(60); ma = m.radians(170)
        d.line([cx, cy, cx + (r - 6) * m.sin(ha), cy - (r - 6) * m.cos(ha)], fill=INK, width=2)   # 时针
        d.line([cx, cy, cx + (r - 4) * m.sin(ma), cy - (r - 4) * m.cos(ma)], fill=INK, width=1)   # 分针
        d.point([(cx, cy)], fill=RED)

def draw_tallcase(d):
    """红木座钟：立柜形+顶檐+钟面+摆窗"""
    d.rounded_rectangle([18, 2, 46, 10], 3, fill=ROD_D)             # 顶檐
    d.rectangle([16, 10, 48, 60], fill=ROD)                          # 柜体
    d.rectangle([18, 12, 46, 58], fill=ROD_L)
    d.rectangle([19, 13, 45, 32], fill=SIL_L)                        # 钟面窗
    clock_face(d, 32, 22, 10)
    d.rectangle([19, 36, 45, 57], fill=(52, 34, 20, 255))            # 摆窗
    d.line([31, 38, 31, 54], fill=GOLD, width=2)                     # 摆杆
    d.ellipse([28, 52, 36, 58], fill=GOLD)                           # 摆锤
    d.line([31, 53, 32, 57], fill=GOLD_L, width=1)
    d.rectangle([16, 58, 48, 62], fill=ROD_D)                        # 底座

def draw_pocket_gold(d):
    """金怀表：圆金壳+白面+表冠+链环"""
    d.ellipse([10, 10, 54, 54], fill=GOLD)                           # 壳
    d.ellipse([13, 13, 51, 51], fill=GOLD_L)
    d.ellipse([16, 16, 48, 48], fill=(240, 236, 226, 255))           # 白面
    clock_face(d, 32, 32, 12)
    d.ellipse([28, 2, 36, 10], fill=GOLD)                            # 表冠
    d.ellipse([30, 0, 34, 6], fill=(0, 0, 0, 0))
    d.ellipse([29, 1, 35, 7], fill=GOLD_L)                           # 冠顶环
    d.line([32, 1, 32, -1], fill=GOLD, width=1) if False else None
    d.ellipse([14, 12, 22, 20], fill=(230, 210, 170, 255))           # 左上高光

def draw_pocket_silver(d):
    """银怀表：银壳+刻度更细"""
    d.ellipse([10, 10, 54, 54], fill=SIL)
    d.ellipse([13, 13, 51, 51], fill=SIL_L)
    d.ellipse([16, 16, 48, 48], fill=(240, 236, 226, 255))
    clock_face(d, 32, 32, 12)
    d.ellipse([28, 2, 36, 10], fill=SIL)
    d.ellipse([29, 1, 35, 7], fill=SIL_L)
    d.ellipse([14, 12, 22, 20], fill=(230, 232, 224, 255))
    d.arc([12, 12, 52, 52], 60, 120, fill=SIL_D, width=2)            # 右下壳影

def draw_wall_round(d):
    """圆形挂钟：木圈+白面+下方摆锤露"""
    d.ellipse([8, 2, 56, 50], fill=ROD_D)                            # 木圈
    d.ellipse([11, 5, 53, 47], fill=ROD)
    d.ellipse([14, 8, 50, 44], fill=(240, 236, 226, 255))
    clock_face(d, 32, 26, 12)
    d.line([31, 48, 31, 60], fill=GOLD, width=2)                     # 摆杆
    d.ellipse([28, 58, 35, 64], fill=GOLD)
    d.rectangle([29, 0, 35, 4], fill=ROD)                            # 挂钩座

def draw_compass(d):
    """航海罗盘：黄铜圆壳+玻璃罩+罗盘面+指针菱形"""
    d.ellipse([8, 8, 56, 56], fill=GOLD)                             # 壳
    d.ellipse([12, 12, 52, 52], fill=GOLD_L)
    d.ellipse([16, 16, 48, 48], fill=(240, 236, 226, 255))           # 盘面
    import math as m
    for i in range(8):
        ang = m.radians(i * 45)
        tx = 32 + 13 * m.sin(ang); ty = 32 - 13 * m.cos(ang)
        d.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=INK)
    d.polygon([(32, 18), (36, 32), (32, 36)], fill=RED)              # 北针（红）
    d.polygon([(32, 36), (36, 32), (28, 32)], fill=INK)              # 南针
    d.ellipse([30, 30, 34, 34], fill=GOLD)                           # 轴心
    d.ellipse([17, 17, 24, 24], fill=(240, 240, 224, 255))           # 玻璃高光
    d.arc([8, 8, 56, 56], 30, 130, fill=GOLD_L, width=2)             # 壳高光

def draw_astrolabe(d):
    """星盘仪：大环+内盘刻度+吊环+指针星"""
    d.ellipse([10, 8, 54, 52], outline=GOLD, width=4)                # 外环
    d.ellipse([15, 13, 49, 47], outline=SIL, width=2)                # 内环
    d.ellipse([17, 15, 47, 45], fill=(240, 236, 226, 255))           # 盘面
    import math as m
    for i in range(12):
        ang = m.radians(i * 30)
        tx = 32 + 11 * m.sin(ang); ty = 30 - 11 * m.cos(ang)
        d.line([tx - 1, ty, tx + 1, ty], fill=INK, width=1)
        d.line([tx, ty - 1, tx, ty + 1], fill=INK, width=1)
    d.line([32, 30, 44, 18], fill=INK, width=2)                      # 照准针 1
    d.line([32, 30, 20, 40], fill=INK_L, width=2)                    # 照准针 2
    d.ellipse([30, 28, 34, 32], fill=GOLD)                           # 中心
    d.ellipse([28, 2, 36, 10], outline=GOLD, width=3)                # 吊环
    for (sx, sy) in [(24, 34), (40, 36), (36, 26)]:                   # 星点
        d.point([(sx, sy)], fill=GOLD_L)
        d.point([(sx + 1, sy)], fill=GOLD)

BUILDERS = {
    'clock_tallcase': draw_tallcase,
    'watch_pocket_gold': draw_pocket_gold,
    'watch_pocket_silver': draw_pocket_silver,
    'clock_wall_round': draw_wall_round,
    'compass_marine': draw_compass,
    'astrolabe': draw_astrolabe,
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
    sheet.save(os.path.join(OUT, 'compare_r16.png'))
    print('r16 OK:', names)

if __name__ == '__main__':
    main()
