# -*- coding: utf-8 -*-
"""第14轮(自动化)：瓷器收官 8 件（青瓷系/粉彩/五彩/郎红/粗碗）→ 瓷器 20/20"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

GLZ_L = (232, 224, 196, 255)
GLZ  = (213, 210, 184, 255)
GLZ_D = (186, 178, 148, 255)
INK  = (68, 70, 76, 255)
RED  = (156, 55, 56, 255)
RED_L = (192, 100, 96, 255)
# 青瓷（龙泉，比汝窑偏绿）
CE_L = (150, 190, 172, 255)
CE  = (108, 152, 128, 255)
CE_D = (74, 112, 94, 255)
# 五彩
WC_R = (196, 60, 56, 255)
WC_G = (105, 148, 74, 255)
WC_Y = (217, 182, 80, 255)
# 郎红
LH_L = (192, 70, 62, 255)
LH  = (166, 48, 44, 255)
LH_D = (120, 32, 30, 255)
# 粗陶
CU_L = (140, 122, 100, 255)
CU  = (117, 100, 80, 255)
CU_D = (84, 72, 58, 255)

def draw_ru_plate(d):
    """汝窑盘：宽浅盘+天青+细开片"""
    d.ellipse([6, 16, 58, 50], fill=(172, 200, 196, 255))
    d.ellipse([10, 19, 54, 47], fill=(129, 158, 158, 255))
    d.ellipse([15, 22, 49, 44], fill=(172, 200, 196, 255))
    for (x0, y0, x1, y1) in [(20, 26, 30, 36), (32, 24, 28, 38), (34, 28, 44, 34), (22, 38, 34, 40), (40, 36, 46, 40)]:
        d.line([x0, y0, x1, y1], fill=(94, 122, 122, 255), width=1)
    d.ellipse([16, 24, 24, 30], fill=(200, 220, 216, 255))
    d.arc([6, 16, 58, 50], 180, 320, fill=(210, 228, 224, 255), width=2)
    d.ellipse([26, 46, 38, 51], fill=(94, 122, 122, 255))            # 底足

def draw_celadon_lotus(d):
    """青瓷莲瓣碗：敞口碗+腹部莲瓣凸棱"""
    d.ellipse([10, 20, 54, 36], fill=(170, 204, 186, 255))          # 口沿
    d.ellipse([13, 22, 51, 34], fill=(74, 112, 94, 255))            # 口内
    d.ellipse([12, 24, 52, 58], fill=CE)                            # 碗身
    d.ellipse([14, 26, 50, 56], fill=CE_L)
    d.ellipse([14, 42, 50, 58], fill=CE_D)                          # 底压暗
    for lx in (16, 24, 32, 40, 46):                                  # 莲瓣棱（竖凸线）
        d.line([lx, 34, lx - 2, 54], fill=CE_D, width=2)
        d.line([lx + 1, 34, lx - 1, 53], fill=(190, 220, 200, 255), width=1)
    d.ellipse([17, 26, 27, 32], fill=(220, 240, 224, 255))          # 左上釉光
    d.rectangle([26, 56, 38, 61], fill=CE_D)                        # 圈足
    d.ellipse([24, 60, 40, 64], fill=CE_L)

def draw_fencai(d):
    """粉彩瓶：白釉+粉彩人物色带+绿叶"""
    d.rounded_rectangle([27, 2, 37, 20], 3, fill=GLZ_L)             # 颈
    d.rectangle([28, 3, 36, 19], fill=GLZ)
    d.ellipse([14, 18, 50, 56], fill=GLZ)                           # 瓶体
    d.ellipse([16, 20, 48, 54], fill=GLZ_L)
    d.ellipse([16, 42, 48, 56], fill=GLZ_D)
    d.ellipse([24, 26, 40, 44], fill=(196, 130, 152, 255))          # 粉彩主纹
    d.ellipse([28, 30, 36, 40], fill=(232, 180, 196, 255))
    d.ellipse([30, 32, 34, 37], fill=(120, 52, 70, 255))            # 花心
    d.polygon([(18, 38), (24, 42), (20, 46)], fill=(105, 148, 74, 255))  # 绿叶
    d.polygon([(44, 36), (38, 42), (44, 46)], fill=(105, 148, 74, 255))
    d.rectangle([26, 54, 38, 59], fill=GLZ_D)
    d.ellipse([24, 58, 40, 63], fill=GLZ_L)

def draw_buried_jar(d):
    """出土青瓷罐：缺盖直口+土锈斑"""
    d.ellipse([18, 4, 46, 12], fill=(120, 112, 92, 255))            # 直口（缺盖）
    d.ellipse([20, 5, 44, 11], fill=(84, 72, 58, 255))
    d.ellipse([10, 10, 54, 56], fill=(108, 152, 128, 255))          # 罐体（青瓷）
    d.ellipse([12, 12, 52, 54], fill=(150, 190, 172, 255))
    d.ellipse([14, 42, 52, 56], fill=(74, 112, 94, 255))            # 底压暗
    # 土锈斑（赭褐附着）
    for (bx, by, bw, bh) in [(16, 18, 12, 9), (36, 24, 14, 10), (22, 34, 10, 8), (38, 40, 12, 9)]:
        d.ellipse([bx, by, bx + bw, by + bh], fill=(139, 118, 82, 255))
        d.ellipse([bx + 2, by + 2, bx + bw - 2, by + bh - 2], fill=(117, 100, 80, 255))
    d.ellipse([18, 14, 30, 22], fill=(190, 210, 190, 255))          # 残存釉光
    d.rectangle([24, 54, 40, 59], fill=(84, 72, 58, 255))

def draw_wucai_bowl(d):
    """五彩碗：白釉碗+红绿黄满彩纹"""
    d.ellipse([8, 20, 56, 36], fill=GLZ_L)
    d.ellipse([11, 22, 53, 34], fill=GLZ_D)
    d.ellipse([13, 23, 51, 32], fill=GLZ)
    d.ellipse([12, 24, 52, 58], fill=GLZ)                           # 碗身
    d.ellipse([14, 26, 50, 56], fill=GLZ_L)
    d.ellipse([14, 44, 50, 58], fill=GLZ_D)
    # 满彩纹带（红绿黄相间弧带）
    d.arc([14, 30, 50, 48], 200, 340, fill=WC_R, width=3)
    d.arc([16, 34, 48, 50], 200, 340, fill=WC_G, width=3)
    d.arc([18, 38, 46, 52], 200, 340, fill=WC_Y, width=2)
    d.ellipse([26, 30, 38, 40], fill=WC_R)                          # 主花
    d.ellipse([29, 33, 35, 37], fill=WC_Y)
    d.ellipse([16, 25, 24, 30], fill=(230, 224, 200, 255))
    d.arc([8, 20, 56, 36], 170, 320, fill=(240, 236, 226, 255), width=2)
    d.rectangle([26, 56, 38, 61], fill=GLZ_D)
    d.ellipse([24, 60, 40, 64], fill=GLZ_L)

def draw_celadon_pair(d):
    """青瓷盏一对：宽浅小盏并排（间距>6px）"""
    for cx in (6, 34):
        d.ellipse([cx, 26, cx + 24, 40], fill=(170, 204, 186, 255)) # 宽口
        d.ellipse([cx + 2, 28, cx + 22, 38], fill=(74, 112, 94, 255))  # 口内
        d.ellipse([cx + 2, 28, cx + 22, 44], fill=CE)               # 浅身
        d.ellipse([cx + 4, 30, cx + 20, 44], fill=CE_L)
        d.ellipse([cx + 4, 38, cx + 20, 45], fill=CE_D)             # 底压暗
        d.ellipse([cx + 4, 29, cx + 11, 33], fill=(220, 240, 224, 255))  # 釉光
        d.rectangle([cx + 9, 43, cx + 15, 48], fill=CE_D)           # 矮圈足
    d.ellipse([26, 14, 34, 22], fill=RED)                           # 中间标印

def draw_langhong(d):
    """郎红釉瓶：撇口+直颈+垂腹，红釉垂流+灯草边"""
    d.ellipse([22, 2, 42, 10], fill=LH_L)                           # 撇口
    d.ellipse([25, 3, 39, 8], fill=(120, 32, 30, 255))              # 口内
    d.rectangle([28, 8, 36, 24], fill=LH)                           # 颈
    d.ellipse([14, 22, 50, 56], fill=LH)                            # 垂腹
    d.ellipse([16, 24, 48, 54], fill=LH_L)
    d.ellipse([16, 42, 48, 56], fill=LH_D)                          # 底部釉浓
    d.line([24, 24, 22, 44], fill=LH_D, width=2)                    # 垂釉纹
    d.line([40, 26, 42, 46], fill=LH_D, width=2)
    d.ellipse([18, 26, 30, 36], fill=(220, 90, 80, 255))            # 釉面高光
    d.arc([14, 22, 50, 34], 180, 360, fill=(240, 200, 190, 255), width=2)  # 灯草边（白口沿）
    d.ellipse([14, 22, 50, 32], fill=(232, 224, 196, 255))
    d.ellipse([17, 23, 47, 30], fill=LH_L)
    d.rectangle([26, 55, 38, 60], fill=GLZ_D)                       # 圈足
    d.ellipse([24, 58, 40, 63], fill=GLZ_L)

def draw_junk_bowl(d):
    """豁口粗碗：灰陶+大豁口+串烟痕"""
    d.ellipse([10, 22, 54, 38], fill=CU_L)                          # 口沿（粗）
    d.ellipse([13, 24, 51, 36], fill=CU_D)
    d.ellipse([12, 24, 52, 58], fill=CU)                            # 碗身
    d.ellipse([14, 26, 50, 56], fill=CU_L)
    d.ellipse([14, 44, 50, 58], fill=CU_D)
    d.polygon([(40, 24), (48, 28), (44, 22)], fill=(0, 0, 0, 0))    # 大豁口
    d.line([40, 24, 48, 30], fill=CU_D, width=2)                    # 豁口边缘
    for sy in (30, 36):                                              # 串烟痕（黑晕）
        d.arc([16, sy, 44, sy + 10], 200, 340, fill=(58, 52, 48, 255), width=3)
    d.line([18, 28, 20, 46], fill=(140, 130, 118, 255), width=1)    # 粗釉流
    d.rectangle([24, 56, 40, 61], fill=CU_D)                        # 圈足（歪）
    d.ellipse([22, 59, 42, 65], fill=(58, 52, 48, 255))

BUILDERS = {
    'plate_ru_celadon': draw_ru_plate,
    'bowl_celadon_lotus': draw_celadon_lotus,
    'vase_fencai': draw_fencai,
    'jar_celadon_buried': draw_buried_jar,
    'bowl_wucai': draw_wucai_bowl,
    'cup_celadon_pair': draw_celadon_pair,
    'vase_langhong': draw_langhong,
    'bowl_cracked_junk': draw_junk_bowl,
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
    sheet.save(os.path.join(OUT, 'compare_r15.png'))
    print('r15 OK:', names)

if __name__ == '__main__':
    main()
