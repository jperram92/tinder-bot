from TinderApi import Tinder
import random
import time
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Email Stuff
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    filename='tinder_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Code
load_dotenv()

sender_email_address = os.getenv('EMAIL_SENDER_ADDRESS')
sender_email_password = os.getenv('EMAIL_SENDER_PASSWORD')
reciever_email_address = os.getenv('EMAIL_RECIEVER_ADDRESS')

emails_sent = 0
likes_sent = 0
passes_sent = 0
matches_count = 0
bot_matches_detected = 0

def detect_bot(user):
    """Basic bot detection based on profile characteristics"""
    suspicious_keywords = ['sugar', 'venmo', 'snapchat premium', 'only.fans']
    
    if 'bio' not in user:
        return False
        
    bio = user.get('bio', '').lower()
    return any(keyword in bio for keyword in suspicious_keywords)

def send_email_stats_update(argument="TinderBot 100 Likes Update"):
    # Declare as global to modify the variables
    global emails_sent, likes_sent, passes_sent, matches_count

    emails_sent += 1

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = reciever_email_address
    msg['Subject'] = (f"{argument} #{emails_sent}. "
                    f"Likes: {likes_sent}, Passes: {passes_sent}, Matches: {matches_count}")
    body = "This is an email update from TinderBot. "

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    
    # Converts the Multipart msg into a string
    text = msg.as_string()

    # Send the email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()    # start TLS for security
    s.login(sender_email_address, sender_email_password)
    s.sendmail(sender_email_address, reciever_email_address, text)

    s.quit()

def swipe_session():
    global likes_sent, passes_sent

    tinder = Tinder(debug=True, x_auth_token=os.getenv('AUTH_TOKEN'))
    users_to_swipe = tinder.swipe.get_users()

    # Wait a lil bit before swiping to avoid suspicion hehe
    time.sleep(max(1, random.random() * 10))

    for user in users_to_swipe:
        # print(user)
        if random.random() < 0.5:
            # LIKE USER
            liked = tinder.swipe.like_user(user["user_id"]) 
            likes_sent += 1
            # print("#### Liked")
            # print(liked) # -> {'status': 200, 'match': False, 'user_id': 'some_user_id', 'likes_left': 100}

            # TODO: different behavior if match is True
        else: 
            # PASS USER
            tinder.swipe.pass_user(user["user_id"]) 
            passes_sent += 1
            # print("#### Not liked")
            
        # Wait between 1 and 10 seconds because we aren't a bot ;)
        time.sleep(max(1, random.random() * 10))
    
    return tinder.matches.get_matches()

hrs_between_swipes = int(input("How many hours between swipes? "))

send_email_stats_update(argument="TinderBot Started")

while True:
    # Chance to skip today
    if random.random() < 0.1:
        print("Skipping today...")
        wait_time = hrs_between_swipes * 60 * 60 + random.randint(0, 3600)
        time.sleep(wait_time)

    print("Starting new swipe session...")
    # Make a new instance of Tinder every session of swiping, avoiding suspicion.
    matches = swipe_session()
    matches_count=len(matches)

    # Send an email every 50 likes sent
    if (emails_sent == 0 or likes_sent % 50 == 0):
        send_email_stats_update(matches_count)
    
    print(f"TinderBot Update. Emails Sent: {emails_sent}, "
          f"Likes: {likes_sent}, Passes: {passes_sent}, Matches: {matches_count}")

    # Swipe again tommorow!
    wait_time = hrs_between_swipes * 60 * 60 + random.randint(0, 3600)
    time.sleep(wait_time)
