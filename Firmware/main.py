# main.py for SEEED XIAO RP2040 macropad
# Features: 3x3 matrix, rotary encoder, OLED, Neopixels, multi-layer control

import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers

# Extensions
from kmk.extensions.rotary_encoder import RotaryEncoder
from kmk.extensions.oled import Oled, OledData
from kmk.extensions.rgb import RGB

#  Keyboard Setup 
keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP26, board.GP27, board.GP28)
keyboard.row_pins = (board.GP2, board.GP4, board.GP3)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

#  Layers 
layers = Layers()
keyboard.modules.append(layers)

#  Rotary Encoder
encoder = RotaryEncoder(
    pin_a=board.GP29,
    pin_b=board.GP0,
    divisor=4,
    map=(
        KC.VOLU,  # clockwise volume up 
        KC.VOLD,  # counter-clockwise volume down
    ),
)
keyboard.extensions.append(encoder)

#  OLED 
oled = Oled(
    i2c=board.I2C(),
    width=128,
    height=32,
    addr=0x3C,
    flip=True,       # flips the display vertically
    
    rotate=180       # rotates the display 180 degrees
)
keyboard.extensions.append(oled)
oled_data = OledData()

#  RGB 
rgb = RGB(
    pixel_pin=board.GP1,
    num_pixels=8,
    hue_default=0,
    sat_default=255,
    val_default=100,
)
keyboard.extensions.append(rgb)

#  Keymap
keyboard.keymap = [
    # Layer 0: KiCad
    [
        KC.LCTRL(KC.LSHIFT(KC.P)), KC.X, KC.MO(1),   # row0
        KC.V, KC.NO, KC.RGB_TOG,                     # row1
        KC.LCTRL(KC.Z), KC.LCTRL(KC.Y), KC.LCTRL(KC.S), # row2
    ],
    # Layer 1: Fusion
    [
        KC.S, KC.E, KC.MO(2),                        # row0
        KC.D, KC.NO, KC.RGB_MOD,                     # row1
        KC.LCTRL(KC.Z), KC.LCTRL(KC.Y), KC.LCTRL(KC.S), # row2
    ],
    # Layer 2: General
    [
        KC.COPY, KC.PASTE, KC.MO(0),                 # row0
        KC.CUT, KC.NO, KC.RGB_HUI,                   # row1
        KC.LCTRL(KC.Z), KC.LCTRL(KC.Y), KC.LCTRL(KC.S), # row2
    ],
]

#  OLED + RGB Layer Feedback 
def update_feedback():
    layer = keyboard.active_layers[0]
    if layer == 0:
        oled_data.text("KiCad Mode", 0, 0)
        rgb.set_hsv(170, 255, 100)  # Blue
    elif layer == 1:
        oled_data.text("Fusion Mode", 0, 0)
        rgb.set_hsv(30, 255, 100)   # Orange
    elif layer == 2:
        oled_data.text("General Mode", 0, 0)
        rgb.set_hsv(85, 255, 100)   # Green

keyboard.before_matrix_scan = update_feedback

#  Run 
if __name__ == '__main__':
    keyboard.go()