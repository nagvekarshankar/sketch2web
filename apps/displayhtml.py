import streamlit as st
import streamlit.components.v1 as components

def display_html():
    st.title('Output HTML')
    HtmlFile = open("html/output.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    #print(source_code)
    components.html(source_code)


    

