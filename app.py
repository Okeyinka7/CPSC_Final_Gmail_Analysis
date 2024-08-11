import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import openai
import os

# from dotenv import load_dotenv
# import os
#
# load_dotenv()  # Load environment variables from .env file
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Gmail API Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_gmail_service():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_emails(service, label_id, max_results):
    results = service.users().messages().list(userId='me', labelIds=[label_id], maxResults=max_results).execute()
    messages = results.get('messages', [])
    return messages

def get_email_content(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    return message

def extract_email_text(email_content):
    parts = email_content.get('payload').get('parts')
    email_text = ''
    for part in parts:
        if part['mimeType'] == 'text/plain':
            email_text += part['body']['data']
    return email_text

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, max_words=50).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment

def summarize_email(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize the following email: {text}",
        max_tokens=60
    )
    return response.choices[0].text.strip()

# Streamlit Application
st.title("Gmail Email Analysis")

service = get_gmail_service()

st.sidebar.header("Options")
option = st.sidebar.selectbox("Choose an option", ["Word Cloud", "Email Summary and Sentiment"])

if option == "Word Cloud":
    st.subheader("Word Cloud of Latest Spam Emails")
    emails = get_emails(service, 'SPAM', 30)
    all_text = ''
    for email in emails:
        email_content = get_email_content(service, email['id'])
        email_text = extract_email_text(email_content)
        all_text += email_text
    generate_wordcloud(all_text)

elif option == "Email Summary and Sentiment":
    st.subheader("Email Summary and Sentiment Analysis")
    emails = get_emails(service, 'INBOX', 10)
    email_titles = [f"Email {i+1}" for i in range(len(emails))]
    selected_email = st.selectbox("Select an email", email_titles)
    selected_email_id = emails[email_titles.index(selected_email)]['id']

    email_content = get_email_content(service, selected_email_id)
    email_text = extract_email_text(email_content)

    summary = summarize_email(email_text)
    sentiment = analyze_sentiment(email_text)

    st.write("### Summary")
    st.write(summary)
    st.write("### Sentiment")
    st.write(f"Polarity: {sentiment.polarity}, Subjectivity: {sentiment.subjectivity}")
