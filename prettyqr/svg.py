def svg_start(size, colour):
    return '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
 "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="%(width)s" height="%(height)s">
    <defs>
        <style type="text/css"><![CDATA[
            .reverse {fill: white}
            .colour {fill: %(colour)s}
        ]]></style>
    </defs>
    <rect x="0" y="0" width="%(width)s" height="%(height)s" class="reverse"/>
''' % {
        'width': size,
        'height': size,
        'colour': colour
    }


def svg_end():
    return '</svg>'
