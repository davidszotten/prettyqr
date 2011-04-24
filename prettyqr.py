import sys
from optparse import OptionParser
from qrencode import encode_scaled, QR_ECLEVEL_H
from prettyqr.blobgrid import BlobGrid
from prettyqr.logos import clear_logo_space, get_svg_logo
from prettyqr.svg import svg_start, svg_end


def main():
    parser = OptionParser(
        usage="usage: %prog [options] text")
    parser.add_option("-o", "--output", dest="output_filename",
        help="write output to FILE", metavar="FLIE", default="output.svg")
    parser.add_option("-l", "--logo", dest="logo_svg",
        help="load logo (partial svg file) from FILE", metavar="FILE")
    parser.add_option("-L", "--logo-raster", dest="logo_png",
        help="load rasterized logo (png) from FILE", metavar="FILE")
    parser.add_option("-c", "--color", dest="colour", default="#a54024",
        help="use COLOR as secondary color")
    parser.add_option("-m", "--min-size", type="int", dest="min_size",
        default="40", help="pad output to minimum size for final QR image")

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit()

    qr = encode_scaled(args[0], options.min_size, level=QR_ECLEVEL_H)
    image = qr[-1]
    array = image.load()
    # assume squares
    size = image.size[0]

    class BlogGridQR(BlobGrid):
        def get_value(self, x, y):
            if not (0 <= x < size) or not (0 <= y < size):
                return 0
            return 1 - array[x, y] / 255

    clear_logo_space(array, size, options.logo_png)
    blob_grid = BlogGridQR(size)

    output = svg_start(size, options.colour)
    output += blob_grid.draw_blobs()
    output += get_svg_logo(options.logo_svg)
    output += svg_end()

    output_file = open(options.output_filename, 'w')
    output_file.write(output)
    output_file.close()

if __name__ == '__main__':
    main()
