from base64 import b64decode

import Orange.data
from Orange.widgets.widget import OWWidget, Msg, Input, Output


import orangecontrib.spectroscopy


class OWTest(OWWidget):
    # Widget's name as displayed in the canvas
    name = "Test image data"

    class Outputs:
        test = Output("Test", Orange.data.Table, default=True)

    want_main_area = False
    resizing_enabled = False

    def mock_visible_image_data(self):
        red_img = b64decode("iVBORw0KGgoAAAANSUhEUgAAAA"
                            "oAAAAKCAYAAACNMs+9AAAAFUlE"
                            "QVR42mP8z8AARIQB46hC+ioEAG"
                            "X8E/cKr6qsAAAAAElFTkSuQmCC")
        black_img = b64decode("iVBORw0KGgoAAAANSUhEUgAAA"
                              "AoAAAAKCAQAAAAnOwc2AAAAEU"
                              "lEQVR42mNk+M+AARiHsiAAcCI"
                              "KAYwFoQ8AAAAASUVORK5CYII=")

        return [
            {
                "name": "Image 01",
                "image_bytes": red_img,
                "pos_x": 100,
                "pos_y": 100,
                "pixel_size_x": 1.7,
                "pixel_size_y": 2.3
            },
            {
                "name": "Image 02",
                "image_bytes": black_img,
                "pos_x": 0.5,
                "pos_y": 0.5,
                "pixel_size_x": 1,
                "pixel_size_y": 0.3
            },
        ]

    def __init__(self):
        super().__init__()

        data_with_visible_images = Orange.data.Table(
            "agilent/4_noimage_agg256.dat"
        )
        data_with_visible_images.attributes["visible_images"] = \
            self.mock_visible_image_data()

        self.Outputs.test.send(data_with_visible_images)


if __name__ == "__main__":  # pragma: no cover
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWTest).run()
