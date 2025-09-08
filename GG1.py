from telethon import TelegramClient, events
from tvDatafeed import TvDatafeed, Interval
from tradingview_ta import TA_Handler
import re
from datetime import datetime

# ================== TELEGRAM BOT CONFIG ==================
bot_token = "7607635182:AAF8sS709kYn7FEYVK2aUOJTre1wSIZnKV8"  # replace with your bot token


client = TelegramClient('XAU2GC1bot', api_id=27423887, api_hash='b85d9b97e033ba7555a5a00e966e5f05').start(bot_token=bot_token)

# Replace these with numeric IDs of your groups
source_group = -1002907509976   # my sample Source group ID
#source_group = -1002615747847   # Gold signal Ali Morad Alian Source group ID 
#target_group = -1002617549397   # Target group ID GC1SIG group
target_group = -1002951018732 
chrome = "C:/CHDRV/chromedriver.exe"  # adjust your path
username = "MR_COIN712"
password = "Tavangar@2025"


# ---------------- LOGIN ----------------
tv = TvDatafeed(username=username, password=password)


# ================== TRADINGVIEW CONFIG ==================
# Create a TvDatafeed instance (guest mode)
tv = TvDatafeed("MR_COIN712","XXXXXXXXX")  # or TvDatafeed(username, password) if you have a TradingView account

symbol1 = 'GC1!'
exchange1 = 'COMEX'
symbol2 = 'XAUUSD'
exchange2 = 'OANDA'

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    c1 = TA_Handler(
        symbol="GC1!",
        screener="futures",   # screener (crypto, forex, stock, futures, etc.)
        exchange="COMEX",     # exchange (match TradingView)
        interval=Interval.INTERVAL_1_MINUTE
    )

    analysis = gc1.get_analysis()
    price = analysis.indicators["close"]

    print("GC1! live price:", price)


# ================== RUN THE BOT ==================

