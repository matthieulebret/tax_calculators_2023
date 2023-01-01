import streamlit as st
import numpy as np
import pandas as pd
import datetime
import xlrd

import plotly.express as px


st.title('Master Tax calculator')

tab1,tab2,tab3 = st.tabs(['Uk tax','French tax','French IFI'])

with tab1:
    st.header('Calculate your UK tax')

    def uktax(comp):
        if comp < 37700:
            tax = comp*0.2
            basic = comp*0.2
            return tax,basic
        elif comp < 125140:
            tax = (comp-37700)*0.4 + 7540
            basic = 37700*0.2
            higher = (comp-37700)*0.4
            return tax, basic,higher
        else:
            basic = 37700*0.2
            higher = (125140-37700)*0.4
            top = (comp-125140)*0.45
            tax = (comp-125140)*0.45 + basic + higher
            return tax,basic,higher,top

    def nic(comp):
        lowlim = 242*52
        uplim = 967*52
        primthr = 242*52
        secthr = 175*52

        if comp < lowlim:
            contrib = 0
        elif comp < uplim:
            contrib = 0.12*(comp - lowlim)
        else:
            contrib = 0.02*(comp - uplim)+0.12*(uplim - lowlim)

        return contrib

    comp = st.number_input('Enter your total comp',value =290000.00,format='%f',step=1.00)

    col1,col2 = st.columns(2)
    with col1:
        st.metric('Your 2023 / 2024 annual net income is:','{:,.2f}'.format(comp - uktax(comp)[0]-nic(comp)))
        st.metric('Your 2023 / 2024 monthly net income is:','{:,.2f}'.format((comp - uktax(comp)[0]-nic(comp))/12))

    with col2:
        st.metric('Your 2023 / 2024 tax is:','{:,.2f}'.format(uktax(comp)[0]))
        st.metric('Your 2023 / 2024 nic is:','{:,.2f}'.format(nic(comp)))

    income = [comp - uktax(comp)[0]-nic(comp), uktax(comp)[0], nic(comp)]
    income = [float(item) for item in income]
    columns = ['Net income','Income tax','NIC']

    df = pd.DataFrame(income, columns)
    df.reset_index(inplace=True)
    df.columns=['Item','Amount']
    df['Total']='Gross income'


    fig = px.sunburst(df,path=['Total','Item'],values='Amount')
    st.plotly_chart(fig)

with tab2:

    st.header('Calculate your French income tax')

    def getfrtax(parts,income):
        income = income / parts
        if income < 10777.00:
            impot = 0.00
        elif income < 27478.00:
            impot = (income - 10777.00)*0.11
        elif income < 78570.00:
            impot = (income - 27478.00)*0.3 + 1837.11
        elif income < 168994.00:
            impot = (income - 78570.00)*0.41 + 17164.71
        else:
            impot = (income - 168994.00)*0.45 + 54238.55
        return impot * parts


    parts = st.number_input('Enter the number of tax pax in the household',value=3.00,format ='%f',step=1.00)
    income = st.number_input('Enter income for the household',value=340000.00,format='%f',step=1.00)

    impot1 = getfrtax(2,income)
    impot2 = getfrtax(parts,income)

    impot = impot1 - (max(min(impot2,1694.00*(parts-2)*2),0))

    col1,col2 = st.columns(2)
    with col1:
        st.metric('Your 2023 annual net income is:','{:,.2f}'.format(income - impot))
        st.metric('Your 2023 monthly net income is:','{:,.2f}'.format((income - impot)/12))

    with col2:
        st.metric('Your 2023 income tax is:','{:,.2f}'.format(impot))


    income = [income-impot,impot]
    columns = ['Net income','Tax']

    df = pd.DataFrame(income,columns)
    df.reset_index(inplace=True)
    df.columns=['Item','Amount']
    df['Total'] = 'Gross income'

    fig = px.sunburst(df,path=['Total','Item'],values='Amount')
    st.plotly_chart(fig)

with tab3:

    st.header('Calculate your IFI')

    def getifi(princip, secondaire):
        assiette = secondaire + princip * 0.7
        if assiette < 1300000:
            return 0
        elif assiette < 2570000:
            return (assiette - 800000)*0.007 + 2500
        elif assiette < 5000000:
            return (assiette -2570000)*0.01 + 11390
        elif assiette < 10000000:
            return (assiette - 5000000)*0.0125 + 35690
        else:
            return (assiette - 10000000)*0.15+98190

    princip = st.number_input('Enter the net value of your main residence',value =1400000.00,format='%f',step=1.00)
    second = st.number_input('Enter the net value of your other real estate assets',value =1500000.00,format='%f',step=1.00)

    st.metric('Your IFI for the year is:','{:,.2f}'.format(getifi(princip,second)))
