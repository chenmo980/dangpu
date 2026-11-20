# -*- coding: utf-8 -*-
"""第19轮续：玉器收官 8 件 → 玉器 20/20、全目录 120 件齐"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw

J_L, J, J_D = (222,230,214,255), (188,202,182,255), (150,168,150,255)
QIN = (160,128,84,255)
INK = (68,70,76,255)
GOLD, GOLD_L = (186,137,83,255), (224,208,155,255)
RED = (156,55,56,255)

def draw_buddha_pendant(d):
    """玉佛坠：坐佛小坠（头+身+座）"""
    d.ellipse([24,8,40,24], fill=J)                                 # 头
    d.ellipse([27,10,37,22], fill=J_L)
    d.ellipse([29,6,35,12], fill=J_D)                               # 肉髻
    d.polygon([(16,48),(48,48),(40,24),(24,24)], fill=J)            # 身
    d.polygon([(20,46),(44,46),(38,27),(26,27)], fill=J_L)
    d.ellipse([12,46,52,58], fill=J_D)                              # 莲座
    d.ellipse([15,48,49,56], fill=J)
    d.point([(32,17)], fill=QIN)                                    # 眉间沁
    d.line([28,30,36,30], fill=J_D, width=1)                        # 衣褶
    d.ellipse([22,10,28,16], fill=(240,244,232,255))                # 玉光

def draw_hairpin_jade(d):
    """玉簪：长杆+簪首鸟形"""
    d.line([12,56,40,16], fill=J_D, width=5)
    d.line([13,55,41,15], fill=J, width=3)
    d.line([14,54,42,14], fill=J_L, width=1)
    d.ellipse([36,6,50,20], fill=J)                                 # 簪首
    d.ellipse([39,9,47,17], fill=J_L)
    d.polygon([(44,8),(50,4),(48,12)], fill=J_D)                    # 首翼
    d.point([(43,11)], fill=QIN)
    d.ellipse([10,52,16,58], fill=J_D)                              # 尾端

def draw_cup_jade(d):
    """玉杯：敛口深杯+双耳"""
    d.ellipse([14,18,50,32], fill=J_D)                              # 口
    d.ellipse([17,20,47,30], fill=(120,148,122,255))                # 口内
    d.ellipse([16,24,48,56], fill=J)                                # 身
    d.ellipse([18,26,46,54], fill=J_L)
    d.ellipse([18,44,46,56], fill=J_D)                              # 底压暗
    d.arc([8,26,20,44], 200, 90, fill=J, width=4)                   # 左耳
    d.arc([44,26,56,44], 90, 340, fill=J, width=4)                  # 右耳
    d.ellipse([24,56,40,62], fill=J_D)                              # 圈足
    d.ellipse([20,24,28,32], fill=(240,244,232,255))                # 玉光
    d.ellipse([38,40,46,48], fill=QIN)                              # 沁

def draw_peach_jade(d):
    """玉桃摆件：双桃+叶+枝"""
    d.ellipse([14,24,42,52], fill=J)                                # 大桃
    d.polygon([(28,26),(28,14),(40,28)], fill=J_D)                  # 桃尖
    d.ellipse([17,27,39,49], fill=J_L)
    d.ellipse([38,20,56,42], fill=J)                                # 小桃
    d.ellipse([41,23,53,39], fill=J_L)
    d.line([28,26,36,18], fill=J_D, width=2)                        # 桃沟
    d.polygon([(30,14),(38,8),(42,16)], fill=(105,148,74,255))      # 叶
    d.line([36,16,40,22], fill=(74,48,28,255), width=2)     # 枝
    d.point([(34,36)], fill=QIN)                                    # 沁
    d.ellipse([20,30,28,38], fill=(240,244,232,255))                # 玉光

def draw_jade_mirror(d):
    """玉背铜镜：铜镜+玉柄/玉背嵌片"""
    d.ellipse([12,4,52,44], fill=(139,110,86,255))                  # 铜镜体
    d.ellipse([15,7,49,41], fill=(166,137,88,255))
    d.ellipse([18,10,46,38], fill=(121,116,110,255))                # 镜面（昏）
    d.ellipse([22,13,42,34], fill=(139,110,86,255))
    d.arc([18,10,46,38], 190, 320, fill=(200,180,140,255), width=1)
    d.rounded_rectangle([24,44,40,62], 3, fill=J)                   # 玉柄
    d.rounded_rectangle([26,46,38,60], 2, fill=J_L)
    d.rectangle([26,46,38,48], fill=GOLD)                           # 柄箍
    d.rectangle([26,46,38,47], fill=GOLD_L)

def draw_beads_string(d):
    """玉珠串：一串 7 珠（弧线排列）"""
    import math as m
    pts = [(8,40),(14,32),(21,26),(29,22),(37,22),(45,26),(52,32)]
    for i,(x,y) in enumerate(pts):
        r = 6 if i % 2 == 0 else 5
        d.ellipse([x-r, y-r, x+r, y+r], fill=J)
        d.ellipse([x-r+1, y-r+1, x+r-1, y+r-1], fill=J_L)
        d.point([(x-r//2, y-r//2)], fill=(240,244,232,255))
        d.point([(x+r//2, y+r//2)], fill=QIN)                       # 交替沁
    for i in range(len(pts)-1):                                      # 串线
        d.line([pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]], fill=(117,100,80,255), width=1)

def draw_junk_scraps(d):
    """玉料边角：碎料堆"""
    d.polygon([(10,44),(22,30),(30,42),(38,28),(50,40),(54,54),(8,54)], fill=J_D)
    d.polygon([(14,44),(22,34),(30,44),(38,32),(48,42),(50,52),(12,52)], fill=J)
    d.polygon([(18,42),(24,36),(30,42)], fill=J_L)
    d.polygon([(34,40),(40,34),(46,42)], fill=J_L)
    d.ellipse([26,44,40,54], fill=QIN)                              # 沁重
    d.line([20,34,26,30], fill=J_D, width=1)                        # 切割痕

def draw_axe_broken(d):
    """残玉斧：斧身断裂+双孔+沁重"""
    d.polygon([(10,10),(38,6),(44,26),(24,30),(14,24)], fill=J)     # 斧身残段
    d.polygon([(12,12),(36,9),(41,24),(24,27),(16,22)], fill=J_L)
    d.line([40,10,46,20], fill=J_D, width=2)  # 断口缘
    d.polygon([(40,10),(48,16),(44,28)], fill=J_D)                  # 断裂斜面
    d.ellipse([14,14,20,20], fill=(0,0,0,0))                        # 孔
    d.ellipse([15,15,19,19], fill=(120,132,120,255))
    d.ellipse([24,18,34,26], fill=QIN)                              # 沁重
    d.line([16,24,36,20], fill=J_D, width=1)                        # 刃缘痕

BUILDERS = {
    'carving_jade_buddha': draw_buddha_pendant,
    'hairpin_jade': draw_hairpin_jade,
    'cup_jade': draw_cup_jade,
    'peach_jade': draw_peach_jade,
    'mirror_jade_bronze_back': draw_jade_mirror,
    'beads_jade_string': draw_beads_string,
    'junk_jade_scraps': draw_junk_scraps,
    'axe_jade_broken': draw_axe_broken,
}

def main():
    for name, fn in BUILDERS.items():
        big = Image.new('RGBA', (SS, SS), (0, 0, 0, 0))
        fn(ImageDraw.Draw(big))
        process(big).save(os.path.join(OUT, f'{name}.png'))
    print('r20 OK:', list(BUILDERS.keys()))

if __name__ == '__main__':
    main()
