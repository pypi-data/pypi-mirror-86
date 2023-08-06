# ASKEW: Perspective transform along specified axes

This is pip installed version of [ASKEW](https://github.com/TheRincon/askew). The other version is the cli tool. The cli version has more features.

## Original Author

Hou-Ning Hu / [@eborboihuc](https://eborboihuc.github.io/)

## Prerequisites

[The original repo](https://github.com/eborboihuc/rotate_3d)(Unmaintained)

This version is made for:
- Python3

Rwquires:
- numpy
- OpenCV

## Installation

```bash
pip3 install askew3
```

## Usage

```python
import askew3

it = askew3.ImageTransformer(img_path, height=height, width=width)
it.skew(theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0) # optional bg = (0,0,0) for background color (supply triplet)
img = it.save(new_img_path)
```
