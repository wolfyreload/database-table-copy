import argparse

parser = argparse.ArgumentParser(description="A bcp wrapper for importing and exporting table data")
parser.add_argument('config_file', type=str, help='config filename')

args = parser.parse_args()

if args.config_file is not None:
    config_filename = args.config_file
