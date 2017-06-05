from django.contrib import admin
from events import models

# Register your models here.

@admin.register(models.Event)  # modelsイベントadminクラスですよと定義(adminに登録したいクラスを作る時)
class EventAdmin(admin.ModelAdmin):
   pass

@admin.register(models.EventQuestion)  # modelsイベントadminクラスですよと定義(adminに登録したいクラスを作る時)
class EventQuestionAdmin(admin.ModelAdmin):
   pass

@admin.register(models.EventBookingList)  # 予約サイト
class EventBookingList(admin.ModelAdmin):
   pass