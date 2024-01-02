# %%
import pandas as pd 
import streamlit as st 
import plotly.express as px 



# %% [markdown]
# # Items to include in the app:
# - One st.header with text (https://docs.streamlit.io/library/api-reference/text/st.header)
# - At least one Plotly Express Histogram using st.write (https://docs.streamlit.io/library/api-reference/write-magic/st.write) or st.plotly_chart (https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart)
# - At least one Plotly Express scatter plot using st.write (https://docs.streamlit.io/library/api-reference/write-magic/st.write) or st.plotly_chart (https://docs.streamlit.io/library/api-reference/charts/st.scatter_chart)
# - At least one checkbox using st.checkbox that changes the behavior of any of the above components (https://docs.streamlit.io/library/api-reference/widgets/st.checkbox)

# %%
#read in data
data = pd.read_csv('vehicles_us.csv')


# %%
#fill in missing values of price and model_year column
data['price'] = data['price'].fillna(0)
data['model_year'] = data['model_year'].fillna(0000).astype(int)

# %%
# create a new column for manufacturer
data['manufacturer'] = data['model'].apply(lambda x: x.split()[0])
data.head()


# %%
data.shape

# %%
# checking for duplicate rows. Results show no duplicated rows in the dataframe
data.duplicated()

# %%
#convert model_year column from float to int

data['model_year'] = data['model_year'].astype(int)
pd.options.display.float_format = '{:,.0f}'.format
data.head()

# %%
st.header('Used Car Market')

# %%
# view data
st.header('Data Viewer')

st.dataframe(data)

# %%
# Create header with an option to filter the data and a checkbox to show only electric vehicles:
# Let users filter data by type of vehicle they are searching for.

st.header('Used Vehicle Inventory')
st.write(""" 
         #### Filter the data below to search inventory by vehicle type and price range. 
         """) 



show_new_ads = st.checkbox('Show vehicles listed in last 30 days')


# %%
if show_new_ads:
    data = data[data.days_listed <= 30]


# %%
# Create options for filter so users can select vehicle by type
vehicle_type = data['type'].unique()
type_choice = st.selectbox('Select vehicle type:', vehicle_type)



# %%
# Next let's create a slider for users to select vehicles by price range
# Create minimum and maximum values for price range
min_price, max_price = int(data['price'].min()), int(data['price'].max())

#create slider
price_range = st.slider(
    "Choose price range", 
    value=(min_price,max_price),min_value=min_price,max_value=max_price )

# %%
# Now we'll filter the dataset based on the users chosen variables
filtered_table = data[(data.type==type_choice) & (data.price>=price_range[0]) & (data.price <= price_range[1])]



#show the final table in streamlit
st.dataframe(filtered_table)

# %%
st.header('Price Analysis')
st.write(""" 
         #### Let's see how different factors can influence the price of a vehicle. We'll take a look at the distribution of the prices based on manufacturer, type of vehicle, and condition of vehicle.
         """ )
# We'll create a histogram with the parameter of choice: manufacturer  condition of vehicle 

# Creating list of options for histogram 
list_for_hist = ['manufacturer', 'type', 'condition']

# Create select box for options
choice_for_hist = st.selectbox('Choose one', list_for_hist)

# plot histogram where price_usd is based on the choice made in the selectbox
fig1 = px.histogram(data, x='price', color=choice_for_hist, title= "<b> Price by {}</b>".format(choice_for_hist))

#adding to streamlit
st.plotly_chart(fig1)


# %%
fig1.show()

# %%
# We also want to take a look at price factor dependent on age of vehicle. Since we have a large variety of years, we'll first sort the years into categories. 

# Create age category of vehicle. 
data['age'] = 2023-data['model_year']

def age_category(x):
    if x<5: return 'less than 5 years'
    elif x>=5 and x<10: return '5-10 years'
    elif x>= 10 and x<20: return '10-20 years'
    else: return 'over 20 years'

data['age_category']= data['age'].apply(age_category)


# %%
# We also want to take a look at which vehicle manufacturer holds the best value. To do this, we'll compare the prices based off the age category and manufacturer. 

st.header('Best Value')
st.write("""
#### Which manufacturer holds the best value? Use the drop down menus to compare vehicle prices by manufacturer and age of vehicle.
""")

# Add select box to choose manufacturer
vehicle_man = data['manufacturer'].unique()
select_man = st.selectbox('Select Manufacturer', vehicle_man) 

# Add select box to choose age of vehicle
age_choice = data['age_category'].unique()
select_age = st.selectbox('Select Age', age_choice)

# Filter data based on user selection
filtered_data = data[(data['manufacturer'] == select_man) & (data['age_category'] == select_age)]

# plot histogram based off user selection of manufacturer and age
fig2 = px.histogram(filtered_data, x='price',  title= f"Price Distribution for {select_man} Vehicles ({select_age})")

#add to streamlit
st.plotly_chart(fig2)

# %%
fig2.show()

# %%
# We want to take a look at how the number of days a vehicle has been listed can affect the price. First we'll put the number of days listed into categories. 


def list_age_category(x):
    if x<7: return '<7'
    elif x>=7 and x<14: return '7-14'
    elif x>= 14 and x<30: return '14-30'
    elif x>= 30 and x<60: return '30-60'
    elif x>= 60 and x<90: return '60-90'
    elif x>= 90 and  x<180: return '90-180'
    else: return '>180'

data['list_age_category']= data['days_listed'].apply(list_age_category)


# %%
st.write(""" 
### Let's take a look at how the number of days the vehicle has been listed affects the price. 
""") 

#import seaborn and matplotlib to create boxplot
import seaborn as sns 
import matplotlib.pyplot as plt

# Create boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(x='list_age_category', y='price', data=data)
plt.title('Price vs. Number of Days Listed')
plt.xlabel('Number of Days Listed')
plt.ylabel('Price USD')

# Display boxplot in streamlit
st.pyplot(plt) 

# %%
st.write('We can see that the longer a vehicle has been listed, the lower the price.')

# %%
st.write(""" 
         ### Now we will examine how mileage affects the price of a vehicle. 
         """)
fig3 = px.scatter(data, x='price', y='odometer', hover_data = ['model_year'], title= 'Price vs. Mileage')
st.plotly_chart(fig3)

# %%
fig3.show()

# %%
st.write("""
#### By using these interactive models, we are able to see how different factors can affect the market price of a vehicle. 
""")


