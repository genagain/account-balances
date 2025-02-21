from datetime import datetime
import logging
import sys
import os
from dotenv.main import load_dotenv
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

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
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send message
        message = client.messages.create(
            body="This is your 5 PM PST notification!",
            from_=from_phone,
            to=to_phone
        )
        
        print(f"Success! Message SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

def main():
    try:
        # Initialize scheduler
        scheduler = BlockingScheduler()
        
        # Schedule the job to run at 5 PM PST
        scheduler.add_job(
            test_send_sms,
            trigger=CronTrigger(
                hour=17,
                minute=0,
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