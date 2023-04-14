# main
import gmwhale
import pricetrack
import fn
import setup_var as sv
import fn_stock

def main():
    while True:
        if fn.time_next_day():
            fn.delay(60) #cool down
            gmwhale.gmwhale()
            fn.delay(2)
            fn.get_report_crypto()
            fn.delay(2)
            fn_stock.get_report_stock()
            fn.delay(2)
            fn_stock.get_exchangerate()
            fn.delay(2)
        if fn.bar_time(sv.interval_candle,fn.time_server()):
            fn.delay(60)
            pricetrack.pricetrack()
        fn.delay(1)

if __name__ == "__main__":
    main()