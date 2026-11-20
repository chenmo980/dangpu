# -*- coding: utf-8 -*-
"""第13轮(自动化)：瓷器第 2 批（单色釉名品 6 件）
zun_tang_sancai / vase_ruyao_tianqing / bowl_doucai_chicken / vase_guan_ge_kai / pot_zisha / censer_jun_purple
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

# 釉色族
TQ_L = (172, 200, 196, 255)   # 天青亮
TQ   = (129, 158, 158, 255)   # 天青
TQ_D = (94, 122, 122, 255)    # 天青暗
SANCAI_A = (217, 142, 43, 255)  # 三彩黄褐
SANCAI_B = (105, 128, 84, 255)  # 三彩绿
SANCAI_C = (156, 85, 60, 255)   # 三彩赭
ZI   = (94, 62, 62, 255)       # 紫砂
ZI_L = (128, 88, 84, 255)
JUN  = (139, 110, 160, 255)    # 钧紫
JUN_L = (162, 138, 180, 255)
JUN_D = (108, 84, 128, 255)
FC   = (196, 130, 152, 255)    # 粉彩
GE_KAI = (74, 48, 28, 255)     # 金丝铁线（开片线）
GLZ_L  = (232, 224, 196, 255)
GLZ_D2 = (186, 178, 148, 255)
INKC   = (68, 70, 76, 255)
GOLDC  = (186, 137, 83, 255)

def draw_sancai(d):
    """唐三彩尊：喇叭口+束颈+圆腹，三彩流釉斑"""
    d.polygon([(20, 2), (44, 2), (40, 16), (24, 16)], fill=TQ_L)    # 喇叭口
    d.ellipse([22, 1, 42, 8], fill=TQ)
    d.rectangle([26, 14, 38, 24], fill=TQ)                          # 束颈
    d.ellipse([12, 22, 52, 58], fill=TQ_D)                          # 圆腹
    d.ellipse([14, 24, 50, 56], fill=TQ)
    d.ellipse([16, 26, 48, 52], fill=TQ_L)
    d.ellipse([14, 44, 50, 58], fill=TQ_D)                          # 底压暗
    d.ellipse([18, 28, 34, 44], fill=SANCAI_A)                      # 黄褐流釉
    d.ellipse([22, 32, 32, 42], fill=SANCAI_B)                      # 绿釉
    d.ellipse([36, 30, 48, 46], fill=SANCAI_C)                      # 赭釉
    d.ellipse([38, 32, 45, 42], fill=SANCAI_B)
    d.line([18, 28, 22, 42], fill=SANCAI_B, width=2)                # 垂釉条
    d.line([42, 28, 46, 44], fill=SANCAI_A, width=2)

def draw_ruyao(d):
    """汝窑天青洗：浅洗+天青釉+细开片纹"""
    d.ellipse([8, 20, 56, 50], fill=TQ_D)                           # 洗身
    d.ellipse([10, 18, 54, 40], fill=TQ_L)                          # 口
    d.ellipse([12, 20, 52, 38], fill=TQ)
    d.ellipse([16, 22, 48, 36], fill=TQ_L)                          # 洗心
    # 开片纹（细线网）
    for (x0, y0, x1, y1) in [(20, 24, 30, 34), (30, 24, 24, 34), (30, 30, 42, 30),
                              (38, 24, 44, 34), (20, 34, 34, 36), (40, 34, 46, 30)]:
        d.line([x0, y0, x1, y1], fill=TQ_D, width=1)
    d.point([(27, 28)], fill=TQ_D)
    d.ellipse([14, 25, 22, 30], fill=(200, 220, 216, 255))          # 左上釉光
    d.ellipse([24, 48, 40, 54], fill=TQ_D)                          # 底足（满釉支烧）
    d.ellipse([26, 50, 38, 54], fill=TQ)

def draw_doucai(d):
    """斗彩鸡缸杯：小巧深腹+斗彩团鸡+青花边"""
    d.ellipse([14, 24, 50, 38], fill=GLZ_L) # 口
    d.ellipse([17, 25, 47, 36], fill=GLZ_D2)
    d.ellipse([19, 26, 45, 35], fill=(69, 145, 139, 255))           # 口沿青花带
    d.ellipse([16, 30, 48, 56], fill=GLZ_L)                         # 深腹
    d.ellipse([18, 32, 46, 54], fill=(224, 216, 190, 255))
    d.ellipse([18, 44, 46, 56], fill=GLZ_D2)          # 底压暗
    d.ellipse([24, 36, 38, 46], fill=(217, 142, 43, 255))           # 斗彩团鸡
    d.ellipse([32, 36, 38, 42], fill=(156, 55, 56, 255))            # 鸡冠
    d.point([(35, 39)], fill=INKC)             # 眼
    d.ellipse([22, 42, 30, 48], fill=(105, 128, 84, 255))           # 山石
    d.arc([14, 24, 50, 38], 170, 320, fill=(240, 236, 226, 255), width=2)
    d.rectangle([28, 54, 36, 59], fill=GLZ_D2)        # 圈足

def draw_ge_kai(d):
    """哥窑开片瓶：直颈瓶+金丝铁线开片"""
    d.rounded_rectangle([26, 2, 38, 20], 3, fill=TQ_L)              # 颈
    d.rectangle([27, 3, 37, 19], fill=TQ)
    d.ellipse([14, 18, 50, 56], fill=TQ_D)                          # 瓶体
    d.ellipse([16, 20, 48, 54], fill=TQ)
    d.ellipse([18, 22, 46, 50], fill=TQ_L)
    d.ellipse([16, 42, 48, 56], fill=TQ_D)
    # 金丝铁线（大开片+小开片）
    for (x0, y0, x1, y1) in [(24, 22, 28, 36), (36, 20, 32, 34), (42, 26, 36, 44), (20, 32, 30, 46), (34, 36, 44, 50)]:
        d.line([x0, y0, x1, y1], fill=GE_KAI, width=1)              # 铁线（深）
    for (x0, y0, x1, y1) in [(28, 26, 32, 32), (38, 32, 34, 40), (22, 38, 28, 42)]:
        d.line([x0, y0, x1, y1], fill=GOLDC, width=1)  # 金丝（细）
    d.rectangle([26, 55, 38, 60], fill=TQ_D)                        # 底
    d.ellipse([24, 58, 40, 63], fill=TQ_L)

def draw_zisha(d):
    """紫砂小壶：圆壶+弯嘴+圆把+壶盖钮"""
    d.ellipse([12, 24, 48, 56], fill=ZI)                            # 壶身
    d.ellipse([14, 26, 46, 54], fill=ZI_L)
    d.ellipse([17, 28, 34, 44], fill=(140, 101, 88, 255))           # 受光
    d.ellipse([16, 46, 44, 56], fill=(74, 48, 48, 255))             # 底压暗
    d.rectangle([26, 16, 38, 26], fill=ZI)                          # 颈
    d.ellipse([25, 12, 39, 20], fill=ZI_L)                          # 盖
    d.ellipse([29, 8, 35, 15], fill=ZI)                             # 钮
    d.point([(32, 10)], fill=ZI_L)
    d.polygon([(44, 30), (58, 24), (58, 32), (46, 36)], fill=ZI)    # 嘴
    d.line([45, 31, 57, 25], fill=ZI_L, width=1)
    d.arc([4, 20, 22, 46], 260, 100, fill=ZI, width=5)              # 圆把
    d.arc([6, 21, 20, 45], 260, 100, fill=ZI_L, width=2)
    d.rectangle([24, 18, 40, 20], fill=(74, 48, 28, 255))           # 盖口线

def draw_jun_censer(d):
    """钧窑紫红斑炉：双耳罐炉+天青底+紫红斑"""
    d.arc([8, 6, 26, 32], 200, 90, fill=PAL['lo2'], width=5)        # 左耳
    d.arc([38, 6, 56, 32], 90, 340, fill=PAL['lo2'], width=5)
    d.arc([9, 7, 25, 31], 200, 80, fill=JUN, width=2)
    d.arc([39, 7, 55, 31], 100, 340, fill=JUN, width=2)
    d.ellipse([12, 24, 52, 56], fill=TQ_D)                          # 炉身（天青底）
    d.ellipse([14, 26, 50, 54], fill=TQ)
    d.ellipse([16, 27, 48, 36], fill=TQ_L)                          # 炉口
    d.ellipse([18, 28, 46, 35], fill=TQ_D)
    d.ellipse([20, 30, 40, 48], fill=JUN)                           # 紫红斑（大）
    d.ellipse([22, 32, 36, 46], fill=JUN_L)
    d.ellipse([34, 30, 48, 44], fill=JUN_D)                         # 斑边玫瑰紫
    d.ellipse([36, 32, 44, 42], fill=JUN)
    d.ellipse([14, 46, 50, 56], fill=TQ_D)
    for lx in (18, 32, 46):                                          # 三足
        d.ellipse([lx - 3, 54, lx + 3, 62], fill=TQ_D)
        d.ellipse([lx - 2, 55, lx + 2, 60], fill=TQ)

BUILDERS = {
    'zun_tang_sancai': draw_sancai,
    'vase_ruyao_tianqing': draw_ruyao,
    'bowl_doucai_chicken': draw_doucai,
    'vase_guan_ge_kai': draw_ge_kai,
    'pot_zisha': draw_zisha,
    'censer_jun_purple': draw_jun_censer,
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
    sheet.save(os.path.join(OUT, 'compare_r14.png'))
    print('r14 OK:', names)

if __name__ == '__main__':
    main()