@client.on(events.NewMessage(chats=source_group))
async def handler(event):
    message = event.message.message
    print("Message received:", message)
    try:
        df1 = tv.get_hist(symbol1, exchange1, interval=Interval.in_1_minute, n_bars=1)   
        GC_price = df1.iloc[-1].close
        df2 = tv.get_hist(symbol2, exchange2, interval=Interval.in_1_minute, n_bars=1)   
        XAU_price = df2.iloc[-1].close        
        df = tv.get_hist(symbol1, exchange1, interval=Interval.in_1_minute, n_bars=1)
        live_price = df.iloc[-1].close
    except Exception as e:
        live_price = "N/A"
        print("Error fetching GC1! or XAU price:", e)
    if "Buy AT" in message:
        print("Trade signal detected!")   
        Order_message = 1
        # Extract numbers from the message
        numbers = re.findall(r"\d+", message)
       
        sl_match = re.search(r"SL:\s*(\d+\.?\d*)", message)
        tp_match = re.search(r"TP:\s*(\d+\.?\d*)", message)        
        Buy_match = re.search(r"Buy AT\s*(\d+\.?\d*)", message)

        sl_value = float(sl_match.group(1)) if sl_match else None
        tp_value = float(tp_match.group(1)) if tp_match else None
        Buy_Value = float(Buy_match.group(1)) if Buy_match else None
        tp_values = [float(v) for v in re.findall(r"✅\s*(\d+\.?\d*)", message)]
        Buy_Value = Buy_Value + float(GC_price - XAU_price) if Buy_match else None
        sl_value = (Buy_Value) - (sl_value/100)
        print("Take Profit values individually:")
        for i, tp in enumerate(tp_values, start=1):
               # tp = tp+10
                print(f"TP{i}: {tp}")
        print("Take Profit values:", tp_values)
       #
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modified_message = (
              f"🕒 Processed at: {timestamp}\n\n"
              f"📌 Original: {message}\n\n"
              f"💰 GC1! Live: {live_price}\n\n"
              f"GC1! Converted values..........\n\n"
              f"Buy Entry Value: {Buy_Value} \n\n"             
        #  f"Other numbers found:\n{numbers_str}"
            )
        for i, tp in enumerate(tp_values, start=1):
                tp = tp + float(GC_price - XAU_price)
                modified_message += f"✅TP{i}: {tp}\n"
        modified_message +=  f"SL: {sl_value}\n\n"        

        try:
           await client.send_message(target_group, modified_message)
           print("Message forwarded successfully!")
        except Exception as e:
           print("Failed to forward message:", e)
    if "SELL AT" in message:
        print("Trade signal detected!")   
        Order_message = 2
            # Extract numbers from the message
        numbers = re.findall(r"\d+", message)
       
        sl_match = re.search(r"SL:\s*(\d+\.?\d*)", message)
        tp_match = re.search(r"TP:\s*(\d+\.?\d*)", message)        
        Sell_match = re.search(r"SELL AT\s*(\d+\.?\d*)", message)

        sl_value = float(sl_match.group(1)) if sl_match else None
        tp_value = float(tp_match.group(1)) if tp_match else None
        Sell_Value = float(Sell_match.group(1)) if Sell_match else None
        tp_values = [float(v) for v in re.findall(r"✅\s*(\d+\.?\d*)", message)]
        Sell_Value = Sell_Value + float(GC_price - XAU_price)
        s2_value = (sl_value/100) + Sell_Value
        print("SL value",sl_value)
        print("SL value",sl_value/100)
        print("SeeL value",Sell_Value)
        
        print("SL value+Sell_Value",sl_value/100+Sell_Value)
        
        
        print("Take Profit values individually:")
        for i, tp in enumerate(tp_values, start=1):
                # tp = tp+10
                  print(f"TP{i}: {tp}")
        print("Take Profit values:", tp_values)
        #
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modified_message = (
                f"🕒 Processed at: {timestamp}\n\n"
                f"📌 Original: {message}\n\n"
                f"💰 GC1! Live: {live_price}\n\n"
                f"GC1! Converted values..........\n\n"
                f"Sell Entry Value: {Sell_Value:.02f} \n\n"             
            #  f"Other numbers found:\n{numbers_str}"
                )
        for i, tp in enumerate(tp_values, start=1):
                    tp = tp - float(GC_price - XAU_price)
                    modified_message += f"✅TP{i}: {tp}\n"
        modified_message +=  f"SL: {s2_value}\n\n"
        
        try:
            await client.send_message(target_group, modified_message)
            print("Message forwarded successfully!")
        except Exception as e:
            print("Failed to forward message:", e)
    if "pip" in message:
            match = re.search(r'(\d+)pip✅', message, re.IGNORECASE)
            if match:
                number = int(match.group(1))            
                modified_message = f"{number}tick ✅\n"
                try:
                    await client.send_message(target_group, modified_message)
                    print("Message forwarded successfully!")
                except Exception as e:
                    print("Failed to forward message:", e)
    if "Tp1" in message:
            match = re.search(r'\d+', message)
            number = int(match.group())   
            number = number + float(GC_price - XAU_price)         
            modified_message = f"{number}TP1 ✅\n"
            try:
                await client.send_message(target_group, modified_message)
                print("Message forwarded successfully!")
            except Exception as e:
                print("Failed to forward message:", e)
    if "Tp2" in message:
            match = re.search(r'\d+', message)
            number = int(match.group())   
            number = number + float(GC_price - XAU_price)         
            modified_message = f"{number}TP2 ✅\n"          
            try:
                await client.send_message(target_group, modified_message)
                print("Message forwarded successfully!")
            except Exception as e:
                print("Failed to forward message:", e)
    if "Tp4" in message:
            match = re.search(r'\d+', text)
            number = int(match.group())   
            number = number + float(GC_price - XAU_price)         
            modified_message = f"{number}TP3 ✅\n"            
            try:
                await client.send_message(target_group, modified_message)
                print("Message forwarded successfully!")
            except Exception as e:
                print("Failed to forward message:", e)
                
    if not any(word in message for word in ["XAUUSD", "Tp1", "Tp2", "Tp3", "pip"]):
        print("⚠️ No trade signal (ignored)")
# ================== RUN THE BOT ==================
print("🚀 Bot is running...")
client.run_until_disconnected()
