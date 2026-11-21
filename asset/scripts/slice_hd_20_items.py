#!/usr/bin/env python3
"""
将 2 张 AI 精品像素精灵总表（2x5 × 2 = 20 件）先整图 BFS 抠图 -> 连通域聚类精准分离每件物品（彻底杜绝邻格窜入），
并将斜置长条物自动旋正铺满 3x1 / 2x1 格子，导出高清版 (W*64)x(H*64) 与原生版 (W*32)x(H*32)！
"""
from collections import deque
import json
from pathlib import Path
import zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/working_dir/c_9dc48f286509629e")
GEN_DIR = ROOT / "user_uploaded_files/ttl=63d/tool_generated"
GRID_STAGE = ROOT / "artifacts/file_generation/ttl=63d/intermediate/grid_140_pack"
STARTER = ROOT / "artifacts/file_generation/ttl=63d/intermediate/starter_pack"
STAGE = ROOT / "artifacts/file_generation/ttl=63d/intermediate/hd20_sliced"
OUT_DIR = ROOT / "artifacts/file_generation/ttl=63d/output"

(STAGE / "hd_64px_per_cell").mkdir(parents=True, exist_ok=True)
(STAGE / "native_32px_per_cell").mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

SHEET1 = GEN_DIR / "watermarked_img_8163125785109633194.jpg"
SHEET2 = GEN_DIR / "watermarked_img_17613088054422660440.jpg"

# (sheet_idx, row, col, id, name, gw, gh, rot_deg)
ITEMS_20 = [
    (1, 0, 0, "weapon_yanling_dao", "雁翎腰刀", 3, 1, -40),
    (1, 0, 1, "weapon_iron_flute", "铁笛暗器", 2, 1, -42),
    (1, 0, 2, "weapon_bronze_dagger", "青铜短匕", 2, 1, -42),
    (1, 0, 3, "weapon_flintlock", "洋造燧发枪", 2, 1, -28),
    (1, 0, 4, "weapon_revolver", "洋行转轮枪", 2, 1, -28),
    (1, 1, 0, "weapon_flying_knife", "柳叶飞刀", 1, 2, 0),
    (1, 1, 1, "weapon_brass_knuckle", "铁莲花指虎", 1, 1, 0),
    (1, 1, 2, "weapon_iron_whip", "九节铁鞭", 2, 2, 0),
    (1, 1, 3, "weapon_crossbow_mini", "袖箭机弩", 2, 2, 0),
    (1, 1, 4, "weapon_military_token", "官造兵符", 1, 1, 0),
    (2, 0, 0, "contra_opium_pipe", "象牙烟枪", 3, 1, -42),
    (2, 0, 1, "contra_opium_lamp", "玻璃烟灯", 1, 2, 0),
    (2, 0, 2, "contra_opium_paste", "土膏烟盒", 1, 1, 0),
    (2, 0, 3, "contra_salt_bag", "私盐麻袋", 2, 2, 0),
    (2, 0, 4, "contra_fake_banknote", "假官银票", 2, 1, 0),
    (2, 1, 0, "contra_fake_seal", "私刻官印", 1, 1, 0),
    (2, 1, 1, "contra_tomb_figurine", "盗墓彩陶俑", 1, 2, 0),
    (2, 1, 2, "contra_coin_sword", "镇煞古钱剑", 2, 1, -42),
    (2, 1, 3, "contra_cinnabar_bottle", "黑市鹤顶红", 1, 1, 0),
    (2, 1, 4, "contra_gunpowder_jar", "走私火药坛", 2, 2, 0),
]


