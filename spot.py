from binance.spot import Spot as Client
import pandas as pd
import time
import requests

def telegramBotSendText(botMessage,id):
    botToken="6070522686:AAEtYoImDUpyOyWl2JiHrWD6GsuDdg2qEZQ" #BotFather'!
    url="https://api.telegram.org/bot"+botToken+"/sendMessage?chat_id="+str(5675598221)+"&parse_mode=Markdown&text="+botMessage
    response=requests.get(url)
    return response.json()

id=5675598221
spot_client=Client("apiKey","secretKey")

#borsa verileri
def exchangeInfo(coinName:str ):
    exc=spot_client.exchange_info(symbol=str(coinName))
    return exc

#mum verileri:
def spotKlinesCoin(coinName:str ,period:str, limit: int=None):
    kline=spot_client.klines(symbol=str(coinName),interval=str(period),limit=limit)
    return kline

def spotAllSymbols():
    response=spot_client.exchange_info()
    return list(map(lambda symbol:symbol["symbol"],response["symbols"]))

spotUsdtList=[]
for coin in spotAllSymbols():
    if "USDT" in coin and "UP" not in coin and "DOWN" not in coin:
        spotUsdtList.append(coin)
    else:
        pass

def spotsymbolsData(coinName:str,period:str,limit:int):
    kline=spotKlinesCoin(coinName=coinName,period=period,limit=limit)
    converted=pd.DataFrame(kline,columns=['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat',
                                      'tbbav', 'tbqav',
                                      'ignore'], dtype=float)
    return converted

def spotTarama(coinList):
    gucluSpotAlis = []
    zayifSpotAlis = []
    while True:
        try:
            for coin in coinList:
                data = spotsymbolsData(coinName=coin, period="15m", limit=21)
                avrg= sum(data["vol"])/ len(data["vol"])
                vol= data["vol"]
                open= data["open"]
                close= data["close"]
                low= data["low"]

                if vol[len(data.index)-2]> (avrg*1.5) and close[len(data.index)-2]> open[len(data.index)-2] and open[len(data.index) - 2] == low[len(data.index) - 2] and open[len(data.index) - 3] > close[len(data.index) - 3]:
                    gucluSpotAlis.append(coin)

                if vol[len(data.index)-2]< (avrg*0.5) and close[len(data.index)-2]> open[len(data.index)-2] and open[len(data.index) - 2] == low[len(data.index) - 2] and open[len(data.index) - 3] > close[len(data.index) - 3]:
                    zayifSpotAlis.append(coin)

        except :
            pass
        if len(gucluSpotAlis)!=0:
            telegramBotSendText(f"Güçlü Spot Alış Sinyali Olan Coinler 💵 : {gucluSpotAlis}", id)
        else:
            pass
        if len(zayifSpotAlis)!=0:
            telegramBotSendText(f"Zayıf Spot Alış Sinyali Olan Coinler 💵 : {zayifSpotAlis}", id)
        else:
            pass
        gucluSpotAlis.clear()
        zayifSpotAlis.clear()
        time.sleep(900)

spotTarama(spotUsdtList)