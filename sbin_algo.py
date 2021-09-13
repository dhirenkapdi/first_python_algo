import fyers_login
import datetime
import pandas as pd
import time
import pdb

fyers = fyers_login.fyers


from_date = '2021-09-09'
to_date = '2021-09-09'
# from_date = datetime.datetime.now().strftime('%Y-%m-%d')
# to_date = datetime.datetime.now().strftime('%Y-%m-%d')

global entry_time, exit_time, current_time

entry_time = datetime.time(12, 30)
exit_time = datetime.time(12,35)
current_time = datetime.datetime.now().time()

def orb_data():
    data = {"symbol":"NSE:SBIN-EQ","resolution":"60","date_format":"1","range_from":from_date,"range_to":to_date,"cont_flag":"1"}
    df = fyers.fyers.history(data)['candles']
    df = pd.DataFrame(df,None,['datetime','open','high','low','close','vol'])
    df['datetime'] = df['datetime'].apply(lambda x:datetime.datetime.fromtimestamp(x))
    orb_high = df['high'].iloc[0]
    orb_low = df['low'].iloc[0]
    return(orb_high, orb_low)

def place_order():
    
    print('wating for trade time...')
    status={}
    while True:
        time.sleep(1)
        current_time = datetime.datetime.now().time()

        if (current_time >= entry_time) and ('traded' not in status):
            print('order placed successful')
            status['traded'] = 'bought'

            risk_point = round((orb_data()[0]) - (orb_data()[1]),2)
            max_loss = 2200
            quantity = int(max_loss/risk_point)

            buy_order_data = {
                "symbol":"NSE:SBIN-EQ",
                "qty":quantity,
                "type":4,
                "side":1,
                "productType":"INTRADAY",
                "limitPrice":round(orb_data()[0]+0.40,2),
                "stopPrice":round(orb_data()[0]+0.10,2),
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":"False",
                "stopLoss":0,
                "takeProfit":0}
            print(fyers.fyers.place_order(buy_order_data))
            

            sell_order_data = {
                "symbol":"NSE:SBIN-EQ",
                "qty":quantity,
                "type":4,
                "side":-1,
                "productType":"INTRADAY",
                "limitPrice":round(orb_data()[1]-0.40,2),
                "stopPrice":round(orb_data()[1]-0.10,2),
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":"False",
                "stopLoss":0,
                "takeProfit":0}
            print(fyers.fyers.place_order(sell_order_data))


            status.update({'name':'SBIN','quantity':quantity})

        if (current_time >= exit_time) and ('traded' in status):
                    print('exited form all position')
                    print('have a good day...')
                    break


if __name__ == '__main__':
    orb_data()
    place_order()