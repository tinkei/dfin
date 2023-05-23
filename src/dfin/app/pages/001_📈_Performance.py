import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time

from dfin.app.utils import setup_yahoo, add_sidebar_selector


st.set_page_config(
    page_title='Performance | dFin',
    page_icon='📈'
)
st.sidebar.header('Performance')
st.write('# Performance of Selected Symbols')
setup_yahoo()
add_sidebar_selector()


if 'animation_shown' in st.session_state and st.session_state['animation_shown']:

    for symbol in st.session_state['selected_symbols']:

        st.write(f'## {symbol}')
        ticker = yf.Ticker(symbol, session=st.session_state['yf_session'])
        underlying_history_1y = ticker.history('1y')

        days = len(underlying_history_1y)
        line_chart = st.line_chart(underlying_history_1y[['High', 'Low']])
        bar_chart = st.bar_chart(underlying_history_1y[['Volume']])
        my_table = st.dataframe(underlying_history_1y, use_container_width=True)

else:

    step = 10
    sleep = 0.05
    progress_bar = st.sidebar.progress(0, text='')
    # status_text = st.sidebar.empty()
    st.session_state['animation_shown'] = True

    for symbol in st.session_state['selected_symbols']:

        st.write(f'## {symbol}')
        ticker = yf.Ticker(symbol, session=st.session_state['yf_session'])
        underlying_history_1y = ticker.history('1y')
        progress_bar.progress(0, text='')

        days = len(underlying_history_1y)
        # Cannot pre-allocate DataFrame, because chart update only works with `add_rows`.
        # line_chart_data = pd.DataFrame(index=underlying_history_1y.index, columns=underlying_history_1y[['High', 'Low']].columns)
        # bar_chart_data = pd.DataFrame(index=underlying_history_1y.index, columns=underlying_history_1y[['Volume']].columns)
        # my_table_data = pd.DataFrame(index=underlying_history_1y.index, columns=underlying_history_1y.columns)
        # line_chart = st.line_chart(line_chart_data)
        # bar_chart = st.bar_chart(bar_chart_data)
        # my_table = st.dataframe(my_table_data, use_container_width=True)
        line_chart = st.line_chart(underlying_history_1y[['High', 'Low']].iloc[:step, :])
        bar_chart = st.bar_chart(underlying_history_1y[['Volume']].iloc[:step, :])
        my_table = st.dataframe(underlying_history_1y.iloc[:step, :], use_container_width=True)
        # status_text.text(f'{symbol} {1/int(np.ceil(days/step))*100:.0f}% complete')
        status_text = f'{symbol} {1/int(np.ceil(days/step))*100:.0f}% complete'
        progress_bar.progress(1/int(np.ceil(days/step)), text=status_text)

        for i in range(2, int(np.ceil(days/step+1))):
            line_chart.add_rows(underlying_history_1y[['High', 'Low']].iloc[step*(i-1):step*i, :])
            bar_chart.add_rows(underlying_history_1y[['Volume']].iloc[step*(i-1):step*i, :])
            my_table.add_rows(underlying_history_1y.iloc[step*(i-1):step*i, :])
            # status_text.text(f'{symbol} {i/int(np.ceil(days/step))*100:.0f}% complete')
            status_text = f'{symbol} {i/int(np.ceil(days/step))*100:.0f}% complete'
            progress_bar.progress(i/int(np.ceil(days/step)), text=status_text)
            time.sleep(sleep)

        time.sleep(sleep*10)

    progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
def re_run():
    st.session_state['animation_shown'] = False
st.button('Re-run animation', on_click=re_run)
