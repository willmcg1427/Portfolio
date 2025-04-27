# Import packages
import requests
import pandas as pd

# export path for easy access when running
export_path = 'C:\Portfolio\MLB_Salaries\CSV_Files\\'

# Function to get baseball data
def get_baseball(page, pageID):
    print(f"Getting Major League page {page} of pageID={pageID}")

    url = "https://databases.usatoday.com/wp-admin/admin-ajax.php"

    # Form data for the POST request
    form_data = {
        'action': "cspFetchTable",
        # This code will change over time, when running a new code can be obtained in the var sitedata string in 
        # the source of https://databases.usatoday.com/major-league-baseball-salaries-2024/ (year does change)
        'security': "ff06d79557",
        'pageID': pageID,
        'sortBy': "PK_ID",
        'page': page,
        'searches': "{}",
        'heads': "true"
    }

    try:
        # Make the request
        response = requests.post(url, data=form_data)

        # Check for HTTP success status
        if response.status_code != 200:
            print(f"Failed to retrieve data for page {page}: HTTP {response.status_code}")
            return pd.DataFrame()

        try:
            # Parse the response as JSON
            json_data = response.json()

            # Extract relevant data
            result_data = json_data.get("data", {}).get("Result", [])


            # Convert to a DataFrame and return
            return pd.DataFrame(result_data)

        except ValueError:
            print("Failed to decode JSON")
            return pd.DataFrame()

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return pd.DataFrame()


# Iterate through the pages and get the data
def get_all_pages(pageID, tot_pages):
    all_data = pd.concat([get_baseball(page, pageID) for page in range(1, tot_pages+1)], ignore_index=True)

    return all_data


# Fetch all pages and store the result in a DataFrame
# 2024
df_2024 = get_all_pages(629,48)[['Player','Team','Position','Salary','Years','Total_value']]
df_2024['Year'] = 2024

# 2023
df_2023 = get_all_pages(444,48)[['Player','Team','Position','Salary','Years','Total_value']]
df_2023['Year'] = 2023

# 2022
df_2022 = get_all_pages(330,49)[['Player','Team','Position','Salary','Years','Total_value']]
df_2022['Year'] = 2022

# 2021
df_2021 = get_all_pages(21,45)[['Player','Team','Position','Salary','Years','Total_value']]
df_2021['Year'] = 2021

# Put them all together in one dataframe
df_2021_to_2024 = pd.concat([df_2021,df_2022,df_2023,df_2024], axis = 0)

# Save to csv
df_2021_to_2024.to_csv(export_path + 'MLB_Salaries_2021_to_2024.csv', index = False)






