from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db import models
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from .models import Project, Tag
from .forms import ContactForm


# PROJECTS LIST (with search, tags, pagination)
def projects_list(request):
    q = request.GET.get("q", "").strip()
    tag_name = request.GET.get("tag", "").strip()

    projects = Project.objects.all()
    if q:
        projects = projects.filter(
            models.Q(title__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(tech_stack__icontains=q)
        )

    active_tag = None
    if tag_name:
        active_tag = get_object_or_404(Tag, name__iexact=tag_name)
        projects = projects.filter(tags=active_tag)

    page_obj = Paginator(projects, 6).get_page(request.GET.get("page"))
    tags = Tag.objects.all()

    return render(request, "showcase/projects_list.html", {
        "page_obj": page_obj,
        "q": q,
        "tags": tags,
        "active_tag": active_tag,
    })


# PROJECT DETAIL (now uses pk instead of slug)
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "showcase/project_detail.html", {"project": project})


# ABOUT PAGE
def about(request):
    return render(request, "showcase/about.html")


# CONTACT PAGE
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
