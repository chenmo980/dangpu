# -*- coding: utf-8 -*-
"""第16轮(自动化)：钟表第 2 批 8 件 sundial/hourglass/carriage/wrist_leather/metronome/barometer/cuckoo/sextant"""
import sys, os, math
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
GLASS = (200, 220, 216, 255)

def draw_sundial(d):
    """案头日晷：底盘+斜晷针+刻度线"""
    d.ellipse([8, 26, 56, 54], fill=SIL_D)                          # 底座
    d.ellipse([10, 24, 54, 48], fill=SIL)                           # 盘
    d.ellipse([13, 26, 51, 42], fill=SIL_L)                         # 盘面
    import math as m
    for i in range(12):                                              # 刻度
        ang = m.radians(i * 30)
        tx = 32 + 15 * m.sin(ang); ty = 34 - 8 * m.cos(ang)
        d.line([tx, ty, tx, ty + 2], fill=INK, width=1)
    d.line([32, 12, 46, 36], fill=GOLD, width=3)                     # 晔针（斜）
    d.line([32, 12, 45, 35], fill=GOLD_L, width=1)
    d.ellipse([29, 9, 35, 15], fill=GOLD)                            # 针座
    d.rectangle([14, 54, 50, 58], fill=ROD)                          # 木底

def draw_hourglass(d):
    """沙漏：双锥玻璃+木框+流沙"""
    d.rectangle([14, 2, 50, 8], fill=ROD)                            # 上框
    d.rectangle([14, 56, 50, 62], fill=ROD)                          # 下框
    for (x0, x1) in [(14, 20), (44, 50)]:
        d.line([x0, 8, x0, 56], fill=ROD_L, width=3)                 # 立柱
        d.line([x1, 8, x1, 56], fill=ROD_L, width=3)
    d.polygon([(20, 8), (44, 8), (33, 30), (31, 30)], fill=GLASS)    # 上锥
    d.polygon([(31, 34), (33, 34), (44, 56), (20, 56)], fill=GLASS)  # 下锥
    d.ellipse([24, 10, 40, 22], fill=(230, 210, 170, 255))           # 上沙
    d.polygon([(26, 20), (38, 20), (33, 30)], fill=(230, 210, 170, 255))
    d.ellipse([24, 42, 40, 55], fill=(230, 210, 170, 255))           # 下沙堆
    d.line([32, 30, 32, 42], fill=GOLD_L, width=1)                   # 流沙柱
    d.ellipse([20, 12, 28, 20], fill=(244, 234, 210, 255))           # 玻璃高光

def draw_carriage(d):
    """旅行钟：小方钟+提手+支脚"""
    d.arc([22, 2, 42, 18], 180, 360, fill=GOLD, width=3)             # 提手
    d.rounded_rectangle([14, 14, 50, 52], 3, fill=ROD)               # 壳
    d.rounded_rectangle([17, 17, 47, 49], 2, fill=ROD_L)
    d.rectangle([19, 19, 45, 47], fill=SIL_L)                        # 钟面
    import math as m
    for i in range(12):
        ang = m.radians(i * 30)
        tx = 32 + 8 * m.sin(ang); ty = 32 - 8 * m.cos(ang)
        d.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=INK)
    d.line([32, 32, 32, 24], fill=INK, width=2)
    d.line([32, 32, 38, 32], fill=INK, width=1)
    d.point([(32, 32)], fill=RED)
    d.rectangle([16, 52, 48, 58], fill=ROD_D)                        # 支脚座

def draw_wrist_leather(d):
    """皮表带腕表：竖表带+圆表头+小表盘"""
    d.rounded_rectangle([24, 2, 40, 22], 3, fill=(140, 101, 64, 255))  # 上带
    for yy in (6, 12, 18):
        d.line([26, yy, 38, yy], fill=(92, 58, 33, 255), width=1)    # 带纹
    d.rounded_rectangle([24, 42, 40, 62], 3, fill=(140, 101, 64, 255))  # 下带
    for yy in (46, 52, 58):
        d.line([26, yy, 38, yy], fill=(92, 58, 33, 255), width=1)
    d.ellipse([18, 18, 46, 46], fill=GOLD)                           # 表头
    d.ellipse([21, 21, 43, 43], fill=(240, 236, 226, 255))           # 表盘
    d.point([(32, 26)], fill=INK)
    d.point([(26, 32)], fill=INK)
    d.point([(38, 32)], fill=INK)
    d.point([(32, 38)], fill=INK)
    d.line([32, 32, 32, 25], fill=INK, width=2)                      # 时针
    d.line([32, 32, 39, 32], fill=INK, width=1)                      # 分针
    d.point([(32, 32)], fill=RED)
    d.ellipse([22, 22, 28, 28], fill=(230, 224, 200, 255))           # 玻璃光

