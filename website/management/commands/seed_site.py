from django.core.management.base import BaseCommand
from website.models import (
    FAQ, NavigationItem, ProcessStep, Project, Service, SiteSettings,
    SocialLink, Statistic, Technology, Testimonial,
)


class Command(BaseCommand):
    help = "Seed the CMS with premium launch-ready agency content."

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create()
        datasets = [
            (NavigationItem, [
                {"label": "About", "url": "#about"}, {"label": "Services", "url": "#services"},
                {"label": "Work", "url": "#work"}, {"label": "Process", "url": "#process"},
            ]),
            (Statistic, [
                {"value": "5+", "label": "Years Experience"},
                {"value": "100+", "label": "Projects Completed"},
                {"value": "4.9/5", "label": "Google Rating"},
                {"value": "40+", "label": "Business Services"},
            ]),
            (Service, [
                {"number": "01", "title": "Digital Flagships", "description": "Category-defining websites built around a clear story, frictionless experience and commercial intent.", "tags": "Strategy, UX/UI, Web development, Django"},
                {"number": "02", "title": "Products & Platforms", "description": "Resilient Django products, mobile apps, portals and operational systems engineered for real-world scale.", "tags": "Django, Mobile apps, ERP, CRM"},
                {"number": "03", "title": "Brand Systems", "description": "Distinctive identities and flexible design systems that make every brand interaction feel unmistakably yours.", "tags": "Positioning, Identity, Graphic design, Guidelines"},
                {"number": "04", "title": "Demand & Growth", "description": "Integrated search, social and paid media programmes designed to create demand and compound performance.", "tags": "SEO, Google Ads, Meta Ads, Social"},
            ]),
            (ProcessStep, [
                {"title": "Discover", "description": "Align on ambition, audience and the business problem worth solving."},
                {"title": "Research", "description": "Find the cultural, customer and category truths that create an edge."},
                {"title": "Design", "description": "Shape the story, system and interactions that make people care."},
                {"title": "Develop", "description": "Engineer a fast, resilient product with considered details throughout."},
                {"title": "Launch", "description": "Deploy confidently with quality assurance, analytics and a clear go-to-market."},
                {"title": "Grow", "description": "Learn from real behaviour and compound performance through focused iteration."},
            ]),
            (Project, [
                {"title": "Arc Capital", "category": "Brand · Product · Engineering", "summary": "Turning complex investing into a remarkably clear experience.", "result": "+214% funded accounts", "theme": "lime"},
                {"title": "Serein House", "category": "Hospitality · Commerce", "summary": "A sensorial digital home for slow, considered travel.", "result": "3.6× direct bookings", "theme": "violet"},
                {"title": "Kinetic Labs", "category": "AI · Product launch", "summary": "Making frontier intelligence feel useful, human and ready.", "result": "12k waitlist signups", "theme": "orange"},
            ]),
            (Technology, [
                {"name": "Python", "short_code": "Py"}, {"name": "Django", "short_code": "Dj"},
                {"name": "React", "short_code": "Re"}, {"name": "Flutter", "short_code": "Fl"},
                {"name": "PostgreSQL", "short_code": "Pg"}, {"name": "AWS", "short_code": "AW"},
                {"name": "Docker", "short_code": "Do"}, {"name": "JavaScript", "short_code": "JS"},
                {"name": "Bootstrap", "short_code": "B5"},
            ]),
            (Testimonial, [
                {"quote": "The Webfix didn’t simply redesign our platform. They changed how we think about the business—and the numbers followed.", "client_name": "Aarav Mehta", "role": "Founder", "company": "Northstar Ventures"},
                {"quote": "Rare strategic clarity, extraordinary craft and a team that genuinely behaves like an extension of ours.", "client_name": "Mira Kapoor", "role": "Chief Growth Officer", "company": "Serein House"},
            ]),
            (FAQ, [
                {"question": "What kind of projects are the best fit?", "answer": "We do our best work with ambitious teams facing a meaningful brand, product or growth challenge. That could be a new market entry, a digital flagship, a complex platform or a performance programme ready to scale."},
                {"question": "How quickly can we launch?", "answer": "A focused brand and website engagement typically takes 8–14 weeks. Larger products are shaped into high-value releases so momentum arrives early without compromising the long-term system."},
                {"question": "Do you work with teams outside India?", "answer": "Yes. Our operating rhythm is designed for thoughtful remote collaboration, and we partner with founders and marketing teams across time zones."},
                {"question": "What happens after launch?", "answer": "We can remain your growth and optimisation partner—using analytics, customer behaviour and campaign performance to decide what should improve next."},
            ]),
            (SocialLink, [
                {"platform": "LinkedIn", "url": "https://www.linkedin.com/"},
                {"platform": "Instagram", "url": "https://www.instagram.com/"},
                {"platform": "Behance", "url": "https://www.behance.net/"},
            ]),
        ]
        for model, rows in datasets:
            if model.objects.exists():
                continue
            for order, row in enumerate(rows, 1):
                model.objects.create(order=order, **row)
        self.stdout.write(self.style.SUCCESS("The Webfix CMS content is ready."))
