import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from numerize.numerize import numerize
from query import view_all_data
import time


st.set_page_config(page_title="DashBoard", page_icon='🌏', layout='wide')
st.subheader('🔔 Insurance Description Analytics')
st.markdown('##')

result =view_all_data()
df=pd.DataFrame(result, columns=['Policy','Expiry','Location','State','Region','Investment','Construction','BusinessType','Earthquake','Flood','Rating','id'])

# side bar
st.sidebar.image('data/logo1.png', caption='Option Analytics')

#switcher
st.sidebar.header('Please Filter')
region = st.sidebar.multiselect(
    'Select Region',
    options=df['Region'].unique(),
    default=df['Region'].unique(),
)
location = st.sidebar.multiselect(
    'Select Location',
    options=df['Location'].unique(),
    default=df['Location'].unique(),
)
construction = st.sidebar.multiselect(
    'Select Construction',
    options=df['Construction'].unique(),
    default=df['Construction'].unique(),
)

df_selection=df.query(
    'Region==@region & Location==@location & Construction == @construction'
)

def home():
    with st.expander('Tabular'):
        show_data = st.multiselect('Filter: ', df_selection.columns, default=[])
        st.write(df_selection[show_data])

    # Compute top analytics
    total_investments = df_selection['Investment'].sum()
    investment_mode = df_selection['Investment'].mode()[0] if not df_selection['Investment'].mode().empty else 0
    investment_mean = df_selection['Investment'].mean()
    investment_median = df_selection['Investment'].median()
    rating = df_selection['Rating'].sum()

    total1, total2, total3, total4, total5 = st.columns(5, gap='large')
    with total1:
        st.info('Total Investment', icon="📌")
        st.metric(label='sum TZS', value=f'{total_investments:,.0f}')
    with total2:
        st.info('Most Frequent', icon="📌")
        st.metric(label='mode TZS', value=f'{investment_mode:,.0f}')
    with total3:
        st.info('Average', icon="📌")
        st.metric(label='mean TZS', value=f'{investment_mean:,.0f}')
    with total4:
        st.info('Central Earnings', icon="📌")
        st.metric(label='median TZS', value=f'{investment_median:,.0f}')
    with total5:
        st.info('Ratings', icon="📌")
        st.metric(label='rating TZS', value=numerize(rating), help=f""" Total Rating: {rating} """)

    st.markdown("""---""")

# graphs

def graphs():
    total_investments = int(df_selection['Investment'].sum())
    averageRating = int(round(df_selection['Investment'].mean(),2))

    investment_by_business_type=(
        df_selection.groupby(by=['BusinessType']).count()[['Investment']].sort_values(by="Investment")
    )
    fig_investment = px.line(
        investment_by_business_type,
        x='Investment',
        y=investment_by_business_type.index,
        orientation='h',
        title='<b>Investment by Business Type</b>',
        color_discrete_sequence=["#0083b8"] * len(investment_by_business_type),
        template='plotly_white',
    )

    fig_investment.update_layout(
        plot_bgcolor='rgb(0,0,0,0)',
        xaxis= (dict(showgrid=False))
    )
    investment_by_state = (
        df_selection.groupby(by=['State']).count()[['Investment']]
    )
    fig_state = px.line(
        investment_by_state,
        x=investment_by_state.index,
        y='Investment',
        orientation='h',
        title='<b>Investment by State</b>',
        color_discrete_sequence=["#0083b8"] * len(investment_by_state),
        template='plotly_white',
    )
    fig_state.update_layout(
        xaxis=dict(tickmode='linear'),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=(dict(showgrid=False))
    )

    left, right =st.columns(2)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

def progressbar():
    st.markdown(
        """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",
        unsafe_allow_html=True, )
    target=3000000000
    current=df_selection['Investment'].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)

    if percent>100:
        st.subheader('Target Done !')
    else:
        st.write(f'you have {percent}% of {format(target, "d")}, TZS')
        for percent_complete in range(percent):
            time.sleep(0.1)
            mybar.progress(percent_complete+1, text='Target Percentage')

def sidebar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )

    if selected == "Home":
        st.subheader(f'Page: {selected}')
        home()
        graphs()
    if selected == "Progress":
        st.subheader(f'Page: {selected}')
        progressbar()
        graphs()

sidebar()

#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""


