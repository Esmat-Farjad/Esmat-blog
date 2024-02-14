from django.contrib.auth import get_user_model
User = get_user_model()


instance = User.objects.create()
instance.save()
instance.delete()