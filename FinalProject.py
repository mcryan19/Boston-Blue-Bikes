"""
Class: CS230--Section 1
Name: Matt Ryan
Description: (Final Project - Boston Blue Bikes)
I pledge that I have completed the programming assignment
independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""

# Things that need to be imported
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk # not used


# Load data function
def load_data_func(file1,file2= '201501-hubway-tripdata 2.csv'): # Two or more parameters (ond with default)
    df1 = pd.read_csv(file1, header=1) # Read in files
    df2 = pd.read_csv(file2, header=0)
    return df1, df2 # return more than one value


# Introduction page function
def intro_func(image1):
    st.header("Welcome to Boston Blue Bikes")
    st.write("Hi! My name is Matt and I created this Streamlit page to allow for the the access and exploration of "
             "Boston Blue Bikes data."
             "\n\nUse the drop-down menu on the left to navigate the site")

    # Image - Page design feature
    image = st.image(image1)
    header = st.header("Enjoy learning more about Boston Blue Bikes!")
    return image,header # return more than one value


# Information on Bikes Based On Location Function
def Location_Data(df1,df2):
    st.header('Location Data')

    # Sub-header
    st.subheader('Bikes per Start Station')

    # Pull Station info
    start_stations = df2["start station name"].unique().tolist()

    # Drop-down bar
    label = 'Choose Start Station'
    selected_choice = st.selectbox(label, start_stations) # First streamlit widget

    # Bikes per Town
    total_bikes = df2[df2["start station name"] == selected_choice]["start station name"].value_counts()
    st.write("Total Bikes: ",total_bikes)

    # Bar Chart
    bikes_per_station = df2["start station name"].value_counts() # Frequency count - Data Analytics Capabilities
    st.bar_chart(bikes_per_station)

    # Sub-header
    st.subheader('Docks per District')

    # Total Docks per District
    district = df1["District"].dropna().unique().tolist() # See citation

    # Drop-down bar
    label = 'Choose District'
    selected_choice2 = st.selectbox(label, district)

    # Bikes per District
    total_docks = df1[df1["District"] == selected_choice2].groupby('Deployment Year')['Total docks'].sum()
    st.write("Total Docks: ", total_docks)

    # Bar Chart
    st.bar_chart(total_docks) # First visualization bar chart

    # Unfortunately, not allowed to use x and y labels when creating streamlit graphs - not sure if due to new streamlit
    # update. Would have had to use matplotlib or other charting packages. Label can be seen on pie chart where
    # matplotlib was used.

# Information on Trips Function
def Trip_Duration(df2):
    # Header
    st.header('Trip Duration Data')

    # Find birth year in dataframe as long as not \n and provide it as option
    age = df2[df2["birth year"] != "\\N"]["birth year"].unique()

    # Sort from youngest to oldest - Data Analytics Capabilities
    age = np.sort(age)[::-1]

    # Button options
    label1 = 'Birth Year'
    selected_choice1 = st.radio(label1, age) # Second Streamlit widget
    selected_choice1 = selected_choice1.strip() # Get rid of \n

    # Filter in case of 'nan' values - subset specifies which rows to drop if there is no value in "tripduration"
    filtered_duration = df2[df2["birth year"] == selected_choice1].dropna(subset=["tripduration"]) # See citation

    # Find average duration of filtered duration data frame - checks to see if user selected an option
    if not filtered_duration.empty:
        Avg_duration = filtered_duration["tripduration"].mean()
        st.write(f"Average Trip Duration for someone born in {selected_choice1}: {Avg_duration:.0f} minutes")

        new_df = df2.groupby("birth year")['tripduration'].mean().reset_index() # see citation
        # Groupby idea I got from GeeksforGeeks see citation
        # Allows you to group data and then I was able to find the mean
        # Reset index resets the dataframe from being grouped

        # Second visualization line chart
        st.line_chart(new_df.set_index('birth year')) # Need set index so birth year is the index of the chart
    else:
        st.write(f"No trip data available")


# Information on User Function
def User_Info(df2):
    # Header
    st.header('User Information')

    # Sub-header
    st.subheader('Age and Gender Breakdown')

    # Options
    age_options = ['Before 1975', 'After 1975']
    gender_options = ['Male', 'Female']

    # Labels
    label_age = 'Choose Age'
    label_gender = 'Choose Gender'

    # Multiselect widget
    selected_choice = st.multiselect(label_age, age_options) # Third streamlit widget
    selected_choice2 = st.multiselect(label_gender, gender_options)

    # Convert birth year to number from string using to-numeric.
    # errors="coerce" makes anything not convertible = NaN
    # Manipulating Data - Data Analytics Capabilities
    df2['birth year'] = pd.to_numeric(df2['birth year'], errors="coerce") # See citation

    # Create new dataframe where value is not Nan
    # Manipulating Data - Data Analytics Capabilities
    new_df2 = df2[df2['birth year'].notna()]

    # Filter based on new data frame birth year - one condition
    if 'Before 1975' in selected_choice:
        correct_data = new_df2[new_df2["birth year"] <= 1975]
    elif 'After 1975' in selected_choice:
        correct_data = new_df2[new_df2["birth year"] > 1975]
    else:
        correct_data = new_df2

    # Further filter based on gender - second condition
    if 'Male' in selected_choice2:
        correct_data = correct_data[correct_data["gender"] == 1]
    elif 'Female' in selected_choice2:
        correct_data = correct_data[correct_data["gender"] == 2]

    # Calculate and display percentage
    total_people_criteria = len(correct_data)
    total_people = len(new_df2)
    percentage = ((total_people_criteria / total_people) * 100) if total_people != 0 else 0 # See citation
    st.write(f"Percentage: {percentage:.0f}%")

    # Third visualization pie chart

    # Header
    st.subheader("Overall Gender Distribution")

    # Chart

    # Count Values
    amount_based_gender = new_df2['gender'].value_counts()

    # Create figure and axis for pie chart
    chart, axis = plt.subplots()

    # Set pie chart on axis, label based on index, format to show one decimal place, set start angle - 90 degrees
    axis.pie(amount_based_gender, labels= amount_based_gender.index, autopct='%1.1f%%', startangle=90)

    # Draw pie chart as circle
    axis.axis('equal')

    # Labels
    plt.xlabel('1 = Male \n 2 = Female')

    # Display chart
    st.pyplot(chart)


def main():
    # Title and Sidebar
    st.title('Matt Ryan CS230 Final Project')
    choice = st.sidebar.selectbox('Choose Option', ['Introduction', 'Location Data', 'Trip Duration',
                                                    'User Information'])

    # Load data - other file set as default parameter
    file1 = (
        '/Users/mattryan/Library/CloudStorage/OneDrive-BentleyUniversity/PyCharmProjects/First/FinalProject/current_'
        'bluebikes_stations.csv')

    df1, df2 = load_data_func(file1)
    print(df1)
    print(df2)

    # New Dataframe that needs to be defined
    new_df = pd.DataFrame(columns=['Birth Year', 'Average Trip Duration'])


    # If statements for sidebar - streamlit feature
    if choice == "Introduction":
        image1 = 'img.png'
        intro_func(image1)
    elif choice == "Location Data":
        Location_Data(df1,df2)
    elif choice == "Trip Duration":
        Trip_Duration(df2)
    elif choice == "User Information":
        User_Info(df2)

if __name__ == "__main__":
    main()

    # Citations
    # Streamlit - https: // streamlit.io / for widgets and other functions
    # GeeksforGeeks for groupby function - https://www.geeksforgeeks.org/python-pandas-dataframe-groupby/
    # if else one line expresssion - https://book.pythontips.com/en/latest/ternary_operators.html
    # errors = "coerce" - https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
    # set_index and reset_index - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html
    # dropna and subet - https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html
    # tolist() - https://www.programiz.com/python-programming/numpy/methods/tolist#:~:text=The%20tolist()%20method%20converts,changing%20its%20data%20or%20dimensions.
