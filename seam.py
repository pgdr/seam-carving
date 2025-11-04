import sys
from PIL import Image, ImageFilter
import numpy as np

try:
    from tqdm import tqdm
except ImportError:
    print("Skipping module tqdm", file=sys.stderr)
    tqdm = list


def compute_energy(img):
    bw = np.array(img.convert("L"))
    gradient_x = np.abs(np.diff(bw, axis=1, prepend=bw[:, :1]))
    gradient_y = np.abs(np.diff(bw, axis=0, prepend=bw[:1, :]))
    energy = gradient_x + gradient_y
    return energy


def compute_cumenergy(energy):
    height, width = energy.shape
    cumenergy = np.zeros((height, width))
    cumenergy[0] = energy[0]

    for i in range(1, height):
        left_shift = np.roll(cumenergy[i - 1], 1)
        right_shift = np.roll(cumenergy[i - 1], -1)
        cumenergy[i] = energy[i] + np.minimum(left_shift, cumenergy[i - 1], right_shift)

    return cumenergy


def find_vertical_seam(cumenergy):
    height, width = cumenergy.shape
    seam = np.zeros(height, dtype=int)
    seam[-1] = np.argmin(cumenergy[-1])

    for i in range(height - 2, -1, -1):
        j = seam[i + 1]
        if j == 0:
            idx = np.argmin(cumenergy[i, j : j + 2])
        elif j == width - 1:
            idx = np.argmin(cumenergy[i, j - 1 : j + 1]) - 1
        else:
            idx = np.argmin(cumenergy[i, j - 1 : j + 2]) - 1
        seam[i] = j + idx

    return seam


def remove_seam(img, seam):
    height, width, channels = img.shape
    new_img = np.zeros((height, width - 1, channels), dtype=img.dtype)

    for i in range(height):
        new_img[i, :, :] = np.delete(img[i, :, :], seam[i], axis=0)

    return new_img


def seam_carving(img, new_width):
    orig_width = img.width
    img = np.array(img)
    for _ in tqdm(range(new_width, orig_width)):
        energy = compute_energy(Image.fromarray(img))
        cumenergy = compute_cumenergy(energy)
        seam = find_vertical_seam(cumenergy)
        img = remove_seam(img, seam)

    return Image.fromarray(img)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit("Usage: seam.py fname.py width")
    fname = sys.argv[1]
    width = int(sys.argv[2])
    input_img = Image.open(fname)
    resized_img = seam_carving(input_img, new_width=width)
    resized_img = resized_img.convert("RGB")
    fname_ = fname.split(".")[0]
    resized_img.save(fname_ + f"-{width}.jpg")
