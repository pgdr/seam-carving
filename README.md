# Seam Carving Program


The Seam Carving program implements an image resizing technique based on
dynamic programming to remove seams with the least energy from an
image. This approach allows for content-aware image resizing, ensuring
minimal distortion of important features.


Seam carving works by identifying and removing "seams," which are paths
of least energy through an image. The energy of a pixel is computed
based on the gradient of pixel intensities, allowing the algorithm to
target areas that have less visual importance for removal.


## Example

When run on this image, with width 400 (currently 539) one can observe
that almost no information is lost

![](assets/black.png)

only bits of Bare Egil, leading to an even more Bare Bare Egil:

![](assets/black-400.jpg)

## Requirements

- Python 3.x
- PIL (Pillow) for image processing
- NumPy for numerical operations
- tqdm for progress visualization

## Usage

To run the program, execute the following command in the terminal:

```
python seam.py <image_filename> <new_width>
```

- `<image_filename>`: Path to the image file you want to resize.
- `<new_width>`: The desired width for the output image.

### Example

```
python seam.py input.jpg 300
```

This command will resize `input.jpg` to a width of 300 pixels, while
keeping the aspect ratio intact by removing the least important seams.
