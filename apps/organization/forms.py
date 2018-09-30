from django import forms

from operation.models import UserAsk

# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     photo = forms.CharField(required=True,min_length=11,max_length=11)
#     course_name = forms.CharField(required= True,max_length=5,min_length=50)


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']