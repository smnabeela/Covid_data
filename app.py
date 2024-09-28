import streamlit as st 
import pandas as pd 
import plotly.express as px

st.set_page_config(layout="wide")
st.header('Covid Data')

data = pd.read_csv('covid_dashboard.csv')

a = data['State/UTs'].unique()
s = st.selectbox('Select State', (a))

df = data[data['State/UTs'] == s]
st.write(df)

with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        c1.metric(label='Total cases', value=round(df['Total Cases'].sum(), 2))
    with c2:
        c2.metric(label='Recovered', value=round(df['Discharged'].sum(), 2))
    with c3:
        c3.metric(label='Death', value=round(df['Deaths'].sum(), 2))
    with c4:
        c4.metric(label='Active', value=round(df['Active Ratio'].sum(), 2))

cl1, cl2, cl3 = st.columns(3)
with cl1:
    fig = px.bar(data, x='Death Ratio', y='State/UTs', title='Death Rate')
    st.write(fig)
with cl2:
    fig1 = px.bar(data, x='Discharged', y='State/UTs', title='Recovery Rate')
    st.write(fig1)
with cl3:
    fig2 = px.pie(data, values='Active', names='Zone', title='Cases by Zone')
    st.write(fig2)

col1, col2 = st.columns(2)
with col1:
    fig3 = px.bar(data, 
                   x='State/UTs', 
                   y=['Active', 'Deaths'], 
                   title='Active Cases and Deaths',
                   labels={'value': 'Count', 'variable': 'Category'},
                   barmode='group')
    st.write(fig3)
with col2:
    fig4 = px.bar(data, 
                   x='State/UTs', 
                   y=['Total Cases', 'Discharged'], 
                   title='Total Discharged',
                   labels={'value': 'Count', 'variable': 'Category'},
                   barmode='group')
    st.write(fig4)

colm1, colm2 = st.columns(2)
with colm1:
    df1= data[['State/UTs', 'Total Cases']].copy()

    highest_cases = df1.nlargest(5, 'Total Cases').reset_index(drop=True)
    lowest_cases = df1.nsmallest(5, 'Total Cases').reset_index(drop=True)

    combined_df = pd.DataFrame({
        'Highest States': highest_cases['State/UTs'],
        'Highest Cases': highest_cases['Total Cases'],
        'Least States': lowest_cases['State/UTs'],
        'Least Cases': lowest_cases['Total Cases']
    })

    def create_bar(value, max_value):
        bar_length = int((value / max_value) * 100) 
        return f"<div style='width: {bar_length}%; background-color: orange; height: 20px;'></div> {value:,}"

    max_highest = highest_cases['Total Cases'].max()
    max_lowest = lowest_cases['Total Cases'].max()

    highest_bars = [create_bar(value, max_highest) for value in highest_cases['Total Cases']]
    lowest_bars = [create_bar(value, max_lowest) for value in lowest_cases['Total Cases']]

    
    combined_df['Highest Cases'] = highest_bars
    combined_df['Least Cases'] = lowest_bars

    st.markdown("<h4 style='text-align: center;'>Total Cases</h4>", unsafe_allow_html=True)
    st.write(combined_df.to_html(escape=False), unsafe_allow_html=True)

