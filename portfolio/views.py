from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from main.models import Contact

from . import content


def _context(**extra):
    return {"c": content, "projects": content.PROJECTS, "capabilities": content.CAPABILITIES, **extra}


def _validate(data):
    errors = {}
    if not data["name"] or len(data["name"]) > 100:
        errors["name"] = "Enter your name (up to 100 characters)."
    try:
        validate_email(data["email"])
    except ValidationError:
        errors["email"] = "Enter a valid email address."
    if len(data["message"]) < 10:
        errors["message"] = "Write at least 10 characters so I know what you need."
    elif len(data["message"]) > 5000:
        errors["message"] = "Keep the message under 5,000 characters."
    return errors


def home(request):
    form = {"name": "", "email": "", "message": ""}
    errors = {}
    if request.method == "POST":
        if request.POST.get("website"):  # honeypot: real visitors never see this field
            return redirect(reverse("home") + "#contact")
        form = {k: request.POST.get(k, "").strip() for k in form}
        errors = _validate(form)
        if not errors:
            name = " ".join(form["name"].split())
            try:
                if not settings.CONTACT_RECIPIENT:
                    raise RuntimeError("Email is not configured")
                EmailMessage(
                    subject=f"Portfolio message from {name}",
                    body=f"Name: {name}\nEmail: {form['email']}\n\n{form['message']}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECIPIENT],
                    reply_to=[form["email"]],
                ).send(fail_silently=False)
            except Exception:
                messages.error(request, "Your message was not sent. Please email me directly instead.")
                errors["send"] = True
            else:
                Contact.objects.create(name=name, email=form["email"], message=form["message"])
                messages.success(request, "Message sent. I will reply to the address you gave.")
                return redirect(reverse("home") + "#contact")
        status = 400
    else:
        status = 200
    return render(request, "portfolio/home.html", _context(form=form, errors=errors), status=status)


def case_study(request, slug):
    project = next((p for p in content.PROJECTS if p["slug"] == slug), None)
    if not project:
        raise Http404
    return render(request, "portfolio/case_study.html", _context(project=project))


def robots(request):
    body = f"User-agent: *\nAllow: /\nSitemap: {request.build_absolute_uri('/sitemap.xml')}\n"
    return HttpResponse(body, content_type="text/plain")


def sitemap(request):
    paths = ["/"] + [reverse("case_study", args=[p["slug"]]) for p in content.PROJECTS]
    urls = "".join(f"<url><loc>{request.build_absolute_uri(p)}</loc></url>" for p in paths)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return HttpResponse(xml, content_type="application/xml")
