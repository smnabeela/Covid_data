import streamlit as st 
import pandas as pd 
import plotly.express as px

st.set_page_config(layout="wide")
st.header('Covid Data')

data = pd.read_csv('/workspaces/Covid_data/Covid_Dashboard1.csv')

a=data['State/UTs'].unique()
s = st.selectbox('Select State',(a))

df=data[data['State/UTs']==s]
st.write(df)

with st.container():
        c1,c2,c3,c4=st.columns(4)
with c1:
        c1.metric(label='Total cases', value=round(df['Total Cases'].sum(),2))
with c2:
        c2.metric(label='Recovered', value=round(df['Discharged'].sum(),2))
with c3:
        c3.metric(label='Death', value=round(df['Deaths'].sum(),2))
with c4:
        c4.metric(label='Active', value=round(df['Active Ratio'].sum(),2))


cl1,cl2,cl3= st.columns(3)
with cl1:
        fig = px.bar(data,x='Death Ratio',y='State/UTs',title='Death Rate')
        st.write(fig)
with cl2:
        fig1 = fig = px.bar(data,x='Discharged',y='State/UTs',title ='Recoverer Rate')
        st.write(fig1)
with cl3:
        fig2 = px.pie(data, values='Active', names='Zone', title='Cases by Zone')
        st.write(fig2)
col1,col2 = st.columns(2)
with col1:
        fig3 = px.bar(data, 
               x='State/UTs', 
               y=['Active', 'Deaths'], 
               title='Active Cases and Deaths',
               labels={'value': 'Count', 'variable': 'Category'},
               barmode ='group')
        st.write(fig3)
with col2:
        fig4 = px.bar(data, 
               x='State/UTs', 
               y=['Total Cases', 'Discharged'], 
               title='Total Discharged',
               labels={'value': 'Count', 'variable': 'Category'},
               barmode ='group')
        st.write(fig4)

colm1,colm2,colm3 =st.columns(3)
with colm1:
        total_cases_df = data[['State/UTs', 'Total Cases']].copy()

        highest_cases = total_cases_df.nlargest(5, 'Total Cases').reset_index(drop=True)
        lowest_cases = total_cases_df.nsmallest(5, 'Total Cases').reset_index(drop=True)

        combined_df = pd.DataFrame({
        'State': highest_cases['State/UTs'],
        'Highest Cases': highest_cases['Total Cases'],
        'States': lowest_cases['State/UTs'],
        'Least Cases': lowest_cases['Total Cases']
        })
        st.markdown("<h4 style='text-align: center;'>Total Cases</h4>", unsafe_allow_html=True)
        st.table(combined_df)