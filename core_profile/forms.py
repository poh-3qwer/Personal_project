from django import forms
from core_profile.models import Account
from PIL import Image


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['human_name',
                  'human_surname',
                  'bio',
                  'email',
                  'phone_number',
                  'avatar',
                  ]

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Розмір аватара не має перевищувати 2МБ.')

            image = Image.open(avatar)

            if image.width != 447 or image.height != 447:
                raise forms.ValidationError('Розмір аватара має бути 447х447 пікс.')
        return avatar