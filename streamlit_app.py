# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col

# Title
st.title(f"customize your smoothie! :tea: {st.__version__}")

st.write(
    """Choose the fruits you want in your custom smoothie."""
)



name_on_order = st.text_input("Name on Smoothie")
st.write("The current name on smoothie is: ", name_on_order)


cnx = st.connection("snowflake")

# Session
session = cnx.session()

# Get fruits
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col('FRUIT_NAME'))

# Convert dataframe to python list
fruit_list = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# Multiselect
ingredientes_list = st.multiselect(
    'choose up to 5 ingredients:',
    fruit_list
)

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)

if ingredientes_list:

    # Create string
    ingredients_string = ' '.join(ingredientes_list)

    # SQL statement
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('submit order')

    # Execute
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
