# -*- coding: utf-8 -*-
"""《掌眼·当铺》当品 icon 流水线 v1
基于 pixel-art-studio 的 pixelstudio 库（skills/pixel-art-studio/scripts/pixelstudio.py）
产出：art/pawnshop-icons/ 下 40 个 48x48 透明 PNG + 缺陷演示 3 张 + 接触表 + spritesheet
"""
import sys, os, csv
sys.path.insert(0, r'C:\Users\Administrator\.zcode\skills\pixel-art-studio\scripts')
from pixelstudio import Sprite, ramp, mix

ROOT = r'C:\测试工作区\probably-stolen-study'
OUT = os.path.join(ROOT, 'pixel-art', 'pawnshop-icons')
os.makedirs(OUT, exist_ok=True)
S = 48

# ---- 色板（源自 art-demo/中国色板.png，12 色 + 扩展 ramp）----
BG_DARK = "#3D3B4F"   # 玄青（描边暗色备选）
PAPER = "#E8D7B0"     # 纸黄
GOLD = ramp("#FFB61E", 4, hue_shift=10)     # 藤黄系（戳记/金字）
SILVER = ramp("#B8BCC8", 5, hue_shift=-6)   # 银灰系
LEATHER = ramp("#8C5B3F", 5, hue_shift=6)   # 胡桃皮系
WOOD = ramp("#5C3A21", 4, hue_shift=4)      # 紫檀系
# 皮毛 ramp（按动物）
FUR = {
    'fox':    ramp("#C4622B", 5, hue_shift=8),
    'sable':  ramp("#6B4423", 5, hue_shift=4),
    'sheep':  ramp("#E8D7B0", 5, hue_shift=6),
    'wolf':   ramp("#8E9099", 5, hue_shift=-4),
    'tiger':  ramp("#D98E2B", 5, hue_shift=10),
    'deer':   ramp("#B08A5A", 5, hue_shift=6),
    'horse':  ramp("#7A5236", 5, hue_shift=4),
    'cow':    ramp("#E5E0D5", 5, hue_shift=4),
    'rabbit': ramp("#A9A29B", 5, hue_shift=0),
    'otter':  ramp("#55402F", 5, hue_shift=2),
}

def R(name):
    """颜色选择器：负索引从暗端取，正索引从亮端取"""
    return name

