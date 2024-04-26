import csv
import json
import argparse

def handle_arguments(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input CSV file path", required=True)
    parser.add_argument("-o", "--output", help="Output JSON file path", required=True)
    return parser.parse_args()

def convert_csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, "r") as csv_file: 
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    with open(json_file_path, "w") as json_file: 
        json.dump(data, json_file, indent=4) 
            

if __name__ == "__main__":
    args = handle_arguments()
    convert_csv_to_json(args.input, args.output)
