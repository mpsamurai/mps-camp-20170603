from django.contrib import admin
from ratings import models


@admin.register(models.Ratings)  # modelsイベントadminクラスですよと定義(adminに登録したいクラスを作る時)
class RatingsAdmin(admin.ModelAdmin):
   pass
