import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import requests
import io
from PIL import Image

usernames = ["zhijie", "yijun", "team4", "parth", "srikanth"]

file_path = Path(__file__).parent.parent / "streamlitUserPW.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(usernames, usernames, hashed_passwords, "streamlitMain", "abcdef", cookie_expiry_days=0)


if st.session_state["authentication_status"]:
    token = st.session_state["token"] 
    # st.warning("token: " + token)
    header = {"Authorization": "Bearer "+ token, "accept": "application/json"}

    authenticator.logout('Logout', 'sidebar')
    st.sidebar.markdown("## APIs Functions")
    def api1():
        st.header("API 1: Search aircraft by Location")
        st.sidebar.subheader("Search aircraft in an Location")

        fun1val1 = st.sidebar.number_input("x_loc: [Pick a number between (0,2560)]",0 ,2560 ,step = 100)
        fun1val2 = st.sidebar.number_input("y_loc: [Pick a number between (0,2560)]",0 ,2560 ,step = 100)
        fun1val3 = st.sidebar.text_input("image_id", max_chars= 50)

        if st.sidebar.button("Select"):
            
            url = f"http://damg7245-zhijie.herokuapp.com/img/airplane/location?x_loc={fun1val1}&y_loc={fun1val2}&image_id={fun1val3}"            

            res = requests.get(url=url, headers = header)
            meta = res.json()
            
            if(res.text[0] == '"'):
                st.write("No image found related to your image id. Try effective image id") 
            else:
                if(meta["has_airplane"] == False):
                    st.write("No airplane in this place, try another location.")
                else: 
                    st.write("There is a airplane! 🎉")
                    xmin, ymin, xmax, ymax = meta["coordinate"]["Xmin"], meta["coordinate"]["Ymin"], meta["coordinate"]["Xmax"], meta["coordinate"]["Ymax"];
                    img_url = f"http://damg7245-zhijie.herokuapp.com/s3/img/location?image_id={fun1val3}&Xmin={xmin}&Ymin={ymin}&Xmax={xmax}&Ymax={ymax}"
                    response = requests.get(url = img_url, headers = header)
                    i = Image.open(io.BytesIO(response.content))
                    st.image(i)
            
                st.subheader("Metadata:")
                st.json( meta )

    def api2():
        st.header("API 2: Get all airplanes' coordinate in picture")
        st.sidebar.subheader("API 2: Get airplanes coordinate in picture")
        fun2val1 = st.sidebar.text_input("image_id", max_chars= 50)
        if st.sidebar.button("Select"):

            res = requests.get(f"https://damg7245-zhijie.herokuapp.com/img/airplanes/coordinates?image_id={fun2val1}", headers = header)
            if(res.text[0] == '"'):
                st.write("No image found related to your image id. Try effective image id") 
            else:
                st.json( res.json() )           
        
    def api3():
        st.header("API 3: Display the top big or small aircraft in one picture")
        fun3val1 = st.sidebar.text_input("image id", max_chars= 50)
        fun3val2 = st.sidebar.number_input("limit of number [Pick a number between (1,10)]",1 ,10)
        fun3flag = st.sidebar.selectbox("Do you want to the most biggest or smallest aircraft", ["Big", "Small"])  # to do ["Big", "Small"]
        if(fun3flag == "Big"):
            fun3val3 = "True"
        elif(fun3flag == "Small"):
            fun3val3 = "False"
        if st.sidebar.button("Select"):

            api3_url = f"https://damg7245-zhijie.herokuapp.com/img/display?image_id={fun3val1}&limit_of_number={fun3val2}&isMaximum={fun3val3}" 
            res = requests.get(url = api3_url, headers = header)

            if(res.text[0] == '"'):
                st.write("No image found related to your image id. Try effective image id") 
            else:


                img_url = f"http://damg7245-zhijie.herokuapp.com/s3/img/airplanes?image_id={fun3val1}&limit_of_number={fun3val2}&isMaximum={fun3val3}"
                response = requests.get(url = img_url, headers = header)

                i = Image.open(io.BytesIO(response.content))
                st.write(f"You Get {fun3val2} {fun3flag}est  airplanes! 🎉")
                st.image(i)
                st.subheader("Metadata:")
                st.json( res.json() ) 
        
    def api4():
        st.header("API 4: Count airplanes in a picture")
        st.sidebar.subheader("Count airplanes in a picture")
        fun4val1 = st.sidebar.text_input("image id", max_chars= 50)

        if st.sidebar.button("Select"):
            url = f"https://damg7245-zhijie.herokuapp.com/img/airplanes/count?image_id={fun4val1}"
            header = {"Authorization": "Bearer "+ token, "accept": "application/json"}
            res = requests.get(url=url, headers = header)
            
            if(res.text[0] == '"'):
                st.write("No image found related to your image id. Try effective image id") 
            else:
                number = res.json()["number_of_airplanes"]
                
                img_url = f"http://damg7245-zhijie.herokuapp.com/s3/img?image_id={fun4val1}" 
                response = requests.get(url = img_url, headers = header)
                i = Image.open(io.BytesIO(response.content))
                st.write(f"There are {number} airplanes in this image ")
                st.image(i)
                st.subheader("Metadata:")        
                st.json( res.json() ) 

        
    def api5():
        st.header("API 5: Search for images by numbers of airplanes")
        st.sidebar.subheader("Search by numbers of airplanes")

        fun5val1 = st.sidebar.number_input("contain aircraft number [Pick a number between (20,100)]",20 ,100)
        fun5val2 = st.sidebar.number_input("limit of number [Pick a number between (1,10)]",1 ,10)

        if st.sidebar.button("Select"):
            url = f'https://damg7245-zhijie.herokuapp.com/img/airplanes/givenNumber?contain_aircraft_number={fun5val1}&limit_of_image={fun5val2}'
            header = {"Authorization": "Bearer "+ token, "accept": "application/json"}
            res = requests.get(url=url, headers = header)
            meta = res.json()
            
            if(res.text[0] == '"'):
                st.write(f"No image in database has {fun5val1} airplanes. Please try another one")            
            else: 
                st.write(f"Congratulations! You find it the image with {fun5val1} airplanes 🎉")
                meta = res.json()
                for i in range(len(meta)):
                    i_id = meta[str(i)]["img_id"]

                    img_url = f"http://damg7245-zhijie.herokuapp.com/s3/img?image_id={i_id}"
                    response = requests.get(url = img_url, headers = header)
                    i = Image.open(io.BytesIO(response.content))
                    st.image(i)

                st.subheader("Metadata:")
                st.json( res.json() )
        
    def api6():
        st.header("API 6: Get pictures that contains top number of airplanes")
        st.sidebar.subheader("Find most airplanes on one or more images")

        fun6val1 = st.sidebar.number_input("number of image: [Pick a number between (1,10)]",1 ,10)

        if st.sidebar.button("Select"):
            url = f"https://damg7245-zhijie.herokuapp.com/img/airplanes/maximum?number_of_image={fun6val1}"
            header = {"Authorization": "Bearer "+ token, "accept": "application/json"}
            res = requests.get(url=url, headers = header)
            meta = res.json()
            
            for i in range(len(meta)):
                i_id = meta[str(i)]["img_id"]

                img_url = f"http://damg7245-zhijie.herokuapp.com/s3/img?image_id={i_id}"
                response = requests.get(url = img_url, headers = header)
                i = Image.open(io.BytesIO(response.content))
                st.image(i)

            st.subheader("Metadata:")
            st.json( res.json() )            

        
    def api7():
        st.header("API 7: Get pictures that contains top number of truncated airplanes")
        st.sidebar.subheader("Find picture with most truncated airplanes")

        fun7val1 = st.sidebar.number_input("number of image [Pick a number between (1,10)]",1 ,10)

        if st.sidebar.button("Select"):
            # url = f"https://damg7245-zhijie.herokuapp.com/img/airplanes/truncated?number_of_image={fun7val1}"
            url = f"https://127.0.0.1:5001/img/airplanes/truncated?number_of_image={fun7val1}"
            header = {"Authorization": "Bearer "+ token, "accept": "application/json"}
            res = requests.get(url=url, headers = header)
            meta = res.json()
            
            for i in range(len(meta)):
                i_id = meta[str(i)]["img_id"]
                # img_url = f"http://damg7245-zhijie.herokuapp.com/s3/img?image_id={i_id}"
                img_url = f"http://127.0.0.1:5001/s3/img?image_id={i_id}"
                response = requests.get(url = img_url, headers = header)
                i = Image.open(io.BytesIO(response.content))
                st.image(i)
            st.subheader("Metadata:")
            st.json( res.json() )
        

    funNum = {
        "API 1: Search by Location": api1,
        "API 2: Get all coordinates": api2,
        "API 3: Get top size aircraft": api3,
        "API 4: Count airplanes": api4,
        "API 5: Search by number": api5,
        "API 6: Get top number aircraft": api6,
        "API 7: Get top number truncated": api7
    }

    selectFun = st.sidebar.selectbox("choose API", funNum.keys())
    funNum[selectFun]()
else:
    st.markdown('# Please go to streamlitMain login')