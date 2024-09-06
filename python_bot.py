import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# List of USDT currency pairs
array_USDT = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'BCCUSDT']

# List of currency pairs between cryptocurrencies
array_coins = [
    'ETHBTC',  # Ethereum to Bitcoin
    'BNBBTC',  # Binance Coin to Bitcoin
    'LTCBTC',  # Litecoin to Bitcoin
    'BNBETH',  # Binance Coin to Ethereum
    'LTCETH',  # Litecoin to Ethereum
    'XMRBTC',  # Monero to Bitcoin
    'ETCBTC',  # Ethereum Classic to Bitcoin
]

# Function to extract base and quote currencies
def extract_base_quote(pair):
    base = pair[:3]
    quote = pair[3:]
    return base, quote

# Function to fetch price data from Binance API
def get_binance_prices():
    url = 'https://api.binance.com/api/v3/ticker/price'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve data from Binance API. Error: {e}")
        return None

# /start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Enter the command /calculate <initial balance in USDT> to start the calculation.')

# /calculate command handler
async def calculate(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Please enter the initial balance in USDT after the /calculate command.')
        return

    try:
        initial_balance = float(context.args[0])
    except ValueError:
        await update.message.reply_text('Invalid balance format. Please enter a valid number.')
        return

    prices_data = get_binance_prices()

    if prices_data:
        prices = {item['symbol']: float(item['price']) for item in prices_data}
        connections = []

        for usdt_pair in array_USDT:
            base_usdt, quote_usdt = extract_base_quote(usdt_pair)

            for coin_pair in array_coins:
                base_coin, quote_coin = extract_base_quote(coin_pair)

                if base_usdt == base_coin and (quote_coin + 'USDT') in array_USDT:
                    intermediate_pair = quote_coin + 'USDT'
                    connections.append((usdt_pair, coin_pair, intermediate_pair,
                                        prices[usdt_pair], prices[coin_pair], prices[intermediate_pair]))
                elif base_usdt == quote_coin and (base_coin + 'USDT') in array_USDT:
                    intermediate_pair = base_coin + 'USDT'
                    connections.append((usdt_pair, coin_pair, intermediate_pair,
                                        prices[usdt_pair], prices[coin_pair], prices[intermediate_pair]))
                elif quote_usdt == base_coin and (quote_coin + 'USDT') in array_USDT:
                    intermediate_pair = quote_coin + 'USDT'
                    connections.append((usdt_pair, coin_pair, intermediate_pair,
                                        prices[usdt_pair], prices[coin_pair], prices[intermediate_pair]))
                elif quote_usdt == quote_coin and (base_coin + 'USDT') in array_USDT:
                    intermediate_pair = base_coin + 'USDT'
                    connections.append((usdt_pair, coin_pair, intermediate_pair,
                                        prices[usdt_pair], prices[coin_pair], prices[intermediate_pair]))

        final_balance = initial_balance
        results = []

        for connection in connections:
            usdt_pair, coin_pair, final_pair, price_usdt_pair, price_coin_pair, price_final_pair = connection
            balance = initial_balance

            if usdt_pair.endswith('USDT'):
                balance /= price_usdt_pair
            else:
                balance *= price_usdt_pair

            if coin_pair.startswith(extract_base_quote(usdt_pair)[0]):
                balance *= price_coin_pair
            else:
                balance /= price_coin_pair

            if final_pair.endswith('USDT'):
                balance *= price_final_pair
            else:
                balance /= price_final_pair

            profit = balance - initial_balance

            if profit > 0:
                final_balance = balance
                profit_percentage = (profit / initial_balance) * 100
                results.append(
                    f"{usdt_pair} ({price_usdt_pair}) -> {coin_pair} ({price_coin_pair}) -> {final_pair} ({price_final_pair}) = {balance:.2f} USDT (Profit: {profit:.2f} USDT, {profit_percentage:.2f}%)"
                )

        if results:
            await update.message.reply_text('\n'.join(results) + f"___________________")
        else:
            await update.message.reply_text('No profitable connections found.')
    else:
        await update.message.reply_text(
            "Failed to retrieve data from Binance API. Please check your connection or API availability.")

def main():
    # Replace 'YOUR_TOKEN' with your bot token
    application = Application.builder().token("YOUR_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("calculate", calculate))

    application.run_polling()

if __name__ == '__main__':
    main()
