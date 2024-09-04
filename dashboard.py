import pandas as pd
import re
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import warnings 

warnings.filterwarnings('ignore')

file_path = "./retail_sales_v2.csv"
df = pd.read_csv(file_path)

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

    return select_df

# Streamlit UI
x_input = st.selectbox('Choose an input variable:', ['Gender', 'Age'])
y_input = st.selectbox('Choose an output variable:', ['Purchased Quantity', 'Sales by different Categories', 'Distribution', 'Overall Sales'])

if x_input == 'Gender':
    if y_input == 'Sales by different Categories':
        show_df = interactive_widget('Gender', 'Sales by different Categories')
        fig = px.bar(show_df, x='Product Category', y='Total Sales', color='Gender',
                     title='Total Sales by Product Category and Gender', barmode='group')
        st.plotly_chart(fig)
    elif y_input == 'Distribution':
        show_df = interactive_widget('Gender', 'Distribution')
        fig = px.pie(show_df, values='Distribution', names='Gender', title='Gender Distribution')
        st.plotly_chart(fig)
    elif y_input == 'Overall Sales':
        show_df = interactive_widget('Gender', 'Overall Sales')
        fig = px.bar(show_df, x='Gender', y='Total Amount', title='Overall Sales by Gender')
        st.plotly_chart(fig)
    elif y_input == 'Purchased Quantity':
        show_df = interactive_widget('Gender', 'Purchased Quantity')
        fig = px.bar(show_df, x='Quantity', y='Frequency', color='Gender',
                     title='Purchase Frequency', barmode='group')
elif x_input == 'Age':
    if y_input == 'Sales by different Categories':
        show_df = interactive_widget('Age Group', 'Sales by different Categories')
        fig = px.bar(show_df, x='Product Category', y='Total Sales', color='Age Group',
                title='Total Sales by Product Category and Gender', barmode='group')
        st.plotly_chart(fig)
    elif y_input == 'Distribution':
        show_df = interactive_widget('Age Group', 'Distribution')
        fig = px.pie(show_df, values='Distribution', names='Age Group', title='Age Distribution')
        st.plotly_chart(fig)
    elif y_input == 'Overall Sales':
        show_df = interactive_widget('Age Group', 'Overall Sales')
        fig = px.bar(show_df, x='Age Group', y='Total Amount', title='Overall Sales by Age Group')
        st.plotly_chart(fig)
    elif y_input == 'Purchased Quantity':
        show_df = interactive_widget('Age Group', 'Purchased Quantity')
        fig = px.bar(show_df, x='Quantity', y='Frequency', color='Age Group',
                     title='Purchase Frequency', barmode='group') 
