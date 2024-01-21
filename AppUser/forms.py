from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True, error_messages={'unique': 'This email is already in use.'})
    # This helps improve the user experience by providing more informative error messages.
    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2")
        
    def save(self, commit = True):
        user = super().save(commit = False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user 
