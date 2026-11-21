#!/usr/bin/env python3
"""
《子时当：阴阳当铺》AI 2D 游戏美术资产批量后处理脚本
=====================================================
功能：
1. 自动抠图：优先使用 rembg（支持 BiRefNet / u2net 等模型）；无 rembg 时支持纯色底（中灰/深黑）快速色键抠图回退。
2. 边缘去杂色（Alpha Defringe）：消除 AI 抠图常见的白边/灰边毛刺。
3. 统一中式暗黑民俗色温（Color Grading）：对齐阴影墨青、高光暖琥珀、适度降饱和 + 微弱宣纸颗粒感。
4. 规范画布尺寸与居中留白：道具按方形透明 PNG 居中排版；立绘按半身竖幅底部对齐（贴合柜台木窗）。
5. 自动导出资产清单 JSON（含尺寸、锚点建议），方便 Unity / Godot 直接导入。

依赖安装（在本地开发环境运行）：
    pip install pillow numpy
    pip install rembg onnxruntime   # 可选：高精度 AI 抠图，推荐配合 BiRefNet 模型

使用示例：
    # 处理货品道具（512x512，居中留白 10%，使用 rembg 抠图）
    python3 batch_process_assets.py --input ./raw_props --output ./out_props --mode prop --size 512

    # 处理半身立绘（768x1024，底部对齐，仅统一色温不抠图）
    python3 batch_process_assets.py --input ./raw_npcs --output ./out_npcs --mode portrait --bg-mode none --width 768 --height 1024
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from PIL import Image, ImageFilter

SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def remove_background_rembg(img: Image.Image, model_name: str = "u2net") -> Image.Image:
    """调用 rembg 进行高精度透明抠图（本地可切换 birefnet-general 获得更锐利边缘）。"""
    try:
        from rembg import new_session, remove  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "未检测到 rembg 库。请运行 `pip install rembg onnxruntime`，或使用 `--bg-mode chroma` / `--bg-mode none`。"
        ) from exc

    session = new_session(model_name)
    out = remove(img.convert("RGBA"), session=session)
    return out.convert("RGBA")


def remove_background_chroma(
    img: Image.Image,
    tolerance: float = 28.0,
    feather: float = 12.0,
) -> Image.Image:
    """
    轻量纯色底抠图回退方案（无需深度学习依赖）。
    自动采样图像四角均值作为背景基准色（适配提示词里的纯灰 #808080 或纯黑 #0E1013 背景）。
    """
    rgba = img.convert("RGBA")
    arr = np.asarray(rgba, dtype=np.float32)
    rgb = arr[..., :3]

    # 采样四个 8x8 角落估算纯色背景
    corners = np.concatenate(
        [
            rgb[:8, :8].reshape(-1, 3),
            rgb[:8, -8:].reshape(-1, 3),
            rgb[-8:, :8].reshape(-1, 3),
            rgb[-8:, -8:].reshape(-1, 3),
        ],
        axis=0,
    )
    bg_color = np.median(corners, axis=0)

    dist = np.linalg.norm(rgb - bg_color, axis=-1)
    alpha = np.clip((dist - tolerance) / max(feather, 1e-5), 0.0, 1.0) * 255.0
    arr[..., 3] = np.minimum(arr[..., 3], alpha)
    return Image.fromarray(arr.astype(np.uint8), mode="RGBA")


def defringe_alpha(img: Image.Image, erode_px: int = 1, alpha_cutoff: int = 18) -> Image.Image:
    """
    边缘去白边/灰边（Alpha Defringe）：
    轻微收缩半透明外缘并清除极低透明度噪点，防止道具摆在深色柜台上出现亮边。
    """
    rgba = img.convert("RGBA")
    r, g, b, a = rgba.split()

    if erode_px > 0:
        a = a.filter(ImageFilter.MinFilter(size=erode_px * 2 + 1))

    a_arr = np.asarray(a, dtype=np.uint8).copy()
    a_arr[a_arr < alpha_cutoff] = 0
    a_clean = Image.fromarray(a_arr, mode="L")
    return Image.merge("RGBA", (r, g, b, a_clean))


def apply_folklore_color_grade(
    img: Image.Image,
    saturation: float = 0.84,
    contrast: float = 1.08,
    shadow_tint: Tuple[float, float, float] = (-4.0, 2.0, 5.0),
    highlight_tint: Tuple[float, float, float] = (8.0, 3.0, -6.0),
    grain_strength: float = 3.5,
    seed: int = 42,
) -> Image.Image:
    """
    统一《子时当》暗黑民俗色温：
    - 适度降低饱和度，消除 AI 生成常见的油腻艳色
    - 暗部微推墨青（冷），亮部微推暖琥珀（油灯光感）
    - 叠加轻微宣纸细颗粒，仅作用于不透明像素
    """
    rgba = img.convert("RGBA")
    arr = np.asarray(rgba, dtype=np.float32)
    rgb = arr[..., :3]
    alpha = arr[..., 3]

    # 1. 降低饱和度（BT.709 亮度权重）
    luma = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    rgb = luma[..., None] + (rgb - luma[..., None]) * saturation

    # 2. 对比度微调（以中灰 128 为中心）
    rgb = (rgb - 128.0) * contrast + 128.0

    # 3. 分离色调（暗部墨青 / 亮部暖灯）
    luma_norm = np.clip(luma / 255.0, 0.0, 1.0)[..., None]
    shadow_weight = (1.0 - luma_norm) ** 1.5
    highlight_weight = luma_norm ** 1.5
    rgb += shadow_weight * np.array(shadow_tint, dtype=np.float32)
    rgb += highlight_weight * np.array(highlight_tint, dtype=np.float32)

    # 4. 轻量宣纸颗粒（仅在有效像素区域叠加）
    if grain_strength > 0:
        rng = np.random.default_rng(seed)
        noise = rng.normal(0.0, grain_strength, size=luma.shape).astype(np.float32)
        mask = (alpha > 0).astype(np.float32)
        rgb += (noise * mask)[..., None]

    arr[..., :3] = np.clip(rgb, 0.0, 255.0)
    return Image.fromarray(arr.astype(np.uint8), mode="RGBA")


def add_subtle_outline(
    img: Image.Image,
    outline_px: int = 2,
    color: Tuple[int, int, int, int] = (14, 16, 19, 230),
) -> Image.Image:
    """给道具添加一圈极细深墨描边，增强在深色木柜台上的剪影辨识度。"""
    if outline_px <= 0:
        return img
    rgba = img.convert("RGBA")
    alpha = rgba.split()[3]
    dilated = alpha.filter(ImageFilter.MaxFilter(size=outline_px * 2 + 1))

    outline_layer = Image.new("RGBA", rgba.size, color)
    outline_layer.putalpha(dilated)
    return Image.alpha_composite(outline_layer, rgba)


def fit_to_canvas(
    img: Image.Image,
    target_w: int,
    target_h: int,
    padding_ratio: float = 0.10,
    align_bottom: bool = False,
) -> Image.Image:
    """按有效透明边界自动裁切、等比缩放，并按规则排版到统一画布尺寸。"""
    rgba = img.convert("RGBA")
    bbox = rgba.getbbox()
    if bbox is None:
        return Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

    cropped = rgba.crop(bbox)
    cw, ch = cropped.size

    usable_w = int(target_w * (1.0 - padding_ratio * 2))
    usable_h = int(target_h * (1.0 - padding_ratio * (1.0 if align_bottom else 2.0)))
    scale = min(usable_w / cw, usable_h / ch)
    new_w = max(1, int(round(cw * scale)))
    new_h = max(1, int(round(ch * scale)))

    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) if align_bottom else (target_h - new_h) // 2
    canvas.paste(resized, (paste_x, paste_y), resized)
    return canvas


def process_directory(
    input_dir: Path,
    output_dir: Path,
    mode: str,
    bg_mode: str,
    rembg_model: str,
    target_w: int,
    target_h: int,
    outline_px: int,
    saturation: float,
    grain: float,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS)
    if not files:
        print(f"[提示] 未在 {input_dir} 中找到支持的图片文件。")
        return

    manifest = []
    for idx, src_path in enumerate(files, start=1):
        img = Image.open(src_path).convert("RGBA")

        if bg_mode == "rembg":
            img = remove_background_rembg(img, model_name=rembg_model)
            img = defringe_alpha(img, erode_px=1)
        elif bg_mode == "chroma":
            img = remove_background_chroma(img)
            img = defringe_alpha(img, erode_px=1)

        img = apply_folklore_color_grade(
            img,
            saturation=saturation,
            grain_strength=grain,
            seed=100 + idx,
        )

        if mode == "prop" and outline_px > 0:
            img = add_subtle_outline(img, outline_px=outline_px)

        img = fit_to_canvas(
            img,
            target_w=target_w,
            target_h=target_h,
            padding_ratio=0.10 if mode == "prop" else 0.05,
            align_bottom=(mode == "portrait"),
        )

        out_name = f"{src_path.stem}.png"
        out_path = output_dir / out_name
        img.save(out_path, format="PNG", optimize=True)

        manifest.append(
            {
                "id": src_path.stem,
                "file": out_name,
                "mode": mode,
                "width": target_w,
                "height": target_h,
                "pivot": [0.5, 0.0] if mode == "portrait" else [0.5, 0.5],
            }
        )
        print(f"[{idx}/{len(files)}] 已处理 -> {out_path}")

    manifest_path = output_dir / "asset_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"完成！共处理 {len(manifest)} 项资产，清单已保存至 {manifest_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="《子时当》AI 游戏美术资产批量抠图与统一色温脚本")
    parser.add_argument("--input", required=True, type=Path, help="原始 AI 出图目录")
    parser.add_argument("--output", required=True, type=Path, help="输出透明 PNG 目录")
    parser.add_argument("--mode", choices=["prop", "portrait"], default="prop", help="资产类型：prop(道具居中) 或 portrait(立绘贴底)")
    parser.add_argument("--bg-mode", choices=["rembg", "chroma", "none"], default="rembg", help="抠图方式")
    parser.add_argument("--rembg-model", default="u2net", help="rembg 模型名，高精度推荐 birefnet-general")
    parser.add_argument("--size", type=int, default=512, help="方形尺寸简写（未指定 width/height 时生效）")
    parser.add_argument("--width", type=int, default=None, help="输出画布宽度")
    parser.add_argument("--height", type=int, default=None, help="输出画布高度")
    parser.add_argument("--outline", type=int, default=2, help="道具深墨描边像素（仅 prop 模式生效，0 为关闭）")
    parser.add_argument("--saturation", type=float, default=0.84, help="统一饱和度系数（默认 0.84 抑制 AI 艳色）")
    parser.add_argument("--grain", type=float, default=3.5, help="宣纸细颗粒强度（0 为关闭）")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_w = args.width or args.size
    target_h = args.height or args.size
    process_directory(
        input_dir=args.input,
        output_dir=args.output,
        mode=args.mode,
        bg_mode=args.bg_mode,
        rembg_model=args.rembg_model,
        target_w=target_w,
        target_h=target_h,
        outline_px=args.outline,
        saturation=args.saturation,
        grain=args.grain,
    )


if __name__ == "__main__":
    main()