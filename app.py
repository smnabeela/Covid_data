import streamlit as st 
import pandas as pd 
import plotly.express as px

# Configure the page layout
st.set_page_config(layout="wide")

# Dashboard title and description
st.markdown("<h1 style='text-align: center;'>COVID-19 Data: India</h1>", unsafe_allow_html=True)
st.markdown("""
**Dashboard Overview:** This interactive dashboard offers an in-depth look at the COVID-19 situation across India's States and Union Territories. 
Users can select specific regions to view key metrics, including total cases, recoveries, deaths, and active cases. 
Visualizations like bar charts and pie charts showcase trends such as recovery and death rates, along with active cases by zones, providing clear insights into the pandemic's impact across the country.
""")

# Load the CSV file (Make sure the CSV file is in the correct path)
data = pd.read_csv('covid_dashboard.csv')

# Dropdown menu for selecting states
states = data['State/UTs'].unique()
selected_state = st.selectbox('Select State', states)

# Filter the data based on the selected state
df = data[data['State/UTs'] == selected_state]
st.write(df)

# Display key metrics in containers
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

# Visualization columns
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

# Bar charts for detailed breakdown
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

# Tables for highest and lowest cases, recovered cases, and deaths
colm1, colm2 = st.columns(2)
with colm1:
    # Highest and lowest total cases table
    df1 = data[['State/UTs', 'Total Cases']].copy()
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

with colm2:
    # Highest and lowest recovered cases table
    df2 = data[['State/UTs', 'Discharged']].copy()
    highest_recovered = df2.nlargest(5, 'Discharged').reset_index(drop=True)
    lowest_recovered = df2.nsmallest(5, 'Discharged').reset_index(drop=True)
    recovered_df = pd.DataFrame({
        'Highest': highest_recovered['State/UTs'],
        'Recovered': highest_recovered['Discharged'],
        'Least': lowest_recovered['State/UTs'],
        'Recovered Cases': lowest_recovered['Discharged']
    })

    max_recovered_highest = highest_recovered['Discharged'].max()
    max_recovered_lowest = lowest_recovered['Discharged'].max()

    highest_recovered_bars = [create_bar(value, max_recovered_highest) for value in highest_recovered['Discharged']]
    lowest_recovered_bars = [create_bar(value, max_recovered_lowest) for value in lowest_recovered['Discharged']]

    recovered_df['Recovered'] = highest_recovered_bars
    recovered_df['Recovered Cases'] = lowest_recovered_bars

    st.markdown("<h4 style='text-align: center;'>Recovered Cases</h4>", unsafe_allow_html=True)
    st.write(recovered_df.to_html(escape=False), unsafe_allow_html=True)

# Additional columns for death cases and new active cases table
cll1, cll2 = st.columns(2)
with cll1:
    # Highest and lowest death cases table
    df3 = data[['State/UTs', 'Deaths']].copy()
    highest_deaths = df3.nlargest(5, 'Deaths').reset_index(drop=True)
    lowest_deaths = df3.nsmallest(5, 'Deaths').reset_index(drop=True)
    death_df = pd.DataFrame({
        'Highest': highest_deaths['State/UTs'],
        'Death%': highest_deaths['Deaths'],
        'Least': lowest_deaths['State/UTs'],
        'Death Cases%': lowest_deaths['Deaths']
    })

    max_deaths_highest = highest_deaths['Deaths'].max()
    max_deaths_lowest = lowest_deaths['Deaths'].max()

    highest_death_bars = [create_bar(value, max_deaths_highest) for value in highest_deaths['Deaths']]
    lowest_death_bars = [create_bar(value, max_deaths_lowest) for value in lowest_deaths['Deaths']]

    death_df['Death%'] = highest_death_bars
    death_df['Death Cases%'] = lowest_death_bars

    st.markdown("<h4 style='text-align: center;'>Death Cases</h4>", unsafe_allow_html=True)
    st.write(death_df.to_html(escape=False), unsafe_allow_html=True)

with cll2:
    # Highest and lowest active cases table
    df4 = data[['State/UTs', 'Active Ratio']].copy()
    highest_active = df4.nlargest(5, 'Active Ratio').reset_index(drop=True)
    lowest_active = df4.nsmallest(5, 'Active Ratio').reset_index(drop=True)
    active_df = pd.DataFrame({
        'Highest': highest_active['State/UTs'],
        'Active Cases': highest_active['Active Ratio'],
        'Least': lowest_active['State/UTs'],
        'Least Active Cases': lowest_active['Active Ratio']
    })

    max_active_highest = highest_active['Active Ratio'].max()
    max_active_lowest = lowest_active['Active Ratio'].max()

    highest_active_bars = [create_bar(value, max_active_highest) for value in highest_active['Active Ratio']]
    lowest_active_bars = [create_bar(value, max_active_lowest) for value in lowest_active['Active Ratio']]

    active_df['Active Cases'] = highest_active_bars
    active_df['Least Active Cases'] = lowest_active_bars

    st.markdown("<h4 style='text-align: center;'>Active Cases</h4>", unsafe_allow_html=True)
    st.write(active_df.to_html(escape=False), unsafe_allow_html=True)
