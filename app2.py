#Import necessary libraries

import streamlit as st
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import openai


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

#Authenticate using the downloaded credentials
def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file('D:\F1\CPSC 4820/client_secret_853326803148-rd5a36lc1irc4il6khaghfmhhkfgg3l6.apps.googleusercontent.com.json', SCOPES)
    creds = flow.run_local_server(port=8080, redirect_uri='http://localhost:8080/')
    service = build('gmail', 'v1', credentials=creds)
    return service

service = authenticate_gmail()

#Fetch emails from the spam folder
def get_spam_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['SPAM'], maxResults=30).execute()
    messages = results.get('messages', [])
    emails = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        emails.append(msg['snippet'])
    return emails

spam_emails = get_spam_emails(service)

# Print spam emails
for email in spam_emails:
    print(email)

#Generate summary and sentiment analysis using OpenAI API

def summarize_email(email):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize this email: {email}",
        max_tokens=50
    )
    summary = response.choices[0].text.strip()
    return summary

def analyze_sentiment(email):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analyze the sentiment of this email: {email}",
        max_tokens=50
    )
    sentiment = response.choices[0].text.strip()
    return sentiment

#Streamlit app

st.title('Gmail Spam Email Analyzer')

option = st.sidebar.selectbox('Choose an option', ['Word Cloud', 'Email Summary and Sentiment Analysis'])

if option == 'Word Cloud':
    st.header('Word Cloud of Spam Emails')
    emails = get_spam_emails(service)
    text = ' '.join(emails)
    wordcloud = WordCloud(width=800, height=400).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

elif option == 'Email Summary and Sentiment Analysis':
    st.header('Email Summary and Sentiment Analysis')
    emails = get_spam_emails(service)[:10]
    selected_email = st.selectbox('Select an email', emails)
    summary = summarize_email(selected_email)
    sentiment = analyze_sentiment(selected_email)
    st.write('Summary:', summary)
    st.write('Sentiment:', sentiment)


