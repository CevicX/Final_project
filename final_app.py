import streamlit as st
import pandas as pd
import numpy as np
import base64
import pickle
import plotly.express as px

model = pickle.load(open('forest_2.pkl', 'rb'))

# Sample DataFrame (replace this with your actual DataFrame)
unique_values_grouped = pd.read_csv('data_test.csv')

# Create a Streamlit app
st.title("Whats your range?")

# Create a selector to switch between pages
page_selector = st.selectbox("Select Page", ["Attribute Selection", "Graphics Page"])

if page_selector == "Attribute Selection":
    st.write(
        "This app allows you to select programming languages and attribute values to suggest a salary range."
    )

    # Create a sidebar for attribute selection
    st.sidebar.title("Options")

    # List of attributes where multiple selections are allowed (Programming Languages)
    multi_select_attributes = [
        'Bash/Shell ( all shells )', 'HTML/CSS', 'JavaScript', 'Ruby', 'SQL',
        'TypeScript', 'C#', 'PowerShell', 'Kotlin', 'Python', 'Java', 'Perl',
        'Dart', 'Go', 'Haskell', 'PHP', 'Delphi', 'C++', 'Clojure', 'Elixir',
        'Lua', 'Rust', 'C', 'Scala', 'GDScript', 'F#', 'Groovy', 'Lisp', 'Swift',
        'Objective-C', 'Visual Basic (.Net)', 'R', 'VBA', 'APL', 'Assembly',
        'Cobol', 'Fortran', 'Julia', 'MATLAB', 'Prolog', 'Crystal', 'SAS',
        'Apex', 'Solidity', 'Erlang', 'Raku', 'Nim', 'Zig', 'Ada', 'OCaml',
        'Flow'
    ]

    # Create a flag to track if "Programming Language" has been displayed
    programming_language_displayed = False

    # Attributes to show outside the "Programming Language" multi-select box
    attributes_to_show = ['RemoteWork', 'EdLevel', 'DevType', 'OrgSize', 'Country', 'YearsCodePro']

    # Initialize selected_programming_languages with an empty list
    selected_programming_languages = []

    # Allow the user to select "Programming Language"
    if not programming_language_displayed:
        selected_programming_languages = st.sidebar.multiselect(
            "Select the programming languages you're familiar with:",
            multi_select_attributes,
            key="programming_languages",  # Unique key
        )
        programming_language_displayed = True

    # Allow the user to select attributes (YearsCodePro, OrgSize, and others)
    selected_attributes = {}
    for column in attributes_to_show:
        options = [f'Select one:'] + [str(val) for val in unique_values_grouped[column].unique()]
        selected_value = st.sidebar.selectbox(
            f"Select {column}",
            options,
            key=f"{column}_selectbox",  # Unique key
        )

        # Store selected value in a dictionary
        selected_attributes[column] = selected_value

    # Display the selected attributes
    st.header("Selected Attributes")
    st.write(selected_attributes)

    # Define a function to adapt a skeleton DataFrame with user inputs
    def adapt_skeleton_with_user_inputs(skeleton_data, user_inputs):
        # Iterate over user_inputs and update skeleton_data accordingly
        for key, value in user_inputs.items():
            if key in skeleton_data.columns:
                skeleton_data[key] = value

        return skeleton_data

    # Create a skeleton DataFrame based on the training data (replace this with your actual training data)
    training_data = pd.read_csv('X.csv')

    # Create a skeleton DataFrame with 0 values for selected or not selected columns
    skeleton_data = pd.DataFrame(0, columns=training_data.columns, index=[0])

    # Check if the user has clicked the "Apply" button
    if st.sidebar.button("Apply"):
        # Adapt the skeleton DataFrame with user inputs for programming languages
        for language in multi_select_attributes:
            if language in selected_programming_languages:
                skeleton_data[language] = 1

        # Adapt the skeleton DataFrame with user inputs for other attributes (YearsCodePro, OrgSize, etc.)
        for column, selected_value in selected_attributes.items():
            if selected_value and selected_value != 'Select one:':
                skeleton_data[column + '_' + selected_value] = 1
        
        # Make a prediction
        predictions = model.predict(skeleton_data)
        st.header("Predictions")
        # Assuming 'predictions' is a NumPy array
        prediction_value = predictions[0]  # Assuming it's a single value in the array

        st.write(f'Our model predicts that you will earn: {prediction_value:.2f} USD.')
        skeleton_data.to_csv('adapted_data.csv', index=False)
        lower_bound = prediction_value * 0.9
        upper_bound = prediction_value * 1.1
        st.write(f'Based on this, you should ask for a salary range(10%) between: {lower_bound:.2f} and {upper_bound:.2f} USD.')


else:
    # Load your dataset for the graphics page
    data = pd.read_csv('data_test.csv',)

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
