from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .models import BlogPost, Brochure, CareerOpening, Inquiry, JobApplication, NewsletterSubscriber, Project, Service, Testimonial


class PlatformTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from django.core.management import call_command
        call_command("seed_site", verbosity=0)
        call_command("seed_platform", verbosity=0)

    def test_all_primary_pages_render(self):
        names = ["home", "about", "founder", "services", "portfolio", "case_studies", "clients", "testimonials", "blog", "careers", "contact", "faq", "privacy", "terms", "refund", "disclaimer", "robots", "sitemap"]
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name), secure=True).status_code, 200)

    def test_every_service_and_blog_renders(self):
        self.assertEqual(Service.objects.filter(is_active=True).count(), 49)
        self.assertEqual(BlogPost.objects.filter(is_published=True).count(), 25)
        for service in Service.objects.filter(is_active=True):
            self.assertEqual(self.client.get(reverse("service_detail", args=[service.slug]), secure=True).status_code, 200)
        for post in BlogPost.objects.filter(is_published=True):
            self.assertEqual(self.client.get(reverse("blog_detail", args=[post.slug]), secure=True).status_code, 200)

    def test_inquiry_and_newsletter_persist(self):
        response = self.client.post(reverse("contact"), {"name":"Riya Sharma","email":"riya@example.com","company":"Northstar","service":"Django product","budget":"₹5L–₹12L","message":"We need a secure customer platform for a national launch."}, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Inquiry.objects.filter(email="riya@example.com").count(), 1)
        response = self.client.post(reverse("newsletter"), {"email":"signal@example.com"}, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(NewsletterSubscriber.objects.filter(email="signal@example.com").exists())

    def test_sitemap_contains_dynamic_content(self):
        xml = self.client.get(reverse("sitemap"), secure=True).content.decode()
        self.assertIn("/services/django-development/", xml)
        self.assertIn("/blog/seo-in-2026", xml)

    def test_brochure_is_registered(self):
        self.assertTrue(Brochure.objects.filter(is_active=True).exists())
    def test_home_has_local_seo_and_guest_decision_content(self):
        response = self.client.get(reverse("home"), secure=True)
        self.assertContains(response, "Digital marketing and technology agency in Indore")
        self.assertContains(response, "Built in Indore. Ready for India.")
        self.assertContains(response, "FAQPage")
        self.assertContains(response, "Why businesses trust The Webfix")
        self.assertEqual(len(response.context["services"]), 6)

    def test_primary_pages_have_no_mojibake(self):
        names = ["home", "about", "founder", "services", "portfolio", "clients", "blog", "careers", "contact", "faq"]
        bad_markers = ("\u00e2", "\u00c3", "\u00c2", "\ufffd")
        for name in names:
            with self.subTest(name=name):
                content = self.client.get(reverse(name), secure=True).content.decode("utf-8")
                for marker in bad_markers:
                    self.assertNotIn(marker, content)
    def test_client_testimonials_are_seeded(self):
        self.assertEqual(Testimonial.objects.filter(is_active=True).count(), 21)
        response = self.client.get(reverse("home"), secure=True)
        self.assertContains(response, "agrasenplywood.com")
        self.assertContains(response, "tridevirealty.in")
        self.assertContains(response, "View 21 client stories")
        names = Testimonial.objects.values_list("client_name", flat=True)
        self.assertEqual(len(names), len(set(names)))
        sunil = Testimonial.objects.get(client_name="Sunil Malviya")
        self.assertEqual(len(sunil.website_list), 4)
    def test_audited_guest_flow(self):
        response = self.client.get(reverse("home") + "?utm_source=test", secure=True)
        self.assertContains(response, 'id="contact"')
        self.assertContains(response, "Client project")
        self.assertNotContains(response, "Verified client")
        self.assertContains(response, "website/css/")
        self.assertContains(response, f'<link rel="canonical" href="https://testserver/">', html=True)
        self.assertEqual(len(response.context["projects"]), 6)
        self.assertEqual(Project.objects.filter(title="APICON Real Infra", is_active=True).count(), 1)

        testimonial_response = self.client.get(reverse("testimonials"), secure=True)
        self.assertTemplateUsed(testimonial_response, "website/pages/testimonials.html")
        self.assertContains(testimonial_response, "Client project", count=21)

    def test_inquiry_notifications_and_spam_trap(self):
        payload = {
            "name": "Asha Verma",
            "email": "asha@example.com",
            "company": "Asha Studio",
            "phone": "9999999999",
            "service": "Website development",
            "budget": "INR 2L-5L",
            "message": "We need a business website.",
            "website": "",
        }
        response = self.client.post(reverse("home"), payload, secure=True)
        self.assertRedirects(response, reverse("home") + "?submitted=1#contact", fetch_redirect_response=False)
        self.assertEqual(Inquiry.objects.filter(email="asha@example.com").count(), 1)
        self.assertEqual(len(mail.outbox), 2)

        payload["email"] = "spam@example.com"
        payload["website"] = "https://spam.example"
        response = self.client.post(reverse("home"), payload, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Inquiry.objects.filter(email="spam@example.com").exists())

    def test_sitemap_contains_static_guest_pages(self):
        xml = self.client.get(reverse("sitemap"), secure=True).content.decode()
        for name in ("about", "faq", "clients", "testimonials", "founder", "careers"):
            with self.subTest(name=name):
                self.assertIn(reverse(name), xml)
    def test_career_application_with_resume_is_saved(self):
        opening = CareerOpening.objects.filter(is_active=True).first()
        resume = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 test resume", content_type="application/pdf")
        response = self.client.post(reverse("careers"), {
            "opening": opening.pk,
            "name": "Aarav Mehta",
            "email": "aarav@example.com",
            "phone": "9999999998",
            "current_location": "Indore, Madhya Pradesh",
            "experience": "3 years",
            "portfolio_url": "https://github.com/aarav",
            "linkedin_url": "https://linkedin.com/in/aarav",
            "cover_note": "I have built and maintained production applications for growing teams.",
            "resume": resume,
            "consent": "on",
        }, secure=True)
        self.assertRedirects(response, reverse("careers") + "?applied=1#application", fetch_redirect_response=False)
        application = JobApplication.objects.get(email="aarav@example.com")
        self.assertEqual(application.opening, opening)
        self.assertEqual(application.status, "new")
        self.assertEqual(len(mail.outbox), 2)
        application.resume.delete(save=False)

    def test_career_resume_type_is_validated(self):
        opening = CareerOpening.objects.filter(is_active=True).first()
        resume = SimpleUploadedFile("resume.exe", b"not a resume", content_type="application/octet-stream")
        response = self.client.post(reverse("careers"), {
            "opening": opening.pk,
            "name": "Invalid File",
            "email": "invalid@example.com",
            "phone": "9999999997",
            "current_location": "Indore",
            "experience": "1 year",
            "cover_note": "Relevant experience details.",
            "resume": resume,
            "consent": "on",
        }, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Upload a PDF, DOC or DOCX resume.")
        self.assertFalse(JobApplication.objects.filter(email="invalid@example.com").exists())