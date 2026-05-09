#!/usr/bin/env python3
from PIL import Image
import numpy as np
import os

def remove_green_screen(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img, dtype=np.float32)

    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]

    # Hard mask: clear green pixels
    hard = (g > 80) & (g > r * 1.18) & (g > b * 1.18)

    # Soft edge: partial transparency for near-green fringe pixels
    greenness = g - np.maximum(r, b)
    soft = (greenness > 12) & ~hard
    soft_alpha = np.clip(255 - (greenness - 12) * 10, 0, 255)

    alpha = np.where(hard, 0.0, np.where(soft, soft_alpha, 255.0))
    data[:,:,3] = alpha

    Image.fromarray(data.astype(np.uint8)).save(output_path, "PNG")
    print(f"  ✓  {output_path}")

pairs = [
    ("images/casual.png", "images/casual_nobg.png"),
    ("images/suit.png",   "images/suit_nobg.png"),
]

print("\n=== Green Screen Removal ===\n")
for src, dst in pairs:
    if os.path.exists(src):
        remove_green_screen(src, dst)
    else:
        print(f"  ✗  Nije pronađen: {src}")
print("\nGotovo!\n")
