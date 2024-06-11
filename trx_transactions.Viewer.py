# import library
from dotenv import load_dotenv
from colorama import Fore
import pyfiglet as pyg
import time, os, requests, logging, webbrowser, sys, shutil

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set TRONSCAN_API_KEY using environment variable or default value
TRONSCAN_API_KEY = os.getenv('TRONSCAN_API_KEY')

VERSION = "1.0.1"
GITHUB_URL = "https://github.com/sayh3x/TRX-Transactions-Viewer"

received_transactions = []
wallet_address = ""
trx_to_usd_rate = 0
is_checking_transactions = False

# Function for Clear Terminal 
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def log_and_animate(message, duration=3, interval=0.5, level='INFO', mote='.'):
    log_message = f'{time.strftime("%Y-%m-%d %H:%M:%S")} - {level} - {message}'
    print(log_message, end='', flush=True)

    end_time = time.time() + duration
    while time.time() < end_time:
        for dots in range(4):
            sys.stdout.write(f'\r{log_message}{mote * dots}{" " * (3 - dots)}')
            sys.stdout.flush()
            time.sleep(interval)
    sys.stdout.write(f'\r{log_message}{mote * 3}\n')
    sys.stdout.flush()

# Check Target TRX Balance with api.tronscan.org  
def check_trx_balance(address, retries=3, delay=5):
    api_url = f"https://api.tronscan.org/api/account?address={address}"

    for attempt in range(retries):
        try:
            response = requests.get(api_url)
            data = response.json()

            if 'balance' in data:
                balance = int(data["balance"]) / 1e6
                return balance
            else:
                logging.error("Error getting balance: %s", data.get("message", "Unknown error"))
                return 0
        except Exception as e:
            if attempt < retries - 1:
                logging.error(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
                return 0

# Get Wallet Transactions
def get_wallet_received_transactions(wallet_address):
    url = f"https://api.tronscan.org/api/transaction?address={wallet_address}&limit=50&sort=-timestamp"
    
    try:
        response = requests.get(url)
        data = response.json()

        if 'data' in data:
            transactions = data["data"]
            received_transactions = [{"value": tx["amount"], "to": tx["toAddress"], "tx_hash": tx["hash"], "from": tx["ownerAddress"], "timestamp": tx["timestamp"]} for tx in transactions if tx["toAddress"] == wallet_address]
            return received_transactions
        else:
            logging.error("Error: %s", data.get("message", "Unknown error"))
            return None
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return None

# Get TRX price with api.coingecko.com api
def get_tron_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=tron&vs_currencies=usd")
        data = response.json()
        tron_price = data["tron"]["usd"]
        return tron_price
    except Exception as e:
        logging.error("Error fetching Tron price: %s", str(e))
        return None

# Convert trx to usd with api
def convert_to_usd(trx_amount, trx_to_usd_rate):
    return trx_amount * trx_to_usd_rate

# Add title for terminal
def set_terminal_title(title):
    os.system(f"echo -n \"\\033]0;{title}\\007\"")

# View output in terminal 
def display_transactions(transactions, trx_to_usd_rate):
    for tx in transactions:
        value_in_trx = int(tx["value"]) / 1e6
        usd_value = convert_to_usd(value_in_trx, trx_to_usd_rate)
        lower_sender_address = tx["from"]
        len_address = len(lower_sender_address)
        mid_point = len_address // 2

        balance = check_trx_balance(address=lower_sender_address)
        balance_in_usd = convert_to_usd(balance, trx_to_usd_rate)

        set_terminal_title(f"Sender Address: {lower_sender_address}")

        print()
        for i in range(len_address):
            if i == mid_point:
                print(f"'{lower_sender_address}'", end='')
            else:
                print('-', end='')
        print('\n')
        print(f"Send Value: {value_in_trx} TRX")
        print(f"TRX Balance: {balance}")
        print(f"Convert TRX to USD: {balance_in_usd}\n")

        print("-" * (len_address * 2))
        print()
# Function for fast save Transactions file
def save_transactions(transactions, trx_to_usd_rate, privios):
    log_and_animate(f'Save transactions in {privios}.txt ', level='Waiting', mote='#')
    if not os.path.exists('trx_log'):
        os.makedirs('trx_log')
                
    with open(os.path.join('trx_log', f'{privios}.txt'), 'w') as file:
        for tx in transactions:
            value_in_trx = int(tx["value"]) / 1e6
            usd_value = convert_to_usd(value_in_trx, trx_to_usd_rate)
            file.write(f"Transaction Hash: {tx['tx_hash']}\n")
            file.write(f"Value: {value_in_trx} TRX\n")
            file.write(f"Value in USD: {usd_value}\n")
            file.write(f"From: {tx['from']}\n")
            file.write(f"To: {tx['to']}\n")
            file.write(f"Timestamp: {tx['timestamp']}\n")
            file.write("\n")
# Check Main Wallet Transaction
def check_wallet(text_input='Enter TRC-20 Wallet (enter 0 to visit GitHub): ', privios=None):
    global received_transactions, wallet_address, trx_to_usd_rate, is_checking_transactions

    print(Fore.GREEN)
    try:
        wallet_address = input(text_input); print(Fore.RESET)
        # Open Github repository 
        if wallet_address == '0':
            clear()
            log_and_animate("Opening GitHub repository ", level='Waiting', mote='*', duration=1)
            webbrowser.open(GITHUB_URL)
            check_wallet(text_input='Enter TRC-20 Wallet for exit(Enter 00): ')
        # Delet Transactions save folder
        elif wallet_address == 'del' or wallet_address == 'rem':
            log_and_animate('Removing ', level='Waiting', mote=';D')
            dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trx_log')
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                main(sayh3x=f"Folder {dir_path} has been removed.")
            else:
                main(sayh3x="i Can't find 'trx_log' folder")
        # Exit in Script 
        elif wallet_address == 'exit' or wallet_address == '00':
            clear()
            log_and_animate(Fore.YELLOW + "Bye ;", level='Exit', mote=')')
            sys.exit()
        # Save Transactions in file
        elif wallet_address == 'save':
            if received_transactions:
                save_transactions(received_transactions, trx_to_usd_rate, privios=privios)
                main(sayh3x=f"Save in path {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trx_log')}")
            else:
                main(sayh3x='Please Enter address wallet\r\nand after enter wallet enter "save".')

        log_and_animate('Checking wallet transactions')
        is_checking_transactions = True

        received_transactions = get_wallet_received_transactions(wallet_address)
        if received_transactions:
            logging.info("Received Transactions:")
            trx_to_usd_rate = get_tron_price() or 0
            display_transactions(received_transactions, trx_to_usd_rate)
            generate_logo(text_info=f'{Fore.GREEN}Completed enter "save" {Fore.RED}!!!{Fore.RESET}')
            check_wallet(privios=wallet_address)
        else:
            log_and_animate("No transactions found or 'Check Api Key'", level='Problem', mote='!')
    
    except KeyboardInterrupt:
        generate_logo(text_info='For Exit Enter "exit" or File"save"')
        check_wallet(text_input='Enter TRC-20 Wallet: ', privios=wallet_address)
    finally:
        is_checking_transactions = False

# Add Logo in terminal 
def generate_logo(text_info=''):
    clear()
    logo = pyg.figlet_format('TRX Viewer', font='slant')
    print(Fore.RED + logo + Fore.RESET)
    
    if len(text_info) > 0:
        print(Fore.RED+f'\n{text_info}\n')

    print(Fore.RED + "𝘋𝘦𝘷𝘦𝘭𝘰𝘱𝘦𝘥 𝘣𝘺 𝙃3𝙓" + Fore.RESET)
    print(Fore.YELLOW + "Version: " + VERSION + Fore.RESET)

# Main Function
def main(sayh3x=''):
    generate_logo(text_info=sayh3x)
    check_wallet()

# Run
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess stopped by user (Ctrl+C)")
        sys.exit()
