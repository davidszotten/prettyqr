import itertools
import Image
from xml.dom import minidom
from xml.parsers.expat import ExpatError


def clear_logo_space(array, size, filename):
    if filename is None:
        return

    # remove any data where logo is
    try:
        logo = Image.open(filename)
        logo_size = logo.size
        logo_array = logo.load()

        if logo_size == (size, size):
            neighbour4 = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]
            for x, y in itertools.product(xrange(size), repeat=2):
                if logo_array[x, y][3] != 0:
                    for offset in neighbour4:
                        array[x + offset[0], y + offset[1]] = 255
        else:
            print "Raster logo size mismatch, ignoring"
    except IOError, e:
        print "Error opening raster logo: [%s] Ignoring." % e.strerror


def get_svg_logo(filename):
    if filename is None:
        return ''

    try:
        with open(filename) as logo_svg:
            try:
                dom = minidom.parse(logo_svg)
                svg_node = dom.getElementsByTagName('svg')[0]
                ignored_nodes = ['metadata', 'defs', 'sodipodi:namedview']
                logo_xml = "\n".join([n.toxml() for n in svg_node.childNodes
                    if n.nodeName not in ignored_nodes])
                return logo_xml

            except ExpatError, e:
                print "Error parsing logo svg. [%s] Ignoring logo." % e

            except IndexError:
                print ("Error parsing logo svg: No <svg> node found. "
                    "Ignoring logo.")
    except IOError, e:
        print "Error opening logo: [%s] Ignoring." % e.strerror

    return ''
