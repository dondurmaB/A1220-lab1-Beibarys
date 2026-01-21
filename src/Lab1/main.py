# main.py
import json
import argparse
from . import file_io as io_mod
from . import gpt

def process_directory(dirpath):
    """Iterate through all receipts and gets data by asking prompt.

    Args:
        dirpath: Direction of a folder that contains receipts.
        
    Returns:
        The dictionary that contains the information of receipts.
    """
    results = {}
    for name, path in io_mod.list_files(dirpath):
        image_b64 = io_mod.encode_file(path)
        data = gpt.extract_receipt_info(image_b64)
        results[name] = data
    return results

def main():
    """Main function that is run, asks two arguments and runs 'process_directory' function.
    Print information if '--print' argument is present.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args()

    data = process_directory(args.dirpath)
    if args.print:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()

