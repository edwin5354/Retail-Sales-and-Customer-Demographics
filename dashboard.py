import pandas as pd
import re
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import warnings 
from prophet import Prophet
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

file_path = r"C:\Users\Edwin\Python\bootcamp\Projects\retails\dataset\retail_sales_v2.csv"
df = pd.read_csv(file_path)

st.title('Retail Sales & Customer Demographics Project')
st.write("Welcome to the Retail Sales Dashboard! Here, you'll find engaging exploratory data analysis (EDA) visualizations that generate interactive graphs. This project aims to uncover sales trends across different time periods, and we'll also explore techniques for clustering and forecasting analysis. Enjoy diving into the data!")

st.subheader('a) Exploratory Data Analysis')

def interactive_widget(x, y):
    if x == 'Gender':
        if y == 'Distribution':
            select_df = df.groupby(x).size().reset_index(name='Distribution')
        elif y == 'Sales by different Categories':
            select_df = df.groupby([x, 'Product Category'])['Total Amount'].sum().reset_index()
            select_df.columns = [x, 'Product Category', 'Total Sales']
        elif y == 'Overall Sales':
            select_df = df.groupby(x)['Total Amount'].sum().reset_index()
            select_df.columns = [x, 'Total Amount']
        elif y == 'Purchased Quantity':
            select_df = df.groupby([x, 'Quantity']).size().reset_index(name='Frequency')
            select_df.columns = [x, 'Quantity', 'Frequency']
        elif y == 'Amount spent per Transaction':
            select_df = df[['Gender', 'Total Amount']]
    elif x == 'Age Group':
        if y == 'Distribution':
            select_df = df.groupby('Age Group').size().reset_index(name='Distribution')
        elif y == 'Sales by different Categories':
            select_df = df.groupby(['Age Group', 'Product Category'])['Total Amount'].sum().reset_index()
            select_df.columns = ['Age Group', 'Product Category', 'Total Sales']
        elif y == 'Overall Sales':
            select_df = df.groupby('Age Group')['Total Amount'].sum().reset_index()
            select_df.columns = ['Age Group', 'Total Amount']
        elif y == 'Purchased Quantity':
            select_df = df.groupby(['Age Group', 'Quantity']).size().reset_index(name='Frequency')
            select_df.columns = ['Age Group', 'Quantity', 'Frequency']
        elif y == 'Amount spent per Transaction':
            select_df = df[['Age Group', 'Total Amount']]

    return select_df

def plot_data(x, y, show_df):
    if y == 'Sales by different Categories':
        fig = px.bar(show_df, x='Product Category', y='Total Sales', color=x,
                     title=f'Total Sales by Product Category and {x}', barmode='group')
    elif y == 'Distribution':
        fig = px.pie(show_df, values='Distribution', names=x, title=f'{x} Distribution')
    elif y == 'Overall Sales':
        fig = px.bar(show_df, x=x, y='Total Amount', title=f'Overall Sales by {x}')
    elif y == 'Purchased Quantity':
        fig = px.bar(show_df, x='Quantity', y='Frequency', color=x,
                     title='Purchase Frequency', barmode='group')
    elif y == 'Amount spent per Transaction':
        fig = px.box(show_df, x=x_input, y='Total Amount', 
                     title= f'Boxplot of Amount Spent per Transaction by {x_input}', 
                     labels={x_input: x_input, 'Total Amount': 'Amount Spent ($)'})
    
    st.plotly_chart(fig)

def time_series_widget(x):
    if x =='Gender':
        new_df = df.groupby(['Gender', 'Date'])['Total Amount'].sum().reset_index()
        fig = px.line(new_df, x='Date', y="Total Amount", color= 'Gender',
                      title = "Time Series Analysis of Total Sales by Gender",
                      labels={x_input: x_input, 'Total Amount': 'Sales ($)'})
    elif x == 'Product Category':
        new_df = df.groupby(['Product Category', 'Date'])['Total Amount'].sum().reset_index()
        fig = px.line(new_df, x='Date', y="Total Amount", color= 'Product Category',
                      title = "Time Series Analysis of Total Sales by Product category",
                      labels={x_input: x_input, 'Total Amount': 'Sales ($)'})
    elif x == 'Overall Sales':
        new_df = df.groupby('Date')['Total Amount'].sum().reset_index()
        fig = px.line(new_df, x='Date', y="Total Amount",
                      title = "Time Series Analysis of Overall Sales",
                      labels={x_input: x_input, 'Total Amount': 'Sales ($)'})

    st.plotly_chart(fig)

# Streamlit UI
x_input = st.selectbox('Choose an input variable:', ['Gender', 'Age Group'])
y_input = st.selectbox('Choose an output variable:', ['Purchased Quantity', 'Sales by different Categories',
                                                       'Distribution', 'Overall Sales', 'Amount spent per Transaction'])

if x_input == 'Gender':
    show_df = interactive_widget('Gender', y_input)
elif x_input == 'Age Group':
    show_df = interactive_widget('Age Group', y_input)

# Call the plotting function
if not show_df.empty:
    plot_data(x_input, y_input, show_df)
else:
    st.write("No data available for the selected criteria.")

st.subheader('b) Time Series Analysis and Forecasting')
time_input = st.selectbox('Please select a variable to display the time-series analysis:', ['Overall Sales', 'Gender', 'Product Category'])

if time_input:
    time_series_widget(time_input)
