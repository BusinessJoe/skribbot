from PIL import Image
import numpy as np

skribblio_palette = ['ffffff',
                     'c1c1c1',
                     'ef130b',
                     'ff7100',
                     'ffe400',
                     '00cc00',
                     '00b2ff',
                     '231fd3',
                     'a300ba',
                     'd37caa',
                     'a0522d',
                     '000000',
                     '4c4c4c',
                     '740b07',
                     'c23800',
                     'e8a200',
                     '005510',
                     '00569e',
                     '0e0865',
                     '550069',
                     'a75574',
                     '63300d',]

def hex_to_rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

skribblio_palette = np.array([hex_to_rgb(h) for h in skribblio_palette])


def color_distance(c1, c2):
    #return np.linalg.norm(c1 - c2, axis=-1) 
    avg_r = (c1[..., 0] + c2[0])/2
    delta_sq = (c1 - c2)**2
    red = (2 + avg_r/256) * delta_sq[..., 0]
    green = 4 * delta_sq[..., 1]
    blue = (2 + (255 - avg_r)/256) * delta_sq[..., 2]
    return np.sqrt(red + green + blue)


def closest_color(c):
    dists = np.array(list(color_distance(c, p) for p in skribblio_palette))
    return skribblio_palette[np.argmin(dists,axis=0)]

def simple_convert(img):
    pix = np.array(img)

    # Remove alpha channel
    try:
        pix = np.delete(pix, 3, 2)
    except IndexError:
        pass

    pix = closest_color(pix)

    pix = pix.astype(np.uint8)
    return pix

def dither_convert(img):
    def clamp(col):
        return np.maximum(np.minimum(col, 255), 0)

    pix = np.array(img)

    try:
        pix = np.delete(pix, 3, 2)
    except IndexError:
        pass

    pix = pix.astype(np.float32)

    for i, row in enumerate(pix):
        for j, c in enumerate(row):
            col = closest_color(c)
            diff = clamp(pix[i][j]) - col
            pix[i][j] = col
            try:
                pix[i][j+1] += 7/16 * diff
            except IndexError:
                pass
            try:
                pix[i+1][j-1] += 3/16 * diff
            except IndexError:
                pass
            try:
                pix[i+1][j] += 5/16 * diff
            except IndexError:
                pass
            try:
                pix[i+1][j+1] += 1/16 * diff
            except IndexError:
                pass

    pix = pix.astype(np.uint8)
    return pix

def separate_channels(pixels):
    colors = []
    for color in skribblio_palette:
        b = np.all(pixels == color, axis=-1)
        colors.append(b)
    return colors

if __name__ == '__main__':
    #print(closest_color(np.array([[[255, 255, 0]]])))
    dither_convert("images/jerrytest.png")
