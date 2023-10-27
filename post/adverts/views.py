from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Advertisement
from django.core.mail import send_mail
from .forms import RegistrationForm, AdvertisementForm, ResponseForm


def generate_and_send_confirmation_code(user):
    # Генерируем случайный код
    confirmation_code = ''.join(random.choice('0123456789') for _ in range(6))
    one_time_code = OneTimeCode.objects.create(user=user, code=confirmation_code)

    # Отправляем код по электронной почте
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {confirmation_code}'
    from_email = 'your@example.com'  # Ваш email
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

# Представление для регистрации пользователей
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            generate_and_send_confirmation_code(user)
        return redirect('login')
    else:
        form = RegistrationForm()
        return render(request, 'registration/signup.html', {'form': form})


# Представление для создания объявления
@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('home')
    else:
        form = AdvertisementForm()
    return render(request, 'create_advertisement.html', {'form': form})


# Представление для отправки отклика
@login_required
def create_response(request, advertisement_id):
    advertisement = Advertisement.objects.get(id=advertisement_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.advertisement = advertisement
            response.save()

            # Отправка уведомления по email
            subject = f'Отклик на ваше объявление: {advertisement.title}'
            message = 'Вы получили новый отклик на ваше объявление.'
            from_email = 'your@example.com'  # Ваш email
            recipient_list = [advertisement.user.email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('home')
    else:
        form = ResponseForm()
    return render(request, 'create_response.html', {'form': form, 'advertisement': advertisement})

