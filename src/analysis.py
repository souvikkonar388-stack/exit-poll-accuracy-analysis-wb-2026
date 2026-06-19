import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

ACTUAL_BJP = 206
ACTUAL_TMC = 82

def run_electoral_analysis():
    csv_path = os.path.join('data', 'exit_poll_data.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing dataset at {csv_path}.")
        
    df = pd.read_csv(csv_path)
    
    df['BJP_mid'] = (df['BJP_low'] + df['BJP_high']) / 2
    df['TMC_mid'] = (df['TMC_low'] + df['TMC_high']) / 2
    df['BJP_error'] = abs(df['BJP_mid'] - ACTUAL_BJP)
    df['BJP_in_range'] = (ACTUAL_BJP >= df['BJP_low']) & (ACTUAL_BJP <= df['BJP_high'])
    df['Winner_called'] = np.where(df['BJP_mid'] > df['TMC_mid'], 'Winning Party', 'Incumbent Party')
    df['Correct_winner'] = df['Winner_called'] == 'Winning Party'
    
    mae = df['BJP_error'].mean()
    rmse = np.sqrt((df['BJP_error'] ** 2).mean())
    
    print("=== CORE ERROR METRICS ===")
    print(f"Mean Absolute Error (MAE): {mae:.1f} seats")
    print(f"Root Mean Squared Error (RMSE): {rmse:.1f} seats\n")
    
    midpoints = df['BJP_mid'].values
    mean_prediction = np.mean(midpoints)
    standard_error = stats.sem(midpoints)
    
    ci = stats.t.interval(0.95, df=len(midpoints)-1, loc=mean_prediction, scale=standard_error)
    
    print("=== STATISTICAL INFERENCE ===")
    print(f"Poll-of-Polls Ensemble Mean: {mean_prediction:.1f} seats")
    print(f"95% Confidence Interval: ({ci[0]:.1f}, {ci[1]:.1f}) seats")
    print(f"Actual Outcome ({ACTUAL_BJP} seats) inside CI: {ci[0] <= ACTUAL_BJP <= ci[1]}\n")
    
    elections = np.array([1, 2, 3, 4, 5]) 
    winning_party_vote_share = np.array([10.2, 40.3, 38.1, 39.0, 45.2])
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(elections, winning_party_vote_share)
    
    print("=== VOTE SHARE REGRESSION TRENDS ===")
    print(f"Growth Rate (Slope): {slope:.2f}% per election cycle")
    print(f"Coefficient of Determination (R²): {r_value**2:.2f}")
    print(f"Statistical Significance (p-value): {p_value:.4f}\n")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    ax.bar(x - 0.2, df['BJP_mid'], 0.35, label='Predicted (Winning Party)', color='#378ADD')
    ax.bar(x + 0.2, [ACTUAL_BJP] * len(df), 0.35, label='Actual Result', color='#1D9E75')
    ax.errorbar(x - 0.2, df['BJP_mid'], yerr=[df['BJP_mid'] - df['BJP_low'], df['BJP_high'] - df['BJP_mid']], fmt='none', color='black', capsize=4)
    ax.set_xticks(x)
    ax.set_xticklabels(df['Agency'], rotation=15, ha='right')
    ax.set_ylabel('Seats')
    ax.set_title('Exit Poll Predictions vs Actual Result')
    ax.axhline(148, color='red', linestyle='--', linewidth=0.8, label='Majority Mark (148)')
    ax.legend()
    plt.tight_layout()
    plt.savefig('agency_comparison.png', dpi=150)
    print("Plots saved successfully as 'agency_comparison.png'.")

if __name__ == '__main__':
    run_electoral_analysis()
