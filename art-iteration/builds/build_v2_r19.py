# -*- coding: utf-8 -*-
"""第18轮(自动化)：钟表收官 5 件 + 玉器快件 6 件"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw, ImageFont

ROD, ROD_D, ROD_L = (92,58,33,255), (74,48,28,255), (140,101,64,255)
SIL_L, SIL, SIL_D = (213,210,184,255), (168,174,165,255), (121,116,110,255)
INK, INK_L = (68,70,76,255), (95,104,104,255)
GOLD, GOLD_L = (186,137,83,255), (224,208,155,255)
RED = (156,55,56,255)
GLASS = (200,220,216,255)
J_L, J, J_D = (222,230,214,255), (188,202,182,255), (150,168,150,255)
QIN = (160,128,84,255)

def clock_face(d, cx, cy, r):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(240,236,226,255))
    for i in range(12):
        a = math.radians(i*30)
        tx, ty = cx+(r-3)*math.sin(a), cy-(r-3)*math.cos(a)
        d.ellipse([tx-1,ty-1,tx+1,ty+1], fill=INK)
    ha = math.radians(60); ma = math.radians(170)
    d.line([cx,cy,cx+(r-6)*math.sin(ha),cy-(r-6)*math.cos(ha)], fill=INK, width=2)
    d.line([cx,cy,cx+(r-4)*math.sin(ma),cy-(r-4)*math.cos(ma)], fill=INK, width=1)
    d.point([(cx,cy)], fill=RED)

def draw_grandfather_knock(d):
    """磕角落地钟：立柜+缺角+裂纹+停摆"""
    d.rounded_rectangle([18,2,46,10],3, fill=ROD_D)
    d.rectangle([16,10,48,60], fill=ROD)
    d.rectangle([18,12,46,58], fill=ROD_L)
    d.polygon([(44,12),(48,12),(48,20)], fill=(0,0,0,0))            # 磕缺角
    d.line([44,12,48,20], fill=INK, width=1)                        # 缺口缘
    d.line([20,14,26,40], fill=INK, width=1)                        # 木裂
    d.rectangle([19,13,45,32], fill=SIL_L)
    clock_face(d, 32, 22, 10)
    d.line([31,38,31,54], fill=SIL_D, width=2)                      # 停摆（灰杆）
    d.ellipse([28,52,36,58], fill=SIL_D)
    d.rectangle([16,58,48,62], fill=ROD_D)

def draw_pocket_broken(d):
    """摔坏怀表：表蒙碎裂+针停+壳凹"""
    d.ellipse([10,10,54,54], fill=SIL_D)
    d.ellipse([13,13,51,51], fill=SIL)
    d.ellipse([16,16,48,48], fill=(225,222,210,255))
    for (x0,y0,x1,y1) in [(32,32,20,20),(32,32,44,22),(32,32,24,44),(32,32,46,42),(20,20,26,14)]:
        d.line([x0,y0,x1,y1], fill=INK, width=1)                    # 蒙面裂纹
    d.polygon([(22,18),(26,14),(30,20)], fill=(0,0,0,0))            # 玻璃崩缺
    d.ellipse([28,2,36,10], fill=SIL_D)
    d.line([32,32,32,25], fill=INK, width=2)                        # 停针
    d.ellipse([29,1,35,7], fill=SIL_L)

def draw_turret(d):
    """塔楼钟模型：方塔+尖顶+双钟面+小铃"""
    d.polygon([(16,8),(48,8),(44,2),(20,2)], fill=ROD_D)            # 尖顶
    d.rectangle([18,8,46,54], fill=ROD)
    d.rectangle([20,10,44,52], fill=ROD_L)
    d.rectangle([21,12,43,32], fill=SIL_L)
    clock_face(d, 32, 22, 9)
    d.rectangle([21,36,43,50], fill=(52,34,20,255))                 # 钟室
    d.ellipse([26,38,38,48], fill=GOLD)                             # 大钟
    d.ellipse([28,40,36,46], fill=GOLD_L)
    d.line([32,38,32,44], fill=ROD_D, width=1)
    d.rectangle([16,54,48,60], fill=ROD_D)

def draw_orrery(d):
    """行星仪：底座+立柱+同心环+行星球"""
    d.ellipse([10,46,54,62], fill=ROD_D)                            # 底座
    d.rectangle([29,36,35,48], fill=ROD)                            # 立柱
    d.ellipse([24,32,40,40], fill=GOLD)                             # 中心太阳
    d.ellipse([26,34,38,38], fill=GOLD_L)
    d.arc([12,28,52,52], 180, 360, fill=SIL_D, width=2)             # 外环
    d.arc([18,30,46,48], 180, 360, fill=SIL, width=2)
    d.line([32,36,14,30], fill=SIL_D, width=2)                      # 行星臂 1
    d.ellipse([10,26,18,34], fill=(69,145,139,255))         # 行星球
    d.point([(13,29)], fill=(230,224,200,255))
    d.line([32,36,50,42], fill=SIL_D, width=2)                      # 臂 2
    d.ellipse([46,38,56,46], fill=RED)                              # 行星 2

def draw_chain_gold(d):
    """金表链：连环扣+尾扣"""
    links = [(8,14),(18,20),(28,14),(38,20),(48,14),(58,20)]
    for i,(x,y) in enumerate(links):
        d.ellipse([x, y, x+12, y+14], outline=GOLD, width=3)
        d.ellipse([x+2, y+2, x+10, y+12], outline=GOLD_L, width=1)
    d.ellipse([54,22,66,36], fill=GOLD)                             # 尾扣
    d.ellipse([57,25,63,33], fill=GOLD_L)

def draw_belt_hook(d):
    """玉带钩：G 形弯钩+兽首+沁"""
    d.arc([10,14,52,52], 240, 90, fill=J_D, width=9)                # 弯体
    d.arc([11,15,51,51], 240, 90, fill=J, width=5)
    d.arc([12,16,50,50], 240, 90, fill=J_L, width=1)
    d.ellipse([6,10,26,30], fill=J)                                 # 兽首
    d.ellipse([9,13,23,27], fill=J_L)
    d.ellipse([13,16,19,22], fill=INK)                              # 眼
    d.ellipse([44,42,56,54], fill=J)                                # 尾钮
    d.ellipse([46,44,54,52], fill=J_L)
    d.ellipse([18,36,26,44], fill=QIN)                              # 沁色

def draw_brush_washer(d):
    """玉笔洗：小圆洗+厚壁+沁"""
    d.ellipse([8,18,56,56], fill=J_D)
    d.ellipse([11,16,53,44], fill=J_L)                              # 口
    d.ellipse([14,19,50,42], fill=(120,148,122,255))                # 洗心
    d.ellipse([17,21,47,40], fill=J_L)
    d.ellipse([12,46,52,56], fill=J_D)                              # 壁底
    d.ellipse([18,22,28,28], fill=(240,244,232,255))                # 釉光
    d.ellipse([40,40,50,50], fill=QIN)                              # 沁

def draw_seal_jade(d):
    """玉印：方印台+兽钮+印面朱底"""
    d.rounded_rectangle([14,30,50,58],3, fill=J)                    # 印台
    d.rounded_rectangle([17,33,47,55],2, fill=J_L)
    d.rectangle([20,44,44,52], fill=RED)                            # 印面朱底
    d.line([24,46,40,46], fill=(120,40,40,255), width=1)
    d.line([24,49,40,49], fill=(120,40,40,255), width=1)
    d.ellipse([22,10,42,32], fill=J)                                # 兽钮（团伏）
    d.ellipse([25,12,39,29], fill=J_L)
    d.ellipse([26,12,30,17], fill=J_D)                              # 钮首
    d.ellipse([34,14,38,18], fill=QIN)                              # 沁
    jade_shine = (240,244,232,255)
    d.arc([17,33,47,55], 180, 320, fill=jade_shine, width=1)

def draw_pipe_jade(d):
    """玉烟嘴：细长锥管+两端铜箍"""
    d.polygon([(12,40),(22,52),(26,48),(16,36)], fill=J)            # 前段
    d.polygon([(24,34),(30,28),(42,14),(36,12),(22,30)], fill=J)    # 后段
    d.ellipse([30,10,46,24], fill=J_D)                              # 后接口
    d.ellipse([8,34,20,46], fill=J_L)                               # 前端厚壁
    d.ellipse([11,37,17,43], fill=INK)                              # 通孔
    d.rectangle([14,30,22,36], fill=GOLD)                           # 铜箍
    d.rectangle([14,30,22,31], fill=GOLD_L)
    d.ellipse([34,12,44,20], fill=QIN)                              # 沁

def draw_bi_disc(d):
    """玉璧：大平圆+中孔+谷纹点"""
    d.ellipse([8,10,56,58], fill=J_D)
    d.ellipse([11,13,53,55], fill=J)
    d.ellipse([15,17,49,51], fill=J_L)
    d.ellipse([24,26,40,42], fill=(0,0,0,0))                        # 中孔
    for (gx,gy) in [(20,22),(30,18),(40,22),(18,34),(46,34),(24,46),(34,48),(44,46)]:
        d.point([(gx,gy)], fill=J_D)                                # 谷纹点
        d.point([(gx+1,gy+1)], fill=QIN)
    jade_shine = (240,244,232,255)
    d.arc([11,13,53,55], 190, 300, fill=jade_shine, width=2)

def draw_cong(d):
    """玉琮：外方内圆双层"""
    d.rounded_rectangle([12,10,52,54],4, fill=J_D)                  # 外方
    d.rounded_rectangle([15,13,49,51],3, fill=J)
    d.rounded_rectangle([18,16,46,48],2, fill=J_L)
    d.ellipse([22,20,42,44], fill=(0,0,0,0))                        # 中孔
    d.line([12,30,52,30], fill=J_D, width=2)                        # 层界
    d.ellipse([24,22,40,42], outline=J_D, width=1)                  # 孔口环
    for (gx,gy) in [(20,18),(38,18),(20,42),(38,42)]:               # 兽面角
        d.ellipse([gx,gy,gx+6,gy+6], fill=J)
        d.point([(gx+3,gy+3)], fill=QIN)
    jade_shine2 = (240,244,232,255)
    d.line([18,16,28,16], fill=jade_shine2, width=1)

BUILDERS = {
    'clock_grandfather_knock': draw_grandfather_knock,
    'watch_pocket_broken': draw_pocket_broken,
    'clock_turret': draw_turret,
    'orrery_planet': draw_orrery,
    'watch_chain_gold': draw_chain_gold,
    'belt_hook_jade': draw_belt_hook,
    'brush_washer_jade': draw_brush_washer,
    'seal_jade': draw_seal_jade,
    'pipe_jade': draw_pipe_jade,
    'bi_disc_jade': draw_bi_disc,
    'cong_jade': draw_cong,
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
    sheet.save(os.path.join(OUT, 'compare_r19.png'))
    print('r19 OK:', names)

if __name__ == '__main__':
    main()
