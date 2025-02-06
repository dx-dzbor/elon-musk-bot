import schedule
import time
import pytz
from datetime import datetime
from typing import Callable, Dict, Any
import logging

class Scheduler:
    def __init__(self):
        self.jobs = {}

    def add_job(self, chat_config: Dict[str, Any], callback: Callable):
        """Add a new scheduled job for a chat."""
        chat_id = str(chat_config['chat_id'])
        timezone = pytz.timezone(chat_config['timezone'])
        schedule_config = chat_config['schedule']
        
        # Convert UTC time to local timezone
        time_str = schedule_config['time']
        day_of_week = schedule_config['day_of_week']
        
        # Schedule the job
        if day_of_week == 0:
            job = schedule.every().sunday.at(time_str)
        elif day_of_week == 1:
            job = schedule.every().monday.at(time_str)
        elif day_of_week == 2:
            job = schedule.every().tuesday.at(time_str)
        elif day_of_week == 3:
            job = schedule.every().wednesday.at(time_str)
        elif day_of_week == 4:
            job = schedule.every().thursday.at(time_str)
        elif day_of_week == 5:
            job = schedule.every().friday.at(time_str)
        else:
            job = schedule.every().saturday.at(time_str)

        job.do(callback, chat_id=chat_id)
        self.jobs[chat_id] = job
        
        logging.info(f"Scheduled job for chat {chat_id} at {time_str} {timezone} on day {day_of_week}")

    def run(self):
        """Run the scheduler."""
        while True:
            schedule.run_pending()
            time.sleep(1) 