def draw_metronome(d):
    """节拍器：梯形塔+摆杆+砝码"""
    d.polygon([(18, 60), (46, 60), (38, 8), (26, 8)], fill=ROD)      # 塔身
    d.polygon([(21, 56), (43, 56), (36, 12), (28, 12)], fill=ROD_L)
    d.line([30, 12, 38, 40], fill=SIL, width=2)                      # 摆杆（斜）
    d.ellipse([35, 36, 43, 44], fill=GOLD)                           # 摆砝码
    d.ellipse([37, 38, 41, 42], fill=GOLD_L)
    d.rectangle([22, 58, 42, 60], fill=ROD_D)                        # 底座
    d.ellipse([29, 10, 35, 14], fill=SIL)                            # 轴帽

def draw_barometer(d):
    """晴雨表：圆壳+白盘+指针+雨云字标"""
    d.ellipse([10, 6, 54, 50], fill=ROD_D)                           # 壳
    d.ellipse([13, 9, 51, 47], fill=ROD_L)
    d.ellipse([16, 12, 48, 44], fill=SIL_L)                          # 盘
    d.arc([19, 15, 45, 41], 180, 360, fill=TEAL, width=2)            # 上半弧（晴）
    d.line([19, 28, 45, 28], fill=INK_L, width=1)                    # 水平线
    d.polygon([(24, 34), (28, 30), (32, 34), (28, 38)], fill=INK)    # 云标
    d.line([32, 32, 42, 20], fill=RED, width=2)                      # 指针
    d.ellipse([30, 30, 34, 34], fill=GOLD)
    d.ellipse([17, 15, 23, 21], fill=(230, 232, 224, 255))           # 玻璃光

def draw_cuckoo(d):
    """布谷鸟钟：尖顶小屋+钟面+小鸟门"""
    d.polygon([(10, 22), (54, 22), (46, 6), (18, 6)], fill=ROD)      # 尖顶
    d.rectangle([12, 22, 52, 56], fill=ROD_L)                        # 屋身
    d.rectangle([19, 26, 45, 46], fill=SIL_L)                        # 钟面区
    d.ellipse([24, 28, 40, 44], fill=(240, 236, 226, 255))
    import math as m
    for i in range(8):
        ang = m.radians(i * 45)
        tx = 32 + 5 * m.sin(ang); ty = 36 - 5 * m.cos(ang)
        d.point([(tx, ty)], fill=INK)
    d.line([32, 36, 32, 31], fill=INK, width=1)
    d.line([32, 36, 36, 36], fill=INK, width=1)
    d.rectangle([14, 46, 22, 54], fill=(52, 34, 20, 255))            # 鸟门（左）
    d.ellipse([15, 48, 21, 54], fill=(140, 101, 64, 255))            # 小鸟
    d.point([(17, 50)], fill=INK)
    d.polygon([(21, 50), (24, 51), (21, 52)], fill=GOLD)             # 鸟喙
    for (lx, ly) in [(24, 56), (40, 56)]:                             # 松果坠
        d.line([lx, 50, lx, 56], fill=GOLD, width=1)
        d.ellipse([lx - 2, 55, lx + 2, 61], fill=(110, 88, 56, 255))

def draw_sextant(d):
    """六分仪：扇形弧架+望远镜+镜组"""
    d.arc([8, 10, 56, 58], 240, 60, fill=GOLD, width=4)              # 弧架（刻度弧）
    import math as m
    for i in range(6):                                                # 弧刻度
        ang = m.radians(240 + i * 60)
        tx = 32 + 24 * m.cos(ang); ty = 34 + 24 * m.sin(ang)
        d.point([(tx, ty)], fill=INK)
    d.line([32, 12, 32, 46], fill=ROD, width=4)                      # 竖架
    d.line([30, 12, 30, 46], fill=ROD_L, width=2)
    d.rounded_rectangle([34, 18, 54, 26], 3, fill=ROD_D)             # 望远镜
    d.ellipse([52, 19, 56, 25], fill=INK)                            # 目镜
    d.rectangle([28, 26, 36, 30], fill=SIL)                          # 镜组盒
    d.rectangle([30, 27, 34, 29], fill=(200, 220, 216, 255))
    d.ellipse([28, 8, 36, 14], fill=GOLD)                            # 顶调节轮
    d.ellipse([30, 9, 34, 13], fill=GOLD_L)

BUILDERS = {
    'sundial_desk': draw_sundial,
    'hourglass': draw_hourglass,
    'clock_carriage': draw_carriage,
    'watch_wrist_leather': draw_wrist_leather,
    'metronome': draw_metronome,
    'barometer': draw_barometer,
    'clock_cuckoo': draw_cuckoo,
    'sextant': draw_sextant,
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
    sheet.save(os.path.join(OUT, 'compare_r17.png'))
    print('r17 OK:', names)

if __name__ == '__main__':
    main()
