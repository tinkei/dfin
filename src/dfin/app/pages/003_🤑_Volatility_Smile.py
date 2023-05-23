import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

from dfin.app.utils import setup_yahoo, add_sidebar_selector


st.set_page_config(
    page_title='Volatility Smile | dFin',
    page_icon='🤑'
)
st.sidebar.header('Volatility Smile')
st.write('# Volatility Smile')
setup_yahoo()
add_sidebar_selector()


tabs = st.tabs(st.session_state['selected_symbols'])
date_filter = pd.Timestamp.utcnow().floor('D') + pd.offsets.Day(-30)

for symbol, tab in zip(st.session_state['selected_symbols'], tabs):

    with tab:

        st.write(f'## {symbol}')
        ticker = yf.Ticker(symbol, session=st.session_state['yf_session'])
        # print(ticker.options)

        if f'{symbol}_default_options' not in st.session_state:
            num_options = len(ticker.options)
            st.session_state[f'{symbol}_default_options'] = ticker.options[max(0,int(num_options/2)-2):min(int(num_options/2)+3,num_options)]

        def update_selected_expirations(symbol):
            st.session_state[f'{symbol}_default_options'] = sorted(st.session_state[f'{symbol}_selected_options'])

        st.multiselect(
            'Select option expirations to display:',
            ticker.options,
            st.session_state[f'{symbol}_default_options'],
            key=f'{symbol}_selected_options',
            on_change=update_selected_expirations,
            args=(symbol,)
        )

        for expiration in st.session_state[f'{symbol}_selected_options']:

            st.write(f'### {expiration}')

            calls = ticker.option_chain(expiration).calls.dropna()
            calls = calls[calls['lastTradeDate'] > date_filter]
            calls = calls[['impliedVolatility', 'strike']]
            calls = calls[(calls != 0).all(axis=1)]
            calls = calls.add_suffix('Call')

            puts = ticker.option_chain(expiration).puts.dropna()
            puts = puts[puts['lastTradeDate'] > date_filter]
            puts = puts[['impliedVolatility', 'strike']]
            puts = puts[(puts != 0).all(axis=1)]
            puts = puts.add_suffix('Put')

            # st.write(f'#### Outer Join:')
            merged = pd.merge(calls, puts, left_on='strikeCall', right_on='strikePut', how='outer')
            merged['strikeCall'] = merged['strikeCall'].fillna(merged['strikePut'])
            merged = merged.drop(['strikePut'], axis=1).rename(columns={'strikeCall': 'strike'}).sort_values(by=['strike']).reset_index(drop=True)
            st.line_chart(merged, x='strike', y=['impliedVolatilityCall', 'impliedVolatilityPut'])
            st.dataframe(merged, use_container_width=True)

            # st.write(f'#### Calls:')
            # st.dataframe(ticker.option_chain(expiration).calls)
            # st.write(f'#### Puts:')
            # st.dataframe(ticker.option_chain(expiration).puts)
