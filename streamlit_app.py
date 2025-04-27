# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import re

# Title and instructions
st.title(":cup_with_straw: Update Your Smoothie Order :cup_with_straw:")
st.write(
  """Modify the fruits in your existing smoothie order by entering your name and choosing new ingredients."""
)

# Input for user's name
name_on_order = st.text_input('Name on Smoothie:')
st.write('Updating order for: ', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

# Multiselect ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 new ingredients:',
    my_dataframe.to_pandas()['FRUIT_NAME'].tolist(),  # Assuming Snowflake stores as UPPERCASE
    max_selections=5
)

# If user selects ingredients
if ingredients_list:
    # Sanitize user input (very important!)
    name_on_order_clean = re.sub(r"[^a-zA-Z0-9\s]", "", name_on_order)

    # Create ingredients string
    ingredients_string = ' '.join(ingredients_list)

    # Prepare the UPDATE SQL
    my_update_stmt = f"""
        UPDATE smoothies.public.orders
        SET ingredients = '{ingredients_string}'
        WHERE name_on_order = '{name_on_order_clean}'
    """

    st.write("Your Update Preview:")
    st.code(my_update_stmt)

    # Button to trigger update
    time_to_update = st.button('Update Order')

    if time_to_update:
        result = session.sql(my_update_stmt).collect()
        st.success('Your Smoothie has been updated!', icon="✅")
