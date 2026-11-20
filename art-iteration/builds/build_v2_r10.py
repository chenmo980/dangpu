# -*- coding: utf-8 -*-
"""第9轮(自动化)：字画第 2 批 couplet/rubbing/calligraphy/portrait/bamboo/fish"""
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
RED    = (156, 55, 56, 255)

def ink_rows(d, x0, x1, y0, rows, height=4, gap=3):
    """画心上的墨字痕（竖排列短横）"""
    for r in range(rows):
        yy = y0 + r * (height + gap)
        d.rectangle([x0, yy, x1, yy + height], fill=INK if r % 2 == 0 else INK_L)

def draw_couplet(d):
    """楹联一对：两条竖轴并排（间距>6px），每条上杆+字条+下杆"""
    for cx in (10, 38):
        d.rounded_rectangle([cx, 2, cx + 16, 8], 2, fill=ROD)
        d.rectangle([cx + 2, 8, cx + 14, 54], fill=PAPER)
        d.rectangle([cx + 2, 8, cx + 14, 11], fill=PAPER_L)
        ink_rows(d, cx + 4, cx + 12, 14, 6, height=3, gap=3)
        d.rectangle([cx + 10, 48, cx + 13, 52], fill=RED)          # 联脚印
        d.rectangle([cx + 2, 54, cx + 14, 58], fill=PAPER_D)
        d.rounded_rectangle([cx, 58, cx + 16, 64], 2, fill=ROD)

def draw_rubbing(d):
    """拓片：黑底白字方块+卷角+题跋条"""
    d.rectangle([8, 8, 52, 44], fill=INK)                           # 拓片黑底
    d.rectangle([8, 8, 52, 10], fill=INK_L)
    for gy in (14, 22, 30):                                          # 白字痕（拓文）
        for gx in (12, 20, 28, 36):
            d.rectangle([gx, gy, gx + 5, gy + 5], fill=PAPER)
            d.rectangle([gx + 1, gy + 1, gx + 4, gy + 4], fill=INK_L)
    d.rectangle([10, 36, 46, 40], fill=PAPER_D)                      # 题跋条
    ink_rows(d, 12, 40, 37, 1, height=2)
    d.rectangle([44, 30, 48, 34], fill=RED)                          # 藏印
    d.polygon([(52, 44), (52, 58), (38, 58)], fill=PAPER_D)          # 卷角
    d.polygon([(52, 44), (52, 56), (40, 56)], fill=PAPER)
    d.line([8, 8, 52, 8], fill=INK_L, width=1)

def draw_calligraphy(d):
    """书法条幅：竖长纸+大字痕（每字带顿笔块）+引首印"""
    d.rounded_rectangle([16, 2, 44, 8], 2, fill=ROD)
    d.rectangle([14, 8, 50, 56], fill=PAPER)
    d.rectangle([14, 8, 50, 11], fill=PAPER_L)
    for gy in (14, 24, 34, 44):                                      # 大字痕
        d.rectangle([22, gy, 42, gy + 7], fill=INK)
        d.rectangle([24, gy + 1, 40, gy + 6], fill=INK_L)
        d.rectangle([26, gy + 2, 32, gy + 5], fill=INK)              # 顿笔重块
    d.rectangle([16, 12, 20, 17], fill=RED)                          # 引首印
    d.rectangle([42, 48, 47, 53], fill=RED)                          # 落款印
    d.rectangle([14, 56, 50, 60], fill=PAPER_D)
    d.rounded_rectangle([16, 60, 44, 64], 2, fill=ROD)

def draw_portrait(d):
    """祖先画像轴：坐姿官服人像（正面）+官帽+供桌"""
    d.rounded_rectangle([16, 2, 44, 8], 2, fill=ROD)
    d.rectangle([14, 8, 50, 58], fill=PAPER)
    d.rectangle([14, 8, 50, 11], fill=PAPER_L)
    d.ellipse([24, 14, 40, 28], fill=(139, 94, 62, 255))             # 脸
    d.rounded_rectangle([23, 10, 41, 17], 3, fill=(52, 40, 33, 255)) # 官帽
    d.rectangle([26, 8, 38, 11], fill=(92, 58, 33, 255))             # 帽檐
    d.point([(29, 20)], fill=INK); d.point([(35, 20)], fill=INK)     # 眼
    d.polygon([(20, 52), (44, 52), (40, 30), (24, 30)], fill=(63, 92, 133, 255))  # 官服
    d.ellipse([29, 30, 35, 36], fill=(230, 224, 200, 255))           # 领
    d.rectangle([28, 38, 36, 42], fill=PAL['gold'])                  # 补子
    d.rectangle([14, 52, 50, 56], fill=(110, 88, 56, 255))           # 供桌沿
    d.rectangle([16, 56, 48, 58], fill=(92, 58, 33, 255))
    d.rectangle([44, 52, 48, 56], fill=RED)                          # 印

def draw_bamboo(d):
    """墨竹小品：横构图竹竿三竿+叶簇"""
    d.rectangle([8, 8, 56, 48], fill=PAPER)
    d.rectangle([8, 8, 56, 11], fill=PAPER_L)
    d.line([14, 44, 22, 12], fill=INK, width=2)                      # 竿1
    for gy in (16, 26, 34):
        d.line([17 + (gy - 16) // 4, gy, 20, gy - 2], fill=INK, width=1)  # 竹节
    d.line([26, 46, 34, 10], fill=INK_L, width=2)                    # 竿2
    d.line([40, 44, 50, 14], fill=INK, width=2)                      # 竿3
    # 叶簇（每簇 3 叶：尖长条）
    for (lx, ly, dx) in [(18, 14, 1), (24, 18, -1), (30, 12, 1), (44, 16, -1), (36, 24, 1), (46, 26, -1), (22, 30, -1), (34, 32, 1)]:
        d.polygon([(lx, ly), (lx + 6 * dx, ly - 3), (lx + 7 * dx, ly - 1)], fill=INK)
    d.rectangle([48, 40, 53, 45], fill=RED)
    d.rectangle([8, 48, 56, 52], fill=PAPER_D)

def draw_fish(d):
    """鱼藻图：横构图+水藻+双鱼"""
    d.rectangle([6, 18, 58, 46], fill=PAPER)
    d.rectangle([6, 18, 58, 21], fill=PAPER_L)
    d.line([8, 24, 56, 24], fill=TEAL, width=1)                      # 水草
    d.line([10, 28, 54, 28], fill=TEAL, width=1)
    # 鱼 1（游右）
    d.ellipse([16, 30, 36, 40], fill=TEAL)
    d.polygon([(36, 32), (44, 28), (44, 40)], fill=TEAL)             # 尾
    d.ellipse([18, 32, 24, 37], fill=(230, 224, 200, 255))
    d.point([(33, 33)], fill=INK)
    # 鱼 2（游左，淡）
    d.ellipse([38, 36, 54, 44], fill=INK_L)
    d.polygon([(38, 38), (32, 35), (32, 45)], fill=INK_L)
    d.point([(41, 39)], fill=PAPER)
    d.rectangle([48, 20, 53, 25], fill=RED)
    d.rectangle([6, 46, 58, 50], fill=PAPER_D)

BUILDERS = {
    'couplet_pair': draw_couplet,
    'rubbing': draw_rubbing,
    'calligraphy_verse': draw_calligraphy,
    'portrait_ancestor': draw_portrait,
    'painting_bamboo': draw_bamboo,
    'painting_fish': draw_fish,
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
    sheet.save(os.path.join(OUT, 'compare_r10.png'))
    print('r10 OK:', names)

if __name__ == '__main__':
    main()
