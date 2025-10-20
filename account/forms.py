from django import forms


class PhoneForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label='شماره تلفن',
        widget=forms.NumberInput(attrs={
            'placeholder': 'شماره تلفن'
        })
    )


class OTPVerifyForm(forms.Form):
    code = forms.CharField(max_length=6, label='کد تایید')
