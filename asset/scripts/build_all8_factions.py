#!/usr/bin/env python3
"""
《掌眼·当铺》全部 8 派系半身像素立绘统一抠图、头像裁切与打包脚本
导出内容：
- 每个派系：128x128 像素立绘、256x256 清晰立绘、64x64 头像（供左墙海捕文书/对话头像使用）
- factions_manifest.json：与《中国当铺版-设计文档.md》8 派系 ID 一一对应
- zhangyan_all8_factions_preview.png：2x4 全部 8 派系透明抠图合集验收图
"""
from collections import deque
import json
from pathlib import Path
import zipfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/working_dir/c_9dc48f286509629e")
GEN_DIR = ROOT / "user_uploaded_files/ttl=63d/tool_generated"
STAGE = ROOT / "artifacts/file_generation/ttl=63d/intermediate/all8_factions"
OUT_DIR = ROOT / "artifacts/file_generation/ttl=63d/output"

STAGE.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

FACTIONS = [
    ("npc_commoner", "街坊小民", "急当低值品", "watermarked_img_17306153687987630553.jpg"),
    ("npc_prodigal", "败家子弟", "高价货急当", "watermarked_img_5370205236790001657.jpg"),
    ("npc_outlaw", "绿林朋友", "夜间销赃", "watermarked_img_9588993088196237890.jpg"),
    ("npc_yamen", "官面衙门", "查抄/收例银", "watermarked_img_2671064218443293212.jpg"),
    ("npc_connoisseur", "古玩行家", "收死当/识赝品", "watermarked_img_9683270925251693547.jpg"),
    ("npc_comprador", "洋行买办", "钟表银器大宗", "watermarked_img_9592456694362098966.jpg"),
    ("npc_rival", "当行同行", "抬杠压价/联号", "watermarked_img_14703164933283071938.jpg"),
    ("npc_lady", "内眷女眷", "闺阁首饰私当", "watermarked_img_8053983606077028095.jpg"),
]


def flood_remove_bg(img: Image.Image, tol: float = 28.0) -> Image.Image:
    rgba = img.convert("RGBA")
    arr = np.asarray(rgba, dtype=np.uint8).copy()
    h, w, _ = arr.shape
    rgb = arr[..., :3].astype(np.float32)

    corners = np.concatenate([
        rgb[:12, :12].reshape(-1, 3),
        rgb[:12, -12:].reshape(-1, 3),
        rgb[-12:, :12].reshape(-1, 3),
        rgb[-12:, -12:].reshape(-1, 3),
    ], axis=0)
    bg = np.median(corners, axis=0)
    dist = np.linalg.norm(rgb - bg, axis=-1)
    is_bg_cand = dist <= tol

    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        if is_bg_cand[0, x]:
            visited[0, x] = True
            q.append((0, x))
        if is_bg_cand[h - 1, x]:
            visited[h - 1, x] = True
            q.append((h - 1, x))
    for y in range(h):
        if is_bg_cand[y, 0] and not visited[y, 0]:
            visited[y, 0] = True
            q.append((y, 0))
        if is_bg_cand[y, w - 1] and not visited[y, w - 1]:
            visited[y, w - 1] = True
            q.append((y, w - 1))

    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and is_bg_cand[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

    arr[visited, 3] = 0
    alpha = arr[..., 3]
    transparent = alpha == 0
    padded = np.pad(transparent, 1, mode="constant", constant_values=True)
    near_trans = padded[:-2, 1:-1] | padded[2:, 1:-1] | padded[1:-1, :-2] | padded[1:-1, 2:]
    fringe = near_trans & (~transparent) & (dist <= tol + 18.0)
    arr[fringe, 3] = 0
    return Image.fromarray(arr, mode="RGBA")


def crop_and_align(rgba: Image.Image, target_size: int) -> Image.Image:
    bbox = rgba.getbbox()
    if not bbox:
        return Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
    cropped = rgba.crop(bbox)
    cw, ch = cropped.size
    scale = min((target_size * 0.90) / cw, (target_size * 0.94) / ch)
    nw, nh = max(1, int(round(cw * scale))), max(1, int(round(ch * scale)))
    resized = cropped.resize((nw, nh), Image.Resampling.BOX)
    canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
    canvas.paste(resized, ((target_size - nw) // 2, target_size - nh), resized)
    return canvas


def make_headshot(rgba_256: Image.Image) -> Image.Image:
    """从 256x256 立绘上方裁切 64x64 头像，用于海捕文书和对话卡片。"""
    head_box = rgba_256.crop((48, 8, 208, 168))
    return head_box.resize((64, 64), Image.Resampling.BOX)


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
    manifest = []
    # 2x4 展示画布：1280 x 760
    sheet = Image.new("RGBA", (1280, 780), (20, 22, 28, 255))
    draw = ImageDraw.Draw(sheet)
    font_h = load_cjk_font(26)
    font_name = load_cjk_font(20)
    font_role = load_cjk_font(15)

    draw.text((36, 20), "《掌眼·当铺》全部 8 派系晚清像素半身立绘（透明 PNG 验收总览）", fill=(255, 182, 30, 255), font=font_h)

    for idx, (fid, cname, role, fname) in enumerate(FACTIONS):
        raw = Image.open(GEN_DIR / fname)
        cut = flood_remove_bg(raw, tol=28.0)
        p128 = crop_and_align(cut, 128)
        p256 = crop_and_align(cut, 256)
        head64 = make_headshot(p256)

        p128.save(STAGE / f"{fid}_128.png", optimize=True)
        p256.save(STAGE / f"{fid}_256.png", optimize=True)
        head64.save(STAGE / f"{fid}_head64.png", optimize=True)

        manifest.append({
            "id": fid,
            "name": cname,
            "role": role,
            "sprite_128": f"{fid}_128.png",
            "sprite_256": f"{fid}_256.png",
            "headshot_64": f"{fid}_head64.png",
        })

        # 排入 2 行 4 列展示图
        r_i, c_i = divmod(idx, 4)
        x0 = 36 + c_i * 308
        y0 = 76 + r_i * 344
        # 背景卡片框（暗黛蓝模拟窗内/暗底验收）
        draw.rectangle([x0, y0, x0 + 284, y0 + 266], fill=(41, 34, 52, 255), outline=(140, 91, 63, 255), width=2)
        p240 = p256.resize((240, 240), Image.Resampling.NEAREST)
        sheet.paste(p240, (x0 + 22, y0 + 24), p240)
        draw.text((x0 + 4, y0 + 276), cname, fill=(232, 215, 176, 255), font=font_name)
        draw.text((x0 + 4, y0 + 304), role, fill=(168, 163, 153, 255), font=font_role)

    (STAGE / "factions_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    preview_path = OUT_DIR / "zhangyan_all8_factions_preview.png"
    sheet.convert("RGB").save(preview_path, optimize=True)

    zip_path = OUT_DIR / "zhangyan_all8_factions_pack.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(STAGE.glob("*")):
            zf.write(f, arcname=f.name)
        zf.write(preview_path, arcname="preview_all8_factions.png")

    print("PREVIEW:", preview_path)
    print("ZIP:", zip_path)
    print("TOTAL FILES PACKED:", len(list(STAGE.glob("*"))))


if __name__ == "__main__":
    main()
