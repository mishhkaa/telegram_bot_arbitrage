Binance Arbitrage Bot
This is a Telegram bot designed to calculate potential arbitrage opportunities between various cryptocurrency pairs on the Binance exchange. Users can input their initial balance in USDT, and the bot will search for profitable connections between different currency pairs based on current market prices retrieved from the Binance API.

Features:
Supports USDT and major cryptocurrency pairs like BTC, ETH, BNB, and others.
Fetches real-time price data from the Binance API.
Identifies arbitrage opportunities by connecting currency pairs across different markets.
Simple and easy-to-use Telegram commands.
How It Works:
The bot listens for the /calculate <initial_balance_in_USDT> command.
It retrieves the latest market prices for a predefined set of cryptocurrency pairs from Binance.
The bot searches for potential arbitrage opportunities by analyzing possible pair connections.
If a profitable opportunity is found, it calculates the potential profit and returns the details to the user.
Telegram Commands:
/start: Start interacting with the bot and get a welcome message.
/calculate <balance>: Perform arbitrage calculations based on your initial balance in USDT.
Prerequisites:
Python 3.x
python-telegram-bot library
Binance API access
Setup Instructions:
Clone the repository.
Install the required libraries: pip install -r requirements.txt.
Replace the placeholder YOUR_TOKEN in the code with your Telegram bot token.
Run the bot with python bot.py.
