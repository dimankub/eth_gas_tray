# ETH Gas Tray

A minimalistic utility for displaying Ethereum gas prices in the system tray.

## Description

- Shows a tray icon with the current Slow gas price (gwei).
- Hovering displays Rapid, Normal, and Slow gas values.
- Prices update every minute.
- If the gas price is too high (>99 gwei), the default ETH icon is shown.

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/dimankub/eth-gas-tray.git
cd eth-gas-tray
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python eth_gas_tray.py
```