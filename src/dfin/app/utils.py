import streamlit as st


# ==============================
# Setup Yahoo Finance API.
# ==============================

def setup_yahoo():

    if 'yf_session' not in st.session_state:

        from requests import Session
        from requests_cache import CacheMixin, SQLiteCache
        from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
        from pyrate_limiter import Duration, RequestRate, Limiter
        class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
            pass

        session = CachedLimiterSession(
            limiter = Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
            bucket_class = MemoryQueueBucket,
            backend = SQLiteCache("yfinance.cache"),
        )

        st.session_state['yf_session'] = session


# ==============================
# Select stock symbols.
# ==============================

def add_sidebar_selector():

    if 'symbols' not in st.session_state:
        st.session_state['symbols'] = set(['AAPL', 'GOOG', 'MSFT'])

    if 'default_symbols' not in st.session_state:
        st.session_state['default_symbols'] = ['GOOG', 'MSFT']

    def update_selection():
        st.session_state['default_symbols'] = sorted(st.session_state['selected_symbols'])

    st.sidebar.multiselect(
        'Select stock symbols to evaluate:',
        sorted(st.session_state['symbols']),
        st.session_state['default_symbols'],
        key='selected_symbols',
        on_change=update_selection,
    )

    # st.sidebar.write('Selected:', st.session_state['selected_symbols'])

    def add_symbol():
        if len(st.session_state['new_symbol']) == 0 or 5 < len(st.session_state['new_symbol']):
            return
        st.session_state['new_symbol'] = st.session_state['new_symbol'].upper()
        if st.session_state['new_symbol'] not in st.session_state['symbols']:
            st.session_state['default_symbols'] += [st.session_state['new_symbol']]
            st.session_state['symbols'].add(st.session_state['new_symbol'])
            st.session_state['default_symbols'] = sorted(st.session_state['default_symbols'])
            st.session_state['symbols'] = sorted(st.session_state['symbols'])

    st.sidebar.text_input(
        'Add symbol',
        '',
        key='new_symbol',
        on_change=add_symbol,
    )
