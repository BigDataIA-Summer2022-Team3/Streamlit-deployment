import streamlit as st
import streamlit.components.v1 as components
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

usernames = ["zhijie", "yijun", "team4", "parth", "srikanth"]

file_path = Path(__file__).parent.parent / "streamlitUserPW.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(usernames, usernames, hashed_passwords, "streamlitMain", "abcdef", cookie_expiry_days=0)


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.title('Team3 API User Guide')
    st.subheader('Welcome! Lets go through our APIs')
    HtmlFile = open("./reports/api_describe_guide.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    print(source_code)
    components.html(source_code, height = 3100, width = 800)
else:
    st.markdown('# Please go to streamlitMain login')