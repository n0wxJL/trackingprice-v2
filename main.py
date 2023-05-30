# main
import gmwhale
import pricetrack
import fn
import fn_stock
import setup_var as sv

def main():
    while True:
        if fn.time_next_day():
            fn.delay(60)
            gmwhale.gmwhale()
            fn.get_report_crypto_v2()
            fn.delay(2)
            fn.get_report_crypto_v2()
            fn.delay(2)
            fn_stock.get_exchangerate()
            fn.delay(2)
            fn_stock.topyield()
        if fn.alert_price(sv.interval_candle,fn.datetimeUtcNow()):
            fn.delay(60)
            print('Pricetrack')
            pricetrack.pricetrack()
        fn.delay(1)

if __name__ == "__main__":
    main()