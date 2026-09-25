from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from .models import Event, Ticket, Registration, Review, Category, EventLocation, EventOrganizer
from .forms import RegistrationForm, ReviewForm, UserProfileForm, EventSearchForm, EventForm, EventLocationForm, EventOrganizerForm,CategoryForm


def event_list(request):
    category_filter = request.GET.get('category')
    date_filter = request.GET.get('date')
    search_query = request.GET.get('search')

    events = Event.objects.all()

    if category_filter:
        events = events.filter(category__name=category_filter)

    if date_filter:
        events = events.filter(start_date__date=date_filter)

    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    categories = Category.objects.all()

    return render(request, 'event_list.html', {
        'events': events,
        'categories': categories
    })


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    tickets = Ticket.objects.filter(event=event)

    reviews = Review.objects.filter(event=event)

    registration = Registration.objects.filter(user=request.user, event=event).first()

    review_form = ReviewForm()

    return render(request, 'event_detail.html', {
        'event': event,
        'tickets': tickets,
        'reviews': reviews,
        'registration': registration,
        'review_form': review_form
    })

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = event.ticket_set.all()

    if request.method == 'POST':
        form = RegistrationForm(request.POST, event_id=event_id)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.save()

            selected_ticket = form.cleaned_data['ticket']

            if selected_ticket and selected_ticket.quantity_available > 0:
                selected_ticket.quantity_available -= 1
                selected_ticket.save()

                messages.success(request, "Ви успішно зареєструвались на подію.")
                return redirect('event_list')
            else:
                messages.error(request, "Цей квиток більше недоступний.")
                return redirect('event_list')
    else:
        form = RegistrationForm(event_id=event_id)

    return render(request, 'register_for_event.html', {'event': event, 'tickets': tickets, 'form': form})

@login_required
def add_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()
            messages.success(request, "Ваш відгук успішно додано.")
            return redirect('event_detail', event_id=event.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'event': event, 'form': form})

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()

    return render(request, 'create_event.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація успішна. Ласкаво просимо!")
            return redirect('event_list')
        else:
            messages.error(request, "Реєстрація не вдалася. Перевірте введені дані та спробуйте знову.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Ви успішно увійшли.")
            next_url = request.GET.get('next', 'event_list')
            return redirect(next_url)
        else:
            messages.error(request, "Невірне ім'я користувача або пароль. Спробуйте ще раз.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Ви успішно вийшли.")
    return redirect('event_list')


@login_required
def profile(request):
    registrations = Registration.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    return render(request, 'profile.html', {'registrations': registrations, 'reviews': reviews})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш профіль успішно оновлено.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def cancel_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id)
    if registration.user == request.user:
        registration.delete()
        return redirect('event_list')
    else:
        return HttpResponse("You are not authorized to cancel this registration.", status=403)

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Нова категорія успішно додана.")
            return redirect('event_list')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

@staff_member_required
def add_event_location(request):
    if request.method == 'POST':
        form = EventLocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Нова локація успішно додана.")
            return redirect('event_list')
    else:
        form = EventLocationForm()

    return render(request, 'add_event_location.html', {'form': form})

@staff_member_required
def add_event_organizer(request):
    if request.method == 'POST':
        form = EventOrganizerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Новий організатор успішно доданий.")
            return redirect('event_list')
    else:
        form = EventOrganizerForm()

    return render(request, 'add_event_organizer.html', {'form': form})