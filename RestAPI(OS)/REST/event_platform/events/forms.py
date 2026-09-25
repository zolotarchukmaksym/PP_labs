from django import forms
from .models import Event, Ticket, Registration, Review, Category, EventLocation, EventOrganizer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Форма реєстрації користувача
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['ticket']  # Ми не включаємо 'event', оскільки воно вже передається через URL
        widgets = {
            'ticket': forms.Select(),  # Додаємо віджет для вибору квитка
        }

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id', None)
        super().__init__(*args, **kwargs)

        if event_id:
            # Фільтруємо квитки для конкретної події
            self.fields['ticket'].queryset = Ticket.objects.filter(event_id=event_id, quantity_available__gt=0)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']  # Поле рейтингу
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


# Форма для фільтрації подій
class EventSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Пошук')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Категорія')
    date = forms.DateField(widget=forms.SelectDateWidget(), required=False, label='Дата')

# Форма для створення події
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'end_date', 'location', 'category', 'organizer']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# Форма для редагування профілю користувача
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

from django import forms
from .models import Category, EventLocation

# Форма для категорій
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

# Форма для додавання нової локації
class EventLocationForm(forms.ModelForm):
    class Meta:
        model = EventLocation
        fields = ['name', 'address', 'contact_email']


class EventOrganizerForm(forms.ModelForm):
    class Meta:
        model = EventOrganizer
        fields = ['user', 'company_name', 'bio']

