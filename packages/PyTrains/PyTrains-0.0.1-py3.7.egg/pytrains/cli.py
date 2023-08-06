import argparse

parser = argparse.ArgumentParser(description="Get realtime UK train information through a simple Python API.")
parser.add_argument("crs", help="CRS code for the station.")
args = parser.parse_args()

def main():
    return