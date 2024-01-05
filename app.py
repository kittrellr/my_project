# %%
import pandas as pd 
import streamlit as st 
import plotly.express as px 



# %% [markdown]
# #### Description
# Web application to create an easy, fun, and exciting way for users to explore the pre-owned vehicle market. The goal is to anticpate the user's needs and provide the tools for them to make the best decision when buying or selling a used vehicle. The app will use interactive models for the user to do their own price analysis and vehicle comparisons. We will use Python for coding, Streamlit for app creation, and Render for deployment. The project will be conducted through GitHub and VS code. This is for simulation and practice only. Instruction and review are provided by the TripleTen learning team. 

# %% [markdown]
# # Code Reference
# For missing or unknown values, they have been filled in the following ways:
# - price: 0
# - model_year: median of 'model' and 'model_year'
# - cylinders: median of 'cylinders' and 'type'
# - odometer: median of 'model', 'model_year', and 'odometer' 
# - paint_color: unknown
# - is_4wd: 0
# 
# 

# %% [markdown]
# # Items to include in the app:
# - One st.header with text (https://docs.streamlit.io/library/api-reference/text/st.header)
# - At least one Plotly Express Histogram using st.write (https://docs.streamlit.io/library/api-reference/write-magic/st.write) or st.plotly_chart (https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart)
# - At least one Plotly Express scatter plot using st.write (https://docs.streamlit.io/library/api-reference/write-magic/st.write) or st.plotly_chart (https://docs.streamlit.io/library/api-reference/charts/st.scatter_chart)
# - At least one checkbox using st.checkbox that changes the behavior of any of the above components (https://docs.streamlit.io/library/api-reference/widgets/st.checkbox)

# %%
#read in data

data = pd.read_csv('vehicles_us.csv')


# %% [markdown]
# # The data is arranged nicely so no need to restructure anything at this time. We will go ahead and add a column for manufacturer sine we'll want that information for our user interface.

# %%
# create a new column for manufacturer

data['manufacturer'] = data['model'].apply(lambda x: x.split()[0])


# %% [markdown]
# # Now we will check our data set for any duplicated rows

# %%
# checking for duplicate rows. Results show no duplicated rows in the dataframe

data.duplicated()

# %% [markdown]
# # Beautiful, there are no duplicated rows.

# %% [markdown]
# # Now we'll check our data for missing values 


# %% [markdown]
# # We will fill in the missing values for each column using fillna and transform methods.

# %%
#fill in missing values using fillna

data['price'] = data['price'].fillna(0)
data['paint_color'] = data['paint_color'].fillna('unknown')
data['is_4wd'] = data['is_4wd'].fillna(0)

# %% [markdown]
# # Now to use the transform method to group the data by relevant columns and find appropriate ways to fill in the missing values

# %%
# fill cylinders column by grouping cylinders and type and filling in the missing values with the median vlaue

data['cylinders'] = data[['cylinders', 'type']].groupby('type').transform(lambda x: x.fillna(x.median()))

# For missing values in model_year, we will group it with the model column and find the median range
data['model_year'] = data[['model_year', 'model']].groupby('model').transform(lambda x: x.fillna(x.median()))

# For the odometer column, we will group by the model and model_year columns to get the median of the odometer readings and fill in the missing values
data ['odometer'] = data.groupby(['model_year', 'model'])['odometer'].transform(lambda x: x.fillna(x.median()))

# %% [markdown]
# # Let's check our dataframe to be sure that all of our missing values have been filled.

# %%
# check the number and percentage of missing values in the dataset

# %% [markdown]
# # Wonderful! Our columns no longer have missing data

# %%
# Checking the data shape to ensure it has the number of columns and rows as expected and it does.


# %% [markdown]
# # The model_year column has ',' which is not how we typically write out a year. I will change the column data from a float to integer to see if that can eliminate that issue. 

# %%
#convert model_year column from float to int

data['model_year'] = data['model_year'].astype(int)



# %% [markdown]
# ## Now that our dataframe is cleaned up, let's work on building our web app by incorporating tables, charts, and applying streamlit code! 

# %% [markdown]
# # First we'll create the header or title for our web app using streamlit header to print the text onto our web page. 

