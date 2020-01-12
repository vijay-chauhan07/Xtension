from django import forms
from .models import Post, Profile , Comment, Images
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'tags',
            'status',
            'restrict_comment',
        
        )
    



EMPTY_USERNAME = "You cant leave this field empty."
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Enter password here...'}))
    confirm_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password here...'}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )
        error_messages={
            'username': {'required': EMPTY_USERNAME}
        }

    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password mismatch")
        return confirm_password
    
    def clean_username(self):
        username=self.cleaned_data['username']

        try:
            user = User.objects.exclude(pk=self.instance.pk).filter(username=username).exists()

        except User.DoesNotExist:
            raise forms.ValidationError(u'Username "%s" is already in use.' %username)
        return username
     
   
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(u'Email "%s" is already registered with us.' %email)

        return email
            







class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=140, label="Username", widget=forms.TextInput(attrs={'placeholder':'Email or Username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)        



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User

        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        ) 
year=[x for x in range(1940,2021)]
class ProfileEditForm(forms.ModelForm):
    dob = forms.DateField(label="Dob", widget=forms.SelectDateWidget(years=year))

    class Meta:

       
        model = Profile
        exclude = ('user','followers',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Text goes here...!!!', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = ('content',)


EMPTY_BODY = "You can't have an empty body"        
class PostUpdateForm(forms.ModelForm):
    class Meta:

        model = Post
        fields = ('title', 'body', 'tags', 'status', 'restrict_comment',)
        
        error_messages={
            'body': {'required': EMPTY_BODY}
        }

class ImageUpdate(forms.ModelForm):
    class Meta:
        model = Images
        exclude = ('post',)