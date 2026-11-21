# 构建 纹理名 -> {file, path_id} 映射（从 res-textures.jsonl，含三个资产文件的记录）
import json, os
textures = {}
for line in open(r'C:\测试工作区\probably-stolen-study\art-iteration\res-textures.jsonl', encoding='utf-8'):
    try:
        d = json.loads(line)
    except Exception:
        continue
    fname = d.get('subject', {}).get('name', '')
    for o in d.get('result', {}).get('objects', []):
        if o['class'] == 'Texture2D' and o.get('name') and o['name'] not in textures:
            textures[o['name']] = {'file': fname, 'path_id': o['path_id']}
print('全部纹理:', len(textures))
rows = list(__import__('csv').DictReader(open(r'C:\测试工作区\probably-stolen-study\art-iteration\original-item-db.csv', encoding='utf-8')))
need_tex = set(r['atlas'].split('/')[-1] for r in rows if r['sprite'])
have = {t: textures[t] for t in need_tex if t in textures}
print('需要纹理:', len(need_tex), '| 可用:', len(have), '| 缺:', sorted(need_tex - set(textures))[:8])
json.dump(have, open(r'C:\测试工作区\probably-stolen-study\art-iteration\needed-textures.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('needed-textures.json 已保存')
