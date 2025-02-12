#!/usr/bin/env python3



import telebot
import googleapiclient.discovery
import requests

# Replace with your Telegram Bot API Token
BOT_TOKEN = "8074027938:AAF5H9ljU9Z0Il6N_IvV3brRjM8cWIqNQMo"

bot = telebot.TeleBot("8074027938:AAF5H9ljU9Z0Il6N_IvV3brRjM8cWIqNQMo")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I will help manage and optimize your social media.")

@bot.message_handler(commands=['analytics'])
def get_analytics(message):
    bot.reply_to(message, "Fetching real-time analytics...")

bot.polling()


import google.auth
from googleapiclient.discovery import build

# Load Google credentials
credentials, project = google.auth.load_credentials_from_file("{"installed":{"client_id":"1050528511747-i0qvbf2tr7137vohq9748kqk3k3tgt5j.apps.googleusercontent.com","project_id":"civil-sprite-450622-v5","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}")

# Connect to Google Analytics API
analytics = build('analyticsreporting', 'v4', credentials=credentials)

def fetch_google_analytics():
    response = analytics.reports().batchGet(
        body={
            'reportRequests': [{
                'viewId': '344855868',
                'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                'metrics': [{'expression': 'ga:pageviews'}]
            }]
        }
    ).execute()
    
    return response['reports'][0]['data']['totals'][0]['values'][0]

@bot.message_handler(commands=['analytics'])
def get_analytics(message):
    pageviews = fetch_google_analytics()
    bot.reply_to(message, f"Website Page Views (Last 7 Days): {pageviews}")

bot.polling()


YOUTUBE_API_KEY = "AIzaSyC0bh3lG105s7ko-T2DlJsYM9mtm9EOv58"

def fetch_youtube_subscribers():
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.channels().list(part="statistics", id="UC8eFyuWmChA3XsDkQyqvw4w")
    response = request.execute()
    
    return response["items"][0]["statistics"]["subscriberCount"]

@bot.message_handler(commands=['youtube'])
def get_youtube_data(message):
    subs = fetch_youtube_subscribers()
    bot.reply_to(message, f"Current YouTube Subscribers: {subs}")

bot.polling()



INSTAGRAM_ACCESS_TOKEN = "IGAAJJEEDzGZB1BZAE9YSHRtZAjNNQUZAoU1NJY2l5UTVTVVFMLUVJQ09SVEFiQ1dQSzFtTlVReGpSd0FqSFo3SGpOZAEtnNURmT1lRckd2Uk5McEN0R215US1PYi1XNFJINGZAPWUpvM1hlUmRwMUMxQVFtUWJWc244SmtxZAHI4R3dVTQZDZD"

def fetch_instagram_followers():
    url = f"https://graph.instagram.com/me?fields=id,username,account_type,media_count&access_token={INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(url).json()
    
    return response["media_count"]

@bot.message_handler(commands=['instagram'])
def get_instagram_data(message):
    followers = fetch_instagram_followers()
    bot.reply_to(message, f"Instagram Posts Count: {followers}")

bot.polling()
