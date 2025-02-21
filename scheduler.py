from datetime import datetime
import logging
import sys
import os
from dotenv.main import load_dotenv
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import plaid
from plaid.api import plaid_api

# Load environment variables
load_dotenv()

# Configure logging to also write to a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('scheduler.log')
    ]
)

def get_account_balances():
    """Fetch account balances from Plaid"""
    try:
        # Initialize Plaid client
        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SECRET'),
            }
        )
        
        api_client = plaid.ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)
        
        # Get account balances
        access_token = os.getenv('PLAID_ACCESS_TOKEN')
        request = {
            "access_token": access_token,
            "options": {
                "min_last_updated_datetime": "2020-01-01T00:00:00Z"
            }
        }
        response = client.accounts_balance_get(request)
        
        # Format balance message
        message_parts = ["Account Balances:"]
        for account in response.accounts:
            balance = account.balances.current
            name = account.name
            message_parts.append(f"{name}: ${balance:,.2f}")
        
        return "\n".join(message_parts)
    except Exception as e:
        logging.error(f"Error fetching Plaid balances: {str(e)}")
        return "Unable to fetch account balances"

def test_send_sms():
    """Test function to send a single SMS message via Twilio"""
    try:
        # Get Twilio credentials from environment variables
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_phone = os.getenv('TWILIO_PHONE_NUMBER')
        to_phone = os.getenv('TO_PHONE_NUMBER')
        
        # Check if all credentials are present
        if not all([account_sid, auth_token, from_phone, to_phone]):
            print("Error: Missing Twilio credentials in .env file")
            return
        
        # Get account balances
        balance_message = get_account_balances()
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send message
        message = client.messages.create(
            body=balance_message,
            from_=from_phone,
            to=to_phone
        )
        
        logging.info(f"Success! Message SID: {message.sid}")
    except Exception as e:
        logging.error(f"Error sending SMS: {str(e)}")

def main():
    try:
        # Initialize scheduler
        scheduler = BlockingScheduler()
        
        # Schedule the job to run at 5 PM PST
        scheduler.add_job(
            test_send_sms,
            trigger=CronTrigger(
                hour=17,
                minute=30,
                timezone=pytz.timezone('America/Los_Angeles')
            )
        )
        
        logging.info("Scheduler started. Press Ctrl+C to exit.")
        scheduler.start()
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")
        sys.exit(0)

if __name__ == '__main__':
    logging.info("Application starting up...")
    main()

# To test Twilio SMS, uncomment and run the following line:
# test_send_sms() 