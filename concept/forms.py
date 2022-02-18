from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
from django.core.mail import EmailMessage

User = get_user_model()

class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #htmlの表示を変更可能にします
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
       model = User
       fields = ("username", "password1", "password2",)


class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'last_name',
            'first_name',
        ]

    def __init__(self, email=None, first_name=None, last_name=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if email:
            self.fields['email'].widget.attrs['value'] = email
        if first_name:
            self.fields['first_name'].widget.attrs['value'] = first_name
        if last_name:
            self.fields['last_name'].widget.attrs['value'] = last_name

    def update(self, user):
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class ContactForm(forms.Form):
 name = forms.CharField(label='名前', max_length=30)
 email = forms.EmailField(label='メール')
 inquiry = forms.CharField(label='問い合わせ内容',widget=forms.Textarea)
   
 def __init__(self, *args, **kwargs):
   super().__init__(*args, **kwargs)

 def send_email(self):
    name = self.cleaned_data['name']
    email = self.cleaned_data['email']
    inquiry = self.cleaned_data['inquiry']
    
    message = EmailMessage(subject=name + "からの問い合わせ",
                            body=inquiry + " 　　　　　　　　　　　　　　　　　　　　　　　" + "問い合わせ元:" + email,
                            from_email=email,
                            to=["masomitsu.work@gmail.com"],
                            #cc=[email]
                            )
    message.send()