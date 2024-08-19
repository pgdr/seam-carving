import sys
from PIL import Image, ImageFilter
import numpy as np
from tqdm import tqdm


def compute_energy(img):
    bw = img.convert("L")
    gradient_x = bw.filter(ImageFilter.FIND_EDGES)
    gradient_y = bw.filter(ImageFilter.FIND_EDGES)
    energy = np.hypot(np.array(gradient_x), np.array(gradient_y))
    return energy


def compute_cumenergy(energy):
    height, width = energy.shape
    cumenergy = energy.copy()

    for i in range(1, height):
        for j in range(width):
            if j == 0:
                c_en = min(cumenergy[i - 1, j], cumenergy[i - 1, j + 1])
            elif j == width - 1:
                c_en = min(cumenergy[i - 1, j - 1], cumenergy[i - 1, j])
            else:
                c_en = min(
                    cumenergy[i - 1, j - 1],
                    cumenergy[i - 1, j],
                    cumenergy[i - 1, j + 1],
                )
            cumenergy[i, j] += c_en

    return cumenergy


def find_vertical_seam(cumenergy):
    height, width = cumenergy.shape
    seam = np.zeros(height, dtype=int)
    seam[-1] = np.argmin(cumenergy[-1])
    for i in range(height - 2, -1, -1):
        j = seam[i + 1]
        if j == 0:
            seam[i] = np.argmin(cumenergy[i, j : j + 2])
        elif j == width - 1:
            seam[i] = np.argmin(cumenergy[i, j - 1 : j + 1]) + j - 1
        else:
            seam[i] = np.argmin(cumenergy[i, j - 1 : j + 2]) + j - 1
    return seam


def remove_seam(img, seam):
    width, height = img.size
    new_img = Image.new("RGB", (width - 1, height))
    for i in range(height):
        k = 0
        for j in range(width):
            if j != seam[i]:
                new_img.putpixel((k, i), img.getpixel((j, i)))
                k += 1
    return new_img


def seam_carving(img, new_width):
    orig_width = img.width
    for _ in tqdm(range(new_width, orig_width)):
        energy = compute_energy(img)
        cumenergy = compute_cumenergy(energy)
        seam = find_vertical_seam(cumenergy)
        img = remove_seam(img, seam)
    return img


if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit("Usage: seam.py fname.py width")
    fname = sys.argv[1]
    width = int(sys.argv[2])
    input_img = Image.open(fname)
    resized_img = seam_carving(input_img, new_width=width)
    fname_ = fname.split(".")[0]
    resized_img.save(fname_ + f"-{width}.jpg")
