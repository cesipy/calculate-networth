import csv
import json
import argparse

def handle_arguments(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file path", required=True)
    parser.add_argument("-o", "--output", help="Output file path", required=True)
    parser.add_argument("-t", "--type", help="Conversion type: 'csv_to_json' or 'json_to_csv'", required=True)
    return parser.parse_args()

def convert_csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, "r") as csv_file: 
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    with open(json_file_path, "w") as json_file: 
        json.dump(data, json_file, indent=4) 

def convert_json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, "r") as json_file: 
        data = json.load(json_file)

    with open(csv_file_path, "w") as csv_file: 
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data: 
            writer.writerow(row)

if __name__ == "__main__":
    args = handle_arguments()
    if args.type == 'csv_to_json':
        convert_csv_to_json(args.input, args.output)
    elif args.type == 'json_to_csv':
        convert_json_to_csv(args.input, args.output)
    else:
        print("Invalid conversion type. Please choose 'csv_to_json' or 'json_to_csv'.")