from django import forms
from .models import Meetings, SignUp, RegisterChama, Article

class Meet(forms.ModelForm):
    class Meta:
        model = Meetings
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Meet, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-group'


class RegisterChamaForm(forms.ModelForm):
    class Meta:
        model = RegisterChama
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RegisterChamaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-group'

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'headline', 'link', 'image']

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():

            visible.field.widget.attrs['class'] = 'form-control' 
