from django.contrib import admin
from rating import models

# Register your models here.

@admin.register(models.Movie)  # modelsイベントadminクラスですよと定義(adminに登録したいクラスを作る時)
class MovieAdmin(admin.ModelAdmin):
   pass

@admin.register(models.User)  # modelsイベントadminクラスですよと定義(adminに登録したいクラスを作る時)
class UserAdmin(admin.ModelAdmin):
   pass

@admin.register(models.Rating)  # modelsイベントadminクラスですよと定義(adminに登録したいクラスを作る時)
class RatingAdmin(admin.ModelAdmin):
   pass