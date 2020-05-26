import os
from PIL import Image, ImageTk
import glob
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
import tkinter as tk

max_images = 10

def download_images(keyword):
    crawler = BingImageCrawler(
        parser_threads=5, downloader_threads=5,
        storage={'backend': 'FileSystem', 'root_dir': 'images'}
    )
    crawler.session.verify = False
    crawler.crawl(keyword=keyword, max_num=max_images, filters={'size': 'medium'})

def pick_image():
    window = tk.Tk()
    image_idx = 1
    panel = tk.Label(window)
    panel.pack(side="bottom", fill="both", expand="yes")

    def update_image(idx):
        nonlocal panel
        path = f"images/{idx:06}.jpg"
        img = ImageTk.PhotoImage(Image.open(path))
        panel.configure(image=img)
        panel.image = img

    def increment_image(*args):
        nonlocal image_idx
        if image_idx < max_images:
            image_idx += 1
            update_image(image_idx)

    def decrement_image(*args):
        nonlocal image_idx
        if image_idx > 1:
            image_idx -= 1
            update_image(image_idx)

    def save_image(*args):
        nonlocal image_idx
        nonlocal window
        path = f"images/{image_idx:06}.jpg" 
        os.rename(path, "images/.saved.jpg")
        window.destroy()

    window.bind("<Right>", increment_image)
    window.bind("<Left>", decrement_image)
    window.bind("<Return>", save_image)

    update_image(image_idx)
    window.mainloop()

def clean_image_directory():
    files = glob.glob('images/*')
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    download_images('cat')
    pick_image()
    clean_image_directory()

