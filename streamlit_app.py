# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
import pandas as pd


# Write directly to the app
st.title(f"Customise your smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you wnat in your custom smoothie
  
  
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, width="stretch")
# st.stop()

# Convert the Snowpark Dataframe to a Pandas Data frame so we can use the LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
# st.stop()


ingredients_List = st.multiselect(
    "Choose up to 5 ingredients?"
    , my_dataframe
    , max_selections=5
)

if ingredients_List:
        # st.write(ingredients_List)
        # st.text(ingredients_List)

        ingredients_string = ''

        for fruit_chosen in ingredients_List:
             ingredients_string += fruit_chosen + ' '
             
             search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
             st.write('The search value for ', fruit_chosen,' is ', search_on, '.')           
          
             st.subheader(fruit_chosen + 'Nutrition Information')
             smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}")
             sf_df = st.dataframe(data=smoothiefroot_response.json(), width="stretch")

        st.write(ingredients_string)




        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +"""')"""

        # st.write(my_insert_stmt)
        # st.stop()

        # if ingredients_string:
        #    session.sql(my_insert_stmt).collect()
        #    

        time_to_insert = st.button('Submit Order')

        if time_to_insert:
              session.sql(my_insert_stmt).collect()

              st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")







