from PIL import Image
import os

# PNG faylini ochish (bu kod turgan papkadan PNG faylini olish)
img = Image.open("iconsss.webp")

# Hozirgi papkada 'favicon.ico' nomi bilan saqlash
current_dir = os.path.dirname(__file__)  # Bu kod turgan papkani olish
output_path = os.path.join(current_dir, "favicon.ico")
img.save(output_path, format="ICO")

print(f"Favicon saqlandi: {output_path}")
