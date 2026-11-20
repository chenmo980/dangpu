# -*- coding: utf-8 -*-
"""第2轮(自动化)：censer 弦纹微调 + hairpin/earring/ring/bell v2 化
复用 build_v2_exemplars 的 process() 管线
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, TRUE, SS
from PIL import Image, ImageDraw, ImageFont

def draw_censer_fixed(d):
    """小银炉 v2.1：弦纹紧贴口沿(≤3px)、耳根埋进炉身、身沿同宽"""
    d.arc([8, 12, 26, 34], 200, 90, fill=PAL['lo2'], width=6)    # 左耳（弧根埋入炉口两侧）
    d.arc([38, 12, 56, 34], 90, 340, fill=PAL['lo2'], width=6)   # 右耳
    d.arc([9, 13, 25, 33], 200, 80, fill=PAL['mid'], width=3)
    d.arc([39, 13, 55, 33], 100, 340, fill=PAL['mid'], width=3)
    d.ellipse([12, 26, 52, 58], fill=PAL['mid'])            # 炉身（与口沿同宽整体）
    d.ellipse([14, 27, 50, 37], fill=PAL['dk2'])            # 炉口
    d.ellipse([16, 28, 48, 36], fill=PAL['dk'])
    d.ellipse([12, 27, 52, 32], fill=PAL['hi'])  # 沿口正面亮带
    d.ellipse([14, 28, 50, 32], fill=PAL['mid'])
    d.ellipse([12, 46, 52, 58], fill=PAL['lo2'])            # 底 1/3 压暗
    d.ellipse([17, 30, 28, 36], fill=PAL['hi'])             # 左上高光
    d.rectangle([12, 33, 52, 35], fill=PAL['gold'])         # 弦纹：贴口沿下缘 2px
    d.rectangle([12, 33, 52, 33], fill=PAL['gold_l'])
    for lx in (18, 30, 42):                                  # 三足
        d.ellipse([lx - 3, 55, lx + 3, 63], fill=PAL['lo'])
        d.ellipse([lx - 2, 56, lx + 2, 61], fill=PAL['lo2'])

def draw_hairpin(d):
    """银簪：斜杆渐细 + 如意云头 + 金芯"""
    d.line([14, 58, 40, 22], fill=PAL['dk'], width=6)       # 杆
    d.line([15, 57, 41, 21], fill=PAL['mid'], width=4)
    d.line([16, 56, 42, 20], fill=PAL['hi'], width=2)
    d.line([13, 59, 15, 56], fill=PAL['lo'], width=3)       # 尾端圆钝
    d.ellipse([36, 8, 52, 24], fill=PAL['mid'])             # 如意头主圆
    d.ellipse([38, 10, 50, 22], fill=PAL['hi'])
    d.ellipse([30, 12, 40, 24], fill=PAL['mid'])            # 左卷
    d.ellipse([32, 14, 38, 22], fill=PAL['hi'])
    d.ellipse([48, 8, 58, 20], fill=PAL['mid'])             # 右卷
    d.ellipse([50, 10, 56, 18], fill=PAL['hi'])
    d.ellipse([42, 13, 46, 17], fill=PAL['gold'])           # 头心金芯
    d.point([(43, 14)], fill=PAL['gold_l'])

def draw_earring(d):
    """银耳坠一对：钩环+细链+水滴坠，间距 22px"""
    for cx in (20, 42):
        d.ellipse([cx - 5, 2, cx + 5, 12], outline=PAL['mid'], width=3)   # 钩环
        d.line([cx, 12, cx, 20], fill=PAL['lo'], width=2)                  # 链
        d.ellipse([cx - 9, 20, cx + 9, 44], fill=PAL['lo'])                # 坠体
        d.ellipse([cx - 7, 22, cx + 7, 42], fill=PAL['mid'])
        d.ellipse([cx - 5, 24, cx + 5, 40], fill=PAL['hi'])
        d.ellipse([cx - 9, 36, cx + 9, 44], fill=PAL['lo2'])               # 底部压暗
        d.ellipse([cx - 4, 26, cx - 1, 31], fill=(230, 232, 224, 255))     # 高光点
        d.rectangle([cx - 2, 18, cx + 2, 21], fill=PAL['gold_d'])          # 链坠接口金扣

def draw_ring(d):
    """银戒指：正放圆环 + 顶部金托红宝石戒面"""
    cx, cy = 32, 38
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=PAL['lo'])
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=PAL['mid'])
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(0, 0, 0, 0))
    d.arc([cx - 13, cy - 13, cx + 13, cy + 13], 190, 320, fill=PAL['hl'], width=2)  # 左上环面高光
    d.arc([cx - 9, cy - 9, cx + 9, cy + 9], 30, 130, fill=PAL['dk'], width=2)       # 右下内影
    d.polygon([(26, 24), (38, 24), (40, 16), (24, 16)], fill=PAL['mid'])    # 托座过渡
    d.ellipse([22, 4, 42, 20], fill=PAL['gold'])            # 金托
    d.ellipse([24, 6, 40, 18], fill=PAL['gold_l'])
    d.ellipse([27, 8, 37, 17], fill=PAL['red'])             # 红宝石
    d.ellipse([29, 9, 34, 13], fill=PAL['red_l'])           # 宝石高光

def draw_bell(d):
    """银铃铛 v2.1：顶环与钟体相连（悬空点修复）"""
    d.ellipse([26, 2, 38, 16], outline=PAL['lo2'], width=5)  # 顶环（粗、下缘入钟体）
    d.ellipse([21, 12, 43, 32], fill=PAL['mid'])             # 上段钟体（顶接环）
    d.ellipse([23, 14, 41, 30], fill=PAL['hi'])
    d.ellipse([24, 15, 40, 29], fill=PAL['mid'])
    d.ellipse([15, 24, 49, 48], fill=PAL['mid'])             # 下段（外扩）
    d.ellipse([17, 26, 47, 46], fill=PAL['hi'])
    d.ellipse([18, 27, 46, 45], fill=PAL['mid'])
    d.ellipse([17, 30, 30, 42], fill=PAL['hi'])              # 左上肩光
    d.ellipse([15, 42, 49, 52], fill=PAL['lo'])              # 底沿外翻
    d.ellipse([15, 46, 49, 52], fill=PAL['lo2'])
    d.rectangle([14, 48, 50, 51], fill=PAL['gold'])          # 底沿金线
    d.rectangle([14, 48, 50, 49], fill=PAL['gold_l'])
    d.line([31, 16, 31, 40], fill=PAL['hi'], width=2)        # 中缝高光
    d.point([(32, 8)], fill=PAL['gold'])

BUILDERS = {
    'hairpin_silver': draw_hairpin,
    'earring_silver': draw_earring,
    'ring_silver': draw_ring,
    'bell_silver': draw_bell,
}

def main():
    results = {}
    for name, fn in BUILDERS.items():
        big = Image.new('RGBA', (SS, SS), (0, 0, 0, 0))
        fn(ImageDraw.Draw(big))
        results[name] = process(big)
        results[name].save(os.path.join(OUT, f'{name}.png'))
    # censer v2.1 重建（微调）
    big = Image.new('RGBA', (SS, SS), (0, 0, 0, 0))
    draw_censer_fixed(ImageDraw.Draw(big))
    censer = process(big)
    censer.save(os.path.join(OUT, 'censer_silver.png'))
    results['censer_silver v2.1'] = censer
    # 三联对比
    font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 14)
    atlas = Image.open(r'C:\测试工作区\probably-stolen-study\analysis\items_medical_atlas.png').convert('RGBA')
    ref = atlas.crop((400, 300, 470, 380)).resize((210, 240), Image.NEAREST)
    ROW = 136
    names = list(results.keys())
    sheet = Image.new('RGBA', (620, len(names) * ROW + 260), (35, 37, 43, 255))
    d2 = ImageDraw.Draw(sheet)
    sheet.paste(ref, (6, 8))
    d2.text((6, 252), '原作参考(风格)', fill=(200, 195, 175, 255), font=font)
    for i, name in enumerate(names):
        y = 8 + i * ROW
        d2.text((240, y + 2), 'v2 ' + name, fill=(160, 210, 170, 255), font=font)
        big = results[name].resize((64, 64), Image.NEAREST)
        sheet.paste(big, (236, y + 22), big)
        base = name.split()[0]
        old_path = os.path.join(r'C:\测试工作区\probably-stolen-study\pixel-art\pawnshop-icons', f'{base}.png')
        if os.path.exists(old_path):
            old = Image.open(old_path).convert('RGBA').resize((64, 64), Image.NEAREST)
            d2.text((320, y + 2), 'v1 旧版', fill=(210, 160, 150, 255), font=font)
            sheet.paste(old, (316, y + 22), old)
        d2.text((404, y + 2), 'v2 @4x', fill=(150, 170, 210, 255), font=font)
        disp = results[name].resize((128, 128), Image.NEAREST)
        sheet.paste(disp, (400, y + 4), disp)
    sheet.save(os.path.join(OUT, 'compare_r3.png'))
    print('r3 OK:', names)

if __name__ == '__main__':
    main()
