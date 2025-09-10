import os
import sys
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount

# --- Configuration ---
# You need to get these from your Facebook Developer account
# It's recommended to use environment variables for security
my_app_id = os.environ.get('FACEBOOK_APP_ID')
my_app_secret = os.environ.get('FACEBOOK_APP_SECRET')
my_access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')

if not all([my_app_id, my_app_secret, my_access_token]):
    print("Error: Please set the FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, and FACEBOOK_ACCESS_TOKEN environment variables.")
    sys.exit(1)

# --- Initialization ---
try:
    FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
    print("Facebook Ads API initialized successfully.")
except Exception as e:
    print(f"Error initializing Facebook Ads API: {e}")
    sys.exit(1)

# --- Fetch Ad Accounts ---
try:
    # 'me' represents the current user
    me = User(fbid='me')

    # Fetch the ad accounts associated with the user
    my_ad_accounts = me.get_ad_accounts(fields=[AdAccount.Field.name, AdAccount.Field.account_id])

    if not my_ad_accounts:
        print("No ad accounts found for this user.")
    else:
        print("Successfully fetched ad accounts:")
        for account in my_ad_accounts:
            print(f"  - Account Name: {account[AdAccount.Field.name]}")
            print(f"    Account ID: {account[AdAccount.Field.account_id]}")

except Exception as e:
    print(f"An error occurred while fetching ad accounts: {e}")
    print("Please check your access token and permissions.")
    sys.exit(1)
