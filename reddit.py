import streamlit as st
from datetime import date
import datetime, asyncpraw, asyncio, re
from transformers import pipeline, RobertaForSequenceClassification, RobertaTokenizer
from reddit_microservices import create_graph

def reddit():
    # st.set_page_config(page_title='Sentiment Analyser - Reddit', page_icon='resources/images/reddit_icon.png', layout='wide')

    # Title & Icon
    _, col1, col2 = st.columns([2.3, 0.45, 3])

    with col1:
        st.image('resources/images/reddit_white.png', width=100)
    with col2:
        st.markdown("<h1 style='text-align: left;'>Reddit</h1>", unsafe_allow_html=True)     

    # User Input
    subreddit_name = st.text_input('Enter sub reddit name')

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

    # Button functionality
    if analyse:
        # Function to clean data
        def clean_text(text):
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            text = text.lower()            
            return text
        
        # Fetching data from subreddit
        async def main():
            async with asyncpraw.Reddit(client_id="WQK5n-GHzXU5IihE1pIH7Q",
                                    client_secret="CU6HY5cmhFBTf6X_sID-MTCgkokjXg",
                                    user_agent="Sentimental Analysis") as reddit:

                subreddit = await reddit.subreddit(subreddit_name)

                start_time = datetime.datetime.combine(start_date, datetime.datetime.min.time())

                end_time = datetime.datetime.combine(end_date, datetime.datetime.max.time())

                posts = subreddit.new(limit=None)

                post_contents = []

                async for post in posts:
                    if start_time <= datetime.datetime.fromtimestamp(post.created_utc) <= end_time:
                        post_contents.append(post.title + " " + post.selftext)

                cleaned_contents = []

                # Cleaning data
                for text in post_contents:
                    cleaned_text = clean_text(text)
                    cleaned_contents.append(cleaned_text)

                await perform_sentiment_analysis(cleaned_contents)

        # Analysing data using RoBERTa
        async def perform_sentiment_analysis(cleaned_contents):
            model = RobertaForSequenceClassification.from_pretrained('roberta-base')
            tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
            sa_pipeline = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

            my_list = cleaned_contents

            outputs = sa_pipeline(my_list)

            sentiments = [output['label'] for output in outputs]

            num_positive = sentiments.count('LABEL_1')
            num_negative = sentiments.count('LABEL_0')
            num_neutral = sentiments.count('LABEL_2')

            overall_max = max([num_positive, num_negative, num_neutral])
            overall_sentiment = ''
            if overall_max == num_positive:
                overall_sentiment = 'POSITIVE'
            elif overall_max == num_negative:
                overall_sentiment = 'NEGATIVE'
            else:
                overall_sentiment = 'NEUTRAL'
            
            # # Displaying result
            st.text('Overall sentiment: ' + overall_sentiment)
            
            # # Plotting graph
            fig = create_graph.execute(num_positive, num_negative, num_neutral)

            # Creating expander
            exp = st.expander('View Graph for better understanding')
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
            # Displaying graph
            exp.pyplot(fig)
            
        asyncio.run(main())  

        

# reddit()