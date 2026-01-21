# file_io.py
import os
import base64

def encode_file(path):
    """Encode bytes to UTF-8 string.

    Args:
        path: The image encoded.

    Returns:
        String that contains encoded bytes from the image.
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def list_files(dirpath):
    """Iterate through all receipts in dirpath.

    Args:
        dirpath: The folder with receipts.
        
    Returns:
        Name and path for each receipt image.
    """
    for name in os.listdir(dirpath):
        path = os.path.join(dirpath, name)
        if os.path.isfile(path):
            yield name, path

