import pyclesperanto_prototype as cle
import numpy as np

def test_flip():
    test = cle.push_zyx(np.asarray([
        [0, 0, 0, 0, 0],
        [0, 1, 2, 0, 0],
        [0, 1, 2, 0, 0],
        [0, 1, 3, 0, 0],
        [0, 0, 0, 0, 0]
    ]))

    reference = cle.push_zyx(np.asarray([
        [0, 0, 0, 0, 0],
        [0, 0, 2, 1, 0],
        [0, 0, 2, 1, 0],
        [0, 0, 3, 1, 0],
        [0, 0, 0, 0, 0]
    ]))

    result = cle.create(test)
    cle.flip(test, result, True, False, False)

    print(result)

    a = cle.pull_zyx(result)
    b = cle.pull_zyx(reference)
    assert (np.array_equal(a, b))

