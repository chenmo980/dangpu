# -*- coding: utf-8 -*-
"""第12轮(自动化)：瓷器第 1 批（青花系 6 件）
porcelain v2 配方：白釉体（纸白 ramp）+青花纹（teal/teal_d）+器形底部压暗+口沿高光
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

GLZ_L = (232, 224, 196, 255)   # 釉亮
GLZ   = (213, 210, 184, 255)   # 釉
GLZ_D = (186, 178, 148, 255)   # 釉暗
BQ    = (69, 145, 139, 255)    # 青花主色
BQ_D  = (47, 117, 111, 255)    # 青花深
BQ_DD = (34, 88, 84, 255)      # 青花最浓

def draw_meiping(d):
    """青花梅瓶：小口+丰肩+收腹+胫撇+缠枝纹"""
    d.ellipse([26, 4, 38, 10], fill=GLZ_L)                          # 小口
    d.rectangle([27, 8, 37, 14], fill=GLZ)                          # 短颈
    d.ellipse([12, 14, 52, 52], fill=GLZ)                           # 丰肩体
    d.ellipse([14, 16, 50, 50], fill=GLZ_L, only=None) if False else None
    d.ellipse([14, 16, 50, 48], fill=GLZ_L)
    d.ellipse([14, 34, 50, 52], fill=GLZ_D)                         # 下腹压暗
    # 缠枝纹（肩部弧带+花点）
    d.arc([16, 18, 48, 34], 180, 360, fill=BQ, width=2)
    for (fx, fy) in [(22, 22), (32, 20), (42, 22)]:
        d.ellipse([fx, fy, fx + 5, fy + 5], fill=BQ_D)
        d.point([(fx + 2, fy + 2)], fill=GLZ_L)
    # 腹部主纹（缠枝莲 2 朵）
    d.arc([18, 30, 46, 48], 200, 340, fill=BQ_D, width=2)
    d.ellipse([28, 34, 36, 42], fill=BQ)
    d.ellipse([30, 36, 34, 40], fill=BQ_DD)
    d.rectangle([22, 52, 42, 56], fill=GLZ_D)                       # 胫
    d.ellipse([24, 55, 40, 60], fill=GLZ_L)                         # 圈足

def draw_guan_ear(d):
    """青花贯耳瓶：直颈+贯耳+腹部蕉叶纹"""
    d.rounded_rectangle([26, 2, 38, 22], 3, fill=GLZ)               # 直颈
    d.rectangle([22, 4, 27, 18], fill=GLZ_L)                        # 贯耳左
    d.rectangle([37, 4, 42, 18], fill=GLZ_L)                        # 贯耳右
    d.rectangle([23, 5, 26, 17], fill=GLZ_D)
    d.rectangle([38, 5, 41, 17], fill=GLZ_D)
    d.ellipse([14, 20, 50, 56], fill=GLZ)                           # 长圆腹
    d.ellipse([16, 22, 48, 52], fill=GLZ_L)
    d.ellipse([16, 42, 48, 56], fill=GLZ_D)                         # 底部压暗
    for (lx, ly) in [(24, 28), (40, 28)]:                            # 腹部蕉叶纹
        d.polygon([(lx, ly), (lx + 4, ly + 10), (lx + 8, ly)], fill=BQ)
        d.line([lx + 4, ly + 2, lx + 4, ly + 9], fill=BQ_DD, width=1)
    d.arc([16, 34, 48, 46], 180, 360, fill=BQ_D, width=2)           # 弦纹带
    d.ellipse([24, 55, 40, 60], fill=GLZ_L)

def draw_yuhuchun(d):
    """玉壶春瓶：撇口+细颈+垂腹"""
    d.ellipse([20, 2, 44, 10], fill=GLZ_L)                          # 撇口
    d.ellipse([23, 3, 41, 9], fill=GLZ_D)                           # 口内
    d.rectangle([27, 9, 37, 26], fill=GLZ)                          # 细颈
    d.line([28, 10, 28, 25], fill=GLZ_L, width=2)
    d.ellipse([14, 24, 50, 56], fill=GLZ)                           # 垂腹
    d.ellipse([16, 26, 48, 54], fill=GLZ_L)
    d.ellipse([16, 42, 48, 56], fill=GLZ_D)
    d.arc([18, 30, 46, 44], 180, 360, fill=BQ, width=2)             # 颈下卷草
    d.ellipse([29, 36, 35, 42], fill=BQ_D)                          # 中心花
    d.polygon([(22, 40), (28, 44), (24, 47)], fill=BQ)              # 叶
    d.polygon([(42, 40), (36, 44), (40, 47)], fill=BQ)
    d.rectangle([26, 54, 38, 58], fill=GLZ_D)                       # 胫
    d.ellipse([24, 57, 40, 62], fill=GLZ_L)

def draw_bowl_dragon(d):
    """青花龙纹碗 v2.2：整椭圆身+口沿盖顶（无缝）"""
    d.ellipse([12, 24, 52, 58], fill=GLZ)                           # 碗身（整椭圆）
    d.ellipse([14, 40, 50, 58], fill=GLZ_D)                         # 底部压暗
    d.ellipse([8, 18, 56, 34], fill=GLZ_L)                          # 口沿
    d.ellipse([11, 20, 53, 31], fill=GLZ_D)                         # 碗口内壁
    d.ellipse([13, 21, 51, 30], fill=BQ_DD)                         # 碗心青花地
    d.ellipse([27, 22, 37, 29], fill=BQ)                            # 团龙身
    d.ellipse([23, 22, 29, 28], fill=BQ_D)                          # 龙首
    d.point([(26, 24)], fill=GLZ)                                   # 眼
    d.ellipse([14, 25, 22, 29], fill=(230, 224, 200, 255))          # 左上釉光
    d.arc([8, 18, 56, 34], 170, 320, fill=(240, 236, 226, 255), width=2)  # 口沿高光
    d.rectangle([26, 56, 38, 61], fill=GLZ_D)                       # 圈足
    d.ellipse([24, 60, 40, 64], fill=GLZ_L)

def draw_plate_fish(d):
    """青花鱼纹盘：浅盘俯视+盘心鱼藻"""
    d.ellipse([6, 14, 58, 52], fill=GLZ_L)                          # 盘外沿
    d.ellipse([10, 17, 54, 49], fill=GLZ)                           # 盘内
    d.ellipse([16, 21, 48, 45], fill=BQ_DD)                         # 盘心青花地
    d.ellipse([26, 27, 38, 37], fill=BQ)                            # 鱼
    d.polygon([(38, 29), (46, 25), (46, 37)], fill=BQ_D)            # 尾
    d.point([(29, 30)], fill=GLZ)                                   # 眼
    d.line([20, 25, 24, 40], fill=BQ_D, width=2)                    # 水藻
    d.line([40, 24, 44, 40], fill=BQ_D, width=2)
    d.ellipse([18, 33, 22, 37], fill=TEAL if False else (192, 100, 96, 255))  # 莲
    d.arc([6, 14, 58, 52], 180, 320, fill=(240, 236, 226, 255), width=2)
    d.ellipse([28, 48, 36, 53], fill=GLZ_D)                         # 底足

def draw_jar_guang(d):
    """青花罐：缺盖+短颈+丰肩+缠枝"""
    d.ellipse([20, 4, 44, 12], fill=GLZ_D)                          # 罐口（敞）
    d.ellipse([22, 5, 42, 11], fill=(120, 112, 104, 255))           # 口内
    d.rectangle([20, 10, 44, 18], fill=GLZ)                         # 短颈
    d.ellipse([10, 16, 54, 56], fill=GLZ)                           # 罐体
    d.ellipse([12, 18, 52, 54], fill=GLZ_L)
    d.ellipse([12, 40, 52, 56], fill=GLZ_D)                         # 底部压暗
    d.arc([14, 20, 50, 34], 180, 360, fill=BQ, width=2)             # 肩部弦纹
    for (fx, fy) in [(20, 24), (44, 24)]:                            # 肩花
        d.ellipse([fx, fy, fx + 6, fy + 6], fill=BQ_D)
    d.arc([16, 32, 48, 50], 190, 350, fill=BQ_D, width=2)           # 腹部缠枝
    d.ellipse([28, 34, 36, 42], fill=BQ)                            # 主花
    d.ellipse([30, 36, 34, 40], fill=BQ_DD)
    d.ellipse([24, 54, 40, 59], fill=GLZ_D)                         # 矮足

BUILDERS = {
    'vase_bq_meiping': draw_meiping,
    'vase_bq_guan': draw_guan_ear,
    'vase_bq_yuhuchun': draw_yuhuchun,
    'bowl_bq_longkou': draw_bowl_dragon,
    'plate_bq_fish': draw_plate_fish,
    'jar_bq_guang': draw_jar_guang,
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
    sheet.save(os.path.join(OUT, 'compare_r13.png'))
    print('r13 OK:', names)

if __name__ == '__main__':
    main()
