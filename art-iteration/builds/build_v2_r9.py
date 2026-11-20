# -*- coding: utf-8 -*-
"""第8轮(自动化)：字画首批 6 件 scroll_landscape/scroll_flowers/handscroll/album_leaf/fan_folded/fan_round
painting v2 配方：纸黄 ramp 画心+深木轴头+墨色内容+红印章+青绿点缀
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

PAPER_L = (232, 224, 196, 255)   # 画心亮
PAPER  = (213, 210, 184, 255)    # paper
PAPER_D = (186, 178, 148, 255)   # 画心暗
INK    = (68, 70, 76, 255)       # 墨 (dk2)
INK_L  = (95, 104, 104, 255)     # 淡墨
ROD    = (92, 58, 33, 255)       # 轴杆（wood）
ROD_D  = (74, 48, 28, 255)
TEAL   = (69, 145, 139, 255)     # 青绿
TEAL_D = (47, 117, 111, 255)
RED    = (156, 55, 56, 255)      # 印章

def draw_scroll_landscape(d):
    """山水立轴：上轴头+画心(远山/水纹)+下轴头"""
    d.rounded_rectangle([18, 2, 46, 8], 3, fill=ROD)                # 上轴头
    d.ellipse([15, 1, 21, 9], fill=ROD_D); d.ellipse([43, 1, 49, 9], fill=ROD_D)  # 轴头凸
    d.rectangle([14, 8, 50, 12], fill=PAPER_D)                      # 天头绫
    d.rectangle([14, 12, 50, 50], fill=PAPER)                       # 画心
    d.rectangle([14, 12, 50, 15], fill=PAPER_L)                     # 画心上部亮
    # 远山两座（青绿）
    d.polygon([(18, 34), (27, 22), (34, 34)], fill=TEAL)
    d.polygon([(26, 34), (35, 25), (44, 34)], fill=TEAL_D)
    d.polygon([(28, 27), (31, 24), (34, 28)], fill=(230, 224, 200, 255))  # 山头留白
    d.line([16, 38, 48, 38], fill=INK_L, width=1)                   # 水纹
    d.line([18, 41, 46, 41], fill=INK_L, width=1)
    d.line([20, 44, 44, 44], fill=INK_L, width=1)
    d.rectangle([42, 15, 47, 20], fill=RED)                         # 印章
    d.rectangle([14, 50, 50, 54], fill=PAPER_D)                     # 地头绫
    d.rounded_rectangle([18, 54, 46, 60], 3, fill=ROD)              # 下轴头
    d.ellipse([15, 53, 21, 61], fill=ROD_D); d.ellipse([43, 53, 49, 61], fill=ROD_D)
    d.rectangle([14, 8, 50, 61], outline=INK, width=1)

def draw_scroll_flowers(d):
    """花鸟立轴：画心枝上双鸟"""
    d.rounded_rectangle([18, 2, 46, 8], 3, fill=ROD)
    d.ellipse([15, 1, 21, 9], fill=ROD_D); d.ellipse([43, 1, 49, 9], fill=ROD_D)
    d.rectangle([14, 8, 50, 54], fill=PAPER)
    d.rectangle([14, 8, 50, 11], fill=PAPER_L)
    d.line([24, 14, 40, 50], fill=(110, 88, 56, 255), width=2)      # 枝
    # 鸟（横放：头右尾左，爪抓枝）
    d.ellipse([24, 26, 38, 38], fill=(217, 142, 43, 255))           # 身
    d.ellipse([26, 28, 36, 36], fill=(232, 170, 96, 255))           # 腹
    d.ellipse([34, 22, 42, 30], fill=(186, 110, 34, 255))           # 头
    d.polygon([(42, 24), (47, 26), (42, 28)], fill=INK)             # 喙
    d.point([(39, 24)], fill=INK)                                   # 眼
    d.polygon([(24, 28), (18, 24), (16, 34), (24, 36)], fill=(140, 78, 26, 255))  # 尾羽分叉
    d.line([28, 38, 27, 42], fill=(92, 58, 33, 255), width=1)       # 爪 1
    d.line([32, 38, 33, 42], fill=(92, 58, 33, 255), width=1)       # 爪 2
    d.ellipse([19, 40, 25, 46], fill=TEAL)                          # 花瓣点
    d.ellipse([16, 46, 22, 52], fill=TEAL)
    d.rectangle([42, 48, 47, 53], fill=RED)                         # 印章
    d.rectangle([14, 54, 50, 58], fill=PAPER_D)
    d.rounded_rectangle([18, 58, 46, 64], 3, fill=ROD)
    d.ellipse([15, 57, 21, 65], fill=ROD_D); d.ellipse([43, 57, 49, 65], fill=ROD_D)

def draw_handscroll(d):
    """手卷：右半卷起圆柱+左半展开画心"""
    d.rounded_rectangle([40, 14, 58, 50], 4, fill=PAPER_D)          # 卷起部分
    d.ellipse([40, 14, 50, 50], fill=PAPER_D)                       # 卷筒端面
    d.ellipse([43, 17, 47, 47], fill=PAPER)
    d.ellipse([43, 26, 47, 38], fill=RED)                           # 卷心轴孔
    d.rectangle([6, 16, 44, 48], fill=PAPER)                        # 展开画心
    d.rectangle([6, 16, 44, 19], fill=PAPER_L)
    d.polygon([(8, 40), (16, 28), (24, 40)], fill=TEAL)             # 小山
    d.polygon([(18, 40), (27, 30), (36, 40)], fill=TEAL_D)
    d.line([7, 44, 43, 44], fill=INK_L, width=1)
    d.line([9, 46, 41, 46], fill=INK_L, width=1)
    d.rectangle([36, 18, 42, 23], fill=RED)                         # 引首印
    d.rectangle([4, 12, 8, 52], fill=ROD)                           # 左轴头
    d.ellipse([2, 10, 10, 18], fill=ROD_D); d.ellipse([2, 46, 10, 54], fill=ROD_D)

def draw_album_leaf(d):
    """册页：叠层纸页+封面"""
    d.rounded_rectangle([10, 14, 54, 54], 3, fill=PAPER_D)          # 底层
    d.rounded_rectangle([12, 12, 52, 50], 3, fill=PAPER)            # 中层
    d.rounded_rectangle([14, 10, 50, 46], 3, fill=PAPER_L)          # 顶层
    d.rounded_rectangle([16, 12, 48, 40], 2, fill=PAPER)            # 打开页
    d.polygon([(20, 36), (28, 24), (36, 36)], fill=TEAL)            # 页上小画
    d.polygon([(28, 36), (36, 26), (44, 36)], fill=TEAL_D)
    d.line([17, 39, 47, 39], fill=INK_L, width=1)
    d.rectangle([40, 14, 46, 19], fill=RED)                         # 印章
    d.rounded_rectangle([14, 40, 50, 58], 3, fill=(47, 74, 111, 255))  # 蓝布封面
    d.rounded_rectangle([17, 43, 47, 55], 2, fill=(63, 92, 133, 255))
    d.rectangle([29, 45, 35, 53], fill=PAPER)                       # 题签
    d.line([30, 47, 34, 51], fill=INK, width=1)

def draw_fan_folded(d):
    """折扇（收拢）：扇骨放射+扇面折叠+流苏"""
    d.polygon([(30, 56), (16, 10), (22, 6), (44, 52)], fill=PAPER_D)  # 展开斜面
    d.polygon([(30, 56), (22, 6), (28, 5), (40, 52)], fill=PAPER)     # 主面
    d.polygon([(30, 56), (28, 5), (34, 4), (44, 50)], fill=PAPER_L)
    for (x0, y0, x1, y1) in [(24, 8, 34, 54), (30, 6, 38, 53), (36, 5, 42, 51)]:
        d.line([x0, y0, x1, y1], fill=ROD_D, width=1)                 # 扇骨
    d.ellipse([27, 52, 35, 60], fill=ROD)                             # 扇钉
    d.ellipse([29, 54, 33, 58], fill=PAL['gold'])
    d.line([32, 60, 32, 64], fill=PAL['red'], width=2)                # 流苏

def draw_fan_round(d):
    """团扇：圆绢面+细框+短柄+枝花纹"""
    d.ellipse([12, 4, 52, 44], fill=PAPER_D)                          # 外框
    d.ellipse([14, 6, 50, 42], fill=PAPER)                            # 绢面
    d.ellipse([16, 8, 48, 40], fill=PAPER_L)
    d.line([24, 14, 40, 34], fill=(110, 88, 56, 255), width=2)        # 花枝
    d.ellipse([34, 12, 42, 20], fill=TEAL)                            # 花
    d.ellipse([30, 18, 36, 24], fill=(230, 224, 200, 255))
    d.ellipse([20, 26, 26, 32], fill=TEAL_D)                          # 叶
    d.rectangle([42, 36, 47, 41], fill=RED)                           # 印章
    d.rectangle([29, 42, 35, 62], fill=ROD)                           # 柄
    d.line([30, 43, 30, 61], fill=ROD_D, width=2)
    d.ellipse([28, 60, 36, 64], fill=PAL['gold_d'])                   # 柄尾

BUILDERS = {
    'scroll_landscape': draw_scroll_landscape,
    'scroll_flowers': draw_scroll_flowers,
    'handscroll': draw_handscroll,
    'album_leaf': draw_album_leaf,
    'fan_folded': draw_fan_folded,
    'fan_round': draw_fan_round,
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
    sheet.save(os.path.join(OUT, 'compare_r9.png'))
    print('r9 OK:', names)

if __name__ == '__main__':
    main()
