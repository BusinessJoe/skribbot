import sys
import autopy
import time
from PIL import Image
from pynput import mouse
import numpy as np
import manip_images
import get_images

palette_corner = None
canvas_corners = [None, None]

def draw_pixels(bool_map):
    toggled = False
    dims = bool_map.shape
    x1, y1 = canvas_corners[0]
    x2, y2 = canvas_corners[1]

    width, height = x2 - x1, y2 - y1

    img_ratio = dims[0] / dims[1]
    canv_ratio = width / height

    if canv_ratio > img_ratio:
        scaling = height / dims[1]
    else:
        scaling = width / dims[0]

    width = scaling * dims[0]
    height = scaling * dims[1]

    x2, y2 = x1 + width, y1 + height

    delay = 0.005
    m = mouse.Controller()

    for y in range(0, dims[0], 1):
        for x in range(0, dims[1], 1):
            x_pos = x1 + (x2 - x1) * x / dims[1]
            y_pos = y1 + (y2 - y1) * y / dims[0]

            if not toggled:
                if bool_map[y][x]:
                    autopy.mouse.move(x=x_pos, y=y_pos)
                    time.sleep(delay)
                    m.press(mouse.Button.left)
                    toggled = True
            if toggled:
                try:
                    if not bool_map[y][x+1]:
                        autopy.mouse.move(x=x_pos, y=y_pos)
                        time.sleep(delay)
                        m.release(mouse.Button.left)
                        toggled = False
                except IndexError:
                    pass

        time.sleep(delay)
        m.release(mouse.Button.left)
        toggled = False

def set_color(idx):
    corner = palette_corner
    cell_size = 24
    top_color_pos = [(corner[0] + i * cell_size, corner[1]) for i in range(11)]
    bot_color_pos = [(corner[0] + i * cell_size, corner[1] + cell_size) for i in range(11)] 

    color_pos = top_color_pos[idx] if idx < 11 else bot_color_pos[idx - 11]
    autopy.mouse.move(*color_pos)
    autopy.mouse.click()

def on_click(x, y, button, pressed):
    global palette_corner
    global canvas_corners

    if button == mouse.Button.left and not pressed:
        if palette_corner is None:
            palette_corner = x, y
        elif canvas_corners[0] is None:
            canvas_corners[0] = x, y
        elif canvas_corners[1] is None:
            canvas_corners[1] = x, y
            return False

if __name__ == '__main__':
    get_images.download_images(sys.argv[1])
    get_images.pick_image()
    get_images.clean_image_directory()

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    img = Image.open('images/.saved.jpg')

    # Resize image to be at most 64x64
    max_size = 64, 64
    img.thumbnail(max_size)

    pixels = manip_images.dither_convert(img)

    pixels = pixels.astype(np.uint8)

    channels = manip_images.separate_channels(pixels)

    for i, channel in enumerate(channels):
        set_color(i)
        draw_pixels(channel)

