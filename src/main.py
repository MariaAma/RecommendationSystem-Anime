import streamlit as st
import appFile
import streamlit.components.v1 as components

st.set_page_config(page_title="anime_recommendations", page_icon="🚀")

if __name__== '__main__':
    
    html_code = '''
    <div style='color:  #735087; padding: 20px; line-height: 40px; center;text-align: center;'>
    <font size="5"><b> Welcome to this project! <br> You don't know, what anime to watch? <br> DON'T WORRY, I got you! </b></font>
    </div>
    '''
    components.html(html_code , height=150)  

    title = st.text_input(":grey[Tell me your favorite Anime.]")

    class MultiApp:  

        def __init__(self):
            self.apps = []

        def run():
            if st.button(":grey[Sumbit]"):
                appFile.app(title)
        
        run()
