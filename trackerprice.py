# main
import time
import gmwhale
import pricetrack
import fn
import setup_var as sv


def main():
    while True:
        if fn.time_next_day():
            gmwhale.gmwhale()
        # if fn.bar_time(sv.interval_candle,fn.time_server()):
        #     pricetrack.pricetrack()
        time.sleep(1)

if __name__ == "__main__":
    main()