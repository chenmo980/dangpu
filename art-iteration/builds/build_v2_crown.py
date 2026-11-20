# -*- coding: utf-8 -*-
"""补建 crown_silver（中式束发冠）v2"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_v2_exemplars import process, PAL, OUT, SS
from PIL import Image, ImageDraw

def draw_crown_v2(d):
    """中式束发冠：圆拱冠体+顶簪横穿+束带+冠足"""
    d.ellipse([14, 12, 50, 46], fill=PAL['lo'])          # 冠体（圆拱）
    d.ellipse([16, 14, 48, 44], fill=PAL['mid'])
    d.ellipse([19, 16, 45, 36], fill=PAL['hi'])          # 顶面受光
    d.ellipse([21, 17, 43, 30], fill=PAL['hl'])          # 冠顶高光
    d.ellipse([24, 4, 40, 16], fill=PAL['mid'])          # 冠顶凸台
    d.ellipse([26, 5, 38, 13], fill=PAL['hi'])
    d.line([16, 8, 48, 8], fill=PAL['gold'], width=3)    # 横簪
    d.line([16, 8, 48, 8], fill=PAL['gold_l'], width=1)
    d.ellipse([14, 6, 20, 12], fill=PAL['gold_d'])       # 簪尾坠
    d.rectangle([20, 36, 44, 40], fill=PAL['mid'])       # 束带
    d.rectangle([20, 36, 44, 37], fill=PAL['gold'])      # 束带金边
    d.rectangle([24, 44, 40, 52], fill=PAL['lo'])        # 冠足
    d.rectangle([26, 45, 38, 51], fill=PAL['lo2'])
    d.ellipse([22, 50, 42, 60], fill=PAL['dk'])          # 冠足底

big = Image.new('RGBA', (SS, SS), (0, 0, 0, 0))
draw_crown_v2(ImageDraw.Draw(big))
img = process(big)
img.save(os.path.join(OUT, 'crown_silver.png'))
print('crown_silver v2 OK')
