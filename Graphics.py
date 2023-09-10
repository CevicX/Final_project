import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset
data = pd.read_csv('data_test.csv')

st.title("Graphics Page")

# Create sidebar filters for developer type, remote work, education level, organization size, and country
selected_devtype = st.sidebar.selectbox('Select Developer Type', ['- Select Developer Type -'] + list(data['DevType'].unique()), index=0)
selected_remote_work = st.sidebar.selectbox('Select Remote Work', ['- Select Remote Work -'] + list(data['RemoteWork'].unique()), index=0)
selected_ed_level = st.sidebar.selectbox('Select Education Level', ['- Select Education Level -'] + list(data['EdLevel'].unique()), index=0)
selected_org_size = st.sidebar.selectbox('Select Organization Size', ['- Select Organization Size -'] + list(data['OrgSize'].unique()), index=0)
selected_country = st.sidebar.selectbox('Select Country', ['- Select Country -'] + list(data['Country'].unique()), index=0)

# Filter the dataset based on the selected filters
if selected_devtype != '- Select Developer Type -':
    filtered_data = data[data['DevType'] == selected_devtype]
else:
    filtered_data = data

if selected_remote_work != '- Select Remote Work -':
    filtered_data = filtered_data[filtered_data['RemoteWork'] == selected_remote_work]

if selected_ed_level != '- Select Education Level -':
    filtered_data = filtered_data[filtered_data['EdLevel'] == selected_ed_level]

if selected_org_size != '- Select Organization Size -':
    filtered_data = filtered_data[filtered_data['OrgSize'] == selected_org_size]

if selected_country != '- Select Country -':
    filtered_data = filtered_data[filtered_data['Country'] == selected_country]

# Scatter Plot
st.subheader("Scatter Plot")

# Define the desired order of 'YearsCodePro' categories
desired_order = [
    "Less than 1 year",
    "2 to 5 years",
    "6 to 10 years",
    "11 to 20 years",
    "21 to 30 years",
    "More than 30 years"
]

# Create the scatter plot with color-coding for the 'YearsCodePro' categories
scatter_fig = px.scatter(
    filtered_data,
    x='YearsCodePro',        # X-axis: YearsCodePro
    y='ConvertedCompYearly', # Y-axis: ConvertedCompYearly
    color='YearsCodePro',    # Color points by 'YearsCodePro' category
    title='Relationship Between Years of Coding and Yearly Compensation',
    labels={'YearsCodePro': 'Years of Coding Experience', 'ConvertedCompYearly': 'Yearly Compensation'},
    
    # Specify the order of 'YearsCodePro' categories
    category_orders={'YearsCodePro': desired_order}
)

# Show the scatter plot inside Streamlit with all categories in the legend
st.plotly_chart(scatter_fig, use_container_width=True)

# Bar Chart
st.subheader("Bar Chart")

# Calculate the total count of each programming language for the selected developer type
language_counts = filtered_data.iloc[:, 7:-1].sum()  # Select columns with programming languages and sum

# Determine the top N programming languages by usage
top_languages = language_counts.sort_values(ascending=False).head(10)  # Adjust the number of top languages as needed

# Create a bar chart showing top programming languages usage
bar_fig = px.bar(
    x=top_languages.index,  # Programming languages
    y=top_languages.values, # Usage counts
    title=f'Top Programming Languages for {selected_devtype}',
    labels={'x': 'Programming Language', 'y': 'Count'},
)

# Show the bar chart inside Streamlit with all categories in the legend
st.plotly_chart(bar_fig, use_container_width=True)
