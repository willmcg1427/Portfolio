# import pandas
import pandas as pd

# export path for easy access when running
export_path = 'C:\Portfolio\MLB_Salaries\CSV_Files\\'

# Read in csv
sal_df = pd.read_csv(export_path + 'MLB_Salaries_2021_to_2024.csv')

# Turning name into first and last name columns
sal_df['First_Name'] = sal_df['Player'].str.split(',').str[1].str.lstrip()
sal_df['Last_Name'] = sal_df['Player'].str.split(',').str[0]
sal_df['First_Name'] = sal_df['First_Name'].str.replace('*','')

# Dropping player column
sal_df.drop('Player',axis = 1, inplace = True)

# Fill in year data for single year contracts
df_2021 = sal_df.loc[sal_df['Year'] == 2021]
df_2021['Years'].replace(' ', '1 (2021-21)', inplace = True)
df_2022 = sal_df.loc[sal_df['Year'] == 2022]
df_2022['Years'].fillna('1 (2022-22)', inplace = True)
df_2023 = sal_df.loc[sal_df['Year'] == 2023]
df_2023['Years'].fillna('1 (2023-23)', inplace = True)
df_2024 = sal_df.loc[sal_df['Year'] == 2024]
df_2024['Years'].fillna('1 (2024-24)', inplace = True)
sal_df = pd.concat([df_2021,df_2022,df_2023,df_2024], axis = 0)

# Cleaning specific years items
sal_df.loc[sal_df['Years'] == '7(2022-28)', 'Years'] = '7 (2022-28)'
sal_df.loc[sal_df['Years'] == '(8 (2024-31)', 'Years'] = '8 (2024-31)'
sal_df.loc[sal_df['Years'] == ' 9 (2023-31)', 'Years'] = '9 (2023-31)'
sal_df.loc[sal_df['Years'] == '3 (2023-35)', 'Years'] = '3 (2023-25)'
sal_df.loc[sal_df['Years'] == '4 (2019-21)', 'Years'] = '3 (2019-21)'

# Creating new columns from years column
sal_df['Length(Years)'] = sal_df['Years'].str.lstrip().str.split(' ').str[0].astype('int64')
sal_df['Start_Year'] = sal_df['Years'].str.lstrip().str.split(' ').str[1].str.replace('(','').str.replace(')','').str.split('-').str[0].astype('int64')
sal_df['End_Year'] = 2000 + sal_df['Years'].str.lstrip().str.split(' ').str[1].str.replace('(','').str.replace(')','').str.split('-').str[1].astype('int64')

# Dropping old Years column
sal_df.drop('Years', axis = 1, inplace = True)

# Cleaning the Total_value column
sal_df.loc[sal_df['Length(Years)'] == 1, 'Total_value'] = sal_df['Salary']
sal_df = sal_df[sal_df['Total_value'].notna()]
sal_df['Total_value'] = sal_df['Total_value'].astype('int64')

# Positon columns
sal_df = sal_df.iloc[:,[5,6,0,1,2,3,7,8,9,4]]

