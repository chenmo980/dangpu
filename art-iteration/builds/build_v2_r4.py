# -*- coding: utf-8 -*-
"""第3轮(自动化)：银器 mirror/pipe/knife/buddha v2 化"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, TRUE, SS
from PIL import Image, ImageDraw, ImageFont

def draw_mirror(d):
    """银镜：圆镜面+对角高光+短柄金箍"""
    cx, cy = 30, 26
    d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=PAL['lo'])   # 外环
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=PAL['hi'])   # 镜面
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=PAL['mid'])  # 镜心（微暗=昏）
    d.arc([cx - 13, cy - 13, cx + 13, cy + 13], 200, 320, fill=(230, 232, 224, 255), width=2)  # 对角高光弧
    d.arc([cx - 17, cy - 17, cx + 17, cy + 17], 20, 120, fill=PAL['dk'], width=2)  # 右下环影
    d.rectangle([27, 42, 35, 56], fill=PAL['mid'])                    # 柄
    d.line([28, 43, 28, 55], fill=PAL['dk'], width=2)
    d.line([33, 43, 33, 55], fill=PAL['hi'], width=2)
    d.rectangle([25, 41, 37, 45], fill=PAL['gold'])                   # 柄肩金箍
    d.rectangle([25, 41, 37, 42], fill=PAL['gold_l'])
    d.ellipse([25, 54, 37, 61], fill=PAL['lo'])                       # 柄尾

def draw_pipe(d):
    """银烟袋 v2.1：杆细长、烟锅小巧、金箍成环"""
    d.line([14, 58, 44, 14], fill=PAL['dk'], width=4)                 # 杆（紫檀，细）
    d.line([15, 57, 45, 13], fill=(92, 58, 33, 255), width=3)
    d.line([15, 56, 45, 12], fill=(122, 82, 51, 255), width=1)        # 受光棱
    d.ellipse([7, 55, 17, 63], fill=PAL['lo'])                        # 烟嘴
    d.ellipse([9, 56, 14, 61], fill=PAL['hi'])
    d.rectangle([44, 6, 56, 15], fill=PAL['mid'])                     # 烟锅体（小）
    d.ellipse([44, 4, 56, 11], fill=PAL['hi'])                        # 锅口
    d.ellipse([47, 5, 53, 9], fill=PAL['dk2'])                        # 锅腔
    d.rectangle([15, 49, 25, 52], fill=PAL['gold'])                   # 嘴箍（细环 3px）
    d.rectangle([15, 49, 25, 50], fill=PAL['gold_l'])
    d.rectangle([37, 15, 47, 18], fill=PAL['gold'])                   # 锅箍（细环）
    d.rectangle([37, 15, 47, 16], fill=PAL['gold_l'])

def draw_knife(d):
    """银匕首：竖直、双刃收尖、血槽、金护手、缠绳柄"""
    d.polygon([(32, 2), (24, 14), (27, 34), (37, 34), (40, 14)], fill=PAL['hi'])   # 刃
    d.polygon([(32, 4), (26, 14), (29, 32), (32, 32)], fill=PAL['mid'])            # 刃右半（暗）
    d.line([32, 6, 32, 32], fill=PAL['lo'], width=1)                  # 血槽中线
    d.line([28, 12, 29, 30], fill=PAL['hl'], width=1)                 # 左刃高光
    d.rectangle([22, 33, 42, 38], fill=PAL['gold'])                   # 护手
    d.rectangle([22, 33, 42, 34], fill=PAL['gold_l'])
    d.rectangle([27, 38, 37, 54], fill=PAL['dk'])                     # 柄
    for yy in (41, 45, 49):                                            # 缠绳
        d.line([27, yy, 37, yy], fill=(92, 58, 33, 255), width=2)
    d.ellipse([27, 53, 37, 62], fill=PAL['gold_d'])                   # 柄尾球
    d.ellipse([29, 55, 34, 59], fill=PAL['gold_l'])

def draw_buddha(d):
    """小银佛 v2.1：背光细弧开口大、莲瓣减疏"""
    d.arc([8, 2, 56, 50], 150, 390, fill=PAL['lo2'], width=3)         # 背光弧（细、开口）
    d.arc([10, 4, 54, 48], 160, 380, fill=PAL['mid'], width=1)
    d.ellipse([25, 12, 39, 26], fill=PAL['hi'])                       # 头
    d.ellipse([28, 8, 36, 16], fill=PAL['mid'])                       # 肉髻
    d.point([(32, 10)], fill=PAL['gold'])
    d.polygon([(18, 50), (46, 50), (40, 26), (24, 26)], fill=PAL['mid'])  # 袈裟身
    d.polygon([(22, 50), (42, 50), (38, 28), (26, 28)], fill=PAL['hi'])
    d.line([32, 28, 32, 48], fill=PAL['lo'], width=2)                 # 衣褶
    d.line([25, 34, 26, 48], fill=PAL['lo'], width=1)
    d.ellipse([12, 48, 52, 60], fill=PAL['lo'])                       # 莲座上层
    d.ellipse([15, 50, 49, 58], fill=PAL['mid'])
    d.ellipse([16, 55, 48, 62], fill=PAL['dk'])                       # 莲座下层
    d.ellipse([18, 56, 46, 61], fill=PAL['lo2'])
    for gx in (24, 32, 40):                                            # 莲瓣痕（减疏）
        d.line([gx, 57, gx - 1, 61], fill=PAL['dk2'], width=1)
    d.point([(26, 30)], fill=PAL['gold_d'])                           # 胸前金饰
    d.point([(38, 30)], fill=PAL['gold_d'])

BUILDERS = {
    'mirror_silver': draw_mirror,
    'pipe_silver': draw_pipe,
    'knife_silver': draw_knife,
    'buddha_silver': draw_buddha,
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
    sheet.save(os.path.join(OUT, 'compare_r4.png'))
    print('r4 OK:', names)

if __name__ == '__main__':
    main()
