import streamlit as st
import pickle
import pandas as pd

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals',
 'Gujarat Titans']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'New Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

add_bg_from_local("Twilight Match at IPL Stadium.png")
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))

with col2:
    bowling_team = st.selectbox(
        'Select the bowling team',
        sorted([t for t in teams if t != batting_team])
    )


selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target', min_value=1, max_value=400, step=1)

col3,col4,col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score', min_value=1, max_value=400, step=1)

with col4:
    balls_left = st.number_input('Balls left', min_value=1, max_value=120, step=1)

with col5:
    wickets = st.number_input('Wickets out', min_value=0, max_value=9, step=1)

if st.button('Predict Probability'):
    if score >= target:
        st.error("Score is not greater than target")
    else:
        runs_left = target - score
        overs_done = (120 - balls_left) / 6
        wickets_remaining = 10 - wickets

        crr = score / overs_done if overs_done > 0 else 0
        rrr = (runs_left * 6) / balls_left

        input_df = pd.DataFrame({
            'batting_team':[batting_team],
            'bowling_team':[bowling_team],
            'city':[selected_city],
            'runs_left':[runs_left],
            'balls_left':[balls_left],
            'wickets_left':[wickets_remaining],
            'first_innings_total':[target],
            'crr':[crr],
            'rrr':[rrr]
        })
        try:
            result = pipe.predict_proba(input_df)
        except Exception as e:
            st.error(f"Prediction error: {e}")
            st.write('Input columns provided:', list(input_df.columns))
            st.write('Input sample:', input_df)
        else:
            loss = result[0][0]
            win = result[0][1]
            st.header(batting_team + " - " + str(round(win*100)) + "%")
            st.header(bowling_team + " - " + str(round(loss*100)) + "%")
