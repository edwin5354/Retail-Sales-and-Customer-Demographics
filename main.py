import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

df = pd.read_csv('retail_sales_dataset.csv')

# Explore Dataset
df.info()
pd.set_option('display.max_columns', None)  # Shows all columns
df.head()
print(df.describe())
df.isnull().sum()

# Check For Duplicates
duplicates = df.duplicated().sum()
print(f'Duplicates Rows: {duplicates}')

# Check for Duplicates for Transaction ID and Customer ID
transaction_dup = df['Transaction ID'].duplicated().sum()
customer_dup = df['Customer ID'].duplicated().sum()
print(f'Transaction Duplicates: {transaction_dup}')
print(f'Customer Duplicates: {customer_dup}')

# Change Date Column from Object to DateTime
df['Date'] = pd.to_datetime(df['Date'])

# Visualize Data
## Sales by Day
sum_sales = df.groupby('Date')['Total Amount'].sum().reset_index()
plt.figure(figsize=(12,6))
plt.plot(sum_sales['Date'], sum_sales['Total Amount'], color='b')
plt.title("Sales by Day")
plt.xlabel("Date")
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.ylabel("Sales")
#plt.savefig('sales_by_day.png')

## Sales by Product
group_prod = df.groupby('Product Category')['Total Amount'].sum().reset_index()
plt.figure(figsize=(12,6))
sns.barplot(x='Product Category', y='Total Amount', data= group_prod)
#plt.savefig('sales_by_product.png')

## Sales by Gender And Age
purchase_counts = df.groupby('Date')['Total Amount'].count().reset_index()
purchase_counts.columns = ['Date', 'Number of Purchases']
plt.figure(figsize=(12,6))
plt.plot(purchase_counts['Date'], purchase_counts['Number of Purchases'], color='b')
plt.title("Number of Purchases by Date")
plt.xlabel("Date")
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to every month
plt.ylabel("Number of Purchases")
#plt.savefig('purchase_by_day.png')

date_range = pd.date_range(start='2023-01-01', end='2023-12-31')
missing_dates = date_range[~date_range.isin(df['Date'])]
#print("Missing Dates:")
#print(missing_dates)

# Price per Unit Histogram
plt.figure(figsize=(12,6))
plt.hist(df['Price per Unit'], bins=30, color='skyblue', edgecolor='black')
plt.title("Price per Unit Distribution")
plt.xlabel("Unit Price")
plt.ylabel("Frequency")
#plt.savefig('price_per_unit_distribution.png')

# Product Spend by Gender
gender_dist = df.groupby(['Gender', 'Product Category'])['Total Amount'].sum().unstack()

colors = ['#003366', '#0066cc', '#66ccff']
gender_dist.plot(kind='bar', stacked=True, figsize=(10,6), color=colors)
plt.title("Total Spend by Product and Gender")
plt.xlabel("Product")
plt.ylabel("Total Spend ($)")
plt.xticks(rotation=0)  # Rotate x-axis labels for better readability
plt.legend(title='Gender')
#plt.savefig('product_spend_by_gender.png')

# Age Histogram
plt.figure(figsize=(10, 6))
plt.hist(df['Age'], bins=8, color='skyblue', edgecolor='black')
plt.title("Distribution of Age")
plt.xlabel("Age")
plt.ylabel("Frequency")
#plt.savefig('age_dist.png')

# Including an Ages column
print(min(df['Age']))
print(max(df['Age']))
bins = [17, 23, 28, 33, 38, 43, 48, 53, 58, 63, 64]
labels = ['18-22', '23-27', '28-32', '33-37', '38-42', '43-47', '48-52', '53-57', '58-62', '63-64']
df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

print(df[df['Age'] == 18])