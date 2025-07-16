import numpy as np
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont
import random

# --- THE FINAL POLISHED EDITION ---
WIDTH, HEIGHT = 500, 300
NAME = "ASHIRVAD"
FONT_FILENAME = "nasalization-rg.ttf"

# --- LAYER CONFIGURATION ---
LAYERS = [
    { # Foreground (Closest, fastest, brightest)
        "font_size": 24, "min_speed": 6, "max_speed": 9,
        "tail_len": 7, "opacity": 1.0,
        "head_color": (255, 200, 200), "tail_color": (255, 50, 50),
        "columns_percentage": 0.8 # Use 80% of possible columns to reduce crowding
    },
    { # Mid-ground
        "font_size": 18, "min_speed": 4, "max_speed": 6,
        "tail_len": 9, "opacity": 0.7,
        "head_color": (200, 100, 100), "tail_color": (150, 0, 0),
        "columns_percentage": 0.7 # Use 70%
    },
    { # Background (Farthest, slowest, dimmest)
        "font_size": 14, "min_speed": 2, "max_speed": 4,
        "tail_len": 12, "opacity": 0.4,
        "head_color": (150, 50, 50), "tail_color": (100, 0, 0),
        "columns_percentage": 0.6 # Use 60%
    }
]

# --- GLOBAL SETTINGS ---
DURATION = 0.05
NUM_FRAMES = 180
BG_COLOR = (0, 0, 0)
name_chars = list(NAME)

# --- FONT LOADING ---
try:
    fonts = [ImageFont.truetype(FONT_FILENAME, l['font_size']) for l in LAYERS]
except IOError:
    print(f"FATAL ERROR: Font file '{FONT_FILENAME}' not found.")
    exit()

# --- INITIALIZE RAIN COLUMNS FOR EACH LAYER ---
rain_layers = []
for i, layer_cfg in enumerate(LAYERS):
    max_cols = WIDTH // layer_cfg['font_size']
    num_cols = int(max_cols * layer_cfg['columns_percentage'])
    
    # Randomly select which columns will have rain
    active_indices = sorted(random.sample(range(max_cols), num_cols))
    
    rain_layers.append([{
        'x_index': idx,
        'y': random.uniform(-HEIGHT, 0),
        'speed': random.uniform(layer_cfg['min_speed'], layer_cfg['max_speed']),
    } for idx in active_indices])


frames = []
print("Rendering Final Polish...")

for frame_num in range(NUM_FRAMES):
    image = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(image)

    for layer_index, layer_cols in enumerate(rain_layers):
        cfg = LAYERS[layer_index]
        font = fonts[layer_index]
        
        for col in layer_cols:
            head_y = col['y']
            for j in range(cfg['tail_len']):
                char_y = head_y - (j * cfg['font_size'])
                if 0 <= char_y < HEIGHT:
                    brightness = (1.0 - (j / cfg['tail_len'])) ** 1.5
                    color_r = int(cfg['tail_color'][0] + (cfg['head_color'][0] - cfg['tail_color'][0]) * brightness)
                    color_g = int(cfg['tail_color'][1] + (cfg['head_color'][1] - cfg['tail_color'][1]) * brightness)
                    color_b = int(cfg['tail_color'][2] + (cfg['head_color'][2] - cfg['tail_color'][2]) * brightness)
                    
                    final_color = (int(color_r * cfg['opacity']), int(color_g * cfg['opacity']), int(color_b * cfg['opacity']))
                    
                    draw.text((col['x_index'] * cfg['font_size'], char_y), random.choice(name_chars), font=font, fill=final_color)

            col['y'] += col['speed']
            if col['y'] - cfg['tail_len'] * cfg['font_size'] > HEIGHT:
                col['y'] = random.uniform(-100, 0)
                col['speed'] = random.uniform(cfg['min_speed'], cfg['max_speed'])

    frames.append(image)
    print(f"Frame {frame_num + 1}/{NUM_FRAMES} rendered.")

print("Saving final render...")
imageio.mimsave(
    "matrix.gif", # Saving directly as matrix.gif
    [np.array(img) for img in frames],
    duration=DURATION,
    loop=0
)
print("✅ Final Polish complete. 'matrix.gif' is ready.")
