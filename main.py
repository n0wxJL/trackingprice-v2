# main
import gmwhale
import pricetrack
import fn
import setup_var as sv
import fn_stock

def main():
    # add call fn between the day
    bar_time = fn.genTimeInterval()
    while True:
        if fn.time_next_day():
            gmwhale.gmwhale()
            fn.delay(60)
            fn.get_report_crypto()
            fn.delay(2)
            fn_stock.get_report_stock()
            fn.delay(2)
            fn_stock.get_exchangerate()
            fn.delay(2)
        
        timenow = fn.datetimeUtcNow()
        bar_time_len = len(bar_time)
        for i in range(bar_time_len):
            if (timenow >= bar_time[i]) and (timenow < bar_time[i+1]):
                pricetrack.pricetrack()
                bar_time.pop(i)
                break

        fn.delay(1)

if __name__ == "__main__":
    main()