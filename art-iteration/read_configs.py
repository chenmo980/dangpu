# -*- coding: utf-8 -*-
import json, os
CFG = r'C:\测试工作区\probably-stolen-study\asset\configs'
for f in ('scene_layout_flat.json', 'grid_layout_spec.json', 'factions_manifest.json', 'hd_20_manifest.json'):
    p = os.path.join(CFG, f)
    print('===', f, '===')
    d = json.load(open(p, encoding='utf-8'))
    print(json.dumps(d, ensure_ascii=False, indent=1)[:850])
    print()
