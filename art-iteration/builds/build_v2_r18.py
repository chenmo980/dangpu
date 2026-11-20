# -*- coding: utf-8 -*-
"""第17轮(自动化)：玉器第 1 批 6 件 bangle_jade_white/pendant_jade_gu/ruyi_jade/archer_ring_feicui/boulder_jade_shanzi/cicada_jade_han
jade v2 配方：玉色 ramp（青白玉/翠玉）+高光弧+沁色斑+雕纹线
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

# 玉色族
J_L = (222, 230, 214, 255)   # 青白玉亮
J  = (188, 202, 182, 255)    # 青白玉
J_D = (150, 168, 150, 255)   # 青白玉暗
F_L = (130, 208, 160, 255)   # 翡翠亮
F  = (84, 178, 118, 255)     # 翡翠
F_D = (52, 132, 84, 255)     # 翡翠暗
QIN = (160, 128, 84, 255)    # 沁色（土沁黄）

def jade_shine(d, x0, y0, x1, y1):
    """玉面高光弧"""
    d.arc([x0, y0, x1, y1], 190, 300, fill=(240, 244, 232, 255), width=2)

def draw_bangle(d):
    """白玉镯：圆环+玉面渐变+沁点"""
    d.ellipse([10, 12, 54, 52], fill=J_D)
    d.ellipse([13, 15, 51, 49], fill=J)
    d.ellipse([17, 19, 47, 45], fill=J_L)
    d.ellipse([22, 24, 42, 40], fill=(0, 0, 0, 0))
    jade_shine(d, 12, 14, 52, 50)
    d.ellipse([40, 14, 47, 21], fill=QIN)                       # 沁色点
    d.ellipse([42, 16, 45, 19], fill=J_L)

def draw_gu_pendant(d):
    """玉珏：缺口环形佩+系孔"""
    d.ellipse([14, 14, 50, 50], fill=J_D)
    d.ellipse([17, 17, 47, 47], fill=J)
    d.ellipse([21, 21, 43, 43], fill=J_L)
    d.polygon([(32, 10), (28, 16), (36, 16)], fill=(0, 0, 0, 0))  # 顶缺口（珏的开口）
    d.ellipse([29, 24, 35, 30], fill=(0, 0, 0, 0))               # 系孔
    jade_shine(d, 16, 16, 48, 46)
    d.ellipse([20, 36, 27, 43], fill=QIN)                        # 沁色
    d.line([20, 20, 28, 28], fill=J_D, width=1)                  # 雕纹

def draw_ruyi(d):
    """玉如意：云头首+弯柄+尾坠"""
    d.ellipse([6, 8, 28, 26], fill=J)                            # 云头左卷
    d.ellipse([9, 11, 25, 23], fill=J_L)
    d.ellipse([18, 4, 40, 22], fill=J)                           # 云头中卷
    d.ellipse([21, 7, 37, 19], fill=J_L)
    d.ellipse([34, 8, 56, 26], fill=J)                           # 云头右卷
    d.ellipse([37, 11, 53, 23], fill=J_L)
    d.ellipse([26, 8, 34, 16], fill=QIN)                         # 头心沁
    d.arc([28, 22, 44, 58], 200, 40, fill=J_D, width=7)          # 弯柄
    d.arc([28, 22, 44, 58], 200, 40, fill=J, width=4)
    d.arc([29, 23, 43, 57], 200, 40, fill=J_L, width=1)
    d.ellipse([40, 52, 52, 62], fill=J)                          # 尾坠
    d.ellipse([42, 54, 50, 60], fill=J_L)
    jade_shine(d, 8, 6, 56, 26)
    d.line([24, 12, 30, 16], fill=J_D, width=1)                  # 头部雕纹

def draw_archer_ring(d):
    """翡翠扳指：厚壁短环+翠色渐变+白棉"""
    d.ellipse([12, 16, 52, 48], fill=F_D)
    d.ellipse([15, 19, 49, 45], fill=F)
    d.ellipse([19, 23, 45, 41], fill=F_L)
    d.ellipse([24, 26, 40, 38], fill=(0, 0, 0, 0))
    d.ellipse([15, 19, 30, 34], fill=(120, 200, 150, 255))       # 翠色浓处
    d.ellipse([18, 21, 27, 31], fill=F_L)
    d.ellipse([34, 30, 42, 37], fill=(230, 234, 220, 255))       # 白棉
    d.point([(37, 33)], fill=F_L)
    jade_shine(d, 14, 18, 50, 46)

def draw_shanzi(d):
    """玉山子：山形雕件（随形玉料+山水浮雕）"""
    d.polygon([(6, 58), (16, 26), (28, 14), (44, 22), (56, 44), (58, 58)], fill=J_D)
    d.polygon([(9, 56), (17, 28), (28, 16), (42, 24), (54, 44), (56, 56)], fill=J)
    d.polygon([(12, 54), (18, 30), (28, 18), (40, 26), (50, 44), (52, 54)], fill=J_L)
    d.polygon([(22, 34), (28, 22), (34, 34)], fill=J)            # 内雕小山
    d.polygon([(34, 40), (40, 30), (46, 40)], fill=J)
    d.line([26, 40, 34, 48], fill=J_D, width=1)                  # 浮雕亭台痕
    d.rectangle([30, 42, 36, 48], fill=J)
    d.line([31, 43, 35, 43], fill=J_D, width=1)
    d.ellipse([36, 46, 44, 52], fill=QIN)                        # 底部沁
    jade_shine(d, 12, 14, 54, 56)

def draw_cicada(d):
    """玉蝉 v2.1：汉八刀风——横体、双斜削大翅、横额线"""
    # 头（左端横条）
    d.rounded_rectangle([6, 24, 16, 40], 3, fill=J_D)
    d.rounded_rectangle([7, 26, 15, 38], 2, fill=J)
    # 双翅（两大斜削三角，向右上展开）
    d.polygon([(14, 26), (44, 10), (52, 24), (24, 36)], fill=J)
    d.polygon([(16, 27), (42, 13), (48, 23), (26, 34)], fill=J_L)
    d.polygon([(14, 32), (40, 24), (48, 36), (22, 42)], fill=J_D)   # 右翅底层
    d.polygon([(16, 33), (38, 26), (45, 35), (24, 41)], fill=J)     # 右翅面
    # 背脊（汉八刀中缝）
    d.line([8, 32, 50, 30], fill=J_D, width=2)
    # 腹（右端收窄）
    d.polygon([(44, 26), (58, 30), (58, 42), (44, 40)], fill=J)
    d.line([46, 30, 56, 34], fill=J_D, width=1)
    # 刀痕斜线（汉八刀特征）
    d.line([20, 30, 34, 16], fill=J_D, width=1)
    d.line([24, 36, 38, 24], fill=J_D, width=1)
    d.ellipse([10, 34, 16, 40], fill=QIN)                           # 沁色
    jade_shine(d, 16, 14, 48, 40)

BUILDERS = {
    'bangle_jade_white': draw_bangle,
    'pendant_jade_gu': draw_gu_pendant,
    'ruyi_jade': draw_ruyi,
    'archer_ring_feicui': draw_archer_ring,
    'boulder_jade_shanzi': draw_shanzi,
    'cicada_jade_han': draw_cicada,
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
    sheet.save(os.path.join(OUT, 'compare_r18.png'))
    print('r18 OK:', names)

if __name__ == '__main__':
    main()
