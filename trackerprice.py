# main
import time
import gmwhale
import pricetrack

def main():
    while True:
        gmwhale.gmwhale()
        pricetrack.pricetrack()
        print(1)
        time.sleep(1)

if __name__ == "__main__":
    main()