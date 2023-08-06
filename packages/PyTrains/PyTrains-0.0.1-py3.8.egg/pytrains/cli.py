from .station import Station
from .data import getName
import argparse

parser = argparse.ArgumentParser(description="Get realtime UK train information through a simple Python API.")
parser.add_argument("crs", help="CRS code for the station.")
args = parser.parse_args()

def main():
    try:
        getName(args.crs)
    except:
        print("[ERROR]: CRS code invalid.")
        return

    station = Station(args.crs)
    print("== Departures from {} ==".format(station.name))
    for departure in station.services:
        delayString = "On time"
        if not departure.delay.isnumeric():
            delayString = "Delayed"
        elif int(departure.delay) > 0:
            delayString = "Delayed by {} minutes".format(departure.delay)
        elif departure.delayCause != "":
            delayString = "Delayed"
        print("{} ({}): {}".format(departure.departureTime.strftime("%H:%M"), delayString, departure.destination))