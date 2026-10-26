import os
from PIL import Image, ImageDraw, ImageFont

W, H = 512, 512
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

cx, cy = W // 2, H // 2

# outer glow circle
for i in range(6, 0, -1):
    d.ellipse((cx-130-i*4, cy-130-i*4, cx+130+i*4, cy+130+i*4), fill=(31, 111, 163, 18))

# main rounded circle gradient-ish
r = 124
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(15, 76, 129, 255))

# inner ring
d.ellipse((cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), outline=(255, 255, 255, 120), width=3)

# medical cross (rounded feel via rectangles)
cross_color = (255, 255, 255, 255)
arm = 46
thick = 22
d.rectangle((cx - thick//2, cy - arm, cx + thick//2, cy + arm), fill=cross_color)
d.rectangle((cx - arm, cy - thick//2, cx + arm, cy + thick//2), fill=cross_color)

# ECG heartbeat line across bottom
ecg = [(cx-90, cy+70),(cx-60, cy+70),(cx-45, cy+40),(cx-30, cy+95),(cx-10, cy+70),(cx+20, cy+70),(cx+40, cy+50),(cx+60, cy+70),(cx+90, cy+70)]
for i in range(len(ecg)-1):
    d.line((ecg[i], ecg[i+1]), fill=(120, 220, 255, 230), width=4)

# ICU text
try:
    font = ImageFont.truetype("arial.ttf", 30)
except Exception:
    font = ImageFont.load_default()
text = "ICU"
bbox = d.textbbox((0, 0), text, font=font)
tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
d.text((cx - tw//2, cy - arm - th - 12), text, fill=(255,255,255,230), font=font)

# save
base = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(base, "logo.png")
img.save(out)
print("saved", out)
# ico (resize)
ico = img.resize((256,256))
ico.save(os.path.join(base, "logo.ico"))
print("done")
