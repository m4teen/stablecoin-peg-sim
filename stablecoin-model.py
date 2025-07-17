"""
stablecoin_model.py

Minimal script version of the Stablecoin Peg Simulator.
Saves plots to disk when run in a non-interactive (headless) environment.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Default parameters
LIQUIDATION_THRESHOLD = 1.5
MIN_PEG_PRICE = 0.80
CONFIDENCE_DECAY = 0.01
DAYS = 30
COLLATERAL_AMOUNT = 1000  # units of ETH

def simulate_stablecoin_peg(initial_collateral_price, price_drop_per_day, stablecoin_supply, days=DAYS):
    """
    Simulates stablecoin peg behavior under declining collateral price.

    Returns:
        collateral_ratios (list of float)
        peg_prices (list of float)
    """
    collateral_ratios = []
    peg_prices = []
    market_price = 1.00

    for day in range(days):
        collateral_price = max(0.01, initial_collateral_price - price_drop_per_day * day)
        collateral_value = collateral_price * COLLATERAL_AMOUNT
        cratio = collateral_value / stablecoin_supply

        if cratio < LIQUIDATION_THRESHOLD:
            market_price = max(MIN_PEG_PRICE, market_price - CONFIDENCE_DECAY)

        collateral_ratios.append(cratio)
        peg_prices.append(market_price)

    return collateral_ratios, peg_prices

def plot_results(collateral_ratios, peg_prices, title_prefix):
    """
    Saves the collateral ratio and peg price plots to the images/ directory.
    """
    os.makedirs("images", exist_ok=True)

    # Collateral Ratio plot
    plt.figure(figsize=(12, 4))
    plt.plot(collateral_ratios, label='Collateral Ratio')
    plt.axhline(y=LIQUIDATION_THRESHOLD, color='r', linestyle='--', label='Liquidation Threshold')
    plt.title(f'{title_prefix} - Collateral Ratio')
    plt.xlabel('Day')
    plt.ylabel('Collateral Ratio')
    plt.legend()
    plt.grid(True)
    cr_path = f"images/{title_prefix.lower().replace(' ', '_')}_cr_ratio.png"
    plt.savefig(cr_path)
    print(f"Saved: {cr_path}")

    # Peg Price plot
    plt.figure(figsize=(12, 4))
    plt.plot(peg_prices, label='Stablecoin Market Price')
    plt.axhline(y=1.0, color='g', linestyle='--', label='Target Peg ($1)')
    plt.title(f'{title_prefix} - Peg Price')
    plt.xlabel('Day')
    plt.ylabel('Market Price')
    plt.legend()
    plt.grid(True)
    peg_path = f"images/{title_prefix.lower().replace(' ', '_')}_peg_price.png"
    plt.savefig(peg_path)
    print(f"Saved: {peg_path}")

if __name__ == "__main__":
    print("Running Example Scenario: Gradual Decay")
    cr, pp = simulate_stablecoin_peg(initial_collateral_price=2000, price_drop_per_day=100, stablecoin_supply=150000)
    plot_results(cr, pp, "Gradual Decay")
