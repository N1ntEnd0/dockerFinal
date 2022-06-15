from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.contrib.auth import get_user_model

from users.utils import check_and_refresh_token
from apscheduler.schedulers.blocking import BlockingScheduler



def refresh_shared_user_job():
    print('Job running')

    User = get_user_model()
    check_and_refresh_token(User.objects.get(username=settings.DEFAULT_SHARED_USER),
                             settings.SOCIAL_AUTH_DEFAULT_PROVIDER)

def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

    scheduler.add_job(
        refresh_shared_user_job,
        trigger='cron',
        day_of_week="1-6",
        hour=6,
        minute=30,
        id="refresh_shared_user_token",
        max_instances=1,
        replace_existing=False
    )

    scheduler.start()
