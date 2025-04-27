# Packages
import pandas as pd

# Load in MLB data
mlb_85_14 = pd.read_csv("dirty_mb_1985-2014.csv")
mlb_11_24 = pd.read_csv("dirty_mb_2011-2024.csv")

# Inspecting data
print(mlb_85_14.head(20))
print(mlb_85_14.info()) # Estimated payroll has missing values
print(mlb_11_24.head(20))
print(mlb_11_24.info())

# Get rid of missing values in estimated payroll
mlb_85_14 = mlb_85_14.dropna(subset = ['est_payroll'])

# Check which years are still represented in the data
print(mlb_85_14['year'].value_counts()) # Number of instances drops drasticatlly after 1985

# Make data set 1985 and beyond
mlb_85_14 = mlb_85_14[mlb_85_14['year'] >= 1985]

# Create win_losses ratio for mlb_11_24
mlb_11_24['wins_losses'] = round(mlb_11_24['Wins'] / (mlb_11_24['Wins'] + mlb_11_24['Losses']), 3)

# Edit column names to match
mlb_11_24.rename(columns = {'Team':'tm', 'Year':'year','Total Payroll Allocations': 'est_payroll', 'Wins':'w','Losses':'l'}, inplace = True)

# Gather important attributes for money ball hypothesis and shrink data sets
col_names = ["tm","year","est_payroll","w","l","wins_losses"]
mlb_85_14 = mlb_85_14[col_names]
mlb_11_24 = mlb_11_24[col_names]

# Remove overlapping years
mlb_11_24 = mlb_11_24[mlb_11_24['year'] > 2014]

# Combine data sets into one
mlb_data = pd.concat([mlb_85_14,mlb_11_24], ignore_index = True).sort_values(by = ['tm','year'])

# Create a new column that is normalized estimated payroll based off of the year
def normalize_zscore(x):
    return (x - x.mean()) / x.std()
mlb_data['norm_payroll'] = mlb_data.groupby('year')['est_payroll'].transform(normalize_zscore)

# Create columns for rank in payroll and wins
mlb_data['payroll_rk'] = mlb_data.groupby('year')['est_payroll'].rank(ascending = False, method = 'first')
mlb_data['top10_payroll'] = 0
mlb_data.loc[mlb_data['payroll_rk'] <= 10,'top10_payroll'] = 1
mlb_data['win_loss_rk'] = mlb_data.groupby('year')['wins_losses'].rank(ascending = False, method = 'first')
mlb_data['top10_win_loss'] = 0
mlb_data.loc[mlb_data['win_loss_rk'] <= 10,'top10_win_loss'] = 1

# Create columns for rank proximity
mlb_data['rk_proximity'] = abs(mlb_data['payroll_rk'] - mlb_data['win_loss_rk'])

# Create column for close proximity
mlb_data['close_rk'] = 0
mlb_data.loc[mlb_data['rk_proximity'] <= 2,'close_rk'] = 1

# Create a csv for the clean data set
mlb_data.to_csv("clean-mlb-standings-and-payroll.csv", index = False)