# %%
#Create header

st.header('Pre-Owned Vehicle Market')

# %% [markdown]
# # Next we'll create a scrollable dataframe to view our entire dataframe on the web app. 

# %%
# Create title for what we are looking at

st.header('Data Viewer (shows all vehicles currently on the market)')

# Embed dataframe using streamlit

st.dataframe(data)

# %% [markdown]
# # Now we'll incorporate user friendly interactive modules so that they can explore and compare pricing of the used vehicle market. 
# 
# # First I'll add a brief description for user to filter data. 
# 
# # I'll also add a checkbox so that the user can search inventory that has been listed in the last 30 days. This will help our user who may have been looking for a period of time to only view vehicles that have been listed in the past month and compare prices on those. 

# %%
# Create header and brief description that tells user what to do next
st.header('Pre-Owned Vehicle Search')
st.write(""" 
         #### Use the interactive models below to search the inventory for your specific wants and needs. Based on your search criteria, you can compare prices of different vehicle listings by their condition, mileage, type, and manufacturer. If you want to view and compare vehicles listed in the past 30 days, select the checkbox below. The results and price charts will only show inventory listed in the last 30 days.   
         """) 


# Adding checkbox for user to filter data to search only new inventory listed 

show_new_ads = st.checkbox('Show vehicles listed in last 30 days')


# %% [markdown]
# # Now to apply the filter for the check box. This will ensure that if this box is selected, all the data on the web app will be filtered to just vehicles listed in the past 30 days.

# %%
# Create filter for checkbox

if show_new_ads:
    data = data[data.days_listed <= 30]


# %% [markdown]
# ## Now that our checkbox is done, we will create the search option widgets for users to narrow down their search criteria. 

# %% [markdown]
# # First we'll create a filter for users to search vehicles by the vehicle type. (SUV, sedan, truck, coupe, bus, etc.)

# %%
# Take a look at vehicle 'type' column and all of its unique values.

vehicle_type = data['type'].unique()

# Use streamlit to embed a dropdown box for users to select a type of vehicle to search for.
type_choice = st.selectbox('Select vehicle type:', vehicle_type)



# %% [markdown]
# # Now that the user has selected a vehicle type they are searching for, we will let them narrow it down even further by price range they want to search in. To do this, I am going to use a slider bar to select the price range.

# %%
# first we'll create minimum and maximum price points for our data by creating new variables using the min() and max() methods.

min_price, max_price = int(data['price'].min()), int(data['price'].max())

#Next we'll create the slider with streamlit. 

price_range = st.slider(
    "Choose price range", 
    value=(min_price,max_price),min_value=min_price,max_value=max_price )

# %% [markdown]
# # Now that the user has narrowed down their search criteria, we will create a new dataframe based on the specific selections. 

# %%
# Filter the dataset based on the users chosen variables
filtered_table = data[(data.type==type_choice) & (data.price>=price_range[0]) & (data.price <= price_range[1])]



#show the final table in streamlit
st.dataframe(filtered_table)

# %% [markdown]
# ## The filtered search features are complete. Now the user can see what inventory is available for their specific wants. The user can stop here or if they want to compare prices and find the best value they can continue below. 
# 
# ## Here is where we will create interactive models for the user to compare pricing of the vehicles they have narrowed down in their search. We'll create numerous charts such as histograms, scatterplots, and box plots, so that they can compare pricing in a variety of ways. 

# %% [markdown]
# # First we'll create a histogram that will let the user compare pricing of the searched vehicles based on the manufacturer, type of vehicle, and the vehicles condition. 
# 
# # I'll add a brief description of what this section of the web app is for and we'll add are charts from there.

# %%
# Create title/header for section using Streamlit. 
st.header('Price Comparison')
st.write(""" 
         #### Let's see how different factors can influence the price of a vehicle. Select an option below to see the price distribution based on manufacturer, type of vehicle, and condition of vehicle. Double click an item on the legend to view just that item distribution.
         """ )

# We'll create a histogram with the parameter of choice: manufacturer, type, & condition of vehicle. 

# Creating list of options for histogram 
list_for_hist = ['manufacturer', 'type', 'condition']

