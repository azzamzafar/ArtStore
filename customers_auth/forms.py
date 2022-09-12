from django import forms
from django_registration.forms import RegistrationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Customer

class ProfileForm(RegistrationForm):

    class Meta(RegistrationForm.Meta):
        model=Customer
        fields = ('username','email','password1','password2')
    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit','Register'))

    username = forms.CharField()    
    # contact details
    
# class ContactForm(forms.ModelForm):
    
#     class Meta():
#         ...