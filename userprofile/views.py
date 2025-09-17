# SpendTrackerMain/userprofile/views.py
import random
import string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from SpendTrackerMain import settings
from .forms import NewAccountForm


class CreateNewAccount(CreateView):
    template_name = 'registration/register.html'
    form_class = NewAccountForm

    def get_success_url(self):
        psw = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + '!$%&?@') for
            _ in range(8))
        print(psw)
        if User.objects.filter(id=self.object.id).exists():
            user_instance = User.objects.get(id=self.object.id)
            user_instance.set_password(psw)
            user_instance.save()
            content = f'USERNAME: {user_instance.username} \n       PASSWORD: {psw}'
            msg_html = render_to_string('registration/invite_user.html', {'content_email': content})
            email = EmailMultiAlternatives(
                subject='SpendTrackerRegistrationData',
                body=content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_instance.email]
            )
            email.attach_alternative(msg_html, 'text/html')
            email.send()
        return reverse('userprofile:inregistrare_reusita')

    def form_invalid(self, form):
        return super(CreateNewAccount, self).form_invalid(form)


def register_success(request):
    return render(request, 'registration/registration_success.html')
