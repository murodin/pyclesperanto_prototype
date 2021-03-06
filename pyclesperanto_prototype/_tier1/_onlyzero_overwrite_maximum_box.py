from .._tier0 import execute

def onlyzero_overwrite_maximum_box (input, flag_dst, destination):
    """Apply a local maximum filter to an image which only overwrites pixels 
    with value 0. 
    
    Parameters
    ----------
    input : Image
    destination : Image
    
    Returns
    -------
    destination
    
    Examples
    --------
    >>> import pyclesperanto_prototype as cle
    >>> cle.onlyzero_overwrite_maximum_box(input, destination)
    
    References
    ----------
    .. [1] https://clij.github.io/clij2-docs/reference_onlyzeroOverwriteMaximumBox
    """


    parameters = {
        "dst": destination,
        "flag_dst": flag_dst,
        "src":input,
    }

    execute(__file__, 'onlyzero_overwrite_maximum_box_' + str(len(destination.shape)) + 'd_x.cl', 'onlyzero_overwrite_maximum_box_' + str(len(destination.shape)) + 'd', destination.shape, parameters)

    return [flag_dst, destination]
