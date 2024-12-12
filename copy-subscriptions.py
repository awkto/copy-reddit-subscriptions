import praw
import os
import json
from datetime import datetime

def authenticate(is_source=True):
    """Authenticates with Reddit using OAuth."""
    try:
        # Use different credentials for source and target
        if is_source:
            client_id = os.environ.get("REDDIT_SOURCE_CLIENT_ID")
            client_secret = os.environ.get("REDDIT_SOURCE_CLIENT_SECRET")
            username = os.environ.get("REDDIT_SOURCE_USERNAME")
            password = os.environ.get("REDDIT_SOURCE_PASSWORD")
        else:
            client_id = os.environ.get("REDDIT_TARGET_CLIENT_ID")
            client_secret = os.environ.get("REDDIT_TARGET_CLIENT_SECRET")
            username = os.environ.get("REDDIT_TARGET_USERNAME")
            password = os.environ.get("REDDIT_TARGET_PASSWORD")

        if not all([client_id, client_secret, username, password]):
            print("Missing credentials:")
            print(f"Client ID: {'Present' if client_id else 'Missing'}")
            print(f"Client Secret: {'Present' if client_secret else 'Missing'}")
            print(f"Username: {'Present' if username else 'Missing'}")
            print(f"Password: {'Present' if password else 'Missing'}")
            return None

        print(f"Attempting to authenticate as user: {username}")
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent="SubscriptionScript/1.0 (by /u/MawJe)"
        )
        me = reddit.user.me()
        print(f"Authentication successful for user: {me.name}")
        return reddit
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_and_save_subscriptions(reddit):
    """Gets list of subreddits and saves them to a file."""
    try:
        print("Fetching subscriptions...")
        subscriptions = []
        for subreddit in reddit.user.subreddits(limit=None):
            print(f"Found subreddit: {subreddit.display_name}")
            subscriptions.append({
                'name': subreddit.display_name,
                'title': subreddit.title,
                'subscribers': subreddit.subscribers,
                'description': subreddit.description[:200] + '...' if subreddit.description else None
            })
        
        if subscriptions:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reddit_subs_{timestamp}.json"
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(subscriptions, f, indent=4)
            
            print(f"\nSaved {len(subscriptions)} subscriptions to {filename}")
            return subscriptions
        else:
            print("No subscriptions found")
            return None
            
    except Exception as e:
        print(f"Error getting subscriptions: {e}")
        return None

def subscribe_from_file(reddit, filename):
    """Subscribe to subreddits from a saved file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            subscriptions = json.load(f)
        
        print(f"\nAttempting to subscribe to {len(subscriptions)} subreddits...")
        success_count = 0
        fail_count = 0
        
        for sub in subscriptions:
            try:
                subreddit = reddit.subreddit(sub['name'])
                subreddit.subscribe()
                print(f"Successfully subscribed to r/{sub['name']}")
                success_count += 1
            except Exception as e:
                print(f"Failed to subscribe to r/{sub['name']}: {e}")
                fail_count += 1
        
        print(f"\nSubscription Results:")
        print(f"Successful: {success_count}")
        print(f"Failed: {fail_count}")
        
    except Exception as e:
        print(f"Error processing subscription file: {e}")

def main():
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "export":
            reddit = authenticate(is_source=True)  # Source user
            if reddit:
                get_and_save_subscriptions(reddit)
        elif sys.argv[1] == "import" and len(sys.argv) > 2:
            reddit = authenticate(is_source=False)  # Target user
            if reddit:
                subscribe_from_file(reddit, sys.argv[2])
        else:
            print("Usage:")
            print("Export: python script.py export")
            print("Import: python script.py import <filename>")
    else:
        print("Please specify mode: export or import")

if __name__ == "__main__":
    main()
