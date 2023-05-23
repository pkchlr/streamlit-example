# Import necessary libraries
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_plotly_events import plotly_events
from streamlit_toggle import toggle
from streamlit_extras.switch_page_button import switch_page
import plotly.graph_objects as go
import ipywidgets as widgets
import seaborn as sns

# Set streamlit page configuration
st.set_page_config(page_title='Global FDI flows', layout='wide', initial_sidebar_state='collapsed')

# Load the data and compute the difference between predicted and actual FDI
df = pd.read_csv("df_full_with_predictions.csv")
df['diff_pred_real_fdi'] = df['Predicted FDI billion USD'] - df['Foreign Direct Investment billion USD']

# Function to switch page
def jump():
    switch_page('page2')

# Set up page layout with 3 columns
header_left, header_mid, header_right = st.columns(3)

# Set page title in the middle column
with header_mid:
    st.title('Global FDI flows')

# Create two more columns for different views
c1, c2 = st.columns([10, 1.5])

# Create a slider to switch between 'Map' and 'Chart' views
slider = c2.select_slider('Normal', ['Map', 'Chart'], label_visibility='hidden')

# If the slider is set to 'Map'
if slider == 'Map':
    st.header("Global FDI Flows View")
    # Create a choropleth map with predicted FDI as the color scale
    fig1 = px.choropleth(df, locations='Country', locationmode='country names', color='Predicted FDI billion USD',
                         color_continuous_scale='Purples')

    # Update the layout of the map
    fig1.update_layout(
        autosize=False,
        width=1200,
        height=600, legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-.50,
            xanchor="right",
            x=1
        ),
        geo=dict(bgcolor='rgb(14,17,23)')
    )

    # Capture selected points from the map
    selected_points = plotly_events(fig1)

    # If any points are selected
    if selected_points:
        a = selected_points[0]
        a = pd.DataFrame.from_dict(a, orient='index')

        # Save the selected country to the session state
        st.session_state.country = df.iloc[a[0]['pointIndex']]['Country']
        # Switch to the second page
        switch_page('page2')

# If the slider is set to 'Chart'
if slider == 'Chart':
    with st.sidebar:
        # Allow the user to select a country from a dropdown
        country_filter = st.selectbox(label='Select The Country',
                                      options=df['Country'].unique())

    # Create a line chart for the selected country showing actual and predicted FDI over time
    linechr = plt.figure(figsize=(16, 5))
    st.header("Global FDI flows view")
    fig2 = sns.lineplot(data=df[df.Country == country_filter], y="Foreign Direct Investment billion USD", x="Year", )
    sns.lineplot(data=df[df.Country == country_filter], y='Predicted FDI billion USD', x="Year")
    fig2.yaxis.label.set_color('white')
    fig2.tick_params(axis='x', colors='white')
    fig2.tick_params(axis='y', colors='white')
    st.pyplot(linechr)

# Add a divider and
# Add a divider line
st.divider()

# Add a header for the ranking section
st.header("Investment Potential Ranking")

# Add some spacing
st.write("#")
st.write("#")

# Compute the difference between predicted and actual FDI again
df['diff_pred_real_fdi'] = df['Predicted FDI billion USD'] - df['Foreign Direct Investment billion USD']

# Calculate the sum of differences by country
fdi_diff = df.groupby('Country')['diff_pred_real_fdi'].sum().to_frame().reset_index().sort_values('diff_pred_real_fdi')

# This line seems to be a duplicate and can be removed
df.groupby('Country')['diff_pred_real_fdi'].sum()

# Set the color scheme for seaborn plots
sns.set(rc={'axes.facecolor': '#0E1117', 'figure.facecolor': '#0E1117'})

# Set up the layout with two columns
col1, col2 = st.columns([1, 2])

# Write a description in the first column
col1.write("Countries ranked based on the difference between predicted and status quo FDI flows.")

# Create a bar chart in the second column
barchr = plt.figure(figsize=(13, 3))
fig = sns.barplot(
    y='Country',
    x='diff_pred_real_fdi',
    data=fdi_diff.tail(5),
    palette=['white', 'aqua', 'deepskyblue', 'fuchsia', 'blueviolet']
)

# Set the title of the bar chart
fig.set_title(label="Ranking", fontdict={
    'size': 20, 'weight': 'bold', 'color': 'white'})
fig.set(xlabel='')
fig.yaxis.label.set_color('white')
fig.tick_params(axis='x', colors='white')
fig.tick_params(axis='y', colors='white')
col2.pyplot(barchr)

# Run the Streamlit app
#streamlit run main.py
