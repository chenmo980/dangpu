# 导出所需 Texture2D 纹理 → 按 sprite rect 切片 → 生成 items-original.json
import json, os, subprocess, csv
from PIL import Image

CLI = r'C:\Users\Administrator\.zcode\tools\craft-anything-0.6.1\craft-anything-0.6.1-windows-x64-portable\craft-anything-cli.exe'
GMD = r'C:\测试工作区\Probably-Stolen-Cyberpunk-Shopkeeper\Probably Stolen\Probably Stolen_Data'
ART = r'C:\测试工作区\probably-stolen-study\art-iteration'
TEXDEST = r'C:\测试工作区\probably-stolen-study\prototype\assets-original\textures'
ICONDEST = r'C:\测试工作区\probably-stolen-study\prototype\assets-original\items'
os.makedirs(TEXDEST, exist_ok=True)
os.makedirs(ICONDEST, exist_ok=True)

needed = json.load(open(os.path.join(ART, 'needed-textures.json'), encoding='utf-8'))
rects = json.load(open(os.path.join(ART, 'sprite-rects.json'), encoding='utf-8'))
rows = list(csv.DictReader(open(r'C:\测试工作区\pawnshop-m0\Pawnshop.M0\item_catalog.csv', encoding='utf-8')))  # 占位
db = list(csv.DictReader(open(os.path.join(ART, 'original-item-db.csv'), encoding='utf-8')))

# 简单标识符→中文词翻译（占位名用，覆盖常见词）
WORDS = {
 'bottled':'瓶装','water':'水','premium':'高级','small':'小','mini':'迷你','large':'大','empty':'空',
 'beer':'啤酒','bottle':'瓶','bottles':'瓶','juice':'果汁','meat':'肉','raw':'生','fat':'肥','morsel':'碎肉',
 'cheese':'奶酪','noodle':'面','cup':'杯','soda':'汽水','energy':'能量','drink':'饮料','icecream':'冰淇淋',
 'milk':'奶','processed':'加工','hot':'辣','sauce':'酱','red':'红','blue':'蓝','violet':'紫','orange':'橙',
 'pink':'粉','dropper':'滴管','cylinder':'量筒','ml':'毫升','ration':'配给','jug':'壶','snack':'零食',
 'bar':'条','blend':'混合','cat':'猫','eat':'食','fresh':'鲜','old':'陈','rusty':'锈','broken':'破',
 'damaged':'损','stolen':'赃','fake':'假','genuine':'真','gold':'金','silver':'银','steel':'钢','iron':'铁',
 'wooden':'木','plastic':'塑','battery':'电池','module':'模块','scanner':'扫描仪','tool':'工具','pistol':'手枪',
 'rifle':'步枪','shotgun':'霰弹','smg':'冲锋枪','sniper':'狙','knife':'刀','sword':'剑','bat':'棒',
 'armor':'甲','helmet':'盔','boots':'靴','gloves':'手套','hat':'帽','vest':'背心','plate':'板',
 'med':'药','meds':'药','health':'医疗','heal':'治疗','stim':'针剂','syringe':'注射器','pill':'药丸',
 'pills':'药丸','capsule':'胶囊','antibiotic':'抗生素','painkiller':'止痛','bandage':'绷带','salve':'药膏',
 'seed':'种子','seeds':'种子','plant':'植物','fertilizer':'肥','soil':'土','pot':'盆','lamp':'灯',
 'furniture':'家具','chair':'椅','table':'桌','bed':'床','rug':'毯','lampshade':'灯罩','poster':'海报',
 'painting':'画','frame':'框','camera':'相机','phone':'手机','laptop':'笔电','tv':'电视','radio':'收音机',
 'cassette':'卡带','tape':'磁带','disk':'碟','chip':'芯片','circuit':'电路','wire':'线','cable':'缆',
 'pipe':'管','valve':'阀','pump':'泵','engine':'引擎','motor':'马达','gear':'齿轮','spring':'弹簧',
 'nut':'螺母','bolt':'螺栓','screw':'螺丝','wrench':'扳手','hammer':'锤','saw':'锯','drill':'钻',
 'perfume':'香水','soap':'皂','towel':'巾','brush':'刷','comb':'梳','mirror':'镜','comb2':'梳',
 'towel2':'巾','candle':'烛','lamp2':'灯','vase':'花瓶','clock':'钟','watch':'表','ring':'戒',
 'necklace':'链','earring':'耳环','bracelet':'镯','coin':'币','gem':'宝','jewel':'宝','pearl':'珠',
 'powerblock':'动力块','postit':'便签','aug':'义体','sec':'安全','dis':'残','ext':'扩','100':'100',
 'beer_case':'箱装啤酒','pet':'宠','food2':'食','decoration':'装饰','ammo':'弹药','ammo_box':'弹药箱',
 'explosive':'爆炸','grenade':'雷','mine':'雷','c4':'C4','paper':'纸','towel3':'巾','mug':'杯',
 'glass':'玻璃','bottlecap':'瓶盖','can':'罐','jar':'罐','box':'箱','crate':'箱','bag':'袋',
 'sack':'袋','bundle':'捆','stack':'叠','pile':'堆','xeno':'异形','imp':'魔','lucky':'幸运',
 'nudka':'伏特加','vodka':'伏特加','galaxy':'星','li':'李','beis':'贝氏','nudka2':'酒',
}
def zh_name(ident):
    words = ident.replace('-', '_').split('_')
    out = []
    for w in words:
        if w.isdigit(): out.append(w); continue
        out.append(WORDS.get(w.lower(), w))
    name = ''.join(out)
    return name if name else ident

