from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from typing import Optional # For better code readability and maintainability.

class EmailBackend(ModelBackend):
    def authenticate(self, request, username: str = None, password: str = None, **kwargs) -> Optional[get_user_model()]:
        
        """
        Authenticates a user by email and password.

        Parameters:
            request (HttpRequest): The HTTP request object.
            username (str): User's email address.
            password (str): User's password.
            **kwargs: Additional keyword arguments.

        Returns:
            get_user_model(): The authenticated user if successful, None otherwise.
        """
        
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            logger.warning(f"Authentication failed for email: {username}")
            return None
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None

    def get_user(self, user_id)-> Optional[get_user_model()]:
        """
        Retrieve a user by user ID.

        Parameters:
            user_id (int): The user ID.

        Returns:
            get_user_model(): The user instance if found, None otherwise.
        """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
