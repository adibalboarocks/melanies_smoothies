# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

option = st.selectbox(
    "What is your favourite fruit?",
    ("Banana", "Strawberries", "Peaches"))

st.write("Your favourite fruit is:", option)
cnx=st.connection("snowflake")
session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options")
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_smoothie = st.text_input("Name on smoothie:")
st.write("The name on the smoothie will be", name_on_smoothie)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose upto 5 ingedients:',
                             my_dataframe,max_selections=5)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string=''
    for fruit in ingredients_list:
        ingredients_string+=fruit
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string +"""' , '"""+name_on_smoothie+ """')"""
    # st.write(my_insert_stmt)

    time_to_insert=st.button('Submit button')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!, '+name_on_smoothie, icon="✅")

