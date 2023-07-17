import streamlit as st
from datetime import date
from youtube_microservices import setup, fetch_data, process_data, analyse_data, create_graphs


def youtube():
    # st.set_page_config(page_title='Sentiment Analyser - YouTube', page_icon='resources/images/yt_icon.png', layout='wide')


    # For the first time use, please uncomment the below lines to download the required resources
    # Also make sure to import nltk
    # nltk.download('vader_lexicon')
    # nltk.download('punkt')
    # nltk.download('stopwords')
    # nltk.download('wordnet')
    
    # Title & Icon
    _, col1, col2 = st.columns([2.2, 0.45, 3])

    with col1:
        st.image('resources/images/yt_bnw.png', width=100)
    with col2:
        st.markdown("<h1 style='text-align: left;'>YouTube</h1>", unsafe_allow_html=True)     
    
    # User inputs
    channel_name = st.text_input('Enter YouTube channel name')

    c1, c2 = st.columns([1, 1])
    with c1:
        start_date = st.date_input('Select start date')
    with c2:
        end_date = st.date_input('Select end date')

    today = date.today()
    if(start_date > end_date or end_date > today):
        st.warning('Please select valid dates')

    # Button
    analyse = False
    _, cl2, _ = st.columns([2.65,1,2])
    with cl2:
        analyse = st.button('Analyse')

    # Button Functionality
    if analyse:
        _, cl, _ = st.columns([2.4,1,2])
        with cl:
            with st.spinner('Please wait...'):
                youtube = setup.execute()
                
                # Fetching data
                transcripts = fetch_data.execute(
                    youtube=youtube,
                    channel_name=channel_name, 
                    start_date=start_date, 
                    end_date=end_date
                )

                # Cleaning data
                normalized_transcripts = process_data.execute(transcripts=transcripts)
                
                # Analysing data
                overall_sentiment, sentiment_percentages, non_zero_word_count = analyse_data.execute(normalized_transcripts=normalized_transcripts)

        # Displaying result
        st.text('Overall sentiment: ' + overall_sentiment.upper())

        # Plotting graphs
        bar_graph = create_graphs.execute(sentiment_percentages, non_zero_word_count)

        # Creating expander
        exp = st.expander('View Graphs for better understanding')
        st.markdown(
            """
            <style>
            body {
                background-color: #F8F8F8;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Displaying graphs
        exp.pyplot(bar_graph)
 
# youtube()
    