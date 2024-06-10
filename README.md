# TRX Transactions Viewer

<p align="center">
  <img src="https://raw.githubusercontent.com/sayh3x/TRX-Transactions-Viewer/main/assets/main.webp" style="max-width: 100%; height: auto;" alt="TRX Transactions Viewer Logo">
</p>

TRX Transactions Viewer is a Python script designed to check the balance of a Tron (TRX) wallet and retrieve transaction information. This tool interacts with the TronScan API to provide detailed insights into wallet activity and balance.

## Features

- Check Tron wallet balance.
- Retrieve and display wallet transactions.
- Convert TRX balance to USD using real-time exchange rates from CoinGecko.
- Log and handle errors gracefully.
- Set terminal title to reflect current operations.

## Requirements

- Python 3.x
- `requests` library
- `colorama` library
- `pyfiglet` library
- `python-dotenv` library

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sayh3x/trx-transactions-viewer.git
    cd trx-transactions-viewer
    ```

2. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your TronScan API key (if required):

    - Create a `.env` file in the root directory of the project.
    - Add your TronScan API key to the `.env` file:

      ```env
      TRONSCAN_API_KEY=your_tronscan_api_key_here
      ```

## Usage

1. Run the script:

    ```bash
    python trx_transactions_viewer.py
    ```

2. Enter the Tron wallet address when prompted.

   The script will output the received transactions, wallet balance, and the balance converted to USD.

3. Save 

   Enter `save` after entering the wallet or press `ctrl+c`.

4. Delete Transactions File

   To delete, enter `del` or `rem` in the input script.

## Example

Here is an example of the script in action:

![Run](https://raw.githubusercontent.com/sayh3x/TRX-Transactions-Viewer/main/assets/trx_work.gif)


```bash
$ python trx_transactions_viewer.py
Enter TRC-20 Wallet : TVjsRYYxJ4k3s23SxPsQiRsq3EegSsdEgG
2024-06-06 06:38:46,169 - INFO - Checking wallet transactions...
2024-06-06 06:38:53,121 - INFO - Received Transactions:

---------------------'TGzz8gjYiYRqpfmDwnLxfgPuLVNmpCswVp'--------------------

Send Value: 100 TRX
TRX Balance: 500 TRX
Convert TRX to USD: 50 USD

------------------------------------------------------------------------------------

---------------------'TXJdXuF3Xf6d59RrGtd5dxNzygfMhX6sEt'--------------------

Send Value: 200 TRX
TRX Balance: 1000 TRX
Convert TRX to USD: 100 USD

------------------------------------------------------------------------------------
```
## Troubleshooting

If you encounter any errors while running the code, here are some potential problems and solutions:

### Problem: Network or Connectivity Issues
**Cause**: The code may fail to execute properly due to network connectivity issues.  
**Solution**: Ensure that you have a stable internet connection. Check your network settings and try accessing other websites to verify your connection.

### Problem: API Endpoint Issues
**Cause**: The code may encounter errors if there is an issue with the API endpoint, such as TronScan.org.  
**Solution**:

- **Check the API Status**: Visit the TronScan.org status page to check if the API service is operational.
- **Verify the API URL**: Ensure that the API endpoint URL in your code is correct.
- **Inspect API Key**: If your API requires an API key, ensure that it is valid and has the necessary permissions.

### Problem: Wallet Address Issues
**Cause**: Errors can occur if the wallet address provided is incorrect or not formatted properly.  
**Solution**:

- **Verify the Wallet Address**: Double-check the wallet address to ensure it is correct and follows the required format.
- **Validate Address Format**: Ensure that the wallet address conforms to the expected format for the specific blockchain (e.g., Tron addresses should start with 'T').

### Example Check:

```sh
# Check internet connectivity
ping -c 4 google.com

# Check API endpoint status
curl -I https://api.tronscan.org/api

# Validate Tron wallet address format
if [[ $wallet_address =~ ^T[a-zA-Z0-9]{33}$ ]]; then
    echo "Valid wallet address"
else
    echo "Invalid wallet address"
fi
```

# Show youre sopport

If you like this project, please consider giving it a star ⭐ on GitHub
