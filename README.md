# Reddit-Subscriptions-Copy
Export list of subreddit subscriptions, then on a different user apply those same subscriptions

## Pre-Requisites
- Access to two Reddit accounts (the old and new one)
- App created on each account to get CLIENT_ID and CLIENT_SECRET (see below)
- Password for both Reddit accounts

## How to create Client ID and Password
Do this on both accounts
1. Login to reddit.com
2. Go to [old.reddit.com/prefs/apps](https://old.reddit.com/prefs/apps/)
3. Create a new app, give it a NAME
4. Choose SCRIPT (not web app or installed app)
5. For URI set it to 'http://localhost:8080'
6. Click CREATE APP
7. Your CLIENT_ID is Right under the app name you can see a string like `tegEVSMMXqRQOfCf_Dz_Yg`
8. Your CLIENT_SECRET is more clearly labelled on this page.
9. Copy both the CLIENT_SECRET and CLIENT_ID and paste it into the vars.sh script
10. For your source account paste them in the SOURCE_CLIENT_ID and SOURCE_CLIENT_SECRET
11. For your target account paste them in the TARGET_CLIENT_ID and TARGET_CLIENT_SECRET

## Install Requirements
Depending on whether your using a virtual environment. Install **praw** with one of these commands
```
pip install praw
python3-pip install praw
sudo apt install python3-pip python3-praw
```
