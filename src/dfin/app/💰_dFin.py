import streamlit as st

from dfin.app.utils import setup_yahoo, add_sidebar_selector


st.set_page_config(
    page_title='dFin',
    page_icon='💰',
)
st.sidebar.header('Introduction')
st.write('# Welcome to dFin! 💰 ')
setup_yahoo()
add_sidebar_selector()


st.sidebar.success('☝🏼 Select a demo above.')

st.markdown(
    """
    [dFin](https://github.com/tinkei/dfin) is an open-source app framework built specifically for Machine Learning in Finance.

    _Currently this is only a visualization of Yahoo! Finance data. No dFin-specific features are involved._

    👈🏼 **Select a demo from the sidebar** to see some examples of what dFin can do!
    """
)