# Create select box of options for user to choose from. 
choice_for_hist = st.selectbox('Choose one', list_for_hist)

# plot histogram where price_usd is based on the choice made in the selectbox.
fig1 = px.histogram(data, x='price', color=choice_for_hist, title= "<b> Price by {}</b>".format(choice_for_hist))

#add histogram visual to web app 
st.plotly_chart(fig1)


# %% [markdown]
# # Lets take a look at what we've created. 

# %%
fig1.show()

# %% [markdown]
# # Let's say our user wants to know which vehicle holds its value the best and doesn't depreciate as fast as another. For this, we'll create a histogram based on manufacturer and age group of the vehicle to compare the prices of those vehicles. 
# 
# # Since there are so many years that we can choose from, we'll create age group categories instead of a specific year. Lets use categories "less than 5 years old", "5-10 years old", "10-20 years old" and "over 20 years old." 

# %%
#create our section title on the user interface portion of the web app. 

st.header('Best Value')
st.write("""
#### Which manufacturer holds the best value? Use the drop down menus and chart below to compare prices based on vehicle manufacturer and age.
""")

# %%
# Create age categories of vehicles with a function. 

data['age'] = 2023-data['model_year']

def age_category(x):
    if x<5: return 'less than 5 years'
    elif x>=5 and x<10: return '5-10 years'
    elif x>= 10 and x<20: return '10-20 years'
    else: return 'over 20 years'

data['age_category']= data['age'].apply(age_category)


# %%

# Add select box for user to choose manufacturer
vehicle_man = data['manufacturer'].unique()
select_man = st.selectbox('Select Manufacturer', vehicle_man) 

# Add select box for user to choose age of vehicle
age_choice = data['age_category'].unique()
select_age = st.selectbox('Select Age', age_choice)

# Filter data based on user selection.
filtered_data = data[(data['manufacturer'] == select_man) & (data['age_category'] == select_age)]

# plot histogram based off user selection of manufacturer and age.
fig2 = px.histogram(filtered_data, x='price',  title= f"Price Distribution for {select_man} Vehicles ({select_age})")

#add histogram to web app using streamlit. 
st.plotly_chart(fig2)

# %% [markdown]
# # Lets take a look at our histogram

# %%
fig2.show()

# %% [markdown]
# ## Let's say the user wants to look at how the number of days a vehicle has been listed can affect the sales price of the vehicle. To do this we will create categories for days listed with a function called 'list_age_category'. We'll use a box plot as our visual to see how the prices compare based on the listing age. 

# %% [markdown]
# # First lets create our web app section header 

# %%
st.write(""" 
### Let's take a look at how the price can be affected by the number of days the vehicle has been listed.
""") 

# %%
# Create days listed age group categories using a function.


def list_age_category(x):
    if x<7: return 'less than 7 days'
    elif x>=7 and x<14: return '7-14 days'
    elif x>= 14 and x<30: return '14-30 days'
    elif x>= 30 and x<60: return '30-60 days'
    elif x>= 60 and x<90: return '60-90 days'
    elif x>= 90 and  x<180: return '90-180 days'
    else: return '>180'

data['list_age_category']= data['days_listed'].apply(list_age_category)


# %%
# Create box plot using streamlit
import altair as alt

chart = alt.Chart(data).mark_boxplot(extent='min-max').encode(x='list_age_category', y='price')

st.altair_chart(chart, theme="streamlit", use_container_width=True)


# %%
st.write('We can see that the longer a vehicle has been listed, the lower the price.')

# %% [markdown]
# ## Finally, we'll create a scatterplot for our user to see how mileage affects the price of a vehicle. We'll use the odometer column for this. 

# %%
# Create Web app title for section. 
st.write(""" 
         ### Now we will examine how mileage affects the price of a vehicle. Hover over the diagram to view price, odometer reading, and model_year of the vehicle.
         """)
fig3 = px.scatter(data, x='price', y='odometer', hover_data = ['model_year'], title= 'Price vs. Mileage')
st.plotly_chart(fig3)

# %%
fig3.show()

# %%
st.write("""
#### Thank you for visiting our web app. We hope you feel more confident in your pre-owned vehicle search! 
""")


