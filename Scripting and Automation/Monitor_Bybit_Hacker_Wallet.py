import time
import requests
import os

# API Configuration
ETHERSCAN_API_KEY = ""
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# HackScan URL for wallets
HACKSCAN_URL = "https://hackscan.hackbounty.io/public/hack-address.json"

# Path to the file where wallets are saved
WALLETS_FILE = ""

# ✅ Function: Save wallets to file
def update_wallets():
    try:
        response = requests.get(HACKSCAN_URL, timeout=10)
        response.raise_for_status()
        wallets = response.json()

        # Filter invalid wallets
        valid_wallets = [w for w in wallets if w.startswith("0x") and len(w) == 42]

        if valid_wallets:
            with open(WALLETS_FILE, "w") as f:
                f.write("\n".join(valid_wallets))
            print(f"✅ {len(valid_wallets)} wallets saved to {WALLETS_FILE}")
        else:
            print("⚠️ No valid wallets found!")
    except Exception as e:
        print(f"⚠️ Error updating wallets: {e}")

# ✅ Function: Read wallets from file
def get_wallets_from_file():
    if os.path.exists(WALLETS_FILE):
        with open(WALLETS_FILE, "r") as f:
            wallets = [line.strip() for line in f.readlines() if line.strip()]
        return wallets
    return []

# ✅ Function: Get transactions for a wallet
def get_transactions(wallet_address):
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY
    }
    
    try:
        response = requests.get("https://api.etherscan.io/api", params=params)
        response_json = response.json()
        
        if response_json.get("status") == "1":
            return response_json["result"]
        else:
            print(f"⚠️ No transactions found for {wallet_address}")
            return []
    except Exception as e:
        print(f"⚠️ Error fetching transactions for {wallet_address}: {e}")
        return []

# ✅ Function: Check transactions and send alerts
def check_wallets():
    wallets = get_wallets_from_file()
    
    if not wallets:
        print("⚠️ No wallets found in file!")
        return

    for wallet in wallets:
        time.sleep(0.2)  # Pause to avoid API rate-limit
        transactions = get_transactions(wallet)

        for tx in transactions:
            timestamp = int(tx["timeStamp"])
            value_eth = int(tx["value"]) / 10**18  # Convert from Wei to ETH

            # Check if transaction is recent and over 1 ETH
            if (time.time() - timestamp < 3600) and (value_eth >= 1.0):
                message = f"""
🚨 New Transaction Alert 🚨
To: {tx['to']}
Amount: {value_eth:.4f} ETH
TX Hash: {tx['hash']}
"""
                send_telegram_message(message)

# ✅ Function: Send message on Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

# 🔄 Update wallets at startup!
update_wallets()

# 🔄 Main loop: Check transactions based on the file
while True:
    check_wallets()  # Check transactions for saved wallets
    time.sleep(3600)  # Wait 1 hour before the next check
