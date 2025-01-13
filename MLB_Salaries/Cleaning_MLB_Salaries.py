# import pandas
import pandas as pd

# export path for easy access when running
export_path = 'C:\Portfolio\MLB_Salaries\\'

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

# Rename and positon columns
sal_df.rename(columns = {'Year':'Year_Gathered'}, inplace = True)
sal_df = sal_df.iloc[:,[5,6,0,1,2,3,7,8,9,4]]

# Save to csv
sal_df.to_csv(export_path + "Clean_MLB_Saleries_2021_to_2024.csv", index = False)
