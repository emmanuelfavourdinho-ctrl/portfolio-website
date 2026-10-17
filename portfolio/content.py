"""Site content. Only verified facts belong here: edit this file, not the templates."""

OWNER = "Nsok Emmanuel"
EMAIL = "nsokemmanuelfavour@gmail.com"
GITHUB = "https://github.com/emmanuelfavourdinho-ctrl"
LINKEDIN = "https://linkedin.com/in/nsok-emmanuel"
REPO = "https://github.com/emmanuelfavourdinho-ctrl/portfolio-site"

PROJECTS = [
    {
        "slug": "newbiz-creation-studio",
        "name": "Newbiz Creation Studio",
        "summary": (
            "A booking website for a hair-braiding studio: customers browse a priced service menu, "
            "request an appointment online, and follow its status with a booking ID."
        ),
        "status": "Live",
        "status_note": "Publicly reachable at the address below. Designed and built by me for a working studio.",
        "stack": ["HTML", "CSS", "JavaScript", "Firebase Hosting"],
        "live": "https://newbizcreation.web.app/index.html",
        "shots": [
            {"src": "img/newbiz-home.jpg", "alt": "Newbiz Creation Studio home page: a dark full-width hero with the headline 'Where style becomes art.', navigation for Home, Services, Gallery and My Booking, and two buttons, Book Appointment and Our Services.", "caption": "Home page"},
            {"src": "img/newbiz-booking.jpg", "alt": "The booking page: a form headed 'Choose your style and time' with a grid of named hairstyles and their prices to select from.", "caption": "Booking page: choosing a service"},
            {"src": "img/newbiz-how-it-works.jpg", "alt": "The 'How it works' section: four steps from picking a style to booking a slot, followed by a call to book an appointment or chat on WhatsApp.", "caption": "How it works"},
        ],
        "case": {
            "context": (
                "A hair studio needs customers to see what it offers and what it costs, ask for an appointment, "
                "and know whether the owner has confirmed it. This site is built to cover that whole path in one place, "
                "with WhatsApp kept as a direct alternative."
            ),
            "contribution": (
                "I designed and built the site from scratch, including the interface and the engineering decisions behind it. "
                "It was made for a real studio's own business, not as a practice exercise."
            ),
            "features": [
                "A service menu with names, prices and options, loaded when the page opens rather than typed into the page.",
                "Links from each service card that open the booking form with that service already chosen.",
                "A booking form for name, phone, email, preferred date and time, and optional notes, with a message on each field that fails validation.",
                "No payment at booking. The request goes to the owner for review, and the customer is shown a booking ID to keep.",
                "A tracking page where a customer enters a booking ID with their phone number, or a phone number alone to list their bookings, and sees which are confirmed or pending.",
                "A gallery, opening hours, published studio policies and a WhatsApp link for customers who would rather message.",
            ],
            "flow_title": "How a booking moves through the site",
            "flow": [
                "The visitor picks a service from the menu, or arrives from a service card with one already selected.",
                "They enter their details and a preferred date and time. Invalid fields are flagged before anything is sent.",
                "The request is submitted without payment and the site shows a booking ID. The site states that a confirmation email is sent.",
                "The owner reviews the request and confirms it, according to the site's own description of the process.",
                "The customer returns to My Booking and checks the status using the booking ID and phone number.",
            ],
            "decisions": [
                {"title": "Verify before showing a booking", "choice": "The tracking page asks for a phone number alongside the booking ID, so a booking is not shown to anyone who only guesses an ID."},
                {"title": "Request, then confirmation", "choice": "A submitted booking is a request that the owner confirms. The interface keeps the two states separate and tells the customer which one applies."},
                {"title": "Keep the direct channel", "choice": "WhatsApp stays available beside the form, so a customer who prefers to message is not forced through it."},
            ],
            "evidence": [
                "The live site is publicly reachable, and its home, booking and tracking pages load.",
                "The screenshots on this page are of the real site.",
                "No traffic, booking volume or revenue figures are claimed, because none have been measured here.",
            ],
        },
    },
    {
        "slug": "portfolio-site",
        "name": "Emmatech portfolio",
        "summary": (
            "This site. A server-rendered Django application with a contact form "
            "that only reports success once the message has actually been sent."
        ),
        "status": "Implemented",
        "status_note": "Local build and automated tests verified. Production deployment not re-verified after this rebuild.",
        "stack": ["Python", "Django", "WhiteNoise", "Gunicorn", "SQLite"],
        "repo": REPO,
        "case": {
            "context": (
                "A personal portfolio had to show work honestly. The existing site was a Django project "
                "styled with Tailwind from a CDN, with placeholder projects, a chat button that never opened, "
                "a beta sign-up form that submitted nowhere, and a contact form that swallowed errors."
            ),
            "contribution": (
                "Sole author. The repository history shows a single account, and the audit, redesign and rebuild "
                "described here are my work."
            ),
            "flow_title": "How a contact message travels",
            "flow": [
                "The browser posts the form with a CSRF token.",
                "The view validates name, email and message on the server, and discards submissions that fill a hidden honeypot field.",
                "Django sends the message over SMTP with the visitor's address as Reply-To.",
                "Only if sending succeeds is a Contact record saved and a success message shown. Otherwise the visitor sees the failure and the direct email address.",
            ],
            "decisions": [
                {
                    "title": "Stay on Django",
                    "problem": "The brief allowed a rewrite in a JavaScript framework.",
                    "choice": "Keep Django with server-rendered templates and no client framework.",
                    "reason": "The site is content plus one form. The existing stack, deployment files and admin already did that job, and a rewrite would add weight without adding capability.",
                    "cost": "No client-side interactivity. The site currently ships no JavaScript at all.",
                },
                {
                    "title": "Make the form tell the truth",
                    "problem": "The original view printed exceptions to the console and rendered the page as if nothing had happened.",
                    "choice": "Validate on the server and show success only after the SMTP send returns.",
                    "reason": "A visitor who is told a message was sent must be right.",
                    "cost": "Delivery depends on Gmail SMTP credentials being configured. Without them the form fails visibly and points to the email address.",
                },
                {
                    "title": "Keep secrets out of the repository",
                    "problem": "The audit found .env, the SQLite database and compiled caches tracked in Git, with no .gitignore.",
                    "choice": "Add .gitignore and .env.example, stop tracking those files, and refuse to start without SECRET_KEY unless DEBUG is on.",
                    "reason": "Configuration belongs in the environment, and failing at startup is safer than running with a missing key.",
                    "cost": "Stopping tracking does not erase history. The old secret key and email password must be rotated.",
                },
            ],
            "challenges": [
                "Secrets already committed to Git history cannot be fixed by a later commit; rotation is the only real remedy, so the case study records it as outstanding work rather than solved.",
                "Failure handling in the original contact view was invisible. Tests now force the send to fail and assert that the visitor is told.",
            ],
            "evidence": [
                "Automated Django tests cover the routes, form validation, the honeypot, a successful send and a failed send.",
                "The production build step, collectstatic, completes without errors.",
                "No performance, traffic or user figures are claimed, because none have been measured.",
            ],
            "reflection": (
                "The next improvements are a tested deployment pipeline that runs collectstatic and the test suite, "
                "moving the database off ephemeral SQLite storage before the Contact records matter, and adding genuine "
                "project screenshots once other work is ready to show."
            ),
        },
    },
]

CAPABILITIES = [
    ("Backend", [("Python", True), ("Django", True), ("Node.js", False), ("Express", False), ("REST APIs", False)]),
    ("Frontend", [("HTML", True), ("CSS", True), ("JavaScript", False), ("React", False), ("Next.js", False)]),
    ("Data", [("SQLite", True), ("Django ORM", True), ("PostgreSQL", False), ("Prisma", False)]),
    ("Mobile", [("Flutter", False), ("Firebase", False)]),
    ("Workflow", [("Git", True), ("GitHub", True), ("Gunicorn", True), ("WhiteNoise", True), ("Render", True)]),
]

ABOUT = [
    "I build web applications and mobile experiences, and I pay attention to the parts that are easy to skip: what happens when a request fails, whether a form tells the truth, whether the next person can read the code.",
    "Most of my work so far is in Python and Django, with JavaScript on the front end. I treat a project as finished when it works under failure, not only when it works in a demo.",
]


# Hero photograph (static/img/). Replace the files and this text to change it.
HERO_IMAGE = {
    "src": "img/hero-2400.webp",
    "src_small": "img/hero-1200.webp",
    "alt": "Two monitors showing code above a keyboard lit by orange light, with a phone playing music between them.",
}

# Photos shown beside the About text. Put files in static/img/about/ and add entries:
#   {"src": "img/about/me-1.jpg", "alt": "Describe what the photo shows", "caption": ""}
ABOUT_PHOTOS = []
