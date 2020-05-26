import os
import glob
import tkinter as tk
from PIL import Image, ImageTk
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from functools import partial
import manip_images

max_images = 16

def download_images(keyword):
    crawler = BingImageCrawler(
        parser_threads=5, downloader_threads=5,
        storage={'backend': 'FileSystem', 'root_dir': 'images'}
    )
    crawler.crawl(keyword=keyword, max_num=max_images, filters={'size': 'medium'})

class ImagePicker(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.window = window
        self.panels = [tk.Label(window) for i in range(16)]
        self.return_image = None

        for i in range(4):
            for j in range(4):
                idx = 4 * i + j
                self.panels[idx].grid(row=i, column=j)
                self.panels[idx].bind("<Button-1>", partial(self.on_click, label=self.panels[idx])) 

        self.load_images()

    def load_images(self):
        for idx, label in enumerate(self.panels, start=1):
            path = f"images/{idx:06}.jpg"
            img = Image.open(path)

            img.thumbnail((64, 64))
            label.image_small = img
            label.dithered = False

            img = img.resize((img.size[0]*3, img.size[1]*3), Image.NEAREST)
            photoimg = ImageTk.PhotoImage(img)
            label.photoimage = photoimg
            label.image = img
            label.configure(image=photoimg)

    def on_click(self, event, label):
        if not label.dithered:
            label.dithered = True

            img = label.image_small

            pix = manip_images.dither_convert(img)
            img = Image.fromarray(pix)

            img = img.resize((img.size[0]*3, img.size[1]*3), Image.NEAREST)
            photoimg = ImageTk.PhotoImage(img)
            label.photoimage = photoimg
            label.image = img
            label.configure(image=photoimg)
        else:
            self.return_image = label.image
            self.window.destroy()

def pick_dithered_image(keyword):
    download_images(keyword)

    root = tk.Tk()
    picker = ImagePicker(root)
    picker.load_images()
    root.mainloop()

    clean_image_directory()

    img = picker.return_image
    return img

def clean_image_directory():
    files = glob.glob('images/*')
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    download_images('cat')
    root = tk.Tk()
    picker = ImagePicker(root)
    picker.load_images()
    root.mainloop()
    img = picker.return_image
    clean_image_directory()

