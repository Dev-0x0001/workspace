from datetime import datetime, timedelta
from dateutil import relativedelta

class ReviewScheduler:
    def __init__(self):
        self.start_date = datetime(2023, 1, 1)
        self.review_time = datetime.strptime("10:00", "%H:%M").time()

    def get_next_review_date(self):
        next_date = self.start_date + relativedelta.relativedelta(weeks=2)
        return next_date.date()

    def format_review_date(self, date: datetime):
        return date.strftime("%Y-%m-%d")