import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import openai
import time

from dotenv import load_dotenv
import os

# load_dotenv()  # Load environment variables from .env file
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to summarize text using OpenAI API
def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize this text: {text}"}
        ]
    )
    summary = response.choices[0].message['content'].strip()
    return summary

# nalyze sentiment using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment

# Streamlit app
st.title("Welcome to Gmail Analysis")

# Sidebar options
st.sidebar.title("Options")
option = st.sidebar.selectbox('Choose an option', ['Word Cloud', 'Email Summary and Sentiment Analysis'])

# # Button to display document
# if st.button('Display Document'):
#     st.write("""
#     # Developing a Streamlit Application for Gmail Analysis
#
#     ## I)	Gmail API
#     Username: testemail4026@gmail.com
#     Password: testemail123
#     """)
#
#     st.image("D:\F1\CPSC 4820\imgs\api_error.jpg")
#
#     st.write("""
#      Authorized redirect URL: http://localhost:8501 (was occupied)
#       http://localhost:2356, (changed different ports, none worked)
#
#
#     ## Section 2
#     This section contains more sample text.
#
#     ## Conclusion
#     This is the conclusion of the sample document.
#     """)


if option == 'Word Cloud':
    st.header('Word Cloud')
    sample_emails = [
        "Congratulations! You've won a prize!",
        "Limited Time Offer - 50% Off!",
        "Urgent: Update Your Account Information",
        "Hi Get exclusive access to our new features by joining our beta program. Click the link below to sign up. [Join Beta] Best The Development Team",
        "Win a Free Gift Card! Hi Enter our contest for a chance to win a free gift card. Click the link below to participate. [Enter Contest] Best The Promotions Team"

    ]
    text = ' '.join(sample_emails)
    wordcloud = WordCloud(width=800, height=400).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

elif option == 'Email Summary and Sentiment Analysis':
    st.header('Email Summary and Sentiment Analysis')
    sample_emails = [
        "Congratulations! You've won a prize!",
        "Limited Time Offer - 50% Off!",
        "Urgent: Update Your Account Information",
         "Hi Get exclusive access to our new features by joining our beta program. Click the link below to sign up. [Join Beta] Best The Development Team",
        "Win a Free Gift Card! Hi Enter our contest for a chance to win a free gift card. Click the link below to participate. [Enter Contest] Best The Promotions Team"
    ]
    selected_email = st.selectbox('Select an email', sample_emails)
    summary = summarize_text(selected_email)
    sentiment = analyze_sentiment(selected_email)
    st.write('Summary:', summary)
    st.write('Sentiment:', sentiment)

