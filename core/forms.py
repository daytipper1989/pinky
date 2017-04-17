from django.forms import ModelForm
import datetime
from django import forms
from models import *
from django.utils.translation import ugettext_lazy as _

class MembershipForm(ModelForm):

    class Meta:
		model = Membership
		fields = ['package']

class CustomerForm(ModelForm):

    class Meta:
		model = Customer
		fields = ['firstName','lastName','mobile','home','address','email','note']

class CustomerSearchForm(forms.Form):
    mobile = forms.CharField(label = _('Mobile Number'),max_length=20,required=True)

class CustomerSelectForm(forms.Form):
    mobile = forms.CharField(label = _('Mobile Number'),max_length=20,required=False)

class EmployeeSelectForm(forms.Form):
    employee = forms.ModelChoiceField(queryset = Employee.objects.all(),required=False)

class PackageSelectForm(forms.Form):
    package = forms.ModelChoiceField(queryset = Package.objects.all(),required=False)

class SkillSelectForm(forms.Form):
    skill = forms.ModelChoiceField(queryset = ClassType.objects.all(),required=False)

class MembershipSelectForm(forms.Form):
    membership = forms.ModelChoiceField(queryset = Membership.objects.all(),required=True)

class TrainerSelectForm(forms.Form):
    trainer = forms.ModelChoiceField(queryset = Trainer.objects.all(),required=False)

class ExerciseSelectForm(forms.Form):
    exercise = forms.ModelChoiceField(queryset = Exercise.objects.all(),required=True)

class ShipmentSelectForm(forms.Form):
    shipment = forms.ModelChoiceField(queryset = Shipment.objects.all(),required=False)

class GovernmentSelectForm(forms.Form):
    government = forms.ModelChoiceField(queryset = Government.objects.all(),required=False,label=_('Governerate'))

class CustomerDetailAttributeSelectForm(forms.Form):
    customerDetailAttribute = forms.ModelChoiceField(queryset = CustomerDetailAttribute.objects.all(),required=True,label=_('Attribute'))

class LocationSelectForm(forms.Form):
    location = forms.ModelChoiceField(queryset = Location.objects.all(),required=True)

    def __init__(self, *args, **kwargs):
        req = kwargs.pop('req', None)
        super(LocationSelectForm, self).__init__(*args, **kwargs)

        if req:
            self.fields['location'].queryset = Employee.objects.get(user=req.user).locations

class AddressForm(forms.Form):
    address = forms.CharField(label = _('Address'), required=False, max_length=255)

class PriceFilterForm(forms.Form):
    minimum = forms.DecimalField(label = _('Minimum Price'), required=False)
    maximum = forms.DecimalField(label = _('Maximum Price'), required=False)

class IntegerAmountForm(forms.Form):
    amount = forms.IntegerField(label = _('Amount'), required=True)

class ClassSelectForm(forms.Form):
    classs = forms.ModelChoiceField(label = _('Class'),queryset = Class.objects.filter(startingTime__gte=datetime.datetime.now()).order_by('startingTime'))

class ClassForm(ModelForm):

    class Meta:
		model = Class
		fields = ['startingTime','trainer','isTrainerPaid','type']
		widgets = {
            'startingTime': forms.TextInput(attrs={'id':'datetimepicker'}),
        }

class ClassTypeForm(ModelForm):

    class Meta:
		model = ClassType
		fields = ['name','description','note']

class TrainerForm(ModelForm):

    class Meta:
		model = Trainer
		fields = ['firstName','lastName','mobile','home','address','note','skill','salary']

class SpaAttendanceForm(ModelForm):

    class Meta:
		model = SpaUsage
		fields = ['startingTime']
		widgets = {
            'startingTime': forms.TextInput(attrs={'id':'datetimepicker'}),
        }

class MachineAttendanceForm(ModelForm):

    class Meta:
		model = MachinesUsage
		fields = ['startingTime']
		widgets = {
            'startingTime': forms.TextInput(attrs={'id':'datetimepicker'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=30)
    password = forms.CharField(label=_('Password'), max_length=100,widget=forms.PasswordInput)