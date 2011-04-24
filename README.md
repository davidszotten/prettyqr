PrettyQR
===

Generate QR codes that look prettier than the default, with round corners and colours. Optionally embed a logo (we use the highest QR error redundancy, 30% so provided the logo isn't too large, the QR code is parsed fine by most readers)

uses [`qrencode`](https://github.com/Arachnid/pyqrencode) (and its dependencies) to generate the raw QR data.

outputs svg files for best quality

Usage
---
    prettyqr.py --options "Some text or url"

Adding logos
----
For best results, two versions of your logo should be provided. First generate a QR code without any logo. Open the output in e.g. [inkscape](http://www.inkscape.org), remove the contents and save a new file with the same dimensions, and your logo in the desired location. In addition, export a raster version of your logo template at 90 dpi, which may be used to clear the QR data from underneath the logo.

Good results for data in the order of short urls has been achieved with logos slightly larger than the (large) corner marking squares.

Note that there is a probability that this makes the QR code unusable. 30% redundancy is built in and it's worked in all (reasonable) examples I've tried. Always test to make sure the final QR code works.


Requirements
---
[`qrencode`](https://github.com/Arachnid/pyqrencode)  
[`libqrencode`](http://fukuchi.org/works/qrencode/index.en.html)  
`PIL`  
`Python >= 2.6` (for now)  
