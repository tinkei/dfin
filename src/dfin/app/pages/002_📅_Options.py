import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

from dfin.app.utils import setup_yahoo, add_sidebar_selector


st.set_page_config(
    page_title='Options | dFin',
    page_icon='📅'
)
st.sidebar.header('Options')
st.write('# Options of Selected Symbols')
setup_yahoo()
add_sidebar_selector()


if 'highlight_itm' not in st.session_state:
    st.session_state['highlight_itm'] = False
    st.session_state['highlight_itm_text'] = 'Highlight in-the-money options (breaks formatting)'

def toggle_itm_highlight():
    st.session_state['highlight_itm'] = not st.session_state['highlight_itm']
    if st.session_state['highlight_itm']:
        st.session_state['highlight_itm_text'] = 'Disable highlighting in-the-money options'
    else:
        st.session_state['highlight_itm_text'] = 'Highlight in-the-money options (breaks formatting)'

st.button(
    st.session_state['highlight_itm_text'],
    key=None,
    on_click=toggle_itm_highlight,
)


def getExponent(number):
    import decimal
    return decimal.Decimal(number).as_tuple().exponent
getExponent = np.vectorize(getExponent)


# Formatting Styler will break default styles.
def format_table(styler: pd.io.formats.style.Styler):
    """Highlight in-the-money options and limit displayed precision of floats."""

    styler.applymap(lambda x: f'background-color: gray', subset=['strike'])
    styler.applymap(lambda x: f'background-color: DarkGreen', subset=(merged.index[merged['inTheMoneyCall']==True].tolist(), [col for col in merged.columns if 'Call' in col]))
    styler.applymap(lambda x: f'background-color: DarkGreen', subset=(merged.index[merged['inTheMoneyPut']==True].tolist(), [col for col in merged.columns if 'Put' in col]))

    for col in ['strike', 'askCall', 'bidCall', 'lastPriceCall', 'askPut', 'bidPut', 'lastPricePut']:
        precision = 3
        exponents = - getExponent(styler.data[col].dropna().to_numpy())
        precision = min(precision, np.max(exponents))
        styler.format(formatter=None, subset=[col], na_rep=None, precision=precision, decimal='.', thousands=',')

    styler.format(formatter=None, subset=['volumeCall', 'volumePut', 'openInterestCall', 'openInterestPut'], na_rep=None, precision=0, decimal='.', thousands=',')

    return styler


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

            calls = ticker.option_chain(expiration).calls
            calls = calls.drop(['currency', 'contractSize', 'percentChange', 'change'], axis=1)
            calls = calls[calls['lastTradeDate'] > date_filter]
            calls = calls.add_suffix('Call')
            calls = calls[(calls.columns.to_list()[2:] + calls.columns.to_list()[:2])[::-1]]

            puts = ticker.option_chain(expiration).puts
            puts = puts.drop(['currency', 'contractSize', 'percentChange', 'change'], axis=1)
            puts = puts[puts['lastTradeDate'] > date_filter]
            puts = puts.add_suffix('Put')
            puts = puts[puts.columns.to_list()[2:] + puts.columns.to_list()[:2]]

            # st.write(f'#### Outer Join:')
            merged = pd.merge(calls, puts, left_on='strikeCall', right_on='strikePut', how='outer')
            merged['strikeCall'] = merged['strikeCall'].fillna(merged['strikePut'])
            merged = merged.drop(['strikePut'], axis=1).rename(columns={'strikeCall': 'strike'}).sort_values(by=['strike']).reset_index(drop=True)

            if st.session_state['highlight_itm']:
                styler = merged.style.pipe(format_table)
                st.dataframe(styler)
            else:
                st.dataframe(merged)

            # st.write(f'#### Calls:')
            # st.dataframe(ticker.option_chain(expiration).calls)
            # st.write(f'#### Puts:')
            # st.dataframe(ticker.option_chain(expiration).puts)
