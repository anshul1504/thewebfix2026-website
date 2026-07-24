# The Webfix — Product & Experience Architecture

## 1. Existing Project Audit

### What is working
- Django 6 project with clear `webfix` configuration and a focused `website` application.
- Existing homepage renders from CMS data and already includes inquiry capture, services, projects, statistics, process, testimonials, FAQs, technologies and social links.
- Reusable ordered model pattern supports editorial ordering and visibility.
- WhiteNoise static delivery, PostgreSQL-compatible environment configuration, media storage, CSRF protection, secure production settings, robots and XML sitemap are present.
- Frontend already uses GSAP, ScrollTrigger, Lenis, Three.js and Swiper with reduced-motion handling.
- Existing database content and public inquiry workflow must remain intact.

### Technical weaknesses discovered
- Homepage is monolithic instead of extending a shared base, so global navigation/footer/SEO can drift between pages.
- Static hardcoded fallback content conflicts with the requirement that every visible item be editable.
- Content page body fields are unstructured text; future iteration needs reusable page sections or tightly defined page-specific models.
- Service slugs need deterministic generation and uniqueness validation before production.
- Home canonical expression and schema need a central SEO resolver.
- Sitemap is hand-built and should include all indexable content with modification dates.
- Newsletter needs validation, consent language and rate-limiting; inquiry endpoint needs spam protection.
- Several strings show encoding corruption from an earlier Windows write path and must be normalized to UTF-8.
- CDN libraries are render-safe because they are deferred, but self-hosting/version pinning and a bundled production asset pipeline are preferable.
- No cache policy, image rendition system, analytics dashboard aggregation, media library, role-specific admin grouping or 404 template yet.
- No automated test suite currently covers every route, canonical metadata, form persistence and sitemap completeness.

### UI/UX weaknesses
- Current lime visual identity conflicts with the requested electric-blue/purple/cyan direction.
- Homepage visual language is strong but repeated card/grid patterns reduce section individuality.
- The hero has a dashboard scene but lacks a meaningful interactive globe, phone/laptop relationship and deeper narrative progression.
- Navigation is desktop-led; mobile menu button has no complete overlay interaction.
- Inner-page hierarchy, breadcrumbs and contextual conversion paths did not exist.
- Portfolio items lack dedicated case-study narrative, challenge/solution/results modules and media sequencing.
- Accessibility requires visible focus states, skip navigation, dialog semantics for mobile navigation and better form error association.
- Motion needs a budget: continuous GPU effects must pause off-screen and simplify on touch/coarse-pointer devices.

## 2. Information Architecture

```
Home
├── About
│   ├── Story, mission, vision, values
│   ├── Journey and achievements
│   └── Process and culture
├── Founder
│   ├── Biography and leadership vision
│   ├── Journey and achievements
│   └── Message and social profiles
├── Services
│   ├── Marketing: digital, social, SEO, paid, email, WhatsApp, content, influencer
│   ├── Brand: strategy, identity, graphic, UI/UX
│   ├── Web: corporate, business, landing, WordPress, Django, Python, web apps
│   ├── Software: ERP, CRM, SaaS, custom software, API
│   ├── Mobile: Android, iOS, Flutter
│   └── Infrastructure: cloud, AWS, servers, maintenance, security, hosting, AI, automation, consulting
├── Work
│   ├── Portfolio index
│   └── Case study detail
├── Clients and testimonials
├── Insights
│   ├── Blog index/search/category
│   └── Blog detail
├── Careers
├── FAQ
├── Contact / book consultation
├── Brochure
└── Legal: privacy, terms, refund, disclaimer, sitemap, 404
```

Primary navigation stays task-focused: Work, Services, About, Insights, Contact. Founder, Clients, Careers and Legal sit in contextual menus/footer.

## 3. Wireframe Planning

### Global shell
- Floating translucent header: circular logo mark, primary navigation, consultation CTA, mobile trigger.
- Full-screen mobile menu: primary links, service shortcuts, contact channels and social proof.
- Footer: oversized brand statement, grouped navigation, newsletter, brochure, social/legal/contact.
- Persistent scroll progress, contextual cursor on fine pointers, WhatsApp quick action.

### Home
1. Cinematic hero: value proposition left; reactive brand orbit plus laptop/phone/analytics ecosystem right.
2. Trust rail: outcomes, markets and client signal.
3. Positioning manifesto with pinned text transition.
4. Horizontal service universe with category grouping.
5. Selected work with asymmetric case-study reveals.
6. Interactive globe / worldwide delivery narrative.
7. Process as sticky storytelling.
8. Technology constellation.
9. Testimonial theatre.
10. FAQ and conversion finale.

### About / Founder
- Editorial hero → story/portrait pairing → mission/vision split → values → horizontal timeline → achievements → culture → CTA.

### Service index / detail
- Index: category navigator → service matrix → capability proof → CTA.
- Detail: breadcrumb hero → overview → benefits → features → pinned process → technology → related work → FAQs → related services → CTA.

### Portfolio / case study
- Filtered cinematic index.
- Detail: outcome-first hero → challenge → strategic idea → experience/media → build details → measured results → testimonial → next case.

### Blog
- Featured editorial story → topic rail → responsive article grid → newsletter.
- Detail: breadcrumb/meta → title → hero image → readable article column → share/progress → related stories.

### Contact
- Intent-led hero → contact channels → qualification form → office/map/hours → expectation setting.

## 4. Component Tree