# Align team names
sal_df.loc[(sal_df['Team'] == 'Chicago Cubs') | (sal_df['Team'] == 'Chi. Cubs') | (sal_df['Team'] == 'Cubs') | (sal_df['Team'] == 'Chic. Cubs'),'Team'] = 'Chicago Cubs'
sal_df.loc[(sal_df['Team'] == 'Chic. White Sox') | (sal_df['Team'] == 'White Sox'),'Team'] = 'Chicago White Sox'
sal_df.loc[(sal_df['Team'] == 'Giants') | (sal_df['Team'] == 'San Francisco'),'Team'] = 'San Francisco Giants'
sal_df.loc[(sal_df['Team'] == 'Athletics') | (sal_df['Team'] == 'Oakland'),'Team'] = 'Oakland Athletics'
sal_df.loc[(sal_df['Team'] == 'Twins') | (sal_df['Team'] == 'Minnesota'),'Team'] = 'Minnesota Twins'
sal_df.loc[(sal_df['Team'] == 'Astros') | (sal_df['Team'] == 'Houston'),'Team'] = 'Houston Astros'
sal_df.loc[(sal_df['Team'] == 'Braves') | (sal_df['Team'] == 'Atlanta'),'Team'] = 'Atlanta Braves'
sal_df.loc[(sal_df['Team'] == 'Brewers') | (sal_df['Team'] == 'Milwaukee'),'Team'] = 'Milwaukee Brewers'
sal_df.loc[(sal_df['Team'] == 'Diamondbacks') | (sal_df['Team'] == 'Arizona'),'Team'] = 'Arizona Diamondbacks'
sal_df.loc[(sal_df['Team'] == 'Pirates') | (sal_df['Team'] == 'Pittsburgh'),'Team'] = 'Pittsburgh Pirates'
sal_df.loc[(sal_df['Team'] == 'Rangers') | (sal_df['Team'] == 'Texas'),'Team'] = 'Texas Rangers'
sal_df.loc[(sal_df['Team'] == 'Rays') | (sal_df['Team'] == 'Tampa Bay'),'Team'] = 'Tampa Bay Rays'
sal_df.loc[(sal_df['Team'] == 'Reds') | (sal_df['Team'] == 'Cincinnati'),'Team'] = 'Cincinnati Reds'
sal_df.loc[(sal_df['Team'] == 'Cardinals') | (sal_df['Team'] == 'St. Louis'),'Team'] = 'St. Louis Cardinals'
sal_df.loc[(sal_df['Team'] == 'Cleveland') | (sal_df['Team'] == 'Guardians'),'Team'] = 'Cleveland Guardians'
sal_df.loc[(sal_df['Team'] == 'Nationals') | (sal_df['Team'] == 'Washington'),'Team'] = 'Washington Nationals'
sal_df.loc[(sal_df['Team'] == 'Padres') | (sal_df['Team'] == 'San Diego') | (sal_df['Team'] == 'San Diego '),'Team'] = 'San Diego Padres'
sal_df.loc[(sal_df['Team'] == 'Red Sox') | (sal_df['Team'] == 'Boston'),'Team'] = 'Boston Red Sox'
sal_df.loc[(sal_df['Team'] == 'Rockies') | (sal_df['Team'] == 'Colorado'),'Team'] = 'Colorado Rockies'
sal_df.loc[(sal_df['Team'] == 'Royals') | (sal_df['Team'] == 'Kansas City'),'Team'] = 'Kansas City Royals'
sal_df.loc[(sal_df['Team'] == 'Yankees') | (sal_df['Team'] == 'N.Y. Yankees'),'Team'] = 'New York Yankees'
sal_df.loc[(sal_df['Team'] == 'Marlins') | (sal_df['Team'] == 'Miami'),'Team'] = 'Miami Marlins'
sal_df.loc[(sal_df['Team'] == 'Mariners') | (sal_df['Team'] == 'Seattle'),'Team'] = 'Seattle Mariners'
sal_df.loc[(sal_df['Team'] == 'Dodgers') | (sal_df['Team'] == 'L.A. Dodgers'),'Team'] = 'Los Angeles Dodgers'
sal_df.loc[(sal_df['Team'] == 'Phillies') | (sal_df['Team'] == 'Philadelphia'),'Team'] = 'Philadelphia Phillies'
sal_df.loc[(sal_df['Team'] == 'Orioles') | (sal_df['Team'] == 'Baltimore'),'Team'] = 'Baltimore Orioles'
sal_df.loc[(sal_df['Team'] == 'Mets') | (sal_df['Team'] == 'N.Y. Mets'),'Team'] = 'New York Mets'
sal_df.loc[(sal_df['Team'] == 'Tigers') | (sal_df['Team'] == 'Detroit'),'Team'] = 'Detroit Tigers'
sal_df.loc[(sal_df['Team'] == 'Blue Jays') | (sal_df['Team'] == 'Toronto'),'Team'] = 'Toronto Blue Jays'
sal_df.loc[(sal_df['Team'] == 'Angels') | (sal_df['Team'] == 'L.A. Angels'),'Team'] = 'Los Angeles Angels'


# Save to csv
sal_df.to_csv(export_path + "Clean_MLB_Salaries_2021_to_2024.csv", index = False)

