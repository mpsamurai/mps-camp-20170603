from django.contrib import admin
from events import models

# Register your models here.

@admin.register(models.Event)  # modelsイベントadminクラスですよと定義(adminに登録したいクラスを作る時)
class EventAdmin(admin.ModelAdmin):
   pass

