# -*- coding: utf-8 -*-
"""第7轮(自动化)：皮具 bracer/saddle/pack/waterskin/pads v2 化
leather v2 配方：64 超采样、胡桃皮 ramp、缝线虚线、铜扣点缀、左上受光、底 1/3 压暗
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

L1 = (166, 128, 88, 255)   # wood_hl
L2 = (140, 101, 64, 255)   # wood_l
L3 = (92, 58, 33, 255)     # wood
L4 = (74, 48, 28, 255)     # wood_d
THREAD = (196, 180, 150, 255)  # 缝线色

def stitches(d, x0, y0, x1, y1, n=4, vert=False):
    """缝线虚线"""
    if vert:
        for i in range(n):
            yy = y0 + (y1 - y0) * i // n + 2
            d.line([x0, yy, x0 + 3, yy], fill=THREAD, width=1)
    else:
        for i in range(n):
            xx = x0 + (x1 - x0) * i // n + 2
            d.line([xx, y0, xx, y0 + 3], fill=THREAD, width=1)

def draw_bracer(d):
    """皮护腕：梯形筒+双绑带+铜扣"""
    d.polygon([(20, 6), (44, 6), (50, 58), (14, 58)], fill=L3)
    d.polygon([(22, 8), (42, 8), (47, 55), (17, 55)], fill=L2)
    d.polygon([(24, 9), (40, 9), (42, 20), (24, 20)], fill=L1)     # 顶部受光
    d.polygon([(17, 46), (47, 46), (50, 55), (14, 55)], fill=L4)    # 底部压暗
    d.rectangle([24, 22, 30, 52], fill=L4)                          # 绑带 1
    d.rectangle([34, 22, 40, 52], fill=L4)                          # 绑带 2
    d.rectangle([25, 23, 29, 51], fill=(60, 40, 22, 255))
    d.rectangle([35, 23, 39, 51], fill=(60, 40, 22, 255))
    d.rectangle([27, 26, 33, 31], fill=PAL['gold'])                 # 铜扣
    d.rectangle([27, 26, 33, 27], fill=PAL['gold_l'])
    d.rectangle([36, 26, 42, 31], fill=PAL['gold'])
    stitches(d, 22, 10, 42, 10, 4)                                  # 顶缝线
    stitches(d, 18, 56, 46, 56, 5)                                  # 底缝线

def draw_saddle(d):
    """皮马鞍：鞍桥+鞍座+肚带+蹬带"""
    d.ellipse([8, 26, 56, 44], fill=L3)                             # 鞍座底
    d.ellipse([11, 28, 53, 42], fill=L2)
    d.polygon([(16, 12), (48, 12), (52, 28), (12, 28)], fill=L2)    # 鞍桥
    d.polygon([(19, 14), (45, 14), (48, 26), (16, 26)], fill=L1)    # 鞍桥面
    d.ellipse([20, 8, 44, 18], fill=L2)                             # 前鞍头
    d.ellipse([22, 9, 42, 16], fill=L1)
    d.ellipse([16, 22, 30, 30], fill=L4)                            # 后鞍头窝
    d.ellipse([18, 23, 28, 29], fill=L3)
    d.line([10, 44, 54, 44], fill=L4, width=4)                      # 鞍沿
    d.line([32, 42, 32, 62], fill=L4, width=5)                      # 肚带
    d.line([33, 42, 33, 62], fill=L2, width=2)
    d.rectangle([28, 34, 36, 40], fill=PAL['gold'])                 # 鞍扣
    stitches(d, 12, 27, 52, 27, 6)
    for (sx, sy) in [(10, 42), (52, 42)]:                            # 蹬带
        d.line([sx, sy, sx, 56], fill=L4, width=3)
        d.ellipse([sx - 3, 54, sx + 4, 62], fill=PAL['lo'])         # 铁镫

def draw_pack(d):
    """皮行囊：方囊+盖+双背带+铜扣+缝线"""
    d.rounded_rectangle([10, 18, 54, 58], 5, fill=L3)
    d.rounded_rectangle([13, 21, 51, 55], 4, fill=L2)
    d.rounded_rectangle([15, 23, 49, 34], 3, fill=L1)               # 囊盖受光
    d.rectangle([10, 32, 54, 36], fill=L4)                          # 盖沿
    d.rectangle([10, 32, 54, 34], fill=L3)
    d.arc([18, 6, 30, 22], 180, 360, fill=L4, width=4)              # 背带左
    d.arc([34, 6, 46, 22], 180, 360, fill=L4, width=4)
    d.arc([19, 7, 29, 21], 180, 360, fill=L2, width=2)
    d.arc([35, 7, 45, 21], 180, 360, fill=L2, width=2)
    d.rectangle([28, 36, 36, 42], fill=PAL['gold'])                 # 铜扣
    d.rectangle([28, 36, 36, 38], fill=PAL['gold_l'])
    stitches(d, 13, 55, 51, 55, 6)
    stitches(d, 13, 40, 51, 40, 6, vert=False)

def draw_waterskin(d):
    """皮水袋：葫芦形+木塞+绑颈+缝线"""
    d.ellipse([16, 24, 48, 58], fill=L3)                            # 下腹
    d.ellipse([18, 26, 46, 56], fill=L2)
    d.ellipse([22, 28, 36, 42], fill=L1)                            # 左上受光
    d.ellipse([30, 44, 46, 57], fill=L4)                            # 右下压暗
    d.polygon([(24, 12), (40, 12), (44, 26), (20, 26)], fill=L2)    # 颈肩
    d.rectangle([25, 4, 39, 14], fill=(101, 82, 60, 255))           # 木塞
    d.ellipse([26, 4, 38, 10], fill=(140, 101, 64, 255))
    d.line([24, 12, 40, 12], fill=L4, width=2)
    d.line([22, 26, 42, 26], fill=L4, width=3)                      # 颈绑
    d.rectangle([23, 24, 41, 27], fill=(117, 78, 48, 255))
    stitches(d, 20, 34, 44, 34, 4)
    d.ellipse([29, 46, 35, 52], fill=PAL['gold_d'])                 # 小铜饰

def draw_pads(d):
    """皮护膝一对：椭圆垫+系带+绗缝格"""
    for kx in (6, 34):
        d.ellipse([kx, 12, kx + 24, 42], fill=L3)
        d.ellipse([kx + 2, 14, kx + 22, 40], fill=L2)
        d.ellipse([kx + 5, 16, kx + 19, 36], fill=L1)               # 受光面
        d.ellipse([kx + 5, 30, kx + 22, 42], fill=L4)               # 底部压暗
        d.line([kx + 6, 22, kx + 18, 22], fill=THREAD, width=1)     # 绗缝
        d.line([kx + 6, 28, kx + 18, 28], fill=THREAD, width=1)
        d.line([kx + 12, 16, kx + 12, 34], fill=THREAD, width=1)
        d.line([kx + 10, 40, kx + 8, 56], fill=L4, width=3)         # 系带
        d.line([kx + 14, 40, kx + 16, 56], fill=L4, width=3)
        d.line([kx + 8, 55, kx + 16, 55], fill=L4, width=2)
        d.point([(kx + 12, 18)], fill=PAL['gold_d'])
    d.line([30, 24, 34, 24], fill=L4, width=2)                      # 一对间距补

BUILDERS = {
    'bracer_leather': draw_bracer,
    'saddle_leather': draw_saddle,
    'pack_leather': draw_pack,
    'waterskin': draw_waterskin,
    'pads_leather': draw_pads,
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
    sheet.save(os.path.join(OUT, 'compare_r8.png'))
    print('r8 OK:', names)

if __name__ == '__main__':
    main()
