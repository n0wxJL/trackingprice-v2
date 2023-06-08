# main
import gmwhale
import pricetrack
import fn
import fn_stock
import setup_var as sv
import lib

def main():
    while True:
        if fn.time_next_day():
            fn.delay(300)
            gmwhale.gmwhale()
            fn.delay(2)
            fn.get_report_crypto_v2()
            fn.delay(2)
            fn_stock.get_report_stock_v2()
            fn.delay(2)
            if lib.nameOfWeek() == 'Monday':
                fn_stock.topyield()
            fn.delay(2)
            fn_stock.get_exchangerate()
        if fn.alert_price(sv.interval_candle,fn.datetimeUtcNow()):
            fn.delay(60)
            pricetrack.pricetrack()
        fn.delay(1)

if __name__ == "__main__":
    main()