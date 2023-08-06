# Shades

## About

Shades is a python module for generative 2d image creation.

The main abstract object is a 'shade' which will determine color based on rules, and contains methods for drawing on images.

The majority of these implement simplex noise fields to determine color resulting in images that will appear different each time they are generated.

Current existing shades are:
    * BlockColor
    * NoiseGradient
    * DomainWarpGradient
    * SwirlOfShades

## Installing Shades

Shades is pip installable with:
'''
python -m pip install shades
'''

[More info here](https://github.com/benrrutter/shades)
