# main
import time
import gmwhale
import pricetrack
import fn


def main():
    while True:
        if fn.time_next_day():
            gmwhale.gmwhale()
        # pricetrack.pricetrack()
        time.sleep(1)

if __name__ == "__main__":
    main()