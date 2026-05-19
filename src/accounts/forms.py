
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'tc_kimlik', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['role'].choices = [
            ('musteri', 'Müşteri'),
            ('satici', 'Satıcı'),
        ]

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
