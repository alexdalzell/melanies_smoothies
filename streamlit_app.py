# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title("Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom **Smoothie!**
    """
)

# Your Name
name = st.text_input('Name on Smoothie', 'Name')
st.write('The name on your Smoothie will be', name)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe, 
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon") + fruit_chosen
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '""" + name + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Thanks ' + name + ', your smoothie is ordered!', icon="✅")





    
