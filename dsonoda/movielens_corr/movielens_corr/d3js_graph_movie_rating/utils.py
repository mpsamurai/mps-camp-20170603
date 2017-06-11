from d3js_graph_movie_rating import models
from d3js_graph_movie_rating import consts
import time
from hashlib import md5


def get_queue_id():
    """
    並列処理のキューを生成
    :return:
    """
    timestamp = time.time()
    timestamp = str(timestamp)
    m = md5()
    m.update(timestamp.encode())
    return m.hexdigest()

def get_sync_status_by_mode(mode):
    """
    並列処理のステータス取得
    :param mode:
    :return:
    """
    try:
        sync_status = models.SyncStatus.objects.get(mode=mode).status
    except models.SyncStatus.DoesNotExist:
        sync_status = 0
    return sync_status

def get_fileupload_status(model):
    """
    ファイルアップロードのステータス取得
    :param mode: モデルの種類
    :return:
    """
    if model.objects.all().count():
        return consts.FILEUPLOAD_STATUS[1][0]
    else:
        return consts.FILEUPLOAD_STATUS[0][0]
