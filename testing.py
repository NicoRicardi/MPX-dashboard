#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 22:52:02 2022

@author: nico
"""
import streamlit as st
from functions import load_data, total_weekly_metrics, plot_tot, plot_countries, \
    barstack_countries, get_daily_count, na_percentage
import plotly.express as px
import pandas as pd
import numpy as np

TITLE = 'Monkey Pox Evolution'
st.set_page_config(page_title=TITLE,
                    page_icon=':chart:',
                    layout='wide',
                    initial_sidebar_state='auto',
                    menu_items={
                                'Get Help': 'https://www.thegraphnetwork.org',
                                'Report a bug': 'https://github.com/thegraphnetwork/MPX-dashboard/issues',
     })
st.sidebar.image('tgn.png')
st.title(TITLE)
with st.sidebar.expander('Additional Information'):
    st.markdown('Data from [Global.Health](https://github.com/globaldothealth/monkeypox "https://github.com/globaldothealth/monkeypox")')
    st.markdown('Rolling averages use an exponential weighing of the data.')

file = 'https://raw.githubusercontent.com/globaldothealth/monkeypox/main/latest.csv'
data_load_state = st.text('Loading data...')
all_cases = load_data(file, cols=None)
# all_cases = load_data(cols=None)
data_load_state.text('Data loaded!')

# df  = pd.DataFrame(all_cases.set_index('Date_confirmation').groupby('Country').count()['ID'])
# df.columns = ['Cases']
# d_iso3 = all_cases.set_index("Country")["Country_ISO3"].to_dict()
# # df["Country"] = df.index
# df = df.reset_index()
# df["Country_ISO3"] = df['Country'].map(d_iso3)

# fig = px.choropleth(df, locations="Country_ISO3",
#                     color="Cases", 
#                     hover_name="Country", # column to add to hover information
#                     color_continuous_scale=px.colors.sequential.Plasma,)

df = pd.DataFrame(all_cases[all_cases.Status=='confirmed'].set_index('Date_confirmation').groupby('Country').resample('D').count()['ID'])
df.columns = ['daily cases']
d_iso3 = all_cases.set_index("Country")["Country_ISO3"].to_dict()
df = df.reset_index()
df["Country_ISO3"] = df['Country'].map(d_iso3)
df["cumulative cases"] = df.groupby('Country').cumsum()['daily cases']
lam = lambda x: x.dayofyear
df['day'] = df['Date_confirmation'].apply(lam)

fig = px.choropleth(df, locations="Country_ISO3",
                    color="cumulative cases", # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma,
                    animation_frame='day')
st.plotly_chart(fig, use_container_width=True)

# date1, date2 = 'Date_confirmation', 'Date_entry'
# notna = all_cases[np.logical_and(all_cases[date1].notna(), all_cases[date2].notna())]
# series = notna[date2] - notna[date1]
# fig = px.histogram(series)
# fig.update_xaxes(
#     dtick="M1",
#     tickformat="%b\n%Y")
# fig.update_xaxes(dtick='D1', tickformat='%D')
# st.plotly_chart(fig, use_container_width=True)