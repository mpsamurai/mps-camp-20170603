from django.contrib import admin
from documents import models


# Register your models here.

@admin.register(models.Document)  # modelsイベントadminクラスですよと定義(adminに登録したいクラスを作る時)
class EventAdmin(admin.ModelAdmin):
   pass
