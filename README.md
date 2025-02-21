# Daily Scheduler

This is a Python application that logs a message every day at 3:30 PM PST using APScheduler.

## Prerequisites

- Python 3.x

## Setup

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Scheduler

To start the scheduler locally:
```bash
python scheduler.py
```

The scheduler will run continuously and log a message every day at 3:30 PM PST. To stop the scheduler, press Ctrl+C.

## Deployment

This application is configured to run on Railway.app using the included `Procfile`. 

To deploy:
1. Push your code to a Git repository
2. Connect your repository to Railway
3. Deploy as a worker service (not a web service)

## Logs

The application logs to both:
- Standard output (visible in console and Railway logs)
- A local file `scheduler.log`

## Notes

- The scheduler uses the America/Los_Angeles timezone (PST/PDT)
- The message will be logged every day at exactly 3:30 PM PST/PDT
- For production use, the application is already configured to run as a worker process on Railway