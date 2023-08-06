import cv2
import numpy as np
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)


def draw_box_on_image(image_array, bounding_boxes, colour=(255, 0, 0), thickness=2):
    """Draw rectangles on a given image represented as a numpy array

    Parameters
    ----------
    image_array: numpy.ndarray
        an image represented as a numpy.ndarray usually returned by cv2.imread
    bounding_boxes: List[((int, int), (int, int))], List[((xmin, ymin), (xmax, ymax))]
        list of bounding box coordinates that need to be drawn on the given image
    colour: tuple(int, int, int), optional, Default(255, 0, 0)=Blue.
        a BGR tuple to define the colour of the bounding box boundary.
    thickness: int, optional, Default=2
        integer value of thickness of the boundary line to be drawn, if -1 then
        a filled rectangle is drawn

    Returns
    -------
    The image in np.array format with the bounding boxes superimposed on the image
    """
    new_image_array = np.copy(image_array)
    for bounding_box in bounding_boxes:
        new_image_array = cv2.rectangle(
            new_image_array,
            bounding_box[0],
            bounding_box[1],
            colour,
            thickness,
        )

    return new_image_array


def draw_text_on_image(image_array, message, top_left, font_path=None, font_size=5, font_colour=(255, 0, 0)):
    """Write text on a given image represented as a numpy array

    Parameters
    ----------
    image_array: numpy.ndarray
        an image represented as a numpy.ndarray usually returned by cv2.imread
    message: str
        text that needs to be written on the image
    top_left: (int, int)
        top left location for the text to start.
        (x_top_left, y_top_left) where top left is origin
    font_path: str
        full path to font .ttf file,
        generally found under
            Mac - /Library/Fonts
            Ubuntu - /usr/share/fonts/truetype/
        example:
            /Library/Fonts/Arial Black.ttf, /Library/Fonts/Georgia.ttf
            /usr/share/fonts/truetype/lato/Lato-Medium.ttf, /usr/share/fonts/truetype/noto/NotoMono-Regular.ttf
    font_size: int, optional, Default=5
        integer value of size of font to be used
    colour: tuple(int, int, int), optional, Default(255, 0, 0)=Red.
        a RGB tuple to define the colour of the bounding box boundary.

    Returns
    -------
    The image in np.array format with the text superimposed at the specified location
    """
    img = Image.fromarray(image_array.astype("uint8"))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=font_size)
    draw.text(top_left, message, fill=font_colour, font=font)
    img_t = np.array(img).astype("uint8")
    return img_t
