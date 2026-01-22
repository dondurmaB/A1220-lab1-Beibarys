# main.py
import json
import argparse
from . import file_io as io_mod
from . import gpt

def process_output(data):
    if data["amount"] == None:
        return data
    
    if data["amount"][0] == "$":
        data["amount"] = data["amount"][1:]
    data["amount"] = float(data["amount"])
    return data

def in_between(dates, date):
    if date == None:
        return False

    try:
        if not dates[0][0:4] <= date[0:4] <= dates[1][0:4]:
            return False
        
        if dates[0][0:4] == date[0:4]:
            if dates[0][5:7] > date[5:7] or (dates[0][5:7] == date[5:7] and dates[0][8:10] > date[8:10]):
                return False
        
        if dates[1][0:4] == date[0:4]:
            if dates[1][5:7] < date[5:7] or (dates[1][5:7] == date[5:7] and dates[1][8:10] < date[8:10]):
                return False
        
        return True
    except Exception:
        return False

def process_directory(dirpath, dates):
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
        if dates is not None and not in_between(dates, data["date"]):
            continue   
        results[name] = process_output(data)
    return results

def main():
    """Main function that is run, asks two arguments and runs 'process_directory' function.
    Print information if '--print' argument is present.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath")
    parser.add_argument("--print", action="store_true")
    parser.add_argument("--expenses", nargs=2, type=str)
    args = parser.parse_args()

    data = process_directory(args.dirpath, args.expenses)

    if args.print:
        print(json.dumps(data, indent=2))

    if args.expenses:
        sm = 0
        for name, info in data.items():
            if info["amount"] is not None and isinstance(info["amount"], float):
                sm += info["amount"]

        print("Total sum: ", sm)

if __name__ == "__main__":
    main()

