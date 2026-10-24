import os
from PIL import Image, ImageDraw, ImageFont

W, H = 256, 256
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# background rounded circle
cx, cy = W // 2, H // 2
r = 118
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(15, 76, 129, 255))

# medical cross
cross_color = (255, 255, 255, 255)
arm = 34
thick = 26
# vertical
d.rectangle((cx - thick//2, cy - arm, cx + thick//2, cy + arm), fill=cross_color)
# horizontal
d.rectangle((cx - arm, cy - thick//2, cx + arm, cy + thick//2), fill=cross_color)

# subtle ring
d.ellipse((cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6), outline=(255, 255, 255, 90), width=3)

# text below cross inside circle? put small "ICU" 
try:
    font = ImageFont.truetype("arial.ttf", 26)
except Exception:
    font = ImageFont.load_default()
text = "ICU"
bbox = d.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
d.text((cx - tw // 2, cy + arm + 8), text, fill=(255, 255, 255, 230), font=font)

# save
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
img.save(out)
print("saved", out)
img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico"))
print("done")
