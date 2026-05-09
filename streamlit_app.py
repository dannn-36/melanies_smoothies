# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests

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
).select(
    col('FRUIT_NAME'),
    col('SEARCH_ON')
)

# Convert Snowpark dataframe to pandas dataframe
pd_df = my_dataframe.to_pandas()

st.dataframe(pd_df)

# Convert dataframe to python list
fruit_list = pd_df['FRUIT_NAME'].tolist()

# Multiselect
ingredientes_list = st.multiselect(
    'choose up to 5 ingredients:',
    fruit_list
)

if ingredientes_list:

    # Create string
    ingredients_string = ' '

    for fruit_chosen in ingredientes_list:

        ingredients_string += fruit_chosen + ' '

        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]

        st.write(
            'The search value for ',
            fruit_chosen,
            ' is ',
            search_on,
            '.'
        )

        st.subheader(fruit_chosen + ' Nutrition Information')

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        st.dataframe(
            data=smoothiefroot_response.json(),
            width='stretch'
        )

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