def draw_ingot(s, w=28, yuanbao=False):
    """银锭/元宝：马蹄形底+顶突；yuanbao 更规整+双戳记"""
    if yuanbao: w = 34
    x0 = (S - w) // 2; x1 = x0 + w
    base, mid, lite, hi = SILVER[0], SILVER[2], SILVER[3], SILVER[4]
    if not yuanbao:
        s.ellipse(x0, 26, x1, 40, base)                # 底座
        s.ellipse(x0 + 2, 24, x1 - 2, 34, mid, only="opaque")
        s.ellipse(x0 + w // 2 - 7, 16, x0 + w // 2 + 7, 28, base)   # 顶突
        s.ellipse(x0 + w // 2 - 5, 17, x0 + w // 2 + 5, 25, mid, only="opaque")
        s.ellipse(x0 + w // 2 - 3, 19, x0 + w // 2 + 3, 23, hi)     # 高光
        s.line(x0 + 4, 34, x1 - 6, 34, mid)             # 底面反光
        s.polygon([(x0 + 4, 28), (x0 + 9, 28), (x0 + 6, 32)], GOLD[2], fill=True)  # 戳记
    else:
        s.ellipse(x0, 26, x1, 42, base)                # 官铸元宝：更宽更扁
        s.ellipse(x0 + 2, 25, x1 - 2, 36, mid, only="opaque")
        s.ellipse(x0 + w // 2 - 9, 14, x0 + w // 2 + 9, 28, base)
        s.ellipse(x0 + w // 2 - 7, 15, x0 + w // 2 + 7, 26, mid, only="opaque")
        s.ellipse(x0 + w // 2 - 4, 17, x0 + w // 2 + 4, 22, hi)
        s.rect(x0 + 4, 37, x1 - 4, 39, GOLD[1])        # 底部金边戳带
        s.polygon([(x0 + 6, 30), (x0 + 11, 30), (x0 + 8, 34)], GOLD[2])
        s.polygon([(x1 - 11, 30), (x1 - 6, 30), (x1 - 8, 34)], GOLD[2])  # 双戳记

def draw_ring(s, small=False):
    """环形：镯/戒指"""
    r = 10 if small else 12
    cx = S // 2
    s.circle(cx, 24, r + 2, SILVER[0], fill=True)
    s.circle(cx, 24, r - 1, SILVER[2], fill=True)
    s.circle(cx, 24, r - 4, SILVER[4], fill=True)
    s.circle(cx, 24, r - 6, None, fill=True)            # 中空
    s.circle(cx - r // 2, 24 - r // 2, 3, SILVER[4])    # 高光点
    if small:
        s.ellipse(cx + 2, 28, cx + 12, 36, SILVER[2])   # 戒面镶嵌
        s.px(cx + 6, 31, SILVER[4])

def draw_pin(s):
    """银簪：斜杆+如意头"""
    s.line(14, 38, 34, 14, SILVER[2])
    s.line(13, 39, 33, 15, SILVER[0])
    s.line(15, 37, 35, 13, SILVER[3])
    s.circle(34, 14, 5, SILVER[2], fill=True)           # 头
    s.circle(34, 14, 3, SILVER[4], fill=True)
    s.px(34, 12, GOLD[2])

def draw_lock(s):
    """长命锁：圆盾+环+穗"""
    s.circle(24, 14, 5, SILVER[2], fill=True)
    s.circle(24, 14, 2, None, fill=True)
    s.ellipse(12, 20, 36, 42, SILVER[1])
    s.ellipse(13, 21, 35, 41, SILVER[3], only="opaque")
    s.ellipse(18, 26, 30, 36, SILVER[4])
    s.rect(22, 42, 26, 46, "#9D2933")                   # 红穗
    s.rect(23, 44, 25, 47, "#C3272B")

def draw_pot(s, spout=False, handle=False, lid=False, bowl=False):
    """壶/碗/炉/盏 家族；bowl=宽扁碗（无颈大口）"""
    base, mid, lite = SILVER[0], SILVER[2], SILVER[4]
    if bowl:
        s.ellipse(8, 22, 40, 40, base)                  # 宽扁碗
        s.ellipse(9, 23, 39, 38, mid, only="opaque")
        s.ellipse(11, 22, 37, 28, "#6A6E78")            # 碗口内沿
        s.ellipse(14, 23, 34, 27, lite)                 # 碗心高光
        s.rect(18, 38, 30, 43, base)                    # 矮足
        return
    s.ellipse(14, 20, 34, 40, base)
    s.ellipse(15, 21, 33, 38, mid, only="opaque")
    s.rect(19, 14, 29, 21, base)
    s.ellipse(18, 12, 30, 18, base)
    s.ellipse(20, 13, 28, 16, lite, only="opaque")
    if spout:
        s.polygon([(32, 22), (40, 16), (40, 22)], base)
    if handle:
        s.contour([(14, 20), (8, 16), (8, 26), (14, 30)], mid, close=False)
    if lid:
        s.ellipse(20, 10, 28, 14, GOLD[1])
    s.ellipse(18, 24, 24, 28, lite)                     # 高光

def draw_figure(s):
    """小银佛：抽象坐像"""
    s.circle(24, 12, 5, SILVER[3], fill=True)           # 头
    s.polygon([(16, 40), (32, 40), (28, 20), (20, 20)], SILVER[1])  # 身
    s.ellipse(18, 36, 30, 42, SILVER[0])                # 莲座
    s.ellipse(20, 24, 28, 30, SILVER[4], only="opaque") # 胸光
    s.px(24, 12, GOLD[2])                               # 顶珠

def draw_mirror(s):
    s.circle(24, 20, 13, SILVER[0], fill=True)
    s.circle(24, 20, 10, SILVER[3], fill=True)
    s.circle(21, 17, 3, SILVER[4])
    s.rect(22, 33, 26, 42, SILVER[1])
    s.rect(21, 41, 27, 44, GOLD[1])

def draw_pipe(s):
    s.line(12, 40, 34, 12, WOOD[1])
    s.line(11, 41, 33, 13, WOOD[0])
    s.line(13, 39, 35, 11, WOOD[2])
    s.rect(32, 8, 40, 16, SILVER[2])
    s.rect(33, 9, 39, 13, SILVER[4])
    s.rect(10, 38, 15, 43, SILVER[1])                   # 银烟嘴

def draw_knife(s):
    s.polygon([(34, 6), (40, 12), (22, 30), (18, 26)], SILVER[3])
    s.line(36, 10, 20, 27, SILVER[4])
    s.polygon([(18, 26), (22, 30), (16, 36), (12, 32)], "#4A3A30")  # 柄
    s.polygon([(20, 24), (26, 28), (22, 33), (16, 29)], GOLD[1])    # 护手斜置贴合


def draw_bell(s):
    s.contour([(24, 10), (24, 8)], SILVER[2], close=False)
    s.circle(24, 9, 3, SILVER[2], fill=True)
    s.circle(24, 9, 1, None, fill=True)
    s.polygon([(14, 34), (34, 34), (28, 14), (20, 14)], SILVER[1])
    s.ellipse(14, 32, 34, 38, SILVER[0])
    s.ellipse(16, 34, 32, 37, SILVER[2], only="opaque")
    s.line(18, 18, 18, 30, SILVER[3])
    s.px(24, 40, GOLD[2])

def draw_crown(s):
    s.polygon([(10, 30), (38, 30), (34, 16), (28, 22), (24, 14), (20, 22), (14, 16)], SILVER[1])
    s.line(10, 30, 38, 30, SILVER[3])
    s.px(24, 16, GOLD[2]); s.px(15, 18, GOLD[2]); s.px(33, 18, GOLD[2])
    s.rect(10, 30, 38, 33, SILVER[0])

def draw_chopsticks(s):
    s.line(16, 10, 20, 40, SILVER[2])
    s.line(28, 10, 32, 40, SILVER[2])
    s.line(16, 10, 20, 40, SILVER[0]); s.px(20, 40, SILVER[0])
    s.line(17, 10, 21, 40, SILVER[4])
    s.line(29, 10, 33, 40, SILVER[4])
    s.rect(14, 12, 22, 15, GOLD[1]); s.rect(26, 12, 34, 15, GOLD[1])  # 束头

def draw_earring(s):
    s.circle(18, 14, 4, SILVER[2], fill=True); s.circle(18, 14, 1, None, fill=True)
    s.line(18, 18, 18, 26, SILVER[2])
    s.ellipse(13, 26, 23, 38, SILVER[1])
    s.ellipse(15, 28, 21, 36, SILVER[4])
    # 第二只
    s.circle(32, 14, 4, SILVER[2], fill=True); s.circle(32, 14, 1, None, fill=True)
    s.line(32, 18, 32, 26, SILVER[2])
    s.ellipse(27, 26, 37, 38, SILVER[1])
    s.ellipse(29, 28, 35, 36, SILVER[4])

def draw_censer(s):
    """双耳宽扁香炉"""
    base, mid, lite = SILVER[0], SILVER[2], SILVER[4]
    s.ellipse(8, 20, 40, 38, base)                      # 宽炉身
    s.ellipse(9, 21, 39, 36, mid, only="opaque")
    s.ellipse(11, 21, 37, 27, "#6A6E78")                # 炉口
    s.ellipse(14, 22, 34, 26, lite)
    s.contour([(10, 20), (4, 12), (10, 10)], mid, close=False)   # 双立耳
    s.contour([(38, 20), (44, 12), (38, 10)], mid, close=False)
    s.rect(17, 38, 31, 44, base)                        # 三足底座
    for lx in (18, 30):
        s.line(lx, 42, lx, 46, SILVER[0])

def draw_crown(s):
    """中式束发冠：圆拱+发簪孔"""
    base, mid, lite = SILVER[0], SILVER[2], SILVER[4]
    s.ellipse(12, 12, 36, 38, base)                     # 圆拱主体
    s.ellipse(14, 14, 34, 36, mid, only="opaque")
    s.ellipse(17, 16, 31, 28, lite)                     # 顶光
    s.rect(22, 6, 26, 13, mid)                          # 冠顶簪座
    s.line(16, 9, 32, 9, GOLD[1])                       # 横簪
    s.px(32, 8, GOLD[2])
    s.line(14, 30, 34, 30, mid)                         # 束带线
    s.rect(20, 34, 28, 40, SILVER[1])                   # 冠足

# ---------- 皮毛家族 ----------
def draw_pelt(s, fur, spots=None, stripes=False, ears=True, tail=2, bundle=False, legs=4):
    """摊开的整张皮：头贴上边、四肢直伸呈放射状——读作皮张而非活物"""
    R = FUR[fur]
    dark, mid, lite, hi = R[0], R[1], R[3], R[4]
    s.ellipse(10, 16, 38, 34, dark)                     # 体（摊平）
    s.ellipse(12, 18, 36, 32, mid, only="opaque")
    s.ellipse(17, 8, 31, 18, dark)                      # 头贴上边摊平
    s.ellipse(19, 9, 29, 16, mid, only="opaque")
    if ears:
        s.polygon([(15, 9), (18, 3), (21, 10)], dark)   # 双耳向上摊
        s.polygon([(27, 10), (30, 3), (33, 9)], dark)
    if legs >= 4:                                       # 四腿放射直伸（皮张摊开感）
        s.line(12, 32, 6, 44, dark); s.line(20, 34, 17, 45, dark)
        s.line(28, 34, 31, 45, dark); s.line(36, 32, 42, 44, dark)
        s.line(13, 32, 7, 44, mid); s.line(19, 34, 17, 44, mid)
        s.line(29, 34, 31, 44, mid); s.line(35, 32, 41, 44, mid)
    elif legs == 2:
        s.line(16, 32, 12, 44, dark); s.line(32, 32, 36, 44, dark)
    if tail == 2:
        s.ellipse(2, 18, 10, 30, dark)                  # 蓬尾
        s.ellipse(4, 20, 8, 28, mid, only="opaque")
    elif tail == 1:
        s.line(2, 25, 10, 26, dark); s.line(2, 24, 10, 25, mid)
    s.noise(8, 16, 40, 34, lite, density=0.10, seed=3)  # 毛尖
    if spots:
        for (sx, sy) in spots:
            s.ellipse(sx, sy, sx + 3, sy + 2, hi)
    if stripes:                                         # 虎纹：深色横带更粗
        for i, sy in enumerate(range(15, 33, 4)):
            s.line(11 + (i % 2), sy, 37 - (i % 2), sy + 1, dark, only="opaque")
    s.outline(WOOD[0], where="inside")

def draw_garment(s, fur, kind='collar'):
    """领子/袄/手套/帽/围脖"""
    R = FUR[fur]
    dark, mid, lite = R[0], R[2], R[4]
    if kind == 'collar':
        s.polygon([(8, 30), (24, 18), (40, 30), (36, 38), (24, 28), (12, 38)], mid)  # 实心主体
        s.noise(10, 20, 38, 38, lite, density=0.12, seed=5)
        s.contour([(8, 30), (24, 18), (40, 30)], dark, close=False)  # 领口弧线
    elif kind == 'coat':
        s.polygon([(12, 12), (36, 12), (42, 42), (6, 42)], mid)
        s.line(24, 12, 24, 42, dark)
        s.rect(20, 20, 28, 24, GOLD[1])                 # 盘扣
        s.noise(8, 12, 40, 42, lite, density=0.08, seed=7)
    elif kind == 'gloves':
        for gx in (10, 27):
            s.rect(gx, 18, gx + 12, 34, mid)
            s.rect(gx + 3, 34, gx + 9, 42, dark)
            s.px(gx + 4, 22, lite)
    elif kind == 'hat':
        s.ellipse(10, 24, 38, 40, mid)
        s.ellipse(14, 12, 34, 28, dark)
        s.noise(14, 12, 34, 28, lite, density=0.10, seed=2)
        s.rect(22, 4, 26, 12, "#C3272B")                # 帽缨
    elif kind == 'stole':
        s.polygon([(4, 18), (44, 16), (44, 30), (4, 32)], mid)          # 加宽成带状
        s.ellipse(2, 14, 12, 34, dark)                                   # 两端垂坠
        s.ellipse(36, 14, 46, 34, dark)
        s.noise(4, 16, 44, 32, lite, density=0.14, seed=9)
    s.outline(WOOD[0], where="inside")

def draw_leather(s, kind='bracer'):
    """皮具：护腕/马鞍/行囊/水袋/护膝"""
    L = LEATHER
    dark, mid, lite = L[0], L[2], L[4]
    if kind == 'bracer':
        s.rect(12, 8, 36, 40, mid)
        s.rect(12, 8, 36, 12, lite)
        s.rect(16, 14, 20, 38, "#573519"); s.rect(28, 14, 32, 38, "#573519")  # 绑带
        s.rect(22, 18, 26, 22, GOLD[2])                 # 铜扣
    elif kind == 'saddle':
        s.ellipse(8, 22, 40, 36, dark)
        s.ellipse(12, 24, 36, 33, mid, only="opaque")
        s.polygon([(16, 12), (32, 12), (36, 24), (12, 24)], mid)  # 鞍桥
        s.ellipse(18, 10, 30, 16, lite)
        s.line(8, 34, 40, 34, "#573519")
        s.line(24, 24, 24, 42, "#573519")               # 肚带
    elif kind == 'pack':
        s.rect(10, 16, 38, 38, mid)
        s.rect(10, 16, 38, 20, lite)
        s.line(16, 16, 16, 38, dark); s.line(32, 16, 32, 38, dark)
        s.contour([(14, 16), (24, 6), (34, 16)], dark, close=False)  # 背带
        s.circle(24, 24, 3, GOLD[2])
    elif kind == 'waterskin':
        s.polygon([(20, 8), (28, 8), (34, 20), (30, 40), (18, 40), (14, 20)], mid)
        s.rect(21, 4, 27, 9, WOOD[1])                   # 木塞
        s.line(20, 16, 28, 24, lite)
        s.line(17, 26, 20, 34, dark)
    elif kind == 'pads':
        for kx in (8, 26):
            s.ellipse(kx, 14, kx + 14, 34, mid)
            s.ellipse(kx + 3, 17, kx + 11, 30, lite, only="opaque")
            s.line(kx + 2, 30, kx + 2, 40, dark); s.line(kx + 12, 30, kx + 12, 40, dark)
    s.outline(WOOD[0], where="inside")

def draw_hide_simple(s, fur, big=False):
    """简单整皮（羊/牛/马/鹿/狼/兔捆）"""
    R = FUR[fur]
    dark, mid, lite = R[0], R[1], R[3]
    s.polygon([(10, 14), (38, 14), (42, 34), (24, 40), (6, 34)], dark)
    s.polygon([(13, 16), (35, 16), (38, 32), (24, 37), (10, 32)], mid)
    s.ellipse(19, 8, 29, 16, dark)                      # 头端
    s.noise(10, 14, 38, 38, lite, density=0.10, seed=4)
    s.outline(WOOD[0], where="inside")

# ---------- 目录：identifier -> 绘制函数 ----------
BUILDERS = {
    'ingot_small':      lambda s: draw_ingot(s, w=18),
    'ingot_mid':        lambda s: draw_ingot(s, w=26),
    'ingot_large':      lambda s: draw_ingot(s, w=36),
    'yuanbao':          lambda s: draw_ingot(s, yuanbao=True),
    'bracelet_silver':  lambda s: draw_ring(s, small=False),
    'hairpin_silver':   draw_pin,
    'lock_silver':      draw_lock,
    'teapot_silver':    lambda s: draw_pot(s, spout=True, handle=True, lid=True),
    'cup_silver':       lambda s: draw_pot(s),
    'chopsticks_silver': draw_chopsticks,
    'buddha_silver':    draw_figure,
    'bell_silver':      draw_bell,
    'mirror_silver':    draw_mirror,
    'pipe_silver':      draw_pipe,
    'knife_silver':     draw_knife,
    'bowl_silver':      lambda s: draw_pot(s, bowl=True),
    'earring_silver':   draw_earring,
    'ring_silver':      lambda s: draw_ring(s, small=True),
    'censer_silver':    draw_censer,
    'crown_silver':     draw_crown,
    'fox_pelt':         lambda s: draw_pelt(s, 'fox', legs=4, tail=2),
    'sable_pelt':       lambda s: draw_pelt(s, 'sable', legs=4, tail=2),
    'sheep_pelt':       lambda s: draw_hide_simple(s, 'sheep'),
    'wolf_pelt':        lambda s: draw_pelt(s, 'wolf', legs=4, tail=1),
    'tiger_pelt':       lambda s: draw_pelt(s, 'tiger', legs=4, tail=1, stripes=True),
    'deer_pelt':        lambda s: draw_pelt(s, 'deer', legs=4, tail=1),
    'fox_collar':       lambda s: draw_garment(s, 'fox', 'collar'),
    'fur_coat':         lambda s: draw_garment(s, 'sable', 'coat'),
    'fur_gloves':       lambda s: draw_garment(s, 'sable', 'gloves'),
    'fur_hat':          lambda s: draw_garment(s, 'fox', 'hat'),
    'horse_hide':       lambda s: draw_hide_simple(s, 'horse'),
    'cow_hide':         lambda s: draw_hide_simple(s, 'cow'),
    'rabbit_bundle':    lambda s: draw_pelt(s, 'rabbit', legs=0, tail=1, ears=False, bundle=True),
    'otter_pelt':       lambda s: draw_pelt(s, 'otter', legs=2, tail=1),
    'sable_stole':      lambda s: draw_garment(s, 'sable', 'stole'),
    'bracer_leather':   lambda s: draw_leather(s, 'bracer'),
    'saddle_leather':   lambda s: draw_leather(s, 'saddle'),
    'pack_leather':     lambda s: draw_leather(s, 'pack'),
    'waterskin':        lambda s: draw_leather(s, 'waterskin'),
    'pads_leather':     lambda s: draw_leather(s, 'pads'),
}

# 缺陷 overlay（真/假双状态的“假”演示：虫蛀/灌铅/磨亮）
def flaw_moth(s):
    """虫蛀：边缘成簇孔洞"""
    for (hx, hy, r) in [(14, 20, 2), (30, 26, 2), (20, 32, 1), (36, 16, 1)]:
        s.circle(hx, hy, r, None, fill=True)
        s.circle(hx + r, hy + 1, 1, None, fill=True)

def flaw_lead(s):
    """灌铅：底部发暗的补块"""
    s.rect(16, 34, 32, 40, "#5A5E6A")
    s.noise(16, 34, 32, 40, "#45484F", density=0.2, seed=6)

def flaw_worn(s):
    """磨亮：中部位图发白"""
    s.ellipse(16, 18, 32, 28, SILVER[4], only="opaque")
    s.noise(16, 18, 32, 28, "#F6F7FA", density=0.15, seed=8)

FLAWS = {
    'fox_pelt': flaw_moth, 'sable_pelt': flaw_moth, 'tiger_pelt': flaw_moth,
    'sheep_pelt': flaw_moth,
    'ingot_mid': flaw_lead, 'yuanbao': flaw_lead, 'ingot_large': flaw_lead,
    'mirror_silver': flaw_worn, 'bracelet_silver': flaw_worn, 'bowl_silver': flaw_worn,
}

def main():
    made = []
    for ident, fn in BUILDERS.items():
        s = Sprite(S, S, palette=None)
        fn(s)
        s.outline(SILVER[0] if 'silver' in ident or ident.startswith(('ingot', 'yuanbao')) else WOOD[0], where="inside")
        # 缺陷演示
        if ident in FLAWS:
            f = Sprite(S, S, palette=None)
            fn(f)
            FLAWS[ident](f)
            f.outline("#1E1B16", where="inside")
            f.save_png(os.path.join(OUT, f'{ident}__flaw.png'), bg=None)
        s.save_png(os.path.join(OUT, f'{ident}.png'), bg=None)
        made.append(ident)
    print(f'{len(made)} icons -> {OUT}')

    # 接触表
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 16)
    cols = 8
    rows = (len(made) + cols - 1) // cols
    cell = 148  # icon 112 + 标签 20 + 余量（修复标签重叠/末行裁切）
    sheet = Image.new('RGB', (cols * cell, rows * cell + 10), (35, 37, 43))
    d = ImageDraw.Draw(sheet)
    for i, ident in enumerate(made):
        img = Image.open(os.path.join(OUT, f'{ident}.png')).convert('RGBA')
        x = (i % cols) * cell; y = (i // cols) * cell
        sheet.paste(img.resize((112, 112), Image.NEAREST), (x + 8, y + 6), img.resize((112, 112), Image.NEAREST))
        d.text((x + 8, y + 122), ident, fill=(200, 195, 175), font=font)
    flaw_names = [k for k in FLAWS if k in made]
    y0 = rows * cell
    for j, ident in enumerate(flaw_names[:4]):
        img = Image.open(os.path.join(OUT, f'{ident}__flaw.png')).convert('RGBA')
        x = (j % cols) * cell
        sheet.paste(img.resize((112, 112), Image.NEAREST), (x + 8, y0 + 6), img.resize((112, 112), Image.NEAREST))
        d.text((x + 8, y0 + 122), ident + ' 缺陷', fill=(200, 120, 100), font=font)
    sheet.save(os.path.join(OUT, 'contact_sheet.png'))
    print('contact_sheet.png OK')

    # ---- spritesheet 图集 + Unity 切片 JSON ----
    import json as _json
    atlas_cols = 8
    pad = 2
    tw = atlas_cols * (S + pad) + pad
    rows_all = (len(made) + atlas_cols - 1) // atlas_cols
    th = rows_all * (S + pad) + pad
    atlas = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    frames_json = []
    for i, ident in enumerate(made):
        img = Image.open(os.path.join(OUT, f'{ident}.png')).convert('RGBA')
        gx = pad + (i % atlas_cols) * (S + pad)
        gy = pad + (i // atlas_cols) * (S + pad)
        atlas.paste(img, (gx, gy))
        frames_json.append({'name': ident, 'x': gx, 'y': gy, 'w': S, 'h': S})
    atlas.save(os.path.join(OUT, 'pawnshop-icons-atlas.png'))
    meta = {'meta': {'app': 'pawnshop icon pipeline', 'image': 'pawnshop-icons-atlas.png',
                     'size': {'w': tw, 'h': th}, 'scale': '1',
                     'unity_grid': {'cellSize': S + pad, 'offset': pad, 'padding': pad}},
            'frames': frames_json}
    with open(os.path.join(OUT, 'pawnshop-icons-atlas.json'), 'w', encoding='utf-8') as fp:
        _json.dump(meta, fp, ensure_ascii=False, indent=1)
    print(f'atlas {tw}x{th} + json OK')

if __name__ == '__main__':
    main()
