from libs.coin.coinone.coinone import CoinOne 



def run(currency):
    bound = 30

    coin = CoinOne()
    recent_complete_orders = coin.get_recent_complete_orders(currency=currency)


    most_recent_time = max([ row['timestamp'] for row in recent_complete_orders])
    most_recent_orders = [row for row in recent_complete_orders if row['timestamp'] > most_recent_time - bound] 

    print(most_recent_orders)

    


if __name__=='__main__':
    currency = 'eth'
    run(currency=currency)



    

