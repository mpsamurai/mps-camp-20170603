
# 性別
GENDER_CHOISE = (('F', 'Female'), ('M', 'Male'))

"""
並列処理を行う機能の種類
1: ファイルアップロード 男女の相関
2: グラフ表示 男女の相関
"""
SYNC_MODE = ((1, 'file_upload_men_women_rating'), (2, 'gpaph_men_women_rating'))

"""
並列処理のステータス
1: キュー発行
2: 処理中
3: 処理完了
"""
SYNC_STATUS = ((1, 'キュー発行済み'), (2, '処理開始'), (3, '処理完了'))

"""
ファイルアップロードのステータス
1: 未アップ
2: アップ済み
"""
FILEUPLOAD_STATUS = ((1, '未アップ'), (2, 'アップ済み'))
