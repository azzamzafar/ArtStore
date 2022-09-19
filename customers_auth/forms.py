from django import forms
from django_registration.forms import RegistrationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Customer
# from phonenumber_field.formfields import PhoneNumberField
# from .models import get_city_values,get_state_values,get_country_values

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
    
class ContactForm(forms.ModelForm):
    
    class Meta():
        model = Customer
        fields = ('country', 'phone','state','city', 'address1', 'address2')
    
    def __init__(self,*args,**kwargs):
        super(ContactForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit',"Add"))
        self.helper.form_style="inline"

    address1 = forms.CharField(widget=forms.Textarea(attrs={"rows":2,'placeholder': 'address line 1'}))
    address2 = forms.CharField(widget=forms.Textarea(attrs={"rows":2,'placeholder': 'address line 2'}))

        # self.helper.form_action("{% url 'profile' %}")
    # phone = PhoneNumberField(region="IN")
    # cities = get_city_values()
    # states = get_state_values()
    # countries = get_country_values()

    # country = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=countries,
    # ) 
    # city = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=cities,
    # ) 
    # state = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.CheckboxSelectMultiple,
    #     choices=states,
    # ) 
    