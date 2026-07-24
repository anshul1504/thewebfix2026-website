from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from website.faq_content import FAQ_CONTENT
from website.models import BlogPost, Brochure, CareerOpening, Client, ContentPage, FounderProfile, FAQ, Product, Project, Service, SiteSettings, SocialLink, Testimonial

SERVICE_GROUPS = {
"Growth": ["Digital Marketing","Social Media Management","SEO","Local SEO","Technical SEO","Google Ads","Meta Ads","Performance Marketing","Email Marketing","WhatsApp Marketing","Content Marketing","Influencer Marketing","Instagram Marketing","Facebook Marketing","LinkedIn Marketing"],
"Brand & Experience": ["Brand Strategy","Brand Identity","Graphic Design","UI UX Design","Logo Design"],
"Web": ["Website Development","Corporate Website","Business Website","Landing Page","WordPress Development","Django Development","Python Development","Web Application Development","Website Design","React Development"],
"Platforms": ["ERP Development","CRM Development","SaaS Development","Custom Software Development","API Development","API Integration"],
"Mobile": ["Android App Development","iOS App Development","Flutter Development"],
"Infrastructure": ["Cloud Hosting","AWS Deployment","Server Management","Website Maintenance","Cyber Security","Domain & Hosting"],
"Intelligence": ["AI Automation","Chatbot Development","Business Automation","IT Consulting"],
}
GROUP_COPY = {
"Growth":"A measurable growth capability connecting audience insight, persuasive creative, channel execution and continuous commercial optimisation.",
"Brand & Experience":"A distinctive brand and experience capability that turns strategic clarity into memorable, consistent customer interactions.",
"Web":"A fast, accessible and conversion-focused digital experience engineered for credibility, editorial control and long-term performance.",
"Platforms":"A secure, scalable business platform shaped around real workflows, clear data and maintainable product architecture.",
"Mobile":"A polished mobile product combining intuitive interaction, reliable integration and production-grade engineering.",
"Infrastructure":"Dependable digital infrastructure designed around security, availability, observability and responsible operational control.",
"Intelligence":"Practical technology guidance and automation that removes repetitive work, improves decisions and keeps people in control.",
}
BLOGS = [
("SEO in 2026: Building Visibility Beyond Ten Blue Links","SEO","Search visibility now spans AI answers, maps, video and traditional results. A resilient strategy must optimise the whole discovery journey."),
("Why Your Google Rankings Stalled - and What to Fix First","Google Ranking","A diagnosis framework for separating technical constraints, weak intent alignment and authority gaps."),
("A Digital Marketing System for Predictable Business Growth","Digital Marketing","Connect positioning, content, media, conversion and retention into one accountable growth engine."),
("What Makes a High-Performance Business Website","Website Development","The essential decisions behind fast, credible websites that convert attention into qualified opportunity."),
("Where AI Automation Creates Real Business Value","AI","A grounded framework for choosing AI workflows that save time without creating uncontrolled operational risk."),
("The Business Growth Metrics Leadership Should Watch","Business Growth","Move beyond dashboard volume and focus on indicators that explain acquisition quality, conversion and retention."),
("Branding That Builds Commercial Preference","Branding","How distinctive strategy and consistent expression reduce price sensitivity and improve marketing efficiency."),
("A Social Media Strategy Built for Relevance, Not Noise","Social Media","A practical editorial model for building a useful social presence without chasing every platform trend."),
("Performance Marketing Without the Short-Term Trap","Performance Marketing","Balance immediate acquisition with creative learning, brand demand and sustainable unit economics."),
("Google Ads: A Better Structure for High-Intent Growth","Google Ads","Campaign architecture, landing-page alignment and measurement principles for accountable paid search."),
("Email Marketing as a Customer Experience","Email Marketing","Design lifecycle communication around customer needs to improve activation, retention and repeat revenue."),
("WordPress or Django: Choosing the Right Foundation","WordPress","A decision guide based on publishing needs, workflow complexity, integrations, security and ownership."),
("Django Architecture for Products Built to Last","Django","Principles for modular domains, secure defaults, efficient queries and maintainable product delivery."),
("Python Automation: From Repetitive Work to Reliable Workflow","Python","How to identify, design and govern automation that saves meaningful time across business operations."),
("CRM Design Around the Way Your Team Actually Sells","CRM","Why adoption improves when pipeline stages, information design and automation reflect real sales behaviour."),
("ERP Implementation: Reduce Risk Before Writing Code","ERP","A phased approach to process discovery, data ownership and adoption for operational transformation."),
("Designing Web Applications People Can Understand","Web Applications","Interaction principles for reducing complexity in dashboards, workflows and data-heavy products."),
("Case Study: Turning Website Friction Into Qualified Demand","Case Studies","How message clarity, experience design and technical speed can improve lead quality."),
("Local SEO for Multi-Location Businesses","Local SEO","A scalable operating model for location pages, Google Business Profiles, reviews and local authority."),
("Building Brand and Demand Together","Business Growth","Why brand investment and activation perform better as one connected commercial system."),
("How Much Does a Professional Website Cost in India?","Website Cost","A practical breakdown of strategy, design, development, content and maintenance costs for Indian businesses."),
("Lead Generation for Indian B2B Companies","Lead Generation","Build a dependable qualified pipeline by connecting market focus, useful content, paid media and sales follow-up."),
("Website Security Essentials for Growing Businesses","Website Security","The practical controls Indian businesses need to protect customer trust, operational continuity and valuable data."),
("Core Web Vitals: Performance That Improves Conversion","Performance","Why loading speed, interaction responsiveness and layout stability matter to revenue as well as search visibility."),
("Cloud Strategy for Scaling Indian Companies","Cloud","How to choose secure, observable and cost-conscious cloud infrastructure without creating unnecessary complexity."),]
TESTIMONIALS = [
    ("Naman Kansal", "Agrasen Plywood", "https://agrasenplywood.com/", "The team understood our product range and dealer-focused business quickly. The website is clear, professional and much easier for customers to explore."),
    ("Anay Kumar Pathak", "APICON", "https://apicon.in/", "The Webfix translated our real-estate vision into a credible digital presence. Communication stayed direct and the final website represents our projects confidently."),
    ("Lav Kumar Goyal", "Greenland H.S. School", "https://greenlandhsschool.in/", "Parents can now find important school information without confusion. The website feels organised, accessible and aligned with the trust our institution has built."),
    ("Rahul Jogi", "Krishna Law Firm", "https://krishnalawfirm.com/", "Our legal practice needed a restrained and trustworthy online presence. The Webfix delivered that balance with clear content and a professional experience."),
    ("Rashi Yadav", "Magical Scissor", "https://magicalscissor.in/", "They captured our salon's personality while keeping services easy to discover. The result feels polished, modern and genuinely connected to our brand."),
    ("Lucky Mehta", "Mehta Construction", "https://mehtaconstruction.com/", "The new website presents our construction capabilities with much more clarity. The process was structured, responsive and comfortable from start to launch."),
    ("Ankit Bhagore", "MP Visit", "https://mpvisit.in/", "The Webfix made a large amount of travel information feel simple to browse. The website gives visitors a much clearer path to discover Madhya Pradesh."),
    ("Rahul Jogi", "Nagas Security", "https://nagassecurity.com/", "Trust and service clarity were essential for our security business. The team built a strong, straightforward website that communicates both effectively."),
    ("Tanishq Agrawal", "Naveen Products", "https://naveenproducts.com/", "Our product portfolio is now presented in a clean and credible way. The Webfix understood our manufacturing business and kept the entire delivery practical."),
    ("Sharukh Malwa", "Richkid", "https://richkid.in/", "The website finally reflects the energy and premium direction of Richkid. The team handled brand presentation, shopping flow and mobile experience with real care."),
    ("Sunil Malviya", "RNT Plus Foundation", "https://rntplusfoundation.org/", "The team gave our initiatives a clear and respectful digital home. Visitors can understand our work, values and social impact much more easily now."),
    ("Sunil Malviya", "RNT Group", "https://rntgroup.co.in/", "The Webfix brought our different business strengths together in one coherent corporate presence. The result feels dependable and built for long-term use."),
    ("Sunil Malviya", "RNT MPL", "https://rntmpl.com/", "From structure to final presentation, the team kept the project focused and professional. Our capabilities are now much easier for clients to understand."),
    ("Shailendra Patel", "Bricks & Roots Buildspace", "https://bricksrootsbuildspace.com/", "Our properties needed strong visual presentation without losing practical information. The Webfix achieved both and made the experience work smoothly across devices."),
    ("Rahul Sharma", "RK Interior Architect", "https://rkinteriorarchitect.com/", "The website lets our work speak visually while keeping project details easy to navigate. It feels refined and appropriate for an architecture and interiors practice."),
    ("Sunil Malviya", "RNT Infratech", "https://rntinfratech.com/", "The new digital presence communicates our infrastructure experience with clarity and confidence. The team was responsive and disciplined throughout the engagement."),
    ("Raunak Rawat", "Shankh Soap", "https://shankhsoap.com/", "The Webfix turned our product story into a fresh, credible website. Customers can understand the brand and range without unnecessary complexity."),
    ("Sumit Agrawal", "Vatsalya Builder", "https://vatsalyabuilder.in/", "Our projects now have a professional platform that supports customer enquiries and sales conversations. The delivery was clear and thoughtfully managed."),
    ("Pankaj Mittal", "Siddhi Construction", "https://siddhiconstruction.in/", "The website has strengthened how we present our projects and experience. It is clean, easy to use and gives prospective clients the right information quickly."),
    ("Paramjeet Jaat", "Swastik Publications", "https://swastikpublicationspvtltd.in/", "Managing a broad publication catalogue online needed careful organisation. The Webfix created a structure that is simple for readers and practical for our team."),
    ("Manoj Tiwari", "Vinayaka Finserv", "https://vinayakafinserv.com/", "Financial services demand clarity and trust. The team delivered a professional website that explains our offering simply and supports confident customer conversations."),
    ("Naman Kansal", "Tridevi Realty", "https://tridevirealty.in/", "The Webfix gave our real-estate business a sharp and credible digital identity. Property information is easier to explore and the overall experience feels premium."),
    ("Navin Soni", "Prosperity Partner", "https://prosperitypartner.in/", "The team organised our financial offering into a clear and trustworthy experience that clients can understand without unnecessary complexity."),
    ("Navin Soni", "Fruitee Delights", "https://fruitedelights.com/", "Our consumer brand now has a fresh digital presence that makes the product range easy to explore and feels consistent across devices."),
    ("Uzma Ji", "Revolutions Beauty", "https://revolutionsbeauty.in/", "The website presents our beauty services with the right balance of personality, polish and practical information for customers."),
    ("Reetika Chauhan", "Dope Mean", "https://dopemean.in/", "The Webfix understood the brand direction and turned it into a confident online experience with a clean, contemporary presentation."),
    ("Lavesh Soni", "Shree Rudra Bullion", "https://shreerudrabullion.com/", "Accuracy, trust and easy access to information were central to this project. The team delivered a professional platform built around those priorities."),
]
PAGES = {
"about":("Inside The Webfix","A small senior team for consequential digital work.","The Webfix removes the distance between strategy and execution. Brand thinkers, designers, engineers and growth specialists work around one commercial problem and stay accountable through launch and learning."),
"founder":("Leadership","The perspective behind The Webfix.","A founder-led company built on the belief that technology should make business clearer, more capable and more human."),
"clients":("Trusted partnerships","Built with ambitious teams.","We work with founders and leaders who value clear thinking, exceptional craft and accountable delivery."),
"careers":("Join the orbit","Do the best work of your career.","Join a focused team where ideas are expected, craft is respected and every person can influence the outcome."),
"contact":("Start something meaningful","Tell us what needs to change.","Share the ambition, challenge and timing. A senior consultant will respond with useful next steps within one business day."),
"privacy":("Legal","Privacy Policy","How The Webfix collects, uses, stores and protects personal information shared through our website, enquiries and services."),
"terms":("Legal","Terms and Conditions","The terms that apply when you use our website, request a proposal or engage The Webfix for digital, website or software services."),
"refund":("Legal","Cancellation and Refund Policy","A clear explanation of project cancellations, non-refundable work, recurring services and how eligible refund requests are reviewed."),
"disclaimer":("Legal","Disclaimer","Important context for information and performance statements published by The Webfix."),
}
LEGAL = "Information submitted through this website is used to respond to requests, provide agreed services and operate the website securely. We do not sell personal information. Access is limited to authorised people and necessary service providers.\n\nProfessional services are governed by a written agreement defining scope, responsibilities, fees, intellectual property and any applicable cancellation or refund terms. Published articles are educational and do not guarantee commercial outcomes.\n\nQuestions, access requests or formal notices may be sent to info@thewebfix.in. We review valid requests promptly and act in accordance with applicable law."

class Command(BaseCommand):
    def handle(self,*args,**options):
        site=SiteSettings.objects.first() or SiteSettings.objects.create()
        site.logo="branding/the-webfix-logo.jpg"; site.email="info@thewebfix.in"; site.phone="9993098691"; site.secondary_phone="9755838625"; site.whatsapp_url="https://wa.me/919977221149?text=Hello%20The%20Webfix%2C%20I%20would%20like%20to%20discuss%20a%20project."; site.accent_color="#D4AF37"; site.background_color="#080705"; site.hero_background="site/agency-team.webp"; site.address="195/6 Ram Nagar, Near Sayaji Hotel, Indore, Madhya Pradesh 452011"; site.map_embed_url="https://www.google.com/maps?q=The%20Webfix%2C%20195%2F6%20Ram%20Nagar%2C%20Near%20Sayaji%20Hotel%2C%20Indore&output=embed"; site.meta_title="The Webfix | Digital Marketing & Website Development Company Indore"; site.meta_description="The Webfix is a premium digital marketing, SEO, website development and software company in Indore serving ambitious businesses across India."; site.keywords="Digital Marketing Agency Indore, Website Development Company Indore, SEO Company Indore, Best Web Development Company, Django Development Company, Digital Marketing Services India, ERP Development, CRM Development, Software Development Company, Website Design India, Google Ads Agency, Meta Ads Agency, Technical SEO Services"; site.save()
        for kind,(eyebrow,title,intro) in PAGES.items():
            body=LEGAL if kind in {"privacy","terms","refund","disclaimer"} else "We partner closely, communicate directly and make decisions with evidence. Senior people remain close to the work, combining independent thinking with the discipline required to deliver dependable outcomes."
            ContentPage.objects.update_or_create(page_type=kind,defaults={"eyebrow":eyebrow,"title":title,"introduction":intro,"body":body,"mission":"Make world-class digital capability accessible to ambitious businesses ready to lead.","vision":"Build a respected independent company whose work creates enduring value.","values":"Clarity over theatre\nCraft with consequence\nProgress through partnership\nCuriosity with discipline","meta_title":f"{title} | The Webfix"[:70],"meta_description":intro[:170]})
        FounderProfile.objects.update_or_create(name="Anshul Agrawal",defaults={"role":"Founder & Managing Director","short_bio":"Founder of The Webfix, building practical digital solutions that help ambitious businesses become clearer, more capable and ready to grow.","biography":"Anshul founded The Webfix with a straightforward belief: a business should not need separate partners to connect strategy, design, technology and growth. The company was built to bring those disciplines together under one accountable team.\n\nHe remains closely involved in discovery, solution planning and delivery standards, helping the team turn complex requirements into clear, useful digital systems.","vision":"Build an Indian digital company known for honest guidance, dependable execution and technology that creates lasting business value.","experience":"5+ years building digital solutions","achievements":"Built an integrated digital and technology practice\nLed the delivery of 100+ business projects\nCreated long-term partnerships across diverse industries\nKept strategy and senior decision-making close to every engagement","message":"Good digital work should make the next business decision clearer, the customer experience simpler and the team more confident about growth.","portrait":"founder/anshul-agrawal-portrait.webp"})
        order=0
        for group,titles in SERVICE_GROUPS.items():
            for title in titles:
                order+=1; description=GROUP_COPY[group]
                defaults={"title":title,"description":description,"overview":f"Our {title.lower()} practice brings senior {group.lower()} thinking and precise execution together around your commercial priorities.","number":f"{order:02d}","eyebrow":group,"benefits":"Sharper strategic focus\nHigher-quality customer action\nA scalable foundation for growth","features":"Senior discovery and direction\nPurpose-built execution\nMeasurement and optimisation","process":"Discover the real constraint\nDefine the strategic system\nDesign and deliver with precision\nLaunch, learn and compound","technologies":"Django · Python · JavaScript · PostgreSQL · AWS","tags":group,"meta_title":f"{title} Services | The Webfix"[:70],"meta_description":description[:170],"order":order,"is_active":True,"icon":"orbit"}
                Service.objects.update_or_create(slug=slugify(title),defaults=defaults)
        featured_projects = [
            ("APICON Real Infra", "Infrastructure & Engineering Website", "A comprehensive corporate website presenting bridge engineering expertise, landmark projects, services and achievements.", "100+ projects showcased", "projects/apicon.webp", "http://apicon.in/", "lime"),
            ("Richkid", "Consumer Brand Website", "A modern consumer-facing website created to communicate the brand, products and customer experience.", "Modern brand presence", "projects/richkid.webp", "http://richkid.in/", "lime"),
            ("Life Holiday", "Travel & Holiday Website", "A customer-friendly travel website designed to present holiday packages, destinations and enquiry options clearly.", "Travel enquiries simplified", "projects/life-holiday.webp", "https://lifeholiday.in/", "orange"),
            ("Greenland H.S. School", "Education Website", "A clear school website connecting parents and students with academics, admissions and institutional information.", "School information online", "projects/greenland-school.webp", "http://greenlandhsschool.in/", "lime"),
            ("Krishna Law Firm", "Legal Services Website", "A trust-focused legal website presenting experience, practice areas, attorneys and consultation access.", "Legal expertise made clear", "projects/krishna-law-firm.webp", "https://krishnalawfirm.com/", "violet"),
            ("RNT MPL", "Corporate Website", "A responsive corporate website designed to communicate company capabilities and business value clearly.", "Clear corporate presence", "projects/rnt-mpl.webp", "http://rntmpl.com/", "orange"),
        ]
        for i, (title, category, summary, result, image, url, theme) in enumerate(featured_projects, 1):
            Project.objects.update_or_create(title=title, defaults={"category": category, "summary": summary, "result": result, "image": image, "project_url": url, "theme": theme, "order": i, "is_active": True})
        featured_service_copy = {
            "digital-marketing": "Connect strategy, creative and campaigns to generate qualified demand and measurable business growth.",
            "seo": "Improve search visibility, technical health and high-intent organic traffic with a focused SEO programme.",
            "social-media-management": "Build a consistent social presence with useful content, community management and performance insight.",
            "website-development": "Launch a fast, mobile-first business website designed for credibility, enquiries and easy content management.",
            "django-development": "Build secure, scalable web applications and portals around your real workflows, integrations and data.",
            "erp-development": "Connect finance, inventory, sales and operations in practical software shaped around how your team works.",
        }
        for slug, description in featured_service_copy.items():
            Service.objects.filter(slug=slug).update(description=description, meta_description=description)
        clients=[("Northstar Ventures","Financial Services","NV","214% growth in funded accounts"),("Serein House","Hospitality","SH","3.6× growth in direct bookings"),("Kinetic Labs","Technology","KL","12,000 qualified launch signups"),("Aster Health","Healthcare","AH","48% faster patient onboarding"),("ForgeWorks","Manufacturing","FW","31% shorter sales cycle"),("Morrow Retail","Commerce","MR","2.4× digital conversion rate"),("Prism Learning","Education","PL","68% growth in completion"),("Terra Foods","Consumer","TF","New category launched nationally")]
        for i,(name,industry,mark,result) in enumerate(clients,1): Client.objects.update_or_create(name=name,defaults={"industry":industry,"logo_text":mark,"result":result,"order":i,"is_active":True})
        grouped_testimonials = {}
        for name, company, website, quote in TESTIMONIALS:
            item = grouped_testimonials.setdefault(name, {"companies": [], "websites": [], "quote": quote})
            if company not in item["companies"]:
                item["companies"].append(company)
            if website not in item["websites"]:
                item["websites"].append(website)

        Testimonial.objects.exclude(client_name__in=grouped_testimonials.keys()).delete()
        for i, (name, item) in enumerate(grouped_testimonials.items(), 1):
            matches = Testimonial.objects.filter(client_name=name).order_by("pk")
            testimonial = matches.first() or Testimonial(client_name=name)
            if testimonial.pk:
                matches.exclude(pk=testimonial.pk).delete()
            testimonial.company = item["companies"][0] if len(item["companies"]) == 1 else f"{len(item['companies'])} client brands"
            testimonial.quote = item["quote"]
            testimonial.role = "Client Partner"
            testimonial.website_url = item["websites"][0]
            testimonial.website_urls = "\n".join(item["websites"])
            testimonial.rating = 5
            testimonial.order = i
            testimonial.is_active = True
            testimonial.save()
        desired_faqs = []
        for faq_order, (category, question, answer) in enumerate(FAQ_CONTENT, 1):
            desired_faqs.append(question)
            FAQ.objects.update_or_create(question=question, defaults={"answer": answer, "category": category, "order": faq_order, "is_active": True})
        FAQ.objects.exclude(question__in=desired_faqs).update(is_active=False)
        CareerOpening.objects.update_or_create(title="Senior Django Engineer",defaults={"location":"Remote / India","employment_type":"Full-time","description":"Own robust Django products from domain modelling through deployment, collaborating closely with design and strategy.","order":1,"is_active":True})
        CareerOpening.objects.update_or_create(title="Product UI/UX Designer",defaults={"location":"Indore / Hybrid","employment_type":"Full-time","description":"Turn complex challenges into clear systems, polished interfaces and meaningful motion.","order":2,"is_active":True})
        now=timezone.now()
        for i,(title,category,excerpt) in enumerate(BLOGS):
            content=f"{excerpt}\n\n## Start with the business decision\n\nEffective {category.lower()} work begins with a precise business question, a defined audience and evidence about the current constraint. Before adding campaigns, pages or tools, identify where customer confidence, operational quality or conversion is being lost. A useful first deliverable is a shared diagnosis and a small set of measurable priorities.\n\n## Build for the complete customer journey\n\nStrategy must connect to the details people actually experience: the search result, message, landing page, follow-up and service delivery. Make those moments coherent, remove avoidable friction and ensure each step helps the customer make a confident decision.\n\n## Measure outcomes, not activity\n\nChoose metrics that reveal business movement. Depending on the goal, that may include qualified enquiries, conversion rate, acquisition cost, sales-cycle time, retention or hours saved. Channel volume is useful context, but it should not be mistaken for commercial progress.\n\n## Create a focused execution rhythm\n\nAssign clear ownership, protect technical and creative quality, and review quantitative behaviour alongside customer and sales feedback. Test materially different ideas, record what each test teaches and improve the underlying system rather than chasing isolated wins.\n\n## What Indian businesses should prioritise\n\nFor a growing business, consistency matters more than an oversized plan. Begin with the highest-value customer journey, make ownership explicit and improve it every month. This keeps investment practical while building capability that can scale.\n\n## Common mistakes to avoid\n\nDo not begin with a long list of tactics, copy a competitor without context or report success through impressions alone. Avoid changing several variables at once, because the team will not know what produced the result. Most importantly, do not leave follow-up and ownership undefined after launch.\n\n## A practical 90-day plan\n\nIn the first 30 days, audit the current journey and agree on one commercial outcome. During days 31 to 60, improve the highest-impact experience and put reliable measurement in place. Use days 61 to 90 to review real behaviour, resolve friction and decide what deserves further investment.\n\n## The Webfix perspective\n\nAt The Webfix in Indore, we connect strategy, design, technology and growth around one commercial problem. That integrated view helps {category.lower()} become a dependable business asset instead of another disconnected activity."
            BlogPost.objects.update_or_create(slug=slugify(title),defaults={"title":title,"category":category,"excerpt":excerpt,"content":content,"author":"The Webfix Editorial Team","image_alt":f"The Webfix insight: {title}","meta_title":f"{title} | The Webfix"[:70],"meta_description":f"{excerpt} Practical guidance from The Webfix, Indore."[:170],"published_at":now-timedelta(days=i*9),"is_published":True,"featured":i==0})
        BlogPost.objects.filter(slug="why-your-google-rankings-stalledand-what-to-fix-first").delete()
        desired_slugs = [slugify(title) for titles in SERVICE_GROUPS.values() for title in titles]
        Service.objects.exclude(slug__in=desired_slugs).update(is_active=False)
        Brochure.objects.update_or_create(title="The Webfix Company Profile", defaults={"file":"brochures/the-webfix-company-profile.pdf", "is_active":True})
        SocialLink.objects.update_or_create(platform="Instagram", defaults={"url":"https://www.instagram.com/","order":1,"is_active":True})
        SocialLink.objects.update_or_create(platform="LinkedIn", defaults={"url":"https://www.linkedin.com/","order":2,"is_active":True})
        SocialLink.objects.update_or_create(platform="WhatsApp", defaults={"url":"https://wa.me/919977221149?text=Hello%20The%20Webfix%2C%20I%20would%20like%20to%20discuss%20a%20project.","order":3,"is_active":True})
        SocialLink.objects.update_or_create(platform="YouTube", defaults={"url":"https://www.youtube.com/@thewebfix","order":4,"is_active":True})
        SocialLink.objects.exclude(platform__in=["Instagram","LinkedIn","WhatsApp","YouTube"]).update(is_active=False)
        products = [
            ("Business Websites","Conversion-focused company websites built for credibility and qualified enquiries."),("Ecommerce Solutions","Scalable commerce experiences connecting discovery, checkout and operations."),("ERP Systems","Connected finance, inventory, procurement and operational control."),("CRM Solutions","Practical customer pipelines that improve sales visibility and follow-up."),("School ERP","Admissions, fees, attendance, learning and parent communication in one system."),("Hospital Management","Secure patient, appointment, billing and clinical operations workflows."),("Restaurant POS","Fast ordering, kitchen, billing and inventory for modern food businesses."),("Inventory Software","Real-time stock visibility, purchasing and movement across locations."),("Billing Software","Reliable invoicing, payments, tax records and business reporting."),("Mobile Apps","Polished Android, iOS and Flutter products built around real customer needs."),("Web Applications","Purpose-built platforms that simplify complex business workflows."),("AI Chatbots","Context-aware support and qualification connected to business knowledge."),("Business Automation","Integrated workflows that remove repetition and reduce operational errors.")]
        for index,(title,description) in enumerate(products,1):
            Product.objects.update_or_create(slug=slugify(title),defaults={"title":title,"description":description,"features":"Strategic discovery\nCustom experience design\nSecure scalable engineering\nAnalytics and ongoing support","image":"site/product-studio.webp" if index%2 else "site/business-consultation.webp","image_alt":f"The Webfix {title.lower()} solution for Indian businesses","cta_text":"Discuss this solution","cta_url":"/contact/","order":index,"is_active":True})
        self.stdout.write(self.style.SUCCESS(f"Seeded {order} services, {len(products)} products and {len(BLOGS)} professional articles."))