from django.contrib import messages
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from .forms import InquiryForm, JobApplicationForm
from .models import (
    BlogPost, Brochure, CareerOpening, Client, ContentPage, FAQ, FounderProfile,
    NavigationItem, NewsletterSubscriber, ProcessStep, Product, Project, Service,
    SiteSettings, SocialLink, Statistic, Technology, Testimonial,
)


def shared():
    footer_slugs = ["digital-marketing", "seo", "website-development", "custom-software-development", "social-media-management", "website-maintenance"]
    footer_map = {item.slug: item for item in Service.objects.filter(is_active=True, slug__in=footer_slugs)}
    return {
        "site": SiteSettings.objects.first() or SiteSettings.objects.create(),
        "global_services": [footer_map[slug] for slug in footer_slugs if slug in footer_map],
        "socials": SocialLink.objects.filter(is_active=True),
        "brochure": Brochure.objects.filter(is_active=True).first(),
    }


def send_branded_email(subject, recipient, heading, intro, rows, *, reply_to=None, action_url="", action_text=""):
    html = render_to_string("website/emails/notification.html", {
        "preheader": subject, "eyebrow": "The Webfix notification", "heading": heading,
        "intro": intro, "rows": rows, "action_url": action_url, "action_text": action_text,
    })
    message = EmailMultiAlternatives(
        subject=subject, body=strip_tags(html), from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient], reply_to=[reply_to] if reply_to else None,
    )
    message.attach_alternative(html, "text/html")
    return message.send(fail_silently=True)


def notify_inquiry(inquiry, site):
    rows = [
        ("Name", inquiry.name), ("Email", inquiry.email), ("Phone", inquiry.phone or "-"),
        ("Company", inquiry.company or "-"), ("Service", inquiry.service),
        ("Budget", inquiry.budget or "-"), ("Project brief", inquiry.message),
    ]
    send_branded_email(
        f"New project enquiry from {inquiry.name}", site.email,
        "A new project enquiry has arrived.",
        "Review the requirement below and respond within one business day.", rows,
        reply_to=inquiry.email, action_url=f"mailto:{inquiry.email}", action_text="Reply to enquiry",
    )
    send_branded_email(
        "We received your project brief | The Webfix", inquiry.email,
        f"Thank you, {inquiry.name}.",
        "Your project brief is with our team. A senior consultant will review it and respond within one business day.",
        [("Service", inquiry.service), ("Budget", inquiry.budget or "To be discussed"), ("Reference", f"Enquiry #{inquiry.pk}")],
        action_url=site.whatsapp_url, action_text="Chat on WhatsApp",
    )

def inquiry_rate_allowed(request):
    address = request.META.get("REMOTE_ADDR", "unknown")
    email = request.POST.get("email", "").strip().lower()
    return cache.add(f"website-inquiry:{address}:{email}", True, timeout=30)


def home(request):
    featured_slugs = ["digital-marketing", "seo", "social-media-management", "website-development", "django-development", "erp-development"]
    featured_map = {item.slug: item for item in Service.objects.filter(is_active=True, slug__in=featured_slugs)}
    featured_services = [featured_map[slug] for slug in featured_slugs if slug in featured_map]
    product_slugs = ["finance-management-software", "business-websites", "ecommerce-solutions", "erp-systems", "crm-solutions", "inventory-software"]
    product_map = {item.slug: item for item in Product.objects.filter(is_active=True, slug__in=product_slugs)}
    featured_products = [product_map[slug] for slug in product_slugs if slug in product_map]
    featured_project_titles = ["APICON Real Infra", "Richkid", "Life Holiday", "Greenland H.S. School", "Krishna Law Firm", "RNT MPL"]
    featured_project_map = {item.title: item for item in Project.objects.filter(is_active=True, title__in=featured_project_titles)}
    featured_projects = [featured_project_map[title] for title in featured_project_titles if title in featured_project_map]
    context = shared() | {
        "nav_items": NavigationItem.objects.filter(is_active=True),
        "stats": Statistic.objects.filter(is_active=True),
        "services": featured_services,
        "steps": ProcessStep.objects.filter(is_active=True),
        "projects": featured_projects,
        "products": featured_products,
        "technologies": Technology.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_active=True),
        "faqs": FAQ.objects.filter(is_active=True),
        "form": InquiryForm(request.POST or None),
    }
    if request.method == "POST" and context["form"].is_valid():
        if not inquiry_rate_allowed(request):
            context["form"].add_error(None, "Please wait a moment before sending another request.")
            return render(request, "website/home.html", context)
        inquiry = context["form"].save()
        notify_inquiry(inquiry, context["site"])
        messages.success(request, "Your brief is in. We will respond within one business day.")
        return redirect(f"{reverse('home')}#contact")
    return render(request, "website/home.html", context)


def content_page(request, page_type):
    page = get_object_or_404(ContentPage, page_type=page_type)
    context = shared() | {"page": page, "stats": Statistic.objects.filter(is_active=True), "steps": ProcessStep.objects.filter(is_active=True)}
    if page_type in {"about", "founder"}:
        context["founder"] = FounderProfile.objects.first()
    if page_type == "clients":
        context["clients"] = Client.objects.filter(is_active=True)
        context["industries"] = Client.objects.filter(is_active=True).values_list("industry", flat=True).distinct()
    if page_type == "careers":
        context["openings"] = CareerOpening.objects.filter(is_active=True)
    return render(request, f"website/pages/{page_type}.html" if page_type in {"about", "founder", "clients", "careers", "contact"} else "website/pages/legal.html", context)


def services(request):
    all_services = list(Service.objects.filter(is_active=True))
    service_map = {item.slug: item for item in all_services}
    group_specs = [
        ("growth", "Digital growth", "Create demand and turn attention into measurable enquiries and revenue.", "fa-chart-line", ["digital-marketing", "seo", "social-media-management", "performance-marketing", "local-seo", "technical-seo", "google-ads", "meta-ads", "email-marketing", "whatsapp-marketing", "content-marketing", "influencer-marketing", "instagram-marketing", "facebook-marketing", "linkedin-marketing"]),
        ("brand", "Brand and experience", "Build a clear identity and customer experience people can recognise and trust.", "fa-pen-ruler", ["brand-strategy", "brand-identity", "ui-ux-design", "graphic-design", "logo-design"]),
        ("web", "Websites and web apps", "Launch fast, credible and conversion-focused digital experiences.", "fa-window-maximize", ["website-development", "website-design", "django-development", "web-application-development", "corporate-website", "business-website", "landing-page", "wordpress-development", "python-development", "react-development"]),
        ("software", "Business software and SaaS", "Turn operational workflows into secure software built around your team.", "fa-cubes", ["custom-software-development", "saas-development", "erp-development", "crm-development", "api-development", "api-integration"]),
        ("mobile", "Mobile applications", "Create polished mobile products with reliable backend integration.", "fa-mobile-screen-button", ["android-app-development", "ios-app-development", "flutter-development"]),
        ("cloud", "Cloud, hosting and support", "Keep websites and applications secure, available and maintained.", "fa-cloud", ["cloud-hosting", "domain-hosting", "aws-deployment", "server-management", "website-maintenance", "cyber-security"]),
        ("automation", "AI, automation and consulting", "Remove repetitive work and make better technology decisions.", "fa-wand-magic-sparkles", ["ai-automation", "business-automation", "chatbot-development", "it-consulting"]),
    ]
    groups = []
    included = set()
    for slug, title, description, icon, service_slugs in group_specs:
        items = [service_map[item_slug] for item_slug in service_slugs if item_slug in service_map]
        included.update(item.pk for item in items)
        groups.append({"slug": slug, "title": title, "description": description, "icon": icon, "featured": items[:4], "more": items[4:], "count": len(items)})
    unmatched = [item for item in all_services if item.pk not in included]
    if unmatched:
        groups.append({"slug": "specialist", "title": "Specialist services", "description": "Additional delivery capability for specific business requirements.", "icon": "fa-toolbox", "featured": unmatched[:4], "more": unmatched[4:], "count": len(unmatched)})
    return render(request, "website/pages/services.html", shared() | {"services": all_services, "service_groups": groups})


def products(request):
    custom_slugs = ["erp-systems", "crm-solutions", "web-applications", "mobile-apps", "business-automation", "ecommerce-solutions"]
    product_map = {item.slug: item for item in Product.objects.filter(is_active=True, slug__in=custom_slugs)}
    custom_products = [product_map[slug] for slug in custom_slugs if slug in product_map]
    return render(request, "website/pages/products.html", shared() | {"products": custom_products})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    category_specs = [
        ("Digital growth", "growth", "fa-chart-line", ["digital-marketing", "seo", "social-media-management", "performance-marketing", "local-seo", "technical-seo", "google-ads", "meta-ads", "email-marketing", "whatsapp-marketing", "content-marketing", "influencer-marketing", "instagram-marketing", "facebook-marketing", "linkedin-marketing"]),
        ("Brand and experience", "brand", "fa-pen-ruler", ["brand-strategy", "brand-identity", "ui-ux-design", "graphic-design", "logo-design"]),
        ("Websites and web apps", "web", "fa-window-maximize", ["website-development", "website-design", "django-development", "web-application-development", "corporate-website", "business-website", "landing-page", "wordpress-development", "python-development", "react-development"]),
        ("Business software and SaaS", "software", "fa-cubes", ["custom-software-development", "saas-development", "erp-development", "crm-development", "api-development", "api-integration"]),
        ("Mobile applications", "mobile", "fa-mobile-screen-button", ["android-app-development", "ios-app-development", "flutter-development"]),
        ("Cloud, hosting and support", "cloud", "fa-cloud", ["cloud-hosting", "domain-hosting", "aws-deployment", "server-management", "website-maintenance", "cyber-security"]),
        ("AI, automation and consulting", "automation", "fa-wand-magic-sparkles", ["ai-automation", "business-automation", "chatbot-development", "it-consulting"]),
    ]
    category_title, category_slug, category_icon, category_slugs = "Digital capability", "specialist", "fa-toolbox", [service.slug]
    for title, group_slug, icon, slugs in category_specs:
        if service.slug in slugs:
            category_title, category_slug, category_icon, category_slugs = title, group_slug, icon, slugs
            break
    group_content = {
        "growth": {
            "intro": "Create a repeatable path from audience attention to qualified business action.",
            "scope_note": "Every workstream is tied to audience intent, channel economics and measurable conversion actions.",
            "process": [("Audit", "Review the market, audience, current channels, data quality and conversion path."), ("Plan", "Define positioning, channel roles, campaign structure, budgets and success measures."), ("Execute", "Create, launch and manage the agreed campaigns, content and tracking."), ("Improve", "Review evidence, test priorities and move effort toward stronger outcomes.")],
            "best_for": ["Businesses that need more qualified enquiries", "Teams spending on marketing without clear attribution", "Brands ready for consistent multi-channel execution"],
            "tools": "GA4, Search Console, Google Ads, Meta Ads, Tag Manager and channel reporting",
        },
        "brand": {
            "intro": "Turn business strategy into a clear identity and experience customers can recognise.",
            "scope_note": "Each output contributes to one coherent brand system rather than a collection of disconnected visuals.",
            "process": [("Discover", "Understand the business, audience, market context and current perception."), ("Define", "Clarify positioning, personality, messaging and the creative direction."), ("Design", "Develop and refine the agreed identity or experience components."), ("Apply", "Prepare practical files, guidance and launch-ready applications.")],
            "best_for": ["New businesses establishing a credible identity", "Growing brands with inconsistent communication", "Teams preparing for a launch or repositioning"],
            "tools": "Figma, Adobe Creative Cloud, collaborative review and reusable brand systems",
        },
        "web": {
            "intro": "Create a fast, credible digital experience that supports discovery, trust and conversion.",
            "scope_note": "The build considers responsive behaviour, accessibility, search visibility, content control and maintainability.",
            "process": [("Discover", "Map audiences, goals, content, functionality and the most important user journeys."), ("Design", "Create the information architecture, responsive interface and conversion path."), ("Develop", "Build the frontend, backend, CMS and required integrations."), ("Launch", "Test performance, accessibility, analytics and production deployment.")],
            "best_for": ["Businesses replacing an outdated website", "Teams launching a new service or digital platform", "Organisations needing secure content and workflow control"],
            "tools": "Django, Python, WordPress, React, JavaScript, PostgreSQL and modern cloud deployment",
        },
        "software": {
            "intro": "Turn operational complexity into secure software your team can use every day.",
            "scope_note": "Workflows are mapped around roles, business rules, data ownership, integrations and measurable adoption.",
            "process": [("Map", "Document users, workflows, business rules, data and integration requirements."), ("Prototype", "Validate critical journeys and product decisions before full engineering."), ("Build", "Deliver the application in testable milestones across frontend, backend and APIs."), ("Roll out", "Migrate, test, deploy, train users and support measured adoption.")],
            "best_for": ["Teams relying on spreadsheets and repeated manual work", "Businesses needing a client, partner or staff portal", "Founders building a SaaS product or operational platform"],
            "tools": "Django, Python, React, REST APIs, PostgreSQL, cloud infrastructure and role-based access",
        },
        "mobile": {
            "intro": "Create a reliable mobile product with intuitive journeys and a maintainable backend.",
            "scope_note": "Mobile decisions cover platform behaviour, offline needs, permissions, APIs, analytics and store readiness.",
            "process": [("Define", "Clarify users, platform needs, device capabilities and release priorities."), ("Prototype", "Design and test the critical mobile journeys and interaction patterns."), ("Develop", "Build the app, backend integrations, notifications and analytics."), ("Release", "Complete device testing, store preparation, submission and post-launch support.")],
            "best_for": ["Businesses extending an existing platform to mobile", "Founders validating a mobile-first product", "Teams digitising field or customer workflows"],
            "tools": "Flutter, Android, iOS, secure APIs, push notifications and store deployment",
        },
        "cloud": {
            "intro": "Keep digital systems available, secure and supported as the business grows.",
            "scope_note": "Infrastructure work prioritises responsible access, backups, monitoring, recoverability and clear ownership.",
            "process": [("Assess", "Review the current setup, risks, performance needs and operational responsibilities."), ("Plan", "Define the hosting, security, migration, maintenance or recovery approach."), ("Implement", "Configure, migrate, harden and document the agreed infrastructure."), ("Maintain", "Monitor health, apply updates and respond through a defined support process.")],
            "best_for": ["Businesses needing dependable website ownership", "Teams preparing to migrate or scale an application", "Organisations without dedicated infrastructure support"],
            "tools": "AWS, Linux, SSL, DNS, backups, monitoring and deployment automation",
        },
        "automation": {
            "intro": "Use technology to remove repetitive work while keeping people in control of important decisions.",
            "scope_note": "Automation starts with a valuable use case, dependable data and a clear human review or escalation path.",
            "process": [("Identify", "Find repetitive work, decision delays and information gaps worth solving."), ("Design", "Map inputs, rules, integrations, exceptions and human checkpoints."), ("Automate", "Build and connect the workflow, assistant or supporting system."), ("Evaluate", "Test accuracy, adoption, controls and the next useful improvement.")],
            "best_for": ["Teams repeating data entry across multiple tools", "Businesses handling high volumes of common enquiries", "Leaders planning technology investments or AI adoption"],
            "tools": "Python, APIs, workflow automation, language models, analytics and human review controls",
        },
        "specialist": {
            "intro": "Apply focused digital capability to a clearly defined business requirement.",
            "scope_note": "The engagement is shaped around the outcome, users and constraints discovered at the start.",
            "process": [("Understand", "Clarify the requirement and current state."), ("Plan", "Agree scope, milestones and measures."), ("Deliver", "Execute the work with visible reviews."), ("Support", "Launch, document and improve where needed.")],
            "best_for": ["Businesses with a defined specialist requirement", "Teams needing an accountable delivery partner", "Projects that need practical senior guidance"],
            "tools": service.technologies or "A practical technology stack selected for the requirement",
        },
    }[category_slug]
    deliverables = [{"title": item, "description": group_content["scope_note"]} for item in service.benefit_list]
    related = Service.objects.filter(is_active=True, slug__in=category_slugs).exclude(pk=service.pk)
    related_map = {item.slug: item for item in related}
    related = [related_map[item_slug] for item_slug in category_slugs if item_slug in related_map][:3]
    service_faqs = [
        {"question": f"What is included in {service.title}?", "answer": f"The exact scope is agreed after discovery. A typical engagement covers {', '.join(item.lower() for item in service.benefit_list)} along with planning, implementation, review and launch support."},
        {"question": "How long does an engagement take?", "answer": "Timing depends on scope, integrations and approval speed. After the first discussion, The Webfix provides a clear milestone plan and delivery range before work starts."},
        {"question": "Can The Webfix work with our current team and systems?", "answer": "Yes. We can work as a focused delivery partner, collaborate with your internal team, and integrate with suitable existing tools or infrastructure."},
        {"question": "What happens after launch?", "answer": "We provide handover, documentation and an appropriate support path. Ongoing maintenance, reporting or improvement can be planned around the service and business need."},
    ]
    return render(request, "website/pages/service_detail.html", shared() | {
        "service": service, "related": related, "category_title": category_title,
        "category_slug": category_slug, "category_icon": category_icon,
        "category_intro": group_content["intro"], "deliverables": deliverables,
        "delivery_process": group_content["process"], "best_for": group_content["best_for"],
        "tools": group_content["tools"], "service_faqs": service_faqs,
    })


def portfolio(request):
    projects = list(Project.objects.filter(is_active=True))
    group_rules = [
        ("Digital Marketing & SEO", ("SEO", "Digital Marketing", "Google Ads", "Meta Ads", "Performance Marketing", "Lead Generation")),
        ("Social Media & Branding", ("Social Media", "Instagram", "Facebook", "LinkedIn", "Branding", "Brand Identity", "Content Marketing")),
        ("Software & Platforms", ("Software", "Platform", "SaaS")),
        ("Real Estate & Infrastructure", ("Real Estate", "Construction", "Infrastructure", "Engineering")),
        ("Corporate & Manufacturing", ("Corporate", "Manufacturing", "Security", "Publishing")),
        ("Consumer & Lifestyle", ("Consumer", "Travel", "Holiday", "Salon", "Beauty", "Product & Dealer")),
    ]
    counts = {}
    for project in projects:
        project.portfolio_group = "Education & Services"
        for group, keywords in group_rules:
            if any(keyword.lower() in project.category.lower() for keyword in keywords):
                project.portfolio_group = group
                break
        project.portfolio_group_slug = project.portfolio_group.lower().replace("&", "and").replace(" ", "-")
        counts[project.portfolio_group] = counts.get(project.portfolio_group, 0) + 1
    group_order = ["Digital Marketing & SEO", "Social Media & Branding", "Software & Platforms", "Real Estate & Infrastructure", "Corporate & Manufacturing", "Consumer & Lifestyle", "Education & Services"]
    featured_project = projects[0] if projects else None
    if featured_project:
        counts[featured_project.portfolio_group] -= 1
    project_groups = [{"name": group, "slug": group.lower().replace("&", "and").replace(" ", "-"), "count": counts.get(group, 0)} for group in group_order if counts.get(group, 0) > 0]
    return render(request, "website/pages/portfolio.html", shared() | {
        "projects": projects[1:] if featured_project else projects,
        "featured_project": featured_project,
        "project_groups": project_groups,
        "project_count": len(projects),
    })


