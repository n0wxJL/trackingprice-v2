# main
import time
import gmwhale
import pricetrack
import fn
import setup_var as sv
import test

def main():
    while True:
        pricetrack.pricetrack()
        if fn.time_next_day():
            gmwhale.gmwhale()
            fn.get_report()
        if fn.bar_time(sv.interval_candle,fn.time_server()):
            pricetrack.pricetrack()
        time.sleep(1)

if __name__ == "__main__":
    main()