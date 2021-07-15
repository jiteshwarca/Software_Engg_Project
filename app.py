import streamlit as st
import pickle 
import pandas as pd
import numpy as np
import datetime
from pmdarima import auto_arima
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import pymongo
import SessionState
import datetime
import json
import requests
from copy import deepcopy
from fake_useragent import UserAgent

from streamlit import caching
import streamlit.components.v1 as components

# #for resetting state
session = SessionState.get(run_id=0)

 #Data Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from feedback import UserAuth
# from dotenv import load_dotenv
# load_dotenv()

engine = create_engine('sqlite:///project_db.sqlite3')
#Connect to DB
Session = sessionmaker(bind=engine)
sess = Session()

model = pickle.load(open('RFmodel.pkl', 'rb'))

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def predict_covid(prediction_value):
    input = np.array([prediction_value])
    prediction = model.predict_proba(input)
    pred = '{0:.{1}f}'.format(prediction[0][0], 5)
    return float(pred)

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_mapping():
    df = pd.read_csv("district_mappingnew.csv")
    return df


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def filter_column(df, col, value):
    df_temp = deepcopy(df.loc[df[col] == value, :])
    return df_temp

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def filter_capacity(df, col, value):
    df_temp = deepcopy(df.loc[df[col] > value, :])
    return df_temp

@st.cache(allow_output_mutation=True)
def Pageviews():
    return []

