import pandas as pd
pd.set_option('display.max_columns', None)

# Reading industry_client_details CSV file using pandas
industry_client_details = pd.read_csv('D:\\Sky\\Data\\industry_client_details.csv')

# Filtering Finance Lending and Block Chain Industries
blockchain_fin_lending = industry_client_details[industry_client_details['industry'].isin(['Finance Lending', 'Block Chain'])]

# Grouping and count number of each industry
block_fin_lending_count = blockchain_fin_lending.groupby('industry').size()

# printing the count for each industry
print('1. How many finance lending and blockchain clients does the organization have?')
print(block_fin_lending_count)
print('\n---------------------------------------------------------------------------\n')

# Reading subscription_information CSV file using pandas
subscription_information = pd.read_csv('D:\\Sky\\Data\\subscription_information.csv')

# Combining industry_client_details and subscription_information
combined_client_info = pd.merge(industry_client_details, subscription_information, on='client_id', how='inner')

# selecting only 2 columns and filtering True values
industry_renewed_status = combined_client_info.loc[combined_client_info['renewed'] == True, ['industry', 'renewed']]

# Grouping to check subscription count for each industry
industry_renewed_status = industry_renewed_status.groupby(['industry']).size().reset_index(name='count')

# Selecting record with highest renewal rate
highest_renewal_rate_industry = industry_renewed_status.loc[industry_renewed_status['count'].idxmax()]

print('2. Which industry in the organization has the highest renewal rate?')
print(highest_renewal_rate_industry)
print('\n---------------------------------------------------------------------------\n')

# Reading financial_information CSV file using pandas
financial_information = pd.read_csv('D:\\Sky\\Data\\finanical_information.csv')

# Filtering renewed subscription = True
renewed_subscriptions = subscription_information[subscription_information['renewed'] == True]

# Converting string columns to datetime
renewed_subscriptions.loc[:,'start_date'] = pd.to_datetime(renewed_subscriptions['start_date'])
renewed_subscriptions.loc[:, 'end_date'] = pd.to_datetime(renewed_subscriptions['end_date'])

financial_information.loc[:, 'start_date'] = pd.to_datetime(financial_information['start_date'])
financial_information.loc[:, 'end_date'] = pd.to_datetime(financial_information['end_date'])

# Joining subscription information with financial information on date to get inflation rate at that point of time
subscription_and_financial_info = renewed_subscriptions.merge(financial_information, how='cross')

# selecting only client_id and inflation_rate
subscription_and_financial_info = subscription_and_financial_info.loc[
    (subscription_and_financial_info['start_date_x'] >= subscription_and_financial_info['start_date_y']) &
    (subscription_and_financial_info['start_date_x'] <= subscription_and_financial_info['end_date_y']),
    ['client_id', 'inflation_rate']
]

# joining with client information to get industry
client_financial_info = pd.merge(industry_client_details, subscription_and_financial_info, on='client_id', how='inner')[['industry', 'inflation_rate']]

# Grouping on industry to get average inflation rate
avg_inflation_rate = client_financial_info.groupby('industry')['inflation_rate'].mean('inflation_rate').reset_index(name='avg_inflation_rate')

print('3. What was the average inflation rate when their subscriptions were renewed?')
print(avg_inflation_rate)
print('\n---------------------------------------------------------------------------\n')

# Reading payment_information CSV file using pandas
payment_information = pd.read_csv('D:\\Sky\\Data\\payment_information.csv')

# Adding year column in dataframe
payment_information['year_of_payment'] = pd.to_datetime(payment_information['payment_date']).dt.year

# Median amount paid per year
med_per_year = payment_information.groupby('year_of_payment')['amount_paid'].median('amount_paid').reset_index(name='median_amount_paid')

# Joining payment information with client information
client_payment_info = pd.merge(payment_information, industry_client_details, on='client_id', how='inner')

# Median amount paid per year per industry
med_per_year_per_industry = client_payment_info.groupby(['year_of_payment', 'industry'])['amount_paid'].median('amount_paid').reset_index(name='median_amount_paid')

print('4. What is the median amount paid each year for all payment methods?')
print('Median per year')
print(med_per_year, '\n')

print('Median per year per industry')
print(med_per_year_per_industry)
print('\n---------------------------------------------------------------------------\n')