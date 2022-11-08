# main
import time
import gmwhale
import pricetrack

def main():
    while True:
        gmwhale.gmwhale()
        pricetrack.pricetrack()
        time.sleep(1)

if __name__ == "__main__":
    main()