# 1) 导出纹理
ok_t = fail_t = 0
for tex, info in needed.items():
    out = os.path.join(TEXDEST, tex + '.png')
    if os.path.exists(out): ok_t += 1; continue
    srcfile = os.path.join(GMD, info['file'])
    r = subprocess.run([CLI, 'game-unity-asset-export', '--path', srcfile, '--path-id', str(info['path_id']),
                        '--deep', '--output', out], capture_output=True)
    if os.path.exists(out): ok_t += 1
    else: fail_t += 1; print('纹理导出失败:', tex, r.stdout[-200:] if r.stdout else '', r.stderr[-200:] if r.stderr else '')
print(f'纹理导出: ok={ok_t} fail={fail_t}')

# 2) 按 rect 切片
sliced = 0
for tex, info in needed.items():
    tex_path = os.path.join(TEXDEST, tex + '.png')
    if not os.path.exists(tex_path): continue
    img = Image.open(tex_path).convert('RGBA')
    W, H = img.size
    # 该纹理下的所有 sprite rect
    for ident, sp, atlas in [(r['identifier'], r['sprite'], r['atlas'].split('/')[-1]) for r in db]:
        if atlas != tex or sp not in rects: continue
        rect = rects[sp]['rect']
        x, y, w, h = rect
        if w <= 0 or h <= 0 or x + w > W or y + h > H: continue
        y_pil = H - y - h                      # Unity 底左 → PIL 顶左
        crop = img.crop((int(x), int(y_pil), int(x + w), int(y_pil + h)))
        crop.save(os.path.join(ICONDEST, sp + '.png'))
        sliced += 1
print('切片 sprite:', sliced)

# 3) 生成 items-original.json（原作目录 400 件：数值+标签+icon 路径+占位中文名）
out_items = []
for r in db:
    ident = r['identifier']
    has_icon = os.path.exists(os.path.join(ICONDEST, r['sprite'] + '.png'))
    out_items.append({
        'id': 'O_' + ident,
        'name': zh_name(ident),
        'orig_name': ident,
        'cat': r['category'],
        'value': int(r['unitValue']) if r['unitValue'] else 10,
        'tags': r['tags'].split(';') if r['tags'] else [],
        'icon': ('assets-original/items/' + r['sprite'] + '.png') if has_icon else '',
    })
json.dump(out_items, open(r'C:\测试工作区\probably-stolen-study\prototype\items-original.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with_icon = sum(1 for i in out_items if i['icon'])
print(f'items-original.json: {len(out_items)} 件, 带图标 {with_icon} 件')