def flood_remove_sheet_bg(sheet_img: Image.Image, tol: float = 24.0) -> Image.Image:
    rgba = sheet_img.convert("RGBA")
    arr = np.asarray(rgba, dtype=np.uint8).copy()
    h, w, _ = arr.shape
    rgb = arr[..., :3].astype(np.float32)

    border = np.concatenate([rgb[0, :], rgb[-1, :], rgb[:, 0], rgb[:, -1]], axis=0)
    bg = np.median(border, axis=0)
    dist = np.linalg.norm(rgb - bg, axis=-1)
    is_bg = dist <= tol

    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        if is_bg[0, x]:
            visited[0, x] = True; q.append((0, x))
        if is_bg[h - 1, x]:
            visited[h - 1, x] = True; q.append((h - 1, x))
    for y in range(h):
        if is_bg[y, 0] and not visited[y, 0]:
            visited[y, 0] = True; q.append((y, 0))
        if is_bg[y, w - 1] and not visited[y, w - 1]:
            visited[y, w - 1] = True; q.append((y, w - 1))

    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and is_bg[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

    arr[visited, 3] = 0
    alpha = arr[..., 3]
    trans = alpha == 0
    pad = np.pad(trans, 1, mode="constant", constant_values=True)
    near = pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:]
    fringe = near & (~trans) & (dist <= tol + 16.0)
    arr[fringe, 3] = 0
    return Image.fromarray(arr, mode="RGBA")


def extract_10_objects(sheet_rgba: Image.Image) -> dict[tuple[int, int], Image.Image]:
    """用连通域将整张 2x5 总表精准拆分成 10 个独立物品，彻底杜绝相邻物品边角窜入！"""
    arr = np.asarray(sheet_rgba, dtype=np.uint8)
    h, w, _ = arr.shape
    solid = arr[..., 3] > 0
    labels = np.zeros((h, w), dtype=np.int32)
    comps = []  # (label_id, count, cx, cy, x0, y0, x1, y1)

    cur_lbl = 0
    for y in range(h):
        for x in range(w):
            if solid[y, x] and labels[y, x] == 0:
                cur_lbl += 1
                q = deque([(y, x)])
                labels[y, x] = cur_lbl
                cnt = 0
                sx = sy = 0
                x0 = x1 = x
                y0 = y1 = y
                while q:
                    cy, cx = q.popleft()
                    cnt += 1
                    sx += cx; sy += cy
                    if cx < x0: x0 = cx
                    if cx > x1: x1 = cx
                    if cy < y0: y0 = cy
                    if cy > y1: y1 = cy
                    for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                        if 0 <= ny < h and 0 <= nx < w and solid[ny, nx] and labels[ny, nx] == 0:
                            labels[ny, nx] = cur_lbl
                            q.append((ny, nx))
                if cnt >= 15:
                    comps.append((cur_lbl, cnt, sx / cnt, sy / cnt, x0, y0, x1, y1))

    # 按面积取最大的 10 个主物体，再按 (行, 列) 排序映射到 (row, col)
    comps.sort(key=lambda c: c[1], reverse=True)
    main10 = comps[:10]
    # 分上下两行（按 cy < h/2）
    top5 = sorted([c for c in main10 if c[3] < h / 2], key=lambda c: c[2])
    bot5 = sorted([c for c in main10 if c[3] >= h / 2], key=lambda c: c[2])

    # 把小碎片（如撒出来的盐粒）归属给最近的 main10 物体（距离 < 90px）
    small_comps = [c for c in comps[10:] if c[1] < 600]
    result = {}
    for r_i, row_list in enumerate([top5, bot5]):
        for c_i, mc in enumerate(row_list):
            lbl_set = {mc[0]}
            x0, y0, x1, y1 = mc[4], mc[5], mc[6], mc[7]
            for sc in small_comps:
                # 仅合并距离主物体边界很近的小碎片（例如麻袋旁边的白色盐粒）
                dx = max(0, x0 - sc[2], sc[2] - x1)
                dy = max(0, y0 - sc[3], sc[3] - y1)
                if dx * dx + dy * dy <= 35 * 35:
                    lbl_set.add(sc[0])
                    x0 = min(x0, sc[4]); y0 = min(y0, sc[5])
                    x1 = max(x1, sc[6]); y1 = max(y1, sc[7])
            sub_arr = arr[y0:y1 + 1, x0:x1 + 1].copy()
            sub_lbl = labels[y0:y1 + 1, x0:x1 + 1]
            mask = np.isin(sub_lbl, list(lbl_set))
            sub_arr[~mask, 3] = 0
            result[(r_i, c_i)] = Image.fromarray(sub_arr, mode="RGBA")
    return result


