from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
class UserManager(BaseUserManager):
    def create_user(self,
                    first_name,
                    last_name,
                    username,
                    email,
                    phone_number,
                    user_role,
                    password=None,
                    **extra_fields):    #extra fields q use kr rahe??
        if not email:
            raise ValueError(_("E-mail is required"))
        email = self.normalize_email(email)
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            phone_number = phone_number,
            user_role = user_role,
            app_points = 0,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using= self.db)
        return user

    def create_superuser(self,
                    first_name,
                    last_name,
                    username,
                    email,
                    phone_number = None,
                    password=None,
                    user_role=None,
                    **extra_fields):
        user_role = 'admin'
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(first_name, last_name,username, email, phone_number,user_role, password, **extra_fields)


