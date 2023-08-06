# gaugan.py 

[![](https://img.shields.io/pypi/v/gaugan?style=plastic)](https://pypi.org/project/gaugan/)
[![](https://img.shields.io/pypi/l/gaugan?style=plastic)](https://unlicense.org/)
[![](https://img.shields.io/pypi/pyversions/gaugan?style=plastic)](https://www.python.org/downloads/)

A Python package providing an interface to NVIDIA's gauGAN project (http://nvidia-research-mingyuliu.com/gaugan/), which turns crude drawings into realistic images using AI.

## Installation
```pip install gaugan```

## Usage
```processImage(image = imageBytes, [style = 1], [url = 'http://12.34.56.78:90/'])```

Returns a bytes object of the processed image in JPG format.

### Parameters
###### ```image```
A bytes object of a PNG image containing the drawing.
###### ```style``` (optional)
Valid values are 'random' or an integer. Default is 'random'.
###### ```url``` (optional)
An URL of a gauGAN server. Useful for bulk processing, as by default it gets a new URL every time ```processImage()``` is called. It is necessary because the URLs are changed periodically. You can get an URL from the ```getUrl()``` function.

### Examples
##### Process image and display it using PIL
```
import gaugan, PIL, io
from PIL import Image

with open('input.png', "rb") as fh:
    image = processImage(fh.read())

PIL.Image.open(io.BytesIO(image)).show()
```
##### Process image and save it to disk
```
import gaugan

with open('input.png', "rb") as fh:
    image = gaugan.processImage(fh.read())

with open('output.jpg', "wb") as fh:
    fh.write(image)
```