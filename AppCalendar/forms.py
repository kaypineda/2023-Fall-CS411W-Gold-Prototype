from django.forms import ModelForm, DateInput
from AppCalendar.models import Task
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class TaskForm(ModelForm):
  class Meta:
    model = Task
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(TaskForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

  class SignUpForm(UserCreationForm):
    class Meta:
      model = User
      fields = ('username', 'password1', 'password2')

  class LoginForm(AuthenticationForm):
      username = forms.CharField()
      password = forms.CharField(widget=forms.PasswordInput)