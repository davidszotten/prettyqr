import unittest
from prettyqr.blobgrid import BlobGrid
from prettyqr.utils import pointwise

LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3


class TestPointwise(unittest.TestCase):

    def test_add(self):
        self.assertEqual(pointwise('add', [1, 1], [2, 2]), [3, 3])

    def test_tuple(self):
        self.assertEqual(pointwise('add', [1, 1], (2, 2)), (3, 3))

    def test_singleton(self):
        self.assertEqual(pointwise('add', [1, 1], 1), [2, 2])

    def test_empty(self):
        self.assertEqual(pointwise('add', [], []), [])

    def test_missing_operator(self):
        self.assertRaises(AttributeError, pointwise, 'noop', [], [])


class TestBlobGrid(unittest.TestCase):

    def setUp(self):
        test_data = [
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 1]]

        class BlobGridTest(BlobGrid):
            def get_value(self, x, y):
                size = len(test_data)
                if not (0 <= x < size) or not (0 <= y < size):
                    return 0
                return test_data[y][x]

        self.blob_grid = BlobGridTest(3)
        self.drawing = self.blob_grid.draw_blobs()

    def test_no_subclass(self):
        blob_grid = BlobGrid(0)
        self.assertRaises(NotImplementedError, blob_grid.draw_blobs)

    def test_can_move(self):
        # counter clockwise
        self.assertTrue(self.blob_grid.can_move((0, 0), DOWN))

    def test_cant_move(self):
        # clockwise
        self.assertFalse(self.blob_grid.can_move((0, 0), RIGHT))

        # outside
        self.assertFalse(self.blob_grid.can_move((0, 0), UP))
        self.assertFalse(self.blob_grid.can_move((0, 0), LEFT))

    def test_find_direction1(self):
        self.assertEquals(self.blob_grid.find_direction((0, 0)), DOWN)

    def test_find_direction2(self):
        self.assertEquals(
            self.blob_grid.find_direction((2, 2)), DOWN)

    def test_find_direction3(self):
        self.assertEquals(
            self.blob_grid.find_direction((2, 2), LEFT), DOWN)

    def test_find_direction4(self):
        self.assertEquals(
            self.blob_grid.find_direction((2, 2), RIGHT), UP)

    def test_move(self):
        self.assertEqual(
            self.blob_grid.move((0, 0), RIGHT), (1, 0))

    def test_draw(self):
        self.assertEqual(self.blob_grid.draw(LEFT, DOWN),
            'c -0.276142374915,0.0 -0.5,0.276142374915 -0.5,0.5 ')

    def test_draw_blobs_lines(self):
        self.assertEquals(
            self.drawing.count('\n'), 2)

    def test_draw_blobs_corners(self):
        self.assertEqual(
            self.drawing.count('c '), 8)

    def test_draw_blobs_lines(self):
        self.assertEqual(
            self.drawing.count('l '), 4)

    def test_draw_blobs_colour_singles(self):
        self.assertEqual(
            self.drawing.count('colour'), 1)


if __name__ == '__main__':
    unittest.main()