def main():
    st.set_page_config(page_title="Covid 19 App ⛑️", page_icon="notebooks/mask.png", layout='wide', initial_sidebar_state='expanded')

    st.title("COVID-19 Help App 🖥️")
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    st.markdown("""
    <style>
    .etitle {
            font-family: "IBM Plex Sans", sans-serif;
            font-weight: bold;
            font-size: 25px;
            color: black;
            margin: 1.5rem 0px 0.5rem;
            padding: 0.5em 0px 0.25em;
            line-height: 1;
            position: relative;
            flex: 1 1 0%;    
    }
    .dashtitle {
            font-family: 'Noto Sans', sans-serif;
            font-size: 20px;
            color: rgb(250, 250, 250);
            margin: 1.5rem 0px 0.5rem;
            padding: 0.5em 0px 0.25em;
            line-height: 1;
            position: relative;
            flex: 1 1 0%;    
    }
    </style>
    """, unsafe_allow_html=True)
    
    tableau_covid_dash = """ 
                            <div class='tableauPlaceholder' id='viz1622650066687' style='position: relative'>
   <noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Covid_Dashboard_16226492198720&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript>
   <object class='tableauViz'  style='display:none;'>
      <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
      <param name='embed_code_version' value='3' />
      <param name='site_root' value='' />
      <param name='name' value='Covid_Dashboard_16226492198720&#47;Dashboard1' />
      <param name='tabs' value='no' />
      <param name='toolbar' value='yes' />
      <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Covid_Dashboard_16226492198720&#47;Dashboard1&#47;1.png' />
      <param name='animate_transition' value='yes' />
      <param name='display_static_image' value='yes' />
      <param name='display_spinner' value='yes' />
      <param name='display_overlay' value='yes' />
      <param name='display_count' value='yes' />
      <param name='language' value='en-GB' />
   </object>
</div>
            <script type='text/javascript'> 
                var divElement = document.getElementById('viz1622650066687');          
                var vizElement = divElement.getElementsByTagName('object')[0];
                if (divElement.offsetWidth > 800) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else if (divElement.offsetWidth > 500) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else {
                    vizElement.style.width = '100%';
                    vizElement.style.height = '1527px';
                }
                var scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);             
            </script>
                            """


    tableau_covid_forecast = """ 
        <div class='tableauPlaceholder' id='viz1622652929015' style='position: relative'>
   <noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Covid-19Forecast_16226528481210&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript>
   <object class='tableauViz'  style='display:none;'>
      <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
      <param name='embed_code_version' value='3' />
      <param name='site_root' value='' />
      <param name='name' value='Covid-19Forecast_16226528481210&#47;Dashboard1' />
      <param name='tabs' value='no' />
      <param name='toolbar' value='yes' />
      <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Covid-19Forecast_16226528481210&#47;Dashboard1&#47;1.png' />
      <param name='animate_transition' value='yes' />
      <param name='display_static_image' value='yes' />
      <param name='display_spinner' value='yes' />
      <param name='display_overlay' value='yes' />
      <param name='display_count' value='yes' />
      <param name='language' value='en-GB' />
   </object>
</div>
        <script type='text/javascript'>                
                var divElement = document.getElementById('viz1622652929015'); 
                var vizElement = divElement.getElementsByTagName('object')[0];
                if (divElement.offsetWidth > 800) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else if (divElement.offsetWidth > 500) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else {
                    vizElement.style.width = '100%';
                    vizElement.style.height = '1527px';
                }
                var scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);                
        </script>
                                """

    tableau_covid_brc = """ 
        
    <div class='tableauPlaceholder' id='viz1622822276953' style='position: relative'>
   <noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ba&#47;Bar_Race_Chart&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript>
   <object class='tableauViz'  style='display:none;'>
      <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
      <param name='embed_code_version' value='3' />
      <param name='site_root' value='' />
      <param name='name' value='Bar_Race_Chart&#47;Dashboard1' />
      <param name='tabs' value='no' />
      <param name='toolbar' value='yes' />
      <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ba&#47;Bar_Race_Chart&#47;Dashboard1&#47;1.png' />
      <param name='animate_transition' value='yes' />
      <param name='display_static_image' value='yes' />
      <param name='display_spinner' value='yes' />
      <param name='display_overlay' value='yes' />
      <param name='display_count' value='yes' />
      <param name='language' value='en-GB' />
   </object>
</div>
        <script type='text/javascript'>  
                var divElement = document.getElementById('viz1622822276953');    
                var vizElement = divElement.getElementsByTagName('object')[0];
                if (divElement.offsetWidth > 800) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else if (divElement.offsetWidth > 500) {
                    vizElement.style.width = '1130px';
                    vizElement.style.height = '727px';
                } else {
                    vizElement.style.width = '100%';
                    vizElement.style.height = '1527px';
                }
                var scriptElement = document.createElement('script');
                scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
                vizElement.parentNode.insertBefore(scriptElement, vizElement);    
         </script>
    
    
    """

    st.write('\n\n\n')


    activities=['Detect Covid Severity','CoWin Slot Checker','Analytics Dashboard']
    option=st.sidebar.selectbox('Menu Navigation',activities)
    st.sidebar.write("\n")
    st.sidebar.title("About The Creators")
    st.sidebar.write("\n")
    st.sidebar.info(
        """
        This Application was developed by  **Jiteshwar**,**Amritesh** and **Priyanka** in lieu of the pandemic situation that has rendered everyone speechless. 
        The app aims to provide a way to check if your symptoms are covid-like with our prediction model , 
        access state helpline numbers , check for available vaccination slots in your locality 
        or even check out the current trend of the pandemic in the analytics dashboard. 
        We have also included a feedback form that you could fill out so we could improve upon the application even further !
        """
    )

    symptoms_list = ['Breathing Problem','Fever','Dry Cough','Sore Throat','Running Nose','Asthma','Chronic Lung Disease','Headache','Heart Disease','Diabetes','Hyper Tension','Fatigue','Gastrointestinal','Abroad travel','Contact with COVID Patient','Attended Large Gathering','Visited Public Exposed Places','Family working inpublic exposed places']
    if option == 'Detect Covid Severity':

        st.markdown('<p class="etitle" style="font-size: 30px;">COVID-19 Severity Prediction Model 😷 </p>', unsafe_allow_html=True)
        st.write('\n')
        st.subheader('Please Select The Applicable Symptoms: ✔️')
        symptoms = st.multiselect('',[*symptoms_list],key='symptoms')
        
        hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


        prediction_value = ['0' for i in range(18)]
        for sym in symptoms:
            index = symptoms_list.index(sym)
            # assigning encoded value to testing frame
            prediction_value[index] = '1'

        st.write("\n")

        cols = st.beta_columns((1,1,8))  #4 for centered  , 8 for Wide

        if cols[1].button("Reset 🔄"):
            session.run_id += 1

        if cols[0].button("Predict 🔮"):
            st.write('\n')
            output=predict_covid(prediction_value)
            output = abs(1-output)
            fout = '{0:.2f}'.format(output*100) 
            
            if output > 0.5:
                st.error('The probability of being COVID positive is {} % \n You are possibily covid positive , please confer with your doctor '.format(fout))
            else:
                st.success('The probability of being COVID positive is {} %, It is unlikely that you are covid postive '.format(fout))
                st.info('if you still have doubts , please contact your physician')
            
        st.write('\n\n\n')


        st.markdown('<p class="etitle">State Helpline Numbers 📞</p>', unsafe_allow_html=True)
        # st.title('State Helpline Numbers 💁🏻')
        dfh = pd.read_excel("helplineNumbers.xlsx")
        # st.dataframe(dfh)

        # helplineNo = list(np.unique(dfh["HelplineNo"].values))
        # st.write(helplineNo)
        helpStates = dfh["State/UT"]
        helplineNo = dfh["HelplineNo"]
        # st.write(helpStates)
        # st.write(helplineNo)
        
        st.write("\n")
        
        selectedState = st.selectbox("Select State 🗺️:", [""] + helpStates)
        colh = st.beta_columns(2)
        
        st.write("\n")
        st.write("\n")
        colh[0].subheader("State")
        colh[1].subheader("Helpline Numbers")
        colh[0].write('\n')
        colh[1].write('\n')
        for i,j in zip(helpStates,helplineNo):
            if selectedState == i:
                colh[0].write(f'{i}')
                colh[1].write(f'{j}')


        st.write("\n\n\n\n")

        st.write("\n\n\n\n")

        st.subheader('Feedback Form ⚡')
        form = st.form(key='my-form')
        name_i = form.text_input('Enter your name 👦: ')
        review_i = form.text_input('Were you satisifed with the prediction 😮 ?')
        improve_i = form.text_input('What can we do to improve 🤔 ?')
        submit = form.form_submit_button('Submit')

        
            

        if submit and name_i and review_i and improve_i:
                
            try:
                session.run_id += 1
                push_data(name_i,review_i,improve_i)
                st.success(f'Thank you {name_i} for the feedback 🥰 !, We are trying our best to improve the application :) ')
            except Exception as e:
                st.error('There seems to be some error 🤔 , please try again later :( ')
                
    if option == 'CoWin Slot Checker':

        hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


        st.markdown('<p class="etitle">CoWin Slot Availabilty 💉 </p>', unsafe_allow_html=True)

        st.write("\n\n")

        st.info("The CoWIN API's requests are limited , Sometimes results may not come. Try again after 5 minutes 🌐 ")

        st.write("\n\n")
    
        try:
            mapping_df = load_mapping()

            rename_mapping = {
                    'date': 'Date',
                    'min_age_limit': 'Minimum Age Limit',
                    'available_capacity': 'Available Capacity',
                    'vaccine': 'Vaccine',
                    'pincode': 'Pincode',
                    'name': 'Hospital Name',
                    'state_name' : 'State',
                    'district_name' : 'District',
                    'block_name': 'Block Name',
                    'fee_type' : 'Fees'
                    }

            # for col in mapping_df:
            #     st.write(col)

            valid_states = list(np.unique(mapping_df["state_name"].values))

            formcheck = st.form(key='my-form3')
            center_column_1, right_column_1 = st.beta_columns(2)



            with center_column_1:
                state_inp = formcheck.selectbox('Select State 🗺️', [""] + valid_states)
                if state_inp != "":
                    mapping_df = filter_column(mapping_df, "state_name", state_inp)



            mapping_dict = pd.Series(mapping_df["district id"].values,
                                    index = mapping_df["district name"].values).to_dict()

            # numdays = st.sidebar.slider('Select Date Range', 0, 100, 10)
            unique_districts = list(mapping_df["district name"].unique())
            unique_districts.sort()
            with right_column_1:
                dist_inp = formcheck.selectbox('Select District 🏙️', unique_districts)

            DIST_ID = mapping_dict[dist_inp]

            base = datetime.datetime.today()
            numdays = 3
            date_list = [base + datetime.timedelta(days=x) for x in range(20)]
            date_str = [x.strftime("%d-%m-%Y") for x in date_list]
            temp_user_agent = UserAgent()
            browser_header = {'User-Agent': temp_user_agent.random}

            final_df = None
            for INP_DATE in date_str:
                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
                response = requests.get(URL, headers=browser_header)
                if (response.ok) and ('centers' in json.loads(response.text)):
                    resp_json = json.loads(response.text)['centers']
                    if resp_json is not None:
                        df = pd.DataFrame(resp_json)
                        if len(df):
                            df = df.explode("sessions")
                            df['min_age_limit'] = df.sessions.apply(lambda x: x['min_age_limit'])
                            df['vaccine'] = df.sessions.apply(lambda x: x['vaccine'])
                            df['available_capacity'] = df.sessions.apply(lambda x: x['available_capacity'])
                            df['date'] = df.sessions.apply(lambda x: x['date'])
                            df = df[["date", "available_capacity", "vaccine", "min_age_limit", "pincode", "name", "state_name", "district_name", "block_name", "fee_type"]]
                            if final_df is not None:
                                final_df = pd.concat([final_df, df])
                            else:
                                final_df = deepcopy(df)
                    else:
                        st.error("No rows in the data Extracted from the API")
            #     else:
            #         st.error("Invalid response")



            if (final_df is not None) and (len(final_df)):
                final_df.drop_duplicates(inplace=True)
                final_df.rename(columns=rename_mapping, inplace=True)

                left_column_2, center_column_2, right_column_2, right_column_2a,  right_column_2b = st.beta_columns(5)
                with left_column_2:
                    valid_pincodes = list(np.unique(final_df["Pincode"].values))
                    pincode_inp = formcheck.selectbox('Select Pincode 📍', [""] + valid_pincodes)
                    if pincode_inp != "":
                        final_df = filter_column(final_df, "Pincode", pincode_inp)

                with center_column_2:
                    valid_age = [18, 45]
                    age_inp = formcheck.selectbox('Select Minimum Age 👨', [""] + valid_age)
                    if age_inp != "":
                        final_df = filter_column(final_df, "Minimum Age Limit", age_inp)

                with right_column_2:
                    valid_payments = ["Free", "Paid"]
                    pay_inp = formcheck.selectbox('Select Free or Paid 🆓 ', [""] + valid_payments)
                    if pay_inp != "":
                        final_df = filter_column(final_df, "Fees", pay_inp)
                
                with right_column_2a:
                    valid_capacity = ["Available"]
                    cap_inp = formcheck.selectbox('Select Availablilty ❇️', [""] + valid_capacity)
                    if cap_inp != "":
                        final_df = filter_capacity(final_df, "Available Capacity", 0)

                with right_column_2b:
                    valid_vaccines = ["COVISHIELD", "COVAXIN"]
                    vaccine_inp = formcheck.selectbox('Select Vaccine💉', [""] + valid_vaccines)
                    if vaccine_inp != "":
                        final_df = filter_column(final_df, "Vaccine", vaccine_inp)
                check = formcheck.form_submit_button("CHECK ✔️")
                if check:
                    table = deepcopy(final_df)
                    table.reset_index(inplace=True, drop=True)
                    st.write("\n")
                    st.subheader(" RESULT :📋 ")
                    st.write("\n\n")
                    st.write(table)
                    
            else:
                formcheck.form_submit_button("CHECK ✔️")
                st.error("THE API call limit has been reached , please try again after 5 minutes.")

            st.write("\n\n\n\n")
        except:
            formcheck.form_submit_button("CHECK ✔️")
            st.error("The Cowin API is not available outside india")


    if option == 'Analytics Dashboard':




        st.markdown("<style> @import url('https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap'); </style>", unsafe_allow_html=True)
        st.markdown('<p class="etitle" style="font-size:30px">Analytics Dashboard 📈</p>', unsafe_allow_html=True)
        st.write("\n")
        st.write("\n")
        st.info("Best Viewed On Desktop , We Are Working On A Better Mobile Experience")
        st.markdown('<p class="etitle" style="font-size:25px">Covid 19 Country Wise Case Visualization 🌎</p>', unsafe_allow_html=True)
        st.write("\n")
        st.subheader("The Below Interactive Dashboard Displays The Covid 19 Country Wise Cases Aggregated By Continents.")
        st.markdown('<p class="dashtitle> <b> The measures used for the original data collection are: <b>  </p>', unsafe_allow_html=True)
        st.write("⛣ Number of Cases Worldwide")
        st.write("⛣ Number of Active Cases In Each Country")
        st.write("⛣ The Aggregrate of the Deaths Prevalent Country Wise")
        st.markdown('<p class="dashtitle"> </p>', unsafe_allow_html=True)
        st.subheader("The Given Dashboard has been produced with the help of Tableau and the data has been updated as of 10/06/21")
        st.markdown('<b> KEY INSIGHTS </b> </p>', unsafe_allow_html=True)
        st.markdown('<p class="dashtitle"> <ul> <li> At present, USA has the highest number of covid cases(33 M) as well as the highest number of deaths (0.59 M) </li>  <li> India still holds second position with 29.1 M covid cases and 0.35 M deaths </li> <li> While Brazil has 0.47 M deaths with 17.03 M covid cases.</li> <li>Greenland is marked as one of the safest place with 43 cases and 0 deaths.</li> </ul></p>', unsafe_allow_html=True)
        st.subheader("We Presently Have Two Filters for both daily & cumulative reports for all the metrics used, which is also reflected in the world map")
        st.write("\n")
        st.write("\n")
        components.html(tableau_covid_dash , width=1600, height=800 )
        st.markdown('<p class="etitle" style="font-size:25px">Covid-19 Forecast Graph 🔮 </p>', unsafe_allow_html=True)
        st.write("\n")
        st.write("\n")
        st.subheader("The Below Interactive Dashboard Displays The Time Series Forecasting of the Confirmed Cases of COVID-19 ,Recovered Cases & Death Rates for Covid Cases")
        st.markdown('<p class="dashtitle> <b> The measures used for the original data collection are: <b>  </p>', unsafe_allow_html=True)
        st.write("⛣ Confirmed Cases of Covid-19 Worldwide ")
        st.write("⛣ Death Rate of Covid-19 ")
        st.write("⛣ Recovered Cases of Covid-19 Worldwide ")
        st.markdown('<p class="dashtitle"> The Given Dashboard has been produced with the help of Tableau and the data has been updated as of 10/06/21</p>', unsafe_allow_html=True)
        st.markdown('<p class="dashtitle"> <b> KEY INSIGHTS </b> </p>', unsafe_allow_html=True)
        st.markdown('<p class="dashtitle"> <ul> <li> Number of confirmed cases for next 3 months will be somewhere in the range of 27 M to 60 M.  </li>  <li> Number of recovered cases will also increase approximately upto 150 M with a death rate 1-2 % </li> </ul></p>', unsafe_allow_html=True)
        st.subheader("Don\'t get worried looking at the increasing number of covid cases, the recovery rate is also increasing. Doesn\'t mean you should take it leniently. Take proper precautions and possibly stay in your home. India is fighting, stay home and let us defeat corona 😁")
        st.write("\n")
        st.write("\n")
        components.html(tableau_covid_forecast , width=1600, height=800 )

        st.markdown('<p class="etitle" style="font-size:25px">Covid-19 Bar Race Chart 📊  </p>', unsafe_allow_html=True)
        st.write("\n")
        st.write("\n")
        st.subheader("Below Bar Race Chart shows the number of covid cases found on each day and plots values of the topmost 10 countries")
        st.write("\n")
        st.write("\n")
        components.html(tableau_covid_brc , width=1600, height=800 )

       

                
if __name__=='__main__':
    main()
