from .._tier0 import Image
from .._tier3 import get_jaccard_index

def get_sorenson_dice_coefficient(src1 : Image, src2 : Image):
    """

    :param src1:
    :param src2:
    :return:
    """

    j = get_jaccard_index(src1, src2)

    return 2.0 * j / (j + 1)