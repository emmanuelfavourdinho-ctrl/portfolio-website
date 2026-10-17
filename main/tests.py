from unittest import mock

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from main.models import Contact

GOOD = {"name": "Ada", "email": "ada@example.com", "message": "Hello, I would like to talk."}


@override_settings(CONTACT_RECIPIENT="me@example.com", DEFAULT_FROM_EMAIL="me@example.com",
                   EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class SiteTests(TestCase):
    def test_routes(self):
        for url in ["/", "/work/portfolio-site/", "/work/newbiz-creation-studio/", "/robots.txt", "/sitemap.xml"]:
            self.assertEqual(self.client.get(url).status_code, 200, url)
        self.assertEqual(self.client.get("/work/nope/").status_code, 404)

    def test_homepage_has_no_dead_links(self):
        html = self.client.get("/").content.decode()
        self.assertNotIn('href="#"', html)
        self.assertIn("Thoughtful software.", html)

    def test_hero_photo_has_alt_text_and_about_photos_are_optional(self):
        from portfolio import content
        html = self.client.get("/").content.decode()
        self.assertIn('class="hero-img"', html)
        self.assertIn(content.HERO_IMAGE["alt"], html)
        self.assertNotIn("about-photos", html)  # nothing rendered until photos are added
        with mock.patch.object(content, "ABOUT_PHOTOS", [{"src": "img/hero-1200.webp", "alt": "Test photo", "caption": ""}]):
            html = self.client.get("/").content.decode()
        self.assertIn('class="about-photos"', html)
        self.assertIn('alt="Test photo"', html)

    def test_valid_message_is_sent_and_saved(self):
        r = self.client.post("/", GOOD)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].reply_to, ["ada@example.com"])
        self.assertEqual(Contact.objects.count(), 1)

    def test_invalid_message_is_rejected_with_errors(self):
        r = self.client.post("/", {"name": "", "email": "bad", "message": "short"})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(len(mail.outbox), 0)
        for text in ["Enter your name", "valid email", "at least 10"]:
            self.assertContains(r, text, status_code=400)

    def test_honeypot_discards_bots(self):
        self.client.post("/", {**GOOD, "website": "http://spam"})
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(Contact.objects.count(), 0)

    def test_send_failure_is_reported_not_hidden(self):
        with mock.patch("django.core.mail.EmailMessage.send", side_effect=OSError("smtp down")):
            r = self.client.post("/", GOOD, follow=False)
        self.assertEqual(r.status_code, 400)
        self.assertContains(r, "was not sent", status_code=400)
        self.assertEqual(Contact.objects.count(), 0)

    @override_settings(CONTACT_RECIPIENT="")
    def test_unconfigured_email_fails_visibly(self):
        r = self.client.post("/", GOOD)
        self.assertContains(r, "was not sent", status_code=400)
