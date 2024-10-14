import pandas as pd
import sqlalchemy
import streamlit as st
from sqlalchemy import create_engine
import mysql.connector
import streamlit.components.v1 as components
import requests

df1 = pd.read_csv(r'path1')
df2 = pd.read_csv(r'path2')

db_url ='mysql+mysqlconnector://...../anime_rec'

for i in range(0,8):
    df2['rating'].replace(i, 0 , inplace=True)    
for i in range(8,11):
    df2['rating'].replace(i, 1 , inplace=True)    

def delete_tables():
            
            mydb = mysql.connector.connect(
            host= serverhost,
            user= serveruser,
            password= serverpassword,
            database="anime_rec"
            )

            mycursor = mydb.cursor()
            sql = "DROP TABLE IF EXISTS anime"
            mycursor.execute(sql)
            sql = "DROP TABLE IF EXISTS anime1"
            mycursor.execute(sql)
            mycursor.close()
            mydb.close()

def app(text1):

        wrong = True
        df33 =pd. DataFrame()
        anime_value = text1.split(",")

        engine = create_engine(db_url)
        engine = sqlalchemy.create_engine(db_url)
        connection = engine.connect()

        for item in anime_value:
            df = df1[df1["name"]== item.strip()]
            if df.head().empty:
                st.write(f":grey[*Couldn't find the anime with title: {item}*]")
            else:
                x = df.iloc[0,0]
                 
                final_df2= df2[df2["anime_id"] == x]
                final_df2= final_df2[final_df2["rating"] ==1 ]
              
                final_df2.to_sql('anime' , con=engine, index= False, if_exists='append')
        
        connection.close()

        engine = sqlalchemy.create_engine(db_url)
        connection = engine.connect()
  
        try:
            my_df = pd.read_sql_query(sql="SELECT user_id FROM anime GROUP BY user_id HAVING COUNT(anime_id)>=3", con=connection)

            for i in my_df["user_id"]:                 
                df22= df2[df2["user_id"]== int(i)]
                final_df= df22[df22["rating"] != -1]
                #final_df = pd.concat([df33, df22], ignore_index=True)
                final_df.to_sql('anime1', con=engine, index= False, if_exists='append')

        except:
            html_c = '''
            <div style='background-color: #181926 ; color:  #735087; padding: 20px; center;text-align: center;'>
            <font size="5"><b> Not Enough User's Reviews for the provided anime! </b></font>
            </div>
            '''
            components.html(html_c, height=200)  
            wrong = False
            delete_tables()
            
        connection.close()

        if wrong:
            engine = sqlalchemy.create_engine(db_url)
            connection = engine.connect()   
            
            try:
                #
                fin_pd = pd.read_sql_query(sql="SELECT anime_id FROM anime1 GROUP BY anime_id HAVING AVG(rating) > 0.7 AND anime_id NOT IN (SELECT anime_id FROM anime) ORDER BY AVG(rating) DESC, COUNT(user_id)  DESC LIMIT 3;", con=connection)
                html_c = '''
                <div style='background-color: #181a26 ; color:  #735087; padding: 5px; center;text-align: center;'>
                <font size="5"><b>Here is the list with the Recommendation Anime! </b></font>
                </div>
                '''
                components.html(html_c, height=60)   

                for i in (fin_pd["anime_id"]):
                    final_df2= df1[df1["anime_id"] == int(i)]
                    
                    anime_name= final_df2['name'].iloc[0]
                    url = f"https://api.jikan.moe/v4/anime?q={anime_name}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        data = response.json()

                        for anime in data['data']:
                            st.write(f"Title: {anime['title']}")
                            st.write(f"Synopsis: {anime['synopsis']}")
                            st.write(final_df2[['name','genre','episodes']])

                            image_url = anime['images']['jpg']['image_url']
                            st.markdown(f'<div style="text-align: center;"><img src="{image_url}" width="240"></div>', unsafe_allow_html=True)
                            break

                    else:
                        print(f"Error: {response.status_code}")

            except:
                html_c = '''
                <div style='background-color: #181926 ; color:  #735087; padding: 20px; center;text-align: center;'>
                <font size="5"><b> Not Enough User's Reviews for the provided anime Or Interal Error! </b></font>
                </div>
                '''
                components.html(html_c, height=200)  
                wrong = False
                delete_tables()

            connection.close()
            
        if wrong:
            delete_tables()


