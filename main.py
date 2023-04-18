# main
import gmwhale
import pricetrack
import fn
import fn_stock

def main():
    bar_time_len = 0
    while True:
        if bar_time_len <= 2:
            bar_time = fn.genTimeInterval()
            bar_time_len = len(bar_time)
        if fn.time_next_day():
            fn.delay(60)
            gmwhale.gmwhale()
            fn.get_report_crypto()
            fn.delay(2)
            fn_stock.get_report_stock()
            fn.delay(2)
            fn_stock.get_exchangerate()
            fn.delay(2)
        
        timenow = fn.datetimeUtcNow()
        for i in range(bar_time_len):
            if (timenow >= bar_time[i]) and (timenow < bar_time[i+1]):
                fn.delay(60)
                pricetrack.pricetrack()
                bar_time.pop(i)
            break
        fn.delay(1)

if __name__ == "__main__":
    main()