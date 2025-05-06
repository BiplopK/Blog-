from django import forms 

class RegistrationForm(forms.Form):
    username=forms.CharField(
        max_length=100,
        label="Username",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
        )
    first_name=forms.CharField(
        max_length=100,
        label="First Name",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Forst Name'})
        )
    last_name=forms.CharField(
        max_length=100,
        label="Last Name",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'})
        )
    email = forms.EmailField(
        max_length=100,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password=forms.CharField(
        max_length=100,
        label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'})
    )
    confirm_password=forms.CharField(
        max_length=100,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'})
    )
    
    def clean(self):
        cleaned_data=super().clean()    
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        
        if password and confirm_password and password!=confirm_password:
            self.add_error("confirm_password","Password did not match")
            
        return cleaned_data


class LoginForm(forms.Form):
    username=forms.CharField(
        max_length=100,
        label="Username",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
    )
    password=forms.CharField(
        max_length=100,
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'})
    )