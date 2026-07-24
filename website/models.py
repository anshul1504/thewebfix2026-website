from django.db import models
from django.utils.text import slugify


class OrderedModel(models.Model):
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ("order", "id")


class SiteSettings(models.Model):
    name = models.CharField(max_length=80, default="The Webfix")
    logo_text = models.CharField(max_length=30, default="THE WEBFIX")
    logo = models.ImageField(upload_to="branding/", blank=True)
    hero_background = models.ImageField(upload_to="site/", blank=True)
    announcement = models.CharField(max_length=140, default="Independent digital studio · India / Worldwide")
    meta_title = models.CharField(max_length=70, default="The Webfix — Digital experiences built to perform")
    meta_description = models.CharField(max_length=170, default="The Webfix creates category-defining websites, campaigns and digital products that turn ambitious brands into market leaders.")
    keywords = models.CharField(max_length=255, default="digital agency, Django development, branding, SEO, performance marketing")
    canonical_url = models.URLField(blank=True)
    og_image = models.URLField(blank=True)
    hero_eyebrow = models.CharField(max_length=100, default="Strategy · Design · Technology · Growth")
    hero_title = models.CharField(max_length=180, default="We turn bold ideas into digital momentum.")
    hero_subtitle = models.TextField(default="An independent digital growth studio building memorable brands, high-performance products and campaigns engineered to compound.")
    primary_cta_text = models.CharField(max_length=40, default="Start a project")
    primary_cta_url = models.CharField(max_length=120, default="#contact")
    secondary_cta_text = models.CharField(max_length=40, default="Explore our work")
    secondary_cta_url = models.CharField(max_length=120, default="#work")
    about_eyebrow = models.CharField(max_length=70, default="Built for the ambitious")
    about_title = models.CharField(max_length=180, default="Not another agency. Your unfair digital advantage.")
    about_body = models.TextField(default="The Webfix brings senior strategy, obsessive craft and measurable growth into one focused team. We partner with businesses ready to challenge the expected—and build the systems that move them forward.")
    contact_title = models.CharField(max_length=150, default="Let’s make your next move impossible to ignore.")
    contact_body = models.TextField(default="Tell us where you want to go. We’ll bring clarity, creative firepower and a practical route to get there.")
    email = models.EmailField(default="hello@thewebfix.com")
    phone = models.CharField(max_length=40, default="+91 98765 43210")
    whatsapp_url = models.URLField(default="https://wa.me/919876543210")
    address = models.CharField(max_length=180, default="India · Partnering worldwide")
    map_embed_url = models.URLField(blank=True)
    footer_text = models.CharField(max_length=150, default="Independent thinking. Relentless execution.")
    accent_color = models.CharField(max_length=20, default="#c7ff4a")
    background_color = models.CharField(max_length=20, default="#080a09")
    font_heading = models.CharField(max_length=80, default="Manrope")
    font_body = models.CharField(max_length=80, default="Inter")
    analytics_id = models.CharField(max_length=40, blank=True)
    office_hours = models.CharField(max_length=120, default="Monday–Saturday · 10:00–19:00 IST")
    secondary_phone = models.CharField(max_length=40, default="9755838625")

    class Meta:
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            self.pk = SiteSettings.objects.first().pk
        super().save(*args, **kwargs)


class NavigationItem(OrderedModel):
    label = models.CharField(max_length=40)
    url = models.CharField(max_length=120)

    def __str__(self):
        return self.label


class Statistic(OrderedModel):
    value = models.CharField(max_length=20)
    label = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.value} {self.label}"


class Service(OrderedModel):
    number = models.CharField(max_length=5, blank=True)
    title = models.CharField(max_length=80)
    description = models.TextField()
    icon = models.CharField(max_length=40, default="asterisk", help_text="Decorative icon name")
    tags = models.CharField(max_length=180, help_text="Comma-separated capabilities")
    slug = models.SlugField(max_length=120, blank=True)
    eyebrow = models.CharField(max_length=100, default="Digital capability")
    overview = models.TextField(blank=True)
    benefits = models.TextField(blank=True, help_text="One benefit per line")
    features = models.TextField(blank=True, help_text="One feature per line")
    process = models.TextField(blank=True, help_text="One process step per line")
    technologies = models.CharField(max_length=255, blank=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=170, blank=True)
    hero_image = models.ImageField(upload_to="services/", blank=True)

    def tag_list(self):
        return [x.strip() for x in self.tags.split(",") if x.strip()]

    @property
    def benefit_list(self):
        return [x.strip() for x in self.benefits.splitlines() if x.strip()]

    @property
    def feature_list(self):
        return [x.strip() for x in self.features.splitlines() if x.strip()]

    @property
    def process_list(self):
        return [x.strip() for x in self.process.splitlines() if x.strip()]

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title


class ProcessStep(OrderedModel):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class Project(OrderedModel):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    summary = models.TextField()
    result = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True)
    project_url = models.URLField(blank=True)
    theme = models.CharField(max_length=20, default="lime", choices=[("lime", "Lime"), ("violet", "Violet"), ("orange", "Orange")])

    @property
    def display_image(self):
        return self.image.url if self.image else self.image_url

    def __str__(self):
        return self.title


