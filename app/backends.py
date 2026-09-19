from django.contrib.auth.backends import BaseBackend
from app.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, username = None, password =None, **kwargs):
        try:
            User_object=User.objects.get(email=username)
            if User_object.check_password(password):
                return User_object
            else:
                return None
        except:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except:
            return None
        
class PhoneBackend(BaseBackend):
    def authenticate(self, request, username =None, password =None, **kwargs):
        try:
            User_object=User.objects.get(phone=username)
            if User_object.check_password(password):
                return User_object
            else:
                return None
        except:
            return None
    
    def get_user(self, user_id):
            try:
                return User.objects.get(id=user_id)
            except:
                return None