```
BaseShell
├── SeoHead
├── PageLoader
├── NoiseAndAurora
├── GlobalHeader
│   ├── BrandMark
│   ├── DesktopNav
│   ├── MobileNavDialog
│   └── MagneticCTA
├── Page
│   ├── Breadcrumbs
│   ├── PageHero / ServiceHero / EditorialHero
│   ├── SectionHeader
│   ├── RichText
│   ├── MetricRail
│   ├── ServiceCard / ProjectCard / ArticleCard / ClientCard
│   ├── ProcessTimeline
│   ├── TestimonialSlider
│   ├── Accordion
│   ├── InquiryForm
│   └── ConversionBand
├── GlobalFooter
│   ├── NavigationGroups
│   ├── NewsletterForm
│   ├── BrochureLink
│   └── LegalLinks
└── MotionSystem
    ├── ScrollProgress
    ├── RevealController
    ├── MagneticPointer
    ├── ParallaxController
    └── ThreeSceneManager
```

Django implementation uses template inheritance and includes for each reusable component. No page duplicates the global shell.

## 5. Database & CMS Structure

### Global
- `SiteSettings` singleton: identity, logo, theme tokens, contact, social sharing, analytics, global SEO.
- `NavigationItem`, `SocialLink`, `Brochure`, `NewsletterSubscriber`.

### Page content
- `ContentPage`: controlled page identity and core editorial fields for About, Founder introduction, Clients, Careers, Contact and legal pages.
- Planned `PageSection`: page, section type, heading, body, media, JSON configuration, order and visibility for reusable controlled sections.
- `FounderProfile`: biography, portrait, vision, experience, achievements, message and social profiles.

### Commercial content
- `Service`: slug, overview, benefits, features, process, technology, hero media and page SEO.
- `Project`: extend with slug, challenge, solution, results, testimonial and case-study gallery.
- `Client`, `Testimonial`, `Inquiry`, `CareerOpening`.

### Editorial
- `BlogPost`: slug, excerpt, structured body, category, author, media alt text, publication state and SEO.
- Planned `BlogCategory`, `BlogAuthor`, `MediaAsset` for normalized editorial workflows.

All public querysets filter publication/visibility, use deterministic ordering, and use `select_related/prefetch_related` when relations are introduced.

## 6. URL Structure

- `/` home
- `/about/`, `/founder/`
- `/services/`, `/services/<service-slug>/`
- `/portfolio/`, `/case-studies/<project-slug>/`
- `/clients/`, `/testimonials/`
- `/blog/`, `/blog/category/<slug>/`, `/blog/<post-slug>/`
- `/careers/`, `/contact/`, `/faq/`
- `/privacy-policy/`, `/terms/`, `/refund-policy/`, `/disclaimer/`
- `/brochure/`, `/sitemap.xml`, `/robots.txt`
- Custom `/404/` template in development; production error handler returns the same design with HTTP 404.

## 7. SEO Structure

- Unique CMS-managed title (target 50–60 characters) and description (target 140–160) per indexable page.
- Self-referencing canonical URLs built from request host unless explicitly overridden.
- Open Graph and Twitter image/title/description parity.
- BreadcrumbList JSON-LD on all inner pages.
- Organization/ProfessionalService JSON-LD globally; Service, Article and FAQPage schemas contextually.
- XML sitemap includes pages, services, projects and published posts with `lastmod` where available.
- Semantic single H1, descriptive image alt fields, logical H2/H3 outline and crawlable internal links.
- Blog and service slugs remain concise and stable; changed slugs require redirect records before production.
- Indexing disabled for admin, internal search result combinations and unpublished content.

## 8. Animation Strategy

- Motion principles: communicate hierarchy, reinforce the circular brand geometry, never delay task completion.
- Loader: circular mark resolves in under 1.2 seconds and is session-aware.
- Hero: Three.js particle field and orbit; pointer response capped to subtle rotation and suspended when tab is hidden.
- Scroll: Lenis feeds ScrollTrigger; one RAF loop only.
- Reveals: transform/opacity/blur with short stagger and reversible refresh-safe triggers.
- Storytelling: one pinned home service segment and one horizontal project rail on desktop; natural vertical flow on mobile.
- Microinteraction: magnetic CTAs only on fine pointers; card tilt capped at 4 degrees.
- Page transitions: short mask transition with navigation allowed immediately.
- Performance budget: no more than one WebGL canvas per page, DPR capped at 1.5, pause off-screen, avoid layout-animation properties.
- Accessibility: `prefers-reduced-motion` removes smooth scrolling, parallax, pinning, loader and continuous animation.

## 9. Responsive Strategy

- Fluid system using `clamp()` rather than device-specific fixed typography.
- Breakpoints: 1440+ cinematic widescreen; 1024–1439 desktop/laptop; 768–1023 tablet; under 768 mobile; under 390 compact mobile.
- Content width capped around 1320px with fluid 18–80px gutters.
- Desktop asymmetric grids collapse to intentional single-column editorial order, not merely stacking visual leftovers.
- Horizontal/pinned narratives become swipe-safe card rails or vertical sequences on touch devices.
- Hero 3D detail reduces progressively; mobile retains one branded orbit and one dashboard card.
- Tap targets minimum 44px; forms become one column; footer groups use accordions only where density demands it.
- Images use intrinsic dimensions, responsive `srcset` once CMS renditions are introduced, WebP/AVIF where supported and lazy loading below the fold.

## 10. Page-by-Page Delivery Order

1. Foundation: UTF-8 cleanup, shared shell, theme tokens, accessibility, SEO resolver, motion controller.
2. Home redesign and global navigation/footer.
3. About and Founder.
4. Services index and all service detail pages.
5. Portfolio and case studies.
6. Clients and testimonials.
7. Blog index/detail and 20 editorial articles.
8. Careers, FAQ, Contact and newsletter.
9. Legal, sitemap, 404 and brochure.
10. Admin dashboard refinement, caching, tests, performance and responsive QA.

Each page is complete only when its CMS editing path, responsive states, metadata, accessibility and automated route/render checks pass.