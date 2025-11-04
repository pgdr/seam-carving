# Seam Carving Program

The Seam Carving program applies a dynamic programming approach to
resize images by removing low-energy "seams", enabling content-aware
resizing with minimal distortion.  It identifies *seams*—paths of least
energy vertically through the image—by computing pixel energy from
intensity gradients.


## Example

When run on this image, with width 400 (currently 539) one can observe
that almost no information is lost

![](assets/black.png)

only bits of Bare Egil, leading to an even more Bare Bare Egil:

![](assets/black-400.jpg)

## Requirements

- `PIL` (Pillow) for image processing
- `numpy` for numerical operations
- (optional) `tqdm` for progress visualization

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
