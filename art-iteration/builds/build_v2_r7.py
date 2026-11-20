# -*- coding: utf-8 -*-
"""第6轮(自动化)：皮货服饰类 v2 化 fox_collar/fur_coat/fur_gloves/fur_hat/sable_stole/otter_pelt
garment v2 配方：64 超采样、布底+皮毛领/边（弧形毛簇）、左上受光、底 1/3 压暗
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

# 皮毛色族（ramp: 亮/中/暗）
FOX  = [(206, 128, 74, 255), (176, 98, 58, 255), (140, 70, 40, 255)]
SABLE= [(166, 128, 88, 255), (140, 101, 64, 255), (74, 48, 28, 255)]
OTTER= [(110, 82, 60, 255), (86, 62, 44, 255), (60, 42, 30, 255)]
CLOTH= [(213, 210, 184, 255), (196, 196, 176, 255), (136, 148, 138, 255)]  # 绸面衬

def fur_edge(d, pts, fur, width=6):
    """沿轮廓画毛簇（短弧组）"""
    m = fur[1]
    for i in range(1, len(pts)):
        d.line([pts[i-1][0], pts[i-1][1], pts[i][0], pts[i][1]], fill=m, width=width)
        d.line([pts[i-1][0]+1, pts[i-1][1]+1, pts[i][0]+1, pts[i][1]+1], fill=fur[0], width=width-2)

def draw_collar(d):
    """狐皮领子：V 形毛领，双层毛簇，衬里可见"""
    d.polygon([(8, 24), (32, 12), (56, 24), (52, 40), (32, 28), (12, 40)], fill=FOX[2])
    d.polygon([(11, 25), (32, 15), (53, 25), (50, 38), (32, 27), (14, 38)], fill=FOX[1])
    d.polygon([(15, 26), (32, 18), (49, 26), (46, 35), (32, 26), (18, 35)], fill=FOX[0])
    fur_edge(d, [(8, 24), (14, 18), (23, 14), (32, 12), (41, 14), (50, 18), (56, 24)], FOX, 5)
    d.line([32, 18, 32, 27], fill=CLOTH[2], width=2)   # 中缝

def draw_coat(d):
    """皮袄：对襟、皮毛领口与下摆、盘扣"""
    d.polygon([(16, 10), (48, 10), (56, 56), (8, 56)], fill=SABLE[1])   # 身
    d.polygon([(18, 13), (46, 13), (53, 52), (11, 52)], fill=SABLE[0])
    d.polygon([(16, 10), (48, 10), (50, 18), (14, 18)], fill=FOX[1])    # 领口毛
    d.polygon([(8, 48), (56, 48), (56, 56), (8, 56)], fill=FOX[2])      # 下摆毛
    d.line([32, 12, 32, 52], fill=PAL['dk2'], width=2)                  # 对襟缝
    for gy in (22, 30, 38, 46):                                          # 盘扣
        d.ellipse([28, gy, 36, gy + 4], fill=PAL['gold'])
        d.ellipse([30, gy + 1, 34, gy + 3], fill=PAL['gold_l'])
    d.arc([18, 14, 46, 30], 20, 160, fill=(230, 200, 150, 255), width=2)  # 受光

def draw_gloves(d):
    """皮手套一对：掌面+拇指+腕口毛边"""
    for gx in (4, 34):
        d.rounded_rectangle([gx, 12, gx + 22, 44], 8, fill=SABLE[1])     # 手背
        d.rounded_rectangle([gx + 2, 14, gx + 20, 42], 7, fill=SABLE[0])
        d.ellipse([gx + 3, 16, gx + 12, 24], fill=(230, 200, 150, 255))  # 受光
        d.rounded_rectangle([gx + 4, 44, gx + 18, 56], 4, fill=SABLE[2]) # 腕筒
        d.line([gx + 4, 56, gx + 18, 56], fill=FOX[0], width=4)          # 腕口毛边
        d.line([gx + 5, 55, gx + 17, 55], fill=FOX[1], width=2)
        d.line([gx + 11, 20, gx + 11, 38], fill=PAL['dk2'], width=1)     # 掌缝
        d.line([gx + 16, 14, gx + 22, 24], fill=SABLE[2], width=5)       # 拇指
    d.rectangle([26, 20, 32, 26], fill=PAL['gold'])                       # 中间小扣

def draw_hat(d):
    """皮帽：瓜皮圆顶+翻毛边+顶红缨"""
    d.ellipse([10, 14, 54, 48], fill=SABLE[1])                  # 帽顶
    d.ellipse([13, 17, 51, 45], fill=SABLE[0])
    d.ellipse([16, 18, 40, 34], fill=(230, 200, 150, 255))      # 受光
    d.arc([14, 16, 50, 36], 200, 340, fill=(230, 200, 150, 255), width=2)
    d.rounded_rectangle([6, 38, 58, 52], 7, fill=FOX[1])        # 翻毛边
    d.rounded_rectangle([8, 40, 56, 50], 6, fill=FOX[0])
    for gx in (12, 22, 32, 42, 52):                              # 毛簇弧
        d.arc([gx, 39, gx + 8, 49], 40, 320, fill=FOX[2], width=2)
    d.rectangle([28, 2, 36, 16], fill=PAL['red'])               # 顶红缨
    d.ellipse([26, 0, 38, 8], fill=PAL['red'])
    d.ellipse([29, 2, 35, 6], fill=PAL['red_l'])

def draw_stole(d):
    """貂皮围脖：宽带状+两端垂穗+毛簇"""
    d.polygon([(4, 18), (60, 16), (60, 32), (4, 34)], fill=SABLE[1])
    d.polygon([(6, 20), (58, 18), (58, 30), (6, 32)], fill=SABLE[0])
    d.ellipse([0, 12, 16, 36], fill=SABLE[2])                   # 左垂坠
    d.ellipse([2, 14, 13, 34], fill=SABLE[1])
    d.ellipse([48, 10, 64, 34], fill=SABLE[2])                  # 右垂坠
    d.ellipse([50, 12, 61, 32], fill=SABLE[1])
    for gx in (12, 22, 32, 42, 52):                              # 毛簇
        d.arc([gx, 16, gx + 9, 30], 30, 330, fill=SABLE[2], width=2)
        d.arc([gx, 15, gx + 9, 29], 60, 300, fill=(230, 200, 150, 255), width=1)
    d.rectangle([28, 20, 36, 28], fill=PAL['gold'])             # 金搭扣
    d.rectangle([28, 20, 36, 22], fill=PAL['gold_l'])

def draw_otter(d):
    """水獭皮：深棕细长皮+圆润头+短耳"""
    l, m, dk = OTTER
    d.ellipse([12, 16, 52, 44], fill=dk)
    d.ellipse([15, 18, 49, 42], fill=m)
    d.ellipse([17, 20, 47, 40], fill=l)
    d.ellipse([24, 8, 40, 20], fill=dk)                         # 头（圆）
    d.ellipse([26, 9, 38, 18], fill=m)
    d.ellipse([19, 5, 25, 12], fill=dk)                         # 小圆耳
    d.ellipse([39, 5, 45, 12], fill=dk)
    d.ellipse([28, 12, 36, 16], fill=l)                         # 鼻梁
    d.line([14, 42, 8, 56], fill=dk, width=5)                   # 短腿
    d.line([46, 42, 54, 56], fill=dk, width=5)
    d.line([15, 42, 9, 55], fill=m, width=2)
    d.line([45, 42, 53, 55], fill=m, width=2)
    d.ellipse([0, 18, 10, 32], fill=dk)                         # 尾
    d.ellipse([2, 20, 8, 30], fill=m)
    d.arc([16, 18, 48, 40], 180, 360, fill=(150, 116, 88, 255), width=2)  # 背脊油光

BUILDERS = {
    'fox_collar': draw_collar,
    'fur_coat': draw_coat,
    'fur_gloves': draw_gloves,
    'fur_hat': draw_hat,
    'sable_stole': draw_stole,
    'otter_pelt': draw_otter,
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
    sheet.save(os.path.join(OUT, 'compare_r7.png'))
    print('r7 OK:', names)

if __name__ == '__main__':
    main()