class Technology(OrderedModel):
    name = models.CharField(max_length=60)
    short_code = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class Testimonial(OrderedModel):
    quote = models.TextField()
    client_name = models.CharField(max_length=80)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    website_url = models.URLField(blank=True)
    website_urls = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    rating = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f"{self.client_name} · {self.company}"

    @property
    def website_list(self):
        websites = [url.strip() for url in self.website_urls.splitlines() if url.strip()]
        return websites or ([self.website_url] if self.website_url else [])
class FAQ(OrderedModel):
    CATEGORY_CHOICES = [
        ("general", "General"), ("website", "Website Development"),
        ("seo", "SEO"), ("social", "Social Media"),
        ("software", "Software & SaaS"), ("hosting", "Hosting & Support"),
        ("commercial", "Pricing & Process"), ("policy", "Policies"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="general")
    question = models.CharField(max_length=180)
    answer = models.TextField()

    def __str__(self):
        return self.question


class SocialLink(OrderedModel):
    platform = models.CharField(max_length=40)
    url = models.URLField()

    def __str__(self):
        return self.platform


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    service = models.CharField(max_length=100)
    budget = models.CharField(max_length=80, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} · {self.service}"

class ContentPage(models.Model):
    PAGE_TYPES = [("about", "About"), ("founder", "Founder"), ("clients", "Our Clients"), ("careers", "Careers"), ("contact", "Contact"), ("privacy", "Privacy Policy"), ("terms", "Terms"), ("refund", "Refund Policy"), ("disclaimer", "Disclaimer")]
    page_type = models.CharField(max_length=30, choices=PAGE_TYPES, unique=True)
    eyebrow = models.CharField(max_length=100)
    title = models.CharField(max_length=180)
    introduction = models.TextField()
    body = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    values = models.TextField(blank=True, help_text="One item per line")
    image = models.ImageField(upload_to="pages/", blank=True)
    meta_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=170)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def value_list(self):
        return [x.strip() for x in self.values.splitlines() if x.strip()]

    def __str__(self):
        return self.get_page_type_display()


class FounderProfile(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="Founder & Managing Director")
    short_bio = models.TextField()
    biography = models.TextField()
    vision = models.TextField()
    experience = models.CharField(max_length=80)
    achievements = models.TextField(help_text="One achievement per line")
    message = models.TextField()
    portrait = models.ImageField(upload_to="founder/", blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    @property
    def achievement_list(self):
        return [x.strip() for x in self.achievements.splitlines() if x.strip()]

    def __str__(self):
        return self.name


class Client(OrderedModel):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=80)
    logo = models.ImageField(upload_to="clients/", blank=True)
    logo_text = models.CharField(max_length=12, blank=True)
    result = models.CharField(max_length=140, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField()
    content = models.TextField()
    category = models.CharField(max_length=80)
    author = models.CharField(max_length=100, default="The Webfix Editorial")
    featured_image = models.ImageField(upload_to="blog/", blank=True)
    image_alt = models.CharField(max_length=180, blank=True)
    meta_title = models.CharField(max_length=70)
    meta_description = models.CharField(max_length=170)
    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ("-published_at",)

    @property
    def article_sections(self):
        sections = []
        for block in [item.strip() for item in self.content.split("\n\n") if item.strip()]:
            if block == self.excerpt.strip():
                continue
            if block.startswith("## "):
                heading = block[3:].strip()
                sections.append({"heading": heading, "slug": slugify(heading), "paragraphs": []})
                continue
            if not sections:
                sections.append({"heading": "Overview", "slug": "overview", "paragraphs": []})
            sections[-1]["paragraphs"].append(block)
        return sections

    def __str__(self):
        return self.title


class CareerOpening(OrderedModel):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Remote / India")
    employment_type = models.CharField(max_length=50, default="Full-time")
    description = models.TextField()
    apply_email = models.EmailField(default="info@thewebfix.in")

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewing", "Reviewing"),
        ("shortlisted", "Shortlisted"),
        ("interview", "Interview"),
        ("rejected", "Not selected"),
        ("hired", "Hired"),
    ]
    opening = models.ForeignKey(CareerOpening, on_delete=models.PROTECT, related_name="applications")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    current_location = models.CharField(max_length=120)
    experience = models.CharField(max_length=80)
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    cover_note = models.TextField()
    resume = models.FileField(upload_to="careers/resumes/%Y/%m/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} - {self.opening.title}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Brochure(models.Model):
    title = models.CharField(max_length=100, default="The Webfix Company Profile")
    file = models.FileField(upload_to="brochures/")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Product(OrderedModel):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    features = models.TextField(help_text="One feature per line")
    image = models.ImageField(upload_to="products/", blank=True)
    image_alt = models.CharField(max_length=180)
    cta_text = models.CharField(max_length=50, default="Explore solution")
    cta_url = models.CharField(max_length=180, default="/contact/")

    @property
    def feature_list(self):
        return [item.strip() for item in self.features.splitlines() if item.strip()]

    def __str__(self):
        return self.title