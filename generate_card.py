import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_card():
    W, H = 1080, 1920
    # Create luxurious dark maroon / wine background
    img = Image.new("RGBA", (W, H), (26, 4, 10, 255))
    draw = ImageDraw.Draw(img)

    # Add radial glow in center
    center_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(center_glow)
    for r in range(700, 0, -10):
        alpha = int(70 * (1 - r / 700))
        glow_draw.ellipse([W//2 - r, 750 - r, W//2 + r, 750 + r], fill=(110, 13, 37, alpha))
    img = Image.alpha_composite(img, center_glow)
    draw = ImageDraw.Draw(img)

    # Draw golden sparkles / bokeh
    import random
    random.seed(42)
    for _ in range(90):
        x = random.randint(30, W - 30)
        y = random.randint(30, H - 30)
        radius = random.randint(2, 6)
        alpha = random.randint(80, 220)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(255, 215, 0, alpha))

    # Load and process punchi photo
    photo_path = r"c:\Users\mandi\OneDrive\Loku punchi birthday\punchi.jpg"
    photo = Image.open(photo_path).convert("RGBA")

    # Crop and resize photo to fit arched frame
    frame_w = 680
    frame_h = 920
    photo = photo.resize((frame_w, frame_h), Image.Resampling.LANCZOS)

    # Create Arch mask
    mask = Image.new("L", (frame_w, frame_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    # Rounded arch top (radius = frame_w // 2)
    mask_draw.pieslice([0, 0, frame_w, frame_w], 180, 360, fill=255)
    mask_draw.rectangle([0, frame_w//2, frame_w, frame_h - 40], fill=255)
    mask_draw.rounded_rectangle([0, frame_h - 100, frame_w, frame_h], radius=35, fill=255)

    # Frame position
    fx = (W - frame_w) // 2
    fy = 320

    # Draw Outer Gold Border
    border_thickness = 10
    outer_w = frame_w + border_thickness * 2
    outer_h = frame_h + border_thickness * 2
    gold_border = Image.new("RGBA", (outer_w, outer_h), (212, 175, 55, 255))
    gold_mask = Image.new("L", (outer_w, outer_h), 0)
    g_draw = ImageDraw.Draw(gold_mask)
    g_draw.pieslice([0, 0, outer_w, outer_w], 180, 360, fill=255)
    g_draw.rectangle([0, outer_w//2, outer_w, outer_h - 40], fill=255)
    g_draw.rounded_rectangle([0, outer_h - 100, outer_w, outer_h], radius=40, fill=255)

    # Paste gold border with shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rectangle([fx - 15, fy - 15, fx + frame_w + 15, fy + frame_h + 20], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(25))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    img.paste(gold_border, (fx - border_thickness, fy - border_thickness), gold_mask)
    img.paste(photo, (fx, fy), mask)

    # Draw decorative headers
    # Load fonts (fallback to default if system font not found)
    try:
        font_script = ImageFont.truetype("georgia.ttf", 78)
        font_sub = ImageFont.truetype("arialbd.ttf", 46)
        font_body = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("georgia.ttf", 32)
    except:
        font_script = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Top Text
    title_text = "Happy Birthday"
    t_bbox = draw.textbbox((0, 0), title_text, font=font_script)
    tw = t_bbox[2] - t_bbox[0]
    draw.text(((W - tw)//2, 150), title_text, fill=(255, 229, 127, 255), font=font_script)

    sub_title = "DEAREST LOKU PUNCHI"
    s_bbox = draw.textbbox((0, 0), sub_title, font=font_sub)
    sw = s_bbox[2] - s_bbox[0]
    draw.text(((W - sw)//2, 240), sub_title, fill=(255, 215, 0, 255), font=font_sub)

    # Stars in Harmony badge
    badge_text = "★ STARS IN HARMONY ★"
    b_bbox = draw.textbbox((0, 0), badge_text, font=font_small)
    bw = b_bbox[2] - b_bbox[0]
    draw.rounded_rectangle([(W - bw)//2 - 25, fy + frame_h - 25, (W + bw)//2 + 25, fy + frame_h + 25], radius=25, fill=(30, 4, 10, 240), outline=(212, 175, 55, 255), width=2)
    draw.text(((W - bw)//2, fy + frame_h - 18), badge_text, fill=(255, 215, 0, 255), font=font_small)

    # Bottom Wishes text
    line1 = "Wishing you endless joy, radiant health,"
    line2 = "and unconditional happiness always!"
    line3 = "May every dream in your heart come true. ✨"
    line4 = "With Love & Blessings ❤️"

    y_start = fy + frame_h + 80
    for line, color in [(line1, (255, 240, 245, 255)), (line2, (255, 240, 245, 255)), (line3, (255, 215, 0, 255)), (line4, (247, 168, 184, 255))]:
        l_bbox = draw.textbbox((0, 0), line, font=font_body)
        lw = l_bbox[2] - l_bbox[0]
        draw.text(((W - lw)//2, y_start), line, fill=color, font=font_body)
        y_start += 55

    # Save image
    out_path = r"c:\Users\mandi\OneDrive\Loku punchi birthday\birthday_status.png"
    img.convert("RGB").save(out_path, quality=95)
    print("Saved card to", out_path)

create_card()

