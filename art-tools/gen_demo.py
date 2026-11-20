# -*- coding: utf-8 -*-
"""《掌眼·当铺》美术演示：中国色板 + 高柜台场景构图 mockup + 当品 icon 流水线样例"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = r'C:\测试工作区\probably-stolen-study\art-demo'
os.makedirs(OUT, exist_ok=True)

# 中国传统色（设计文档美术方向）
PALETTE = [
    ('朱砂', '#C3272B'), ('胭脂', '#9D2933'), ('藤黄', '#FFB61E'), ('秋香', '#D9B611'),
    ('月白', '#D6ECF0'), ('黛蓝', '#425066'), ('玄青', '#3D3B4F'), ('黛绿', '#2B4A3D'),
    ('紫檀', '#4C2A20'), ('胡桃', '#8C5B3F'), ('纸黄', '#E8D7B0'), ('银灰', '#B8BCC8'),
]
def C(n):
    return next(hexv for name, hexv in PALETTE if name == n)

def load_font(size):
    for f in (r'C:\Windows\Fonts\simhei.ttf', r'C:\Windows\Fonts\msyh.ttc'):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()

# ---------- 1. 色板 ----------
sw, sh = 150, 90
pal = Image.new('RGB', (sw * 4, sh * 3), C('玄青'))
d = ImageDraw.Draw(pal)
for i, (name, hexv) in enumerate(PALETTE):
    x, y = (i % 4) * sw, (i // 4) * sh
    d.rectangle([x + 8, y + 8, x + sw - 8, y + sh - 34], fill=hexv)
    f = load_font(20)
    d.text((x + 12, y + sh - 30), f'{name} {hexv}', fill='#D8D3C0', font=f)
pal.save(os.path.join(OUT, '中国色板.png'))

# ---------- 2. 高柜台场景构图 mockup（320x180 逻辑像素，4x 放大） ----------
W, H, S = 320, 180, 4
img = Image.new('RGB', (W, H))
d = ImageDraw.Draw(img)

# 背景墙面（黛青）+ 阴影
d.rectangle([0, 0, W, 118], fill=C('黛蓝'))
d.rectangle([0, 0, W, 118], fill=None)
for y in range(0, 118, 6):          # 砖缝暗纹
    d.line([0, y, W, y], fill='#3A4656')
d.rectangle([0, 118, W, H], fill=C('紫檀'))  # 柜台后地面暗部

# 匾额「掌眼·當」
d.rectangle([108, 10, 214, 40], fill=C('紫檀'), outline='#2A1B14')
f32 = load_font(22)
d.text((128, 14), '掌眼當', fill=C('藤黄'), font=f32)
d.rectangle([104, 6, 218, 44], outline=C('秋香'))

# 字画（墙上挂轴）
d.rectangle([30, 20, 62, 90], fill=C('纸黄'), outline='#B8A67E')
d.rectangle([258, 20, 290, 90], fill=C('纸黄'), outline='#B8A67E')
d.line([36, 35, 56, 80], fill='#7A6A4F', width=2)
d.line([42, 30, 46, 84], fill='#7A6A4F', width=1)
d.ellipse([266, 40, 284, 58], outline='#6B5B3F', width=2)

# 灯笼（左上/右上）
for lx in (86, 232):
    d.ellipse([lx - 10, 48, lx + 10, 68], fill=C('朱砂'), outline='#8E1A14')
    d.line([lx, 38, lx, 48], fill='#8E1A14')
    d.line([lx - 10, 58, lx + 10, 58], fill='#8E1A14')
    d.line([lx - 6, 68, lx - 6, 76], fill=C('藤黄'))
    d.line([lx + 6, 68, lx + 6, 76], fill=C('藤黄'))

# 客人（柜台外，只见上半身——高柜台演出核心）
d.rectangle([150, 84, 196, 118], fill=C('胭脂'))            # 身体
d.ellipse([160, 62, 186, 88], fill='#E8C29E')               # 脸
d.rectangle([158, 60, 188, 70], fill='#2A2020')             # 发辫/帽
d.line([173, 88, 173, 104], fill='#5B3A2E', width=3)        # 辫子
d.ellipse([196, 70, 214, 92], fill=C('胭脂'))               # 手臂

# 高柜台（前景，占画面下 1/3）
d.rectangle([0, 118, W, 128], fill=C('胡桃'))               # 柜面顶
d.line([0, 118, W, 118], fill='#A9764F')                    # 顶面高光
d.rectangle([0, 128, W, H], fill='#6B4423')                 # 柜身
for x in range(0, W, 64):                                    # 板缝
    d.line([x, 128, x, H], fill='#573519')
d.rectangle([0, 118, W, 121], fill='#A9764F')

# 柜上前景当品（玩家侧）
d.ellipse([40, 108, 76, 126], fill='#C9CBD4')               # 银锭
d.ellipse([50, 112, 66, 122], fill='#E4E6EE')
d.polygon([(120, 126), (136, 126), (132, 96), (124, 96)], fill=C('月白'))  # 瓷瓶
d.ellipse([122, 88, 134, 98], fill=C('月白'))
d.line([124, 104, 132, 118], fill=C('黛蓝'), width=2)        # 青花
d.rectangle([200, 104, 244, 126], fill=C('纸黄'), outline='#B8A67E')        # 字画卷
d.ellipse([244, 108, 250, 122], fill=C('朱砂'))

# 对话气泡
d.rounded_rectangle([196, 52, 292, 84], 6, fill=C('纸黄'), outline='#8A7A58')
d.polygon([(196, 72), (186, 78), (196, 82)], fill=C('纸黄'))
f_s = load_font(11)
d.text((203, 58), '这镯子，死当八十两。', fill='#4A3A20', font=f_s)

# UI 框架占位（当票面板 + 磨价按钮）
d.rectangle([8, 132, 108, 176], fill=C('纸黄'), outline='#8A7A58')
f_u = load_font(12)
d.text((14, 136), '当票·活当', fill='#7A2A20', font=f_u)
d.text((14, 152), '月息二分', fill='#4A3A20', font=f_u)
d.rectangle([226, 136, 312, 152], fill=C('黛绿'), outline='#1E3328')
d.text((240, 139), '磨价', fill=C('月白'), font=f_u)
d.rectangle([226, 156, 312, 172], fill=C('胭脂'), outline='#6E1B22')
d.text((240, 159), '死当', fill='#F0E6D0', font=f_u)

img.resize((W * S, H * S), Image.NEAREST).save(os.path.join(OUT, '高柜台构图mockup.png'))

# ---------- 3. 当品 icon 流水线样例（48x48 逻辑，3x 放大） ----------
ICON = 48
icons = Image.new('RGB', (ICON * 4 * 3 + 50, ICON * 3 + 20), '#23252B')
di = ImageDraw.Draw(icons)

def new_icon():
    ic = Image.new('RGB', (ICON, ICON), (35, 37, 43))
    return ic, ImageDraw.Draw(ic)

# 银锭
ic, i2 = new_icon()
i2.ellipse([6, 22, 42, 38], fill='#C9CBD4', outline='#8E9099')
i2.ellipse([14, 14, 34, 26], fill='#E4E6EE', outline='#8E9099')
i2.ellipse([20, 18, 28, 24], fill='#F6F7FA')
for px in range(8, 40, 5): i2.point((px, 34), fill='#9FA1AA')
icons.paste(ic.resize((ICON*3, ICON*3), Image.NEAREST), (10, 10))

# 青花小瓶
ic, i2 = new_icon()
i2.polygon([(16, 42), (32, 42), (29, 16), (19, 16)], fill=C('月白'), outline='#9FB4B8')
i2.rectangle([20, 10, 28, 16], fill=C('月白'), outline='#9FB4B8')
i2.line([21, 24, 27, 34], fill=C('黛蓝'), width=2)
i2.ellipse([22, 20, 26, 23], fill=C('黛蓝'))
icons.paste(ic.resize((ICON*3, ICON*3), Image.NEAREST), (ICON*3 + 20, 10))

# 字画卷
ic, i2 = new_icon()
i2.rectangle([8, 14, 40, 34], fill=C('纸黄'), outline='#B8A67E')
i2.rectangle([4, 12, 10, 36], fill=C('紫檀'))
i2.rectangle([38, 12, 44, 36], fill=C('紫檀'))
i2.line([14, 20, 34, 28], fill='#6B5B3F', width=2)
i2.ellipse([36, 30, 42, 35], fill=C('朱砂'))
icons.paste(ic.resize((ICON*3, ICON*3), Image.NEAREST), (ICON*6 + 30, 10))

# 玉镯
ic, i2 = new_icon()
i2.ellipse([8, 12, 40, 40], outline=C('黛绿'), width=5)
i2.ellipse([16, 20, 32, 33], outline='#3E6B55', width=3)
i2.point((38, 16), fill='#7FC0A0'); i2.point((10, 34), fill='#7FC0A0')
icons.paste(ic.resize((ICON*3, ICON*3), Image.NEAREST), (ICON*9 + 40, 10))

icons.save(os.path.join(OUT, '当品icon流水线样例.png'))
print('OK ->', OUT)