def fit_multicell(cut_rgba: Image.Image, gw: int, gh: int, cell_px: int, rot_deg: float = 0) -> Image.Image:
    im = cut_rgba
    if rot_deg != 0:
        im = im.rotate(rot_deg, resample=Image.Resampling.BICUBIC, expand=True)
    bbox = im.getbbox()
    tw, th = gw * cell_px, gh * cell_px
    if not bbox:
        return Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    crop = im.crop(bbox)
    cw, ch = crop.size
    pad = max(2, int(cell_px * 0.06))
    scale = min((tw - pad * 2) / cw, (th - pad * 2) / ch)
    nw, nh = max(1, int(round(cw * scale))), max(1, int(round(ch * scale)))
    resized = crop.resize((nw, nh), Image.Resampling.LANCZOS if cell_px >= 64 else Image.Resampling.BOX)
    canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    canvas.paste(resized, ((tw - nw) // 2, (th - nh) // 2), resized)
    return canvas


def load_cjk_font(size: int):
    for p in [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main():
    s1_cut = flood_remove_sheet_bg(Image.open(SHEET1), tol=24.0)
    s2_cut = flood_remove_sheet_bg(Image.open(SHEET2), tol=24.0)
    objs = {1: extract_10_objects(s1_cut), 2: extract_10_objects(s2_cut)}

    sliced_hd = {}
    manifest = []
    for s_idx, r_i, c_i, iid, name, gw, gh, rot in ITEMS_20:
        raw_obj = objs[s_idx][(r_i, c_i)]
        hd_im = fit_multicell(raw_obj, gw, gh, cell_px=64, rot_deg=rot)
        nat_im = fit_multicell(raw_obj, gw, gh, cell_px=32, rot_deg=rot)
        hd_im.save(STAGE / "hd_64px_per_cell" / f"{iid}.png", optimize=True)
        nat_im.save(STAGE / "native_32px_per_cell" / f"{iid}.png", optimize=True)
        sliced_hd[iid] = (hd_im, gw, gh, name)
        manifest.append({
            "id": iid, "name": name, "shape": f"{gw}x{gh}",
            "hd_file": f"hd_64px_per_cell/{iid}.png",
            "native_file": f"native_32px_per_cell/{iid}.png",
        })

    (STAGE / "hd_20_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 合成高清实机验收图
    bg_day = Image.open(GRID_STAGE / "scene_hd_flat/bg_alley_hd_day.png").convert("RGBA")
    fg_day = Image.open(GRID_STAGE / "scene_hd_flat/fg_interior_hd_day.png").convert("RGBA")
    npc_yamen = Image.open(STARTER / "npc_yamen_256.png").convert("RGBA").resize((276, 276), Image.Resampling.NEAREST)

    comp = bg_day.copy()
    comp.paste(npc_yamen, ((505 + 881) // 2 - 138, 410 - 266), npc_yamen)
    comp.alpha_composite(fg_day)

    d = ImageDraw.Draw(comp)
    d.text((112, 86), "初五 · 距交租 3 日", fill=(232, 215, 176, 255), font=load_cjk_font(24))

    GRID_C = 34
    DESK_X0, DESK_Y0 = 32, 444
    STOR_X0, STOR_Y0 = 446, 582

    ov = Image.new("RGBA", comp.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for r_i in range(3):
        for c_i in range(28):
            rx, ry = DESK_X0 + c_i * GRID_C, DESK_Y0 + r_i * GRID_C
            od.rectangle([rx, ry, rx + GRID_C - 2, ry + GRID_C - 2], fill=(20, 16, 24, 34), outline=(232, 215, 176, 50), width=1)
    for r_i in range(5):
        for c_i in range(14):
            rx, ry = STOR_X0 + c_i * GRID_C, STOR_Y0 + r_i * GRID_C
            od.rectangle([rx, ry, rx + GRID_C - 2, ry + GRID_C - 2], fill=(18, 16, 26, 155), outline=(112, 86, 68, 180), width=1)
    comp.alpha_composite(ov)

    def place_hd(iid: str, gx0: int, gy0: int, col: int, row: int):
        im, gw, gh, _ = sliced_hd[iid]
        tw, th = gw * GRID_C - 2, gh * GRID_C - 2
        sc = im.resize((tw, th), Image.Resampling.LANCZOS)
        comp.paste(sc, (gx0 + col * GRID_C, gy0 + row * GRID_C), sc)

    for iid, c_i, r_i in [
        ("weapon_yanling_dao", 1, 1),
        ("weapon_flintlock", 5, 1),
        ("weapon_revolver", 8, 1),
        ("contra_salt_bag", 11, 0),
        ("contra_opium_pipe", 14, 1),
        ("contra_opium_lamp", 18, 0),
        ("contra_fake_banknote", 20, 1),
        ("contra_fake_seal", 23, 1),
        ("weapon_bronze_dagger", 25, 1),
        ("contra_cinnabar_bottle", 26, 2),
    ]:
        place_hd(iid, DESK_X0, DESK_Y0, c_i, r_i)

    for iid, c_i, r_i in [
        ("weapon_iron_whip", 0, 0),
        ("weapon_crossbow_mini", 2, 0),
        ("contra_gunpowder_jar", 4, 0),
        ("contra_salt_bag", 6, 0),
        ("weapon_yanling_dao", 8, 0),
        ("contra_coin_sword", 11, 0),
        ("weapon_military_token", 13, 0),
        ("weapon_flying_knife", 0, 2),
        ("contra_tomb_figurine", 1, 2),
        ("contra_opium_lamp", 2, 2),
        ("weapon_iron_flute", 3, 2),
        ("weapon_flintlock", 5, 2),
        ("weapon_revolver", 7, 2),
        ("contra_fake_banknote", 9, 2),
        ("contra_opium_pipe", 11, 2),
        ("weapon_brass_knuckle", 3, 3),
        ("contra_opium_paste", 4, 3),
        ("contra_fake_seal", 5, 3),
        ("contra_cinnabar_bottle", 6, 3),
        ("weapon_bronze_dagger", 7, 3),
    ]:
        place_hd(iid, STOR_X0, STOR_Y0, c_i, r_i)

    total = Image.new("RGBA", (1376, 1200), (18, 20, 26, 255))
    total.paste(comp, (0, 0))
    td = ImageDraw.Draw(total)
    fh = load_cjk_font(22)
    fs = load_cjk_font(14)

    td.line([(0, 768), (1376, 768)], fill=(140, 91, 63, 255), width=3)
    td.text((28, 782), "AI 精灵总表连通域精切方案（2 次生图 = 20 件商业级高清像素道具 · 旋正铺满多格 · 零串边）", fill=(255, 182, 30, 255), font=fh)

    for idx, (_, _, _, iid, name, gw, gh, _) in enumerate(ITEMS_20):
        r_i, c_i = divmod(idx, 10)
        x0 = 28 + c_i * 133
        y0 = 824 + r_i * 182
        td.rectangle([x0, y0, x0 + 122, y0 + 144], fill=(41, 34, 52, 255), outline=(140, 91, 63, 255), width=1)
        im, _, _, _ = sliced_hd[iid]
        sc = min(114 / im.width, 134 / im.height)
        nw, nh = max(1, int(im.width * sc)), max(1, int(im.height * sc))
        disp = im.resize((nw, nh), Image.Resampling.LANCZOS)
        total.paste(disp, (x0 + (122 - nw) // 2, y0 + (144 - nh) // 2), disp)
        td.text((x0 + 4, y0 + 150), f"{name} {gw}×{gh}", fill=(232, 215, 176, 255), font=fs)

    preview_path = OUT_DIR / "zhangyan_hd_items_ingame_preview.png"
    total.convert("RGB").save(preview_path, optimize=True)

    zip_path = OUT_DIR / "zhangyan_hd20_items_pack.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(STAGE.rglob("*")):
            if p.is_file():
                zf.write(p, arcname=str(p.relative_to(STAGE)))
        zf.write(preview_path, arcname="zhangyan_hd_items_ingame_preview.png")

    print("DONE:", preview_path)


if __name__ == "__main__":
    main()
