# -*- coding: utf-8 -*-
"""冒烟测试：验证 pixel-art-studio 的 pixelstudio.py 在本机可用"""
import sys
SKILL = r'C:\Users\Administrator\.zcode\skills\pixel-art-studio\scripts'
sys.path.insert(0, SKILL)
from pixelstudio import Sprite, PALETTES, ramp

BODY = ramp("#C3272B", 4)  # 朱砂 4 阶 ramp
s = Sprite(32, 32, palette=BODY + ["#3D3B4F", "#E8D7B0"])
s.ellipse(8, 14, 24, 26, BODY[0])
s.ellipse(8, 12, 23, 24, BODY[2], only="opaque")
s.outline(BODY[0], where="inside")
s.preview(r'C:\测试工作区\probably-stolen-study\art-demo\smoke_pixelstudio.png', scale=8)
s.stats()
print("pixel-art-studio SMOKE OK")
