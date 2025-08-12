from django.shortcuts import render, redirect
from .models import Project
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .forms import ContactForm


def home(request):
    projects = Project.objects.all()
    return render(request, 'showcase/home.html', {'projects': projects})


def about(request):
    return render(request, 'showcase/about.html')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            subject = f"Portfolio contact from {name}"
            body = f"From: {name} <{email}>\n\n{message}"
            try:
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
            else:
                messages.success(request, "Thanks! Your message has been sent.")
                return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "showcase/contact.html", {"form": form})
