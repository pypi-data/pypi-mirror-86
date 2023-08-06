import imageio
import matplotlib.pyplot as plt
from scipy.ndimage import binary_erosion
from PIL import Image, ImageDraw
from iidfile import IIDFile

IIDFILE = "tests/assets/0c47bd8282594ae931d9.iid"
PREFILE = "tests/assets/0c47bd8282594ae931d9.jpg"


def run():
    """Run default tests
    :return:
    """
    _look_for_and_filter()
    _region()
    _at()
    _graph()


def _graph(visualize=False):
    """Test of graph()"""
    iidfile = IIDFile(fpath=IIDFILE)
    iidfile.fetch(everything=True)

    nodes, edges = iidfile.overlap_graph()

    assert len(nodes) == 115, "Something fishy with the graph()"
    assert len(edges) == 412, "Something fishy with the graph()"

    if visualize:

        select = 50

        im = imageio.imread(PREFILE)

        A, B, area = edges[select]

        if B.seg.area > A.seg.area:
            A, B = B, A

        minr, minc, maxr, maxc = A.seg.bbox
        subcanvas = im[minr:maxr, minc:maxc]
        stroke = A.seg.mask() & ~binary_erosion(A.seg.mask(), iterations=1)
        subcanvas[stroke] = [255, 0, 0]
        im[minr:maxr, minc:maxc] = subcanvas

        minr, minc, maxr, maxc = B.seg.bbox
        subcanvas = im[minr:maxr, minc:maxc]
        stroke = B.seg.mask() & ~binary_erosion(B.seg.mask(), iterations=1)
        subcanvas[stroke] = [0, 255, 0]
        im[minr:maxr, minc:maxc] = subcanvas

        plt.figure(figsize=(10, 10))
        plt.imshow(im)
        plt.show()


def _at(visualize=False):
    """Naive test of at()"""

    iidfile = IIDFile(fpath=IIDFILE)

    # XY
    xy = (370, 650)
    iidfile.fetch(groups=['iid'], segs=True)
    entries = iidfile.at(*xy, only_loaded=True)

    assert len(entries) == 1, "Something fishy with iidfile.at()"

    if visualize:

        im = imageio.imread(PREFILE)

        for entry in entries:
            minr, minc, maxr, maxc = entry.seg.bbox
            subcanvas = im[minr:maxr, minc:maxc]
            subcanvas[entry.seg.mask()] = subcanvas[entry.seg.mask()] * [255, 0, 0]
            im[minr:maxr, minc:maxc] = subcanvas

        image = Image.fromarray(im, 'RGB')
        draw = ImageDraw.Draw(image)

        # Entries
        for entry in entries:
            poly = entry.seg.bbox_polygon()
            poly = poly + [poly[0]]
            draw.line(poly, fill="#F00", width=1)

        # Search point
        x, y = xy
        draw.ellipse([(x-5, y-5), (x+5, y+5)], fill="#0F0", width=4)

        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.show()


def _region(visualize=False):
    """Naive test of region()"""

    iidfile = IIDFile(fpath=IIDFILE)

    # Bounds
    minr, minc, maxr, maxc = (450, 160, 800, 485)
    bbox = minr, minc, maxr, maxc

    iidfile.fetch(groups=['iid'], segs=True)
    entries = iidfile.region(bbox, only_loaded=True)
    assert len(entries) == 21, "Something fishy with iidfile.region()"

    if visualize:

        image = Image.fromarray(imageio.imread(PREFILE), 'RGB')
        draw = ImageDraw.Draw(image)

        # Entries
        for entry in entries:
            poly = entry.seg.bbox_polygon()
            poly = poly + [poly[0]]
            draw.line(poly, fill="#F00", width=1)

        # Main box
        x, y, w, h = minc, minr, maxc - minc, maxr - minr
        searchbox = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
        draw.line(searchbox, fill="#0F0", width=4)

        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.show()


def _look_for_and_filter():
    """Naive test of find() and filter()"""

    iidfile = IIDFile(fpath=IIDFILE)
    entries = iidfile.fetch(all_keys=True)

    # Test find
    query = [entry.iid.address for entry in entries[:20]]
    found = iidfile.look_for(addresses=query, segs=True, groups='iid', domains='ae73'.encode())

    assert len(found) == 15, "Something fishy with iidfile.found()"

    # Test filter
    matches = iidfile.filter(area=(2000, 4000), domains='ae73'.encode())

    assert len(matches) == 6, "Something fishy with iidfile.filter()"

