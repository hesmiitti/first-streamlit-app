import streamlit
import snowflake.connector
import pandas
import requests

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi (kö?)')
streamlit.write('The user entered fruit', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json())

# palauttaa json-version datasta ja normalisoi sen 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# tulostaa taulukkona normalisoidun datan
streamlit.dataframe(fruityvice_normalized)

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list order by FRUIT_NAME")
my_data_rows = my_cur.fetchall()
streamlit.header("Fruit_Load_List contains:")
streamlit.dataframe(my_data_rows)

#streamlit.header("Lisää hedelma:")
#add_my_fruit = streamlit.text_input('Anna uusi lisattava hedelma:','')
#my_cur.execute("insert into FRUIT_LOAD_LIST values ('"+add_my_fruit+"')")
#streamlit.write('Kiitos, että lisäsit hedelmän: ', add_my_fruit)
