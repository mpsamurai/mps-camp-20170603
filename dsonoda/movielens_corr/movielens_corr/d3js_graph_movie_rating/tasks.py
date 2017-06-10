from movielens_corr.celery import app as celery_app
from celery.utils.log import get_task_logger
from d3js_graph_movie_rating import models

logger = get_task_logger(__name__)

#celery のタスク化
@celery_app.task
def add_with_sleep(x,y):
    import time
    time.sleep(60)
    r = x + y
    logger.info('The answer is %s' % r)
    return r