def testimonials(request):
    return render(request, "website/pages/testimonials.html", shared() | {"testimonials": Testimonial.objects.filter(is_active=True)})


def blog(request):
    published = BlogPost.objects.filter(is_published=True)
    categories = list(published.values_list("category", flat=True).distinct().order_by("category"))
    query = request.GET.get("q", "").strip()
    active_category = request.GET.get("category", "").strip()
    posts = published
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query) | Q(category__icontains=query))
    if active_category:
        posts = posts.filter(category=active_category)
    featured = None if query or active_category else (published.filter(featured=True).first() or published.first())
    if featured:
        posts = posts.exclude(pk=featured.pk)
    page_obj = Paginator(posts, 9).get_page(request.GET.get("page"))
    return render(request, "website/pages/blog.html", shared() | {
        "posts": page_obj, "page_obj": page_obj, "featured": featured,
        "categories": categories, "query": query, "active_category": active_category,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related = list(BlogPost.objects.filter(is_published=True, category=post.category).exclude(pk=post.pk)[:3])
    if len(related) < 3:
        related_ids = [item.pk for item in related]
        related.extend(BlogPost.objects.filter(is_published=True).exclude(pk__in=[post.pk, *related_ids])[:3-len(related)])
    reading_minutes = max(2, (len(post.content.split()) + 199) // 200)
    return render(request, "website/pages/blog_detail.html", shared() | {
        "post": post, "related": related, "reading_minutes": reading_minutes,
    })


def faq(request):
    return render(request, "website/pages/faq.html", shared() | {"faqs": FAQ.objects.filter(is_active=True)})


def careers(request):
    page = get_object_or_404(ContentPage, page_type="careers")
    openings = CareerOpening.objects.filter(is_active=True)
    initial = {}
    requested_role = request.GET.get("role", "").strip()
    if requested_role:
        selected = openings.filter(pk=requested_role).first()
        if selected:
            initial["opening"] = selected
    form = JobApplicationForm(request.POST or None, request.FILES or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        address = request.META.get("REMOTE_ADDR", "unknown")
        email = form.cleaned_data["email"].strip().lower()
        if not cache.add(f"career-application:{address}:{email}", True, timeout=60):
            form.add_error(None, "Please wait a moment before sending another application.")
        else:
            application = form.save()
            site = shared()["site"]
            application_rows = [
                ("Candidate", application.name), ("Email", application.email),
                ("Phone", application.phone), ("Current location", application.current_location),
                ("Experience", application.experience), ("Applied role", application.opening.title),
                ("Portfolio", application.portfolio_url or "-"), ("LinkedIn", application.linkedin_url or "-"),
                ("Application note", application.cover_note),
            ]
            send_branded_email(
                f"New career application: {application.opening.title}",
                application.opening.apply_email or site.email,
                "A new candidate has applied.",
                "Review the candidate details and resume in the website administration panel.",
                application_rows, reply_to=application.email,
                action_url=f"{settings.SITE_URL}/admin/website/jobapplication/{application.pk}/change/",
                action_text="Review application",
            )
            send_branded_email(
                "Application received | The Webfix", application.email,
                f"Application received, {application.name}.",
                "Thank you for considering The Webfix. Our team will review your profile and contact you if your experience matches the next stage.",
                [("Role", application.opening.title), ("Location", application.opening.location), ("Reference", f"Application #{application.pk}")],
                action_url=f"{settings.SITE_URL}/careers/", action_text="View careers",
            )
            messages.success(request, "Application received. We will contact you if your profile matches the next stage.")
            return redirect(f"{reverse('careers')}?applied=1#application")
    return render(request, "website/pages/careers.html", shared() | {"page": page, "openings": openings, "application_form": form})

def contact(request):
    page = get_object_or_404(ContentPage, page_type="contact")
    form = InquiryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not inquiry_rate_allowed(request):
            form.add_error(None, "Please wait a moment before sending another request.")
            return render(request, "website/pages/contact.html", shared() | {"page": page, "form": form, "faqs": FAQ.objects.filter(is_active=True)[:5]})
        inquiry = form.save()
        notify_inquiry(inquiry, shared()["site"])
        messages.success(request, "Thank you. A senior consultant will contact you within one business day.")
        return redirect("contact")
    return render(request, "website/pages/contact.html", shared() | {"page": page, "form": form, "faqs": FAQ.objects.filter(is_active=True)[:5]})



def plans(request):
    return render(request, "website/pages/plans.html", shared())


def error_400(request, exception=None):
    return render(request, "website/pages/error.html", shared() | {"error_code": "400", "error_title": "We could not understand that request.", "error_message": "The request was incomplete or invalid. Please return to the previous page and try again."}, status=400)


def error_403(request, exception=None):
    return render(request, "website/pages/error.html", shared() | {"error_code": "403", "error_title": "This page is not available to you.", "error_message": "You may not have permission to view this page, or your session may have expired."}, status=403)


def error_404(request, exception=None):
    return render(request, "website/pages/error.html", shared() | {"error_code": "404", "error_title": "That page has moved or does not exist.", "error_message": "The link may be outdated. Use the options below to continue exploring The Webfix."}, status=404)


def error_500(request):
    return render(request, "website/pages/error.html", shared() | {"error_code": "500", "error_title": "Something did not load correctly.", "error_message": "Please try again shortly or contact us if your request is urgent."}, status=500)

def newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
        else:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, "You are on the list. Expect useful thinking, not noise.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


def robots(request):
    return HttpResponse("User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: " + request.build_absolute_uri("/sitemap.xml"), content_type="text/plain")


def sitemap(request):
    static_names = ["home", "about", "founder", "services", "products", "portfolio", "clients", "testimonials", "blog", "careers", "contact", "faq", "plans", "privacy", "terms", "refund", "disclaimer"]
    urls = [request.build_absolute_uri(reverse(name)) for name in static_names]
    urls += [request.build_absolute_uri(reverse("service_detail", args=[x.slug])) for x in Service.objects.filter(is_active=True)]
    urls += [request.build_absolute_uri(reverse("blog_detail", args=[x.slug])) for x in BlogPost.objects.filter(is_published=True)]
    xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>"
    return HttpResponse(xml, content_type="application/xml")