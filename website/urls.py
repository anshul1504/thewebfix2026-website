from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.content_page, {"page_type": "about"}, name="about"),
    path("founder/", views.content_page, {"page_type": "founder"}, name="founder"),
    path("services/", views.services, name="services"),
    path("products/", views.products, name="products"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("case-studies/", views.portfolio, name="case_studies"),
    path("clients/", views.content_page, {"page_type": "clients"}, name="clients"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("careers/", views.careers, name="careers"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("plans/", views.plans, name="plans"),
    path("privacy-policy/", views.content_page, {"page_type": "privacy"}, name="privacy"),
    path("terms/", views.content_page, {"page_type": "terms"}, name="terms"),
    path("refund-policy/", views.content_page, {"page_type": "refund"}, name="refund"),
    path("cancellation-refund-policy/", views.content_page, {"page_type": "refund"}, name="cancellation_refund"),
    path("disclaimer/", views.content_page, {"page_type": "disclaimer"}, name="disclaimer"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
]