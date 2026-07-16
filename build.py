#!/usr/bin/env python3
"""
Static site generator for gregcastellanos.com.

Every page is rendered from the content model + shared templates below, so
header, footer, meta, and structure stay in one place. Output is plain static
HTML written to the repo root for GitHub Pages.

Usage:  python3 build.py
No dependencies — Python 3 standard library only.
"""

import html
import json
import os

# --------------------------------------------------------------------------
# Site configuration
# --------------------------------------------------------------------------
BASE_URL = "https://gregcastellanos.com"
NAME = "Gregory Castellanos"
EMAIL = "gregcastellanoswork@gmail.com"
COACHING_URL = "https://castellanoscoaching.com"
# LinkedIn / social: wired into the footer and structured data.
LINKEDIN_URL = "https://www.linkedin.com/in/gregcastellanos"

ROOT = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("Home", "index.html"),
    ("People", "people.html"),
    ("Ideas", "ideas.html"),
    ("Brands", "brands.html"),
    ("Technology", "technology.html"),
    ("Experiences", "experiences.html"),
    ("Places", "places.html"),
    ("Work", "work.html"),
    ("About", "about.html"),
    ("Contact", "contact.html"),
]

ROLES = ["Founder", "Learning Designer", "AI Evaluation Specialist",
         "Executive Function Coach", "Event Producer", "Inventor"]

# --------------------------------------------------------------------------
# Inline SVG art (theme-aware via currentColor where possible)
# --------------------------------------------------------------------------
BRAND_MARK = (
    '<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
    '<circle cx="24" cy="27" r="7.5" fill="#a9772f"/>'
    '<g stroke="#a9772f" stroke-width="2" stroke-linecap="round">'
    '<line x1="24" y1="6" x2="24" y2="11"/><line x1="9" y1="12" x2="12" y2="15"/>'
    '<line x1="39" y1="12" x2="36" y2="15"/><line x1="4" y1="27" x2="9" y2="27"/>'
    '<line x1="39" y1="27" x2="44" y2="27"/></g>'
    '<path d="M4 40 H44" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>'
    '<path d="M17 40 L23 31 M31 40 L25 31" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" opacity=".5"/></svg>'
)

AREA_GLYPHS = {
    "people": '<path d="M8 26c0-4 3.2-6 8-6s8 2 8 6" /><circle cx="16" cy="12" r="4.2"/>'
              '<path d="M24 26c0-3.4 2.4-5.2 6-5.2" opacity=".6"/><circle cx="27" cy="12.5" r="3.2" opacity=".6"/>',
    "ideas": '<path d="M16 5a9 9 0 0 0-5 16.5c1 .8 1.5 1.6 1.5 3V26h7v-1.5c0-1.4.5-2.2 1.5-3A9 9 0 0 0 16 5Z"/>'
             '<path d="M13 29h6" /><path d="M14 26v3M18 26v3" opacity=".6"/>',
    "brands": '<circle cx="16" cy="16" r="10.5"/><circle cx="16" cy="16" r="5" opacity=".7"/>'
              '<circle cx="16" cy="16" r="1.4" fill="currentColor" stroke="none"/>',
    "technology": '<circle cx="8" cy="16" r="3"/><circle cx="24" cy="8" r="3"/><circle cx="24" cy="24" r="3"/>'
                  '<path d="M10.6 14.6 21.4 9.4M10.6 17.4 21.4 22.6M24 11v10" opacity=".7"/>',
    "experiences": '<path d="M4 16h3l3-8 4 18 4-24 4 20 3-6h3" stroke-linejoin="round" stroke-linecap="round"/>',
    "places": '<path d="M16 3c-5 0-9 3.8-9 9 0 6.6 9 17 9 17s9-10.4 9-17c0-5.2-4-9-9-9Z"/>'
              '<circle cx="16" cy="12" r="3.4"/>',
}

def area_glyph(slug):
    return ('<svg class="area-glyph" viewBox="0 0 32 32" fill="none" stroke="currentColor" '
            'stroke-width="1.8" aria-hidden="true" focusable="false">' + AREA_GLYPHS[slug] + '</svg>')

# Six-part ecosystem diagram for the home hero.
def ecosystem_art():
    nodes = [
        (200, 60, "#315d82", "People"),
        (321, 130, "#6f8560", "Ideas"),
        (321, 270, "#a57933", "Brands"),
        (200, 340, "#294a6d", "Technology"),
        (79, 270, "#855c43", "Experiences"),
        (79, 130, "#536f58", "Places"),
    ]
    lines = "".join(
        f'<line x1="200" y1="200" x2="{x}" y2="{y}" stroke="currentColor" stroke-width="1.5" opacity=".28"/>'
        for x, y, _c, _l in nodes)
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="30" fill="{c}"/>'
        f'<text x="{x}" y="{y+3.5}" text-anchor="middle" font-size="9" font-weight="700" '
        f'fill="#fff" font-family="Inter,sans-serif">{l}</text>'
        for x, y, c, l in nodes)
    return (
        '<svg class="ecosystem-svg" viewBox="0 0 400 400" role="img" '
        'aria-label="A six-part ecosystem: People, Ideas, Brands, Technology, Experiences, and Places connected around one practice.">'
        + lines + dots +
        '<circle cx="200" cy="200" r="46" fill="none" stroke="#a9772f" stroke-width="2"/>'
        '<circle cx="200" cy="200" r="38" fill="currentColor" opacity=".92"/>'
        '<text x="200" y="196" text-anchor="middle" font-size="20" font-weight="700" '
        'fill="#a9772f" font-family="Iowan Old Style,Georgia,serif">GC</text>'
        '<text x="200" y="214" text-anchor="middle" font-size="8.5" letter-spacing="1.5" '
        'fill="#fff" font-family="Inter,sans-serif" opacity=".8">ONE PRACTICE</text>'
        '</svg>')

ICON_SUN = ('<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/>'
            '<path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M19.1 4.9l-1.4 1.4M6.3 17.7l-1.4 1.4"/></svg>')
ICON_MOON = ('<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4 6.5 6.5 0 0 0 20 14.5Z"/></svg>')

# --------------------------------------------------------------------------
# Area + content model
# --------------------------------------------------------------------------
AREAS = [
    {
        "slug": "people", "name": "People", "venture": "Castellanos Coaching",
        "color": "#315d82", "url": COACHING_URL,
        "cue": "Clarity in motion",
        "purpose": "Executive function coaching and learning systems that build real independence.",
        "detail": "Person-centered support for 30+ Autistic and ADHD clients since 2020 — including Regional Center and Self-Determination Program participants — plus AI-literacy teaching for youth.",
        "hero_h1": "Capability, independence, and practical support for real life.",
        "hero_lede": "Castellanos Coaching is the people-centered part of the practice: executive function, independence, academic support, and family collaboration, grounded in twenty years of learning design.",
        "cta": "Visit Castellanos Coaching", "cta_href": COACHING_URL,
        "index": [
            "Executive function and independence",
            "Neurodivergent teens and adults",
            "Family support and provider collaboration",
            "Academic coaching, tutoring, and study systems",
        ],
        "copy": [
            ("What this work holds",
             "Learning science, structure, empathy, and accountability. The goal is not to make someone look impressive on paper — it is to help them understand what is happening, build systems they can sustain, and practice the next step until it becomes possible."),
            ("The Castellanos Compass",
             "Within Castellanos Coaching, Greg works through four stages — Clarity, Alignment, Foundation, and Expansion — as a human-development framework. On this umbrella site it is introduced, not copied in full; the coaching site carries the detail."),
            ("Credentialed and experienced",
             "A Master of Arts in Teaching (Honors) and twenty years across classrooms, makerspaces, and community programs sit behind the coaching — including AI-literacy teaching for youth at the Boys &amp; Girls Club of San Francisco and lead-educator work at The Branson School."),
        ],
        "includes": [
            "Executive function and independence", "Neurodivergent teens and adults",
            "Family support and provider collaboration", "Academic coaching, tutoring, and study systems",
            "College, employment, and transition planning", "Curriculum design, workshops, and mentoring",
        ],
        "related": ["Castellanos Coaching", "AI You Trust", "TechShop STEAM Program", "Selectas Flow"],
    },
    {
        "slug": "ideas", "name": "Ideas", "venture": "Castellanos Consulting",
        "color": "#6f8560", "url": "",
        "cue": "The real opportunity",
        "purpose": "Turning ambitious visions into fundable plans and working programs.",
        "detail": "Founder of 4+ ventures and nonprofits — strategy, program design, grant writing, and conservation work supporting initiatives that protect thousands of acres.",
        "hero_h1": "Strategy for visions that have substance but need shape.",
        "hero_lede": "Greg helps founders, organizations, and community projects understand what they are building, who it serves, and what has to happen next.",
        "cta": "Talk about ideas", "cta_href": "contact.html",
        "index": [
            "Venture and program strategy", "Founder and startup support",
            "Nonprofit, grants, and partnerships", "Conservation and social-impact concepts",
        ],
        "copy": [
            ("Useful strategy",
             "This work spans venture development, organizational clarity, program design, partnership logic, and fundable project development — the same work behind Local Maker Mart's nonprofit setup and ProNara conservation initiatives protecting thousands of acres."),
            ("Typical situations",
             "A founder has a compelling vision but no coherent plan. An organization has too many disconnected initiatives. A property has potential but no direction. A community project needs structure, partners, and language people can trust."),
            ("A simple working sequence",
             "Listen and understand. Find the real opportunity. Clarify the vision. Align people and systems. Build a usable plan. Help move it into action — the same diagnose-and-build loop Greg has run across four founded ventures."),
        ],
        "includes": [
            "Venture and program strategy", "Founder and startup support",
            "Nonprofit governance and grant writing", "Partnership and community development",
            "Conservation and social-impact concepts", "Actionable plans for complex projects",
        ],
        "related": ["Local Maker Mart", "ProNara Conservation", "Recreation Experiences", "AI You Trust"],
    },
    {
        "slug": "brands", "name": "Brands", "venture": "Castellanos Creative",
        "color": "#a57933", "url": "",
        "cue": "Meaning made visible",
        "purpose": "Clarity first — naming, messaging, identity, and websites that make meaning legible.",
        "detail": "Two decades bridging interactive design, brand strategy, and build — from positioning to a shipped site, including web work for the Shangri-La Sonoma Retreat Center.",
        "hero_h1": "Brand work that starts with meaning, not decoration.",
        "hero_lede": "A strong brand is a clear idea made understandable — through language, identity, rhythm, design, and the experience someone has when they encounter it.",
        "cta": "Talk about brands", "cta_href": "contact.html",
        "index": [
            "Positioning, naming, and messaging", "Identity direction and visual storytelling",
            "Website strategy, design, and build", "Presentation and pitch materials",
        ],
        "copy": [
            ("Clarity before style",
             "Many branding problems are really clarity problems. Greg helps identify what the work is about, what needs to be said, what to leave out, and how the experience should feel — grounded in a B.A. in Interactive Multimedia and years of user-centered design."),
            ("Connected creative direction",
             "This work connects strategy, language, design, technology, and implementation: naming, positioning, messaging, identity direction, websites, presentations, and content systems — from concept through a site that ships."),
            ("For real projects",
             "It is most useful when a founder, organization, initiative, place, or event has depth but has not yet found the words, structure, and visual direction that make it easy to understand and trust."),
        ],
        "includes": [
            "Positioning, naming, and messaging", "Identity direction and visual storytelling",
            "Website strategy, design, and build", "Presentation and pitch materials",
            "Campaign and launch concepts", "Creative systems that can be maintained",
        ],
        "related": ["Local Maker Mart", "Recreation Sound Systems", "Recreation Experiences"],
    },
    {
        "slug": "technology", "name": "Technology", "venture": "AI You Trust",
        "color": "#294a6d", "url": "",
        "cue": "Tools people can trust",
        "purpose": "Human-centered AI — evaluation, literacy, and tools people can use with judgment.",
        "detail": "Building Coherence on the Anthropic API; two decades of rubric-driven evaluation now applied to AI output; command of the full digital-fabrication stack.",
        "hero_h1": "Tools should make people more capable, not more confused.",
        "hero_lede": "Greg's technology work spans AI evaluation and literacy, educational tools, interactive media, and the digital-fabrication stack — always in service of the person using it.",
        "cta": "Talk about technology", "cta_href": "contact.html",
        "index": [
            "AI evaluation and human-in-the-loop review", "AI literacy and responsible adoption",
            "Educational tools and interactive media", "Digital fabrication and creative technology",
        ],
        "copy": [
            ("AI with judgment",
             "AI You Trust is a direction for helping people understand and use AI without surrendering their judgment. Greg is building Coherence — an AI-powered browser extension on the Anthropic API that surfaces emotionally manipulative content patterns online — using human-in-the-loop design from concept through prototype. <em>(In development.)</em>"),
            ("Evaluation is the throughline",
             "Two decades of rubric design, structured observation, and learning-outcome measurement translate directly to evaluating AI output for accuracy, usability, and potential harm. It is the same disciplined, criteria-based judgment, applied to a new medium."),
            ("Fluency with taste",
             "Comfortable across digital systems, interactive media, AV, and the fabrication stack — CAD, laser cutting, CNC, 3D printing, and electronics. The value is not technology for its own sake; it is choosing and shaping tools that serve the person, project, or place."),
        ],
        "includes": [
            "AI evaluation and human-in-the-loop review", "AI literacy and responsible adoption",
            "Educational tools and interactive media", "Web tools and digital systems",
            "AV, sound, lighting, and production workflows", "Digital fabrication and prototyping",
        ],
        "related": ["Coherence", "AI You Trust", "TechShop STEAM Program", "Castellanos Coaching"],
    },
    {
        "slug": "experiences", "name": "Experiences", "venture": "Recreation Experiences",
        "color": "#855c43", "url": "",
        "hero_image": "greg-production.jpg",
        "hero_alt": "Greg Castellanos running graphics and playback from the production desk at a live gala.",
        "cue": "Gatherings with intention",
        "purpose": "Events shaped with sound, hospitality, and calm production.",
        "detail": "100+ events over a decade; Executive Producer of the sold-out 250-person Convergence 2026; supported productions for Google, Stripe, Nasdaq, and the World Economic Forum through leading Bay Area production companies.",
        "hero_h1": "Gatherings shaped with sound, care, flow, and technical calm.",
        "hero_lede": "Greg's experience work grew from patented sound systems and live production into a broader practice of designing how people gather, listen, celebrate, and feel held in a place.",
        "cta": "Talk about experiences", "cta_href": "contact.html",
        "index": [
            "Event production and stage management", "Sound, lighting, video, and AV operation",
            "Retreats, fundraisers, and community gatherings", "DJing, curation, and radio",
        ],
        "copy": [
            ("More than logistics",
             "A good experience is not just a schedule or a playlist. It is the relationship between sound, light, hospitality, setting, pacing, and what people are invited to do together — held with the calm that a decade of production builds."),
            ("Produced and supported",
             "Greg was Executive Producer of Convergence 2026, a sold-out 250-person, 15-artist production, and has produced or supported 100+ events over ten years — from the Ghost Town Gala at Shangri-La Sonoma to GOAT My Valentine, a Goatlandia benefit in Sebastopol. Through CAVL, JNSQ, Got Light, and Vario he has supported productions for Google, Stripe, Atlassian, GitHub, Nasdaq, SF MoMA, and the World Economic Forum."),
            ("Sound at the root",
             "It began with Recreation Sound Systems — two U.S. patents for sustainable, resonance-based audio — and continues on the air through Selectas Flow on KGGV 95.1 FM. Private venue and client details stay private."),
        ],
        "includes": [
            "Event production and stage management", "Run-of-show, GFX, and playback operation",
            "Live sound, lighting, video, and AV", "Retreats, fundraisers, and community gatherings",
            "DJ experiences and radio curation", "Creative and technical direction",
        ],
        "related": ["Convergence 2026", "Recreation Sound Systems", "Enterprise Production Support", "Selectas Flow"],
    },
    {
        "slug": "places", "name": "Places", "venture": "Common Ground Works",
        "color": "#536f58", "url": "",
        "cue": "Potential made practical",
        "purpose": "Helping overlooked places become useful, welcoming, and alive.",
        "detail": "Place strategy and guest-readiness rooted in retreat-center and hospitality work across Sonoma County, and community place-making at Local Maker Mart.",
        "hero_h1": "Common Ground Works",
        "hero_lede": "Helping overlooked places become more useful, welcoming, and alive — through place strategy, stewardship, guest readiness, hospitality thinking, creative reuse, and practical activation.",
        "cta": "Talk about places", "cta_href": "contact.html",
        "index": [
            "Place strategy and creative reuse", "Guest readiness and hospitality systems",
            "Stewardship and practical activation", "Retreat and community environments",
        ],
        "copy": [
            ("Place strategy",
             "Clarify what a place can hold, who it serves, how people move through it, and what makes it ready for use — informed by producing events at retreat centers like Shangri-La Sonoma and building a nonprofit maker hub in North Beach."),
            ("Stewardship and readiness",
             "Beautification, organization, guest experience, and hospitality systems that make potential easier to use. The same care that goes into a run-of-show goes into readying a space for people."),
            ("Role and boundaries",
             "Common Ground Works is not architecture, contracting, brokerage, or property management. Private addresses, owners, and venue details stay private."),
        ],
        "includes": [
            "Place strategy and creative reuse", "Property organization and guest readiness",
            "Stewardship and hospitality systems", "Spatial and experience planning",
            "Retreat and community environments", "Activation, maintenance, and readiness",
        ],
        "related": ["Local Maker Mart", "Recreation Experiences", "ProNara Conservation", "Convergence 2026"],
    },
]
AREA_BY_NAME = {a["name"]: a for a in AREAS}
AREA_COLOR = {a["slug"]: a["color"] for a in AREAS}

# Proof stats (phrasing follows the master source bank verification flags)
STATS = [
    ("20+", "Years of practice"),
    ("2", "U.S. patents"),
    ("4+", "Ventures founded"),
    ("30+", "Coaching clients since 2020"),
    ("100+", "Events produced or supported"),
    ("Nationwide", "STEAM curriculum adoption"),
]

# The method (aligned to the Castellanos Compass)
METHOD = [
    ("Understand", "Find the real situation and the people inside it before proposing anything."),
    ("Clarify", "Name what matters, cut what doesn't, and locate the real opportunity."),
    ("Build", "Design the system and the next usable step — not a plan that sits on a shelf."),
    ("Sustain", "Hand off something people can keep running without you in the room."),
]

CURRENT = [
    "AI evaluation, AI literacy, and human-centered tool design — including Coherence on the Anthropic API.",
    "Executive function coaching and practical independence systems through Castellanos Coaching.",
    "Events and place-based projects, from Recreation Experiences to Common Ground Works.",
]

# Case studies — real work, phrased to the source-bank rules. areas = filter tags.
CASES = [
    {
        "name": "Convergence 2026", "kicker": "Event Production",
        "areas": ["experiences", "ideas", "places"],
        "role": "Executive Producer",
        "blurb": "A sold-out 250-person, 15-artist vernal-equinox production at Redwood Underground. Greg owned the budget, stage management, run-of-show, and stakeholder coordination end to end.",
        "status": "Produced March 2026.", "tags": ["Experiences", "Ideas", "Places"],
    },
    {
        "name": "Recreation Sound Systems", "kicker": "Invention & Product",
        "areas": ["technology", "brands", "experiences"],
        "role": "Founder & CEO (2013–2020)",
        "blurb": "Built a patented audio-hardware and event-production company from the ground up — earning two U.S. design patents, "
                 "<a href=\"https://patents.google.com/patent/USD739846S/en\">D739,846</a> and "
                 "<a href=\"https://patents.google.com/patent/USD815617S/en\">D815,617</a>, and taking product from concept to manufactured reality.",
        "status": "Legacy venture; patents held.", "tags": ["Technology", "Brands", "Experiences"],
    },
    {
        "name": "TechShop STEAM Program", "kicker": "Learning Design",
        "areas": ["technology", "people", "ideas"],
        "role": "Lead STEAM Educator & Instructional Designer",
        "blurb": "Designed and launched a flagship STEAM program adopted across multiple TechShop locations nationwide, and co-designed TechShop Inside — a mobile makerspace bringing fabrication and STEAM education to underserved communities.",
        "status": "2014–2019.", "tags": ["Technology", "People", "Ideas"],
    },
    {
        "name": "Castellanos Coaching", "kicker": "Coaching & Neurodiversity",
        "areas": ["people", "ideas", "technology"],
        "role": "Founder & Executive Function Coach",
        "blurb": "A dedicated practice supporting 30+ Autistic and ADHD clients since 2020 — including Regional Center and Self-Determination Program participants — with person-centered planning and individualized progress systems.",
        "status": "Active — dedicated site at castellanoscoaching.com.", "tags": ["People", "Ideas", "Technology"],
        "link": COACHING_URL, "link_label": "Visit Castellanos Coaching",
    },
    {
        "name": "Local Maker Mart", "kicker": "Community & Nonprofit",
        "areas": ["ideas", "brands", "places", "people"],
        "role": "Founder, CEO & Program Director (2019–2022)",
        "blurb": "A nonprofit community arts center and maker hub in North Beach, San Francisco. Greg owned facility acquisition, governance, grant writing, partnerships, and the Maker Mart Academy youth programs.",
        "status": "Legacy venture and reference point for current place-based work.", "tags": ["Ideas", "Brands", "Places"],
    },
    {
        "name": "Coherence", "kicker": "Applied AI",
        "areas": ["technology", "ideas"],
        "role": "Founder & Builder",
        "blurb": "An AI-powered browser extension on the Anthropic API that surfaces emotionally manipulative content patterns online, applying human-in-the-loop evaluation from concept through prototype.",
        "status": "In development.", "tags": ["Technology", "Ideas"],
    },
    {
        "name": "Enterprise Production Support", "kicker": "Live Production",
        "areas": ["experiences", "technology"],
        "role": "GFX / Playback / V1 Operator (freelance)",
        "blurb": "A live corporate-AV professional with 15+ years on conferences, general sessions, and executive keynotes. Through CAVL, JNSQ, Got Light, and Vario, Greg has supported productions for Google, Stripe, Atlassian, GitHub, Nasdaq, SF MoMA, and the World Economic Forum — running graphics, playback, and V1 with live cue-to-cue calling and composure in show-critical environments.",
        "status": "2022–present.", "tags": ["Experiences", "Technology"],
    },
    {
        "name": "ProNara Conservation", "kicker": "Conservation",
        "areas": ["ideas", "places"],
        "role": "Advisor & Fundraising Support",
        "blurb": "Supported rainforest conservation initiatives protecting thousands of acres, contributing strategic planning, sustainability education, ecotourism development, and fundraising.",
        "status": "Ongoing.", "tags": ["Ideas", "Places"],
    },
    {
        "name": "Selectas Flow", "kicker": "Radio & Culture",
        "areas": ["experiences", "people"],
        "role": "Host, DJ & Curator",
        "blurb": "A recurring community radio show on KGGV 95.1 FM — listening, curation, rhythm, and the culture of gathering, produced and hosted by Greg.",
        "status": "On air, KGGV 95.1 FM.", "tags": ["Experiences", "People"],
    },
]
CASE_BY_NAME = {c["name"]: c for c in CASES}

TIMELINE = [
    ("2000–2004", "B.A. Interactive Multimedia (Honors), Columbia College Chicago"),
    ("2004–2006", "Master of Arts in Teaching (Honors), Columbia College Chicago"),
    ("2007–2008", "Director of Arts &amp; Technology, Oakland Aviation High School"),
    ("2013–2020", "Founder &amp; CEO, Recreation Sound Systems — two U.S. patents"),
    ("2014–2019", "Lead STEAM Educator &amp; Designer, TechShop — nationwide curriculum"),
    ("2019–2022", "Founder, Local Maker Mart nonprofit arts &amp; maker hub"),
    ("2020–now", "Founder, Castellanos Coaching — executive function systems"),
    ("2022–now", "Live production (CAVL, JNSQ, Got Light) &amp; Broadway Studios / FAME"),
    ("2023–now", "STEM &amp; AI Educator, Boys &amp; Girls Club of San Francisco"),
    ("2024–now", "Building Coherence, an AI tool on the Anthropic API"),
    ("2026", "Executive Producer, Convergence — sold-out 250-person production"),
]

RECOGNITION = [
    'Two U.S. design patents for portable audio technology — '
    '<a href="https://patents.google.com/patent/USD739846S/en">D739,846</a> (Portable sound system) and '
    '<a href="https://patents.google.com/patent/USD815617S/en">D815,617</a> (Portable yoga block speaker).',
    "STEAM curriculum adopted across multiple TechShop locations nationally.",
    "Selected as Lead Educator, Next Generation Scholars Summer Academy at The Branson School (2024).",
    "Graduated with Honors at both degree levels, Columbia College Chicago.",
]

CREDENTIALS = [
    "M.A.T., Columbia College Chicago — Honors, GPA 3.9",
    "B.A. Interactive Multimedia, Columbia College Chicago — Honors, GPA 3.8",
    "Illinois Type 03 &amp; Type 09 teaching certificates; endorsements in Visual Arts and Computer Applications",
]

SKILL_DOMAINS = [
    "AI evaluation", "Learning design", "Executive-function coaching", "Event production",
    "Product &amp; fabrication", "Program leadership", "Community &amp; nonprofit", "Creative direction",
]

SPEAKING_TOPICS = [
    "Executive function and independence", "Neurodivergence and practical support",
    "Human-centered AI and AI literacy", "Education, project-based learning, and creative technology",
    "Entrepreneurship and community building", "Multidisciplinary careers",
    "Events, hospitality, and experience design", "Turning ambitious ideas into actionable projects",
]
SPEAKING_FORMATS = ["Workshops", "Talks", "Panels", "Parent groups", "School sessions",
                    "Retreat programs", "Guest teaching", "Moderation"]

TESTIMONIALS = [
    ("Greg helped me stop overthinking and actually take steps. We worked on school, jobs, track, and planning my future in a way that felt real.", "Logan D.", "Coaching client"),
    ("Greg actually listened to what I wanted. He helped me think about school, work, and real-life stuff without making me feel talked down to.", "Rune C.", "Coaching client"),
    ("Greg helps me work on being more independent. I have a real job now, I go to concerts, and I'm learning how to handle more things on my own.", "Alex G.", "Coaching client"),
    ("Greg helped me get organized and start doing things instead of avoiding them. He made everything feel less overwhelming.", "Seth A.", "Coaching client"),
]

FAQ = [
    ("Is this the coaching website?",
     "No — this is Greg's umbrella site. Executive function coaching lives at its own dedicated home, "
     "<a href=\"" + COACHING_URL + "\">castellanoscoaching.com</a>, with service details, fit, and next steps."),
    ("How do the six areas relate?",
     "They are one practice, not six businesses. People, Ideas, Brands, Technology, Experiences, and Places share the "
     "same method: understand the people, clarify the opportunity, build the system, and hand off something that lasts."),
    ("What kinds of projects are the best fit?",
     "Work with people, moving parts, and a need for good judgment — an unusual founder problem, a program that needs "
     "shape, an event that needs calm production, or a place with hidden potential."),
    ("How is private and client work handled?",
     "Private client, family, student, venue, and property details are never published. Projects are described at a high "
     "level, and outcomes, figures, and testimonials are never invented. See the "
     "<a href=\"privacy.html\">privacy note</a>."),
]

# --------------------------------------------------------------------------
# Template helpers
# --------------------------------------------------------------------------
def head(title, description, path, extra_ld=None, area_color=None):
    canonical = BASE_URL + "/" + ("" if path == "index.html" else path)
    person = {
        "@type": "Person", "@id": BASE_URL + "/#greg", "name": NAME,
        "alternateName": "Greg Castellanos", "url": BASE_URL,
        "jobTitle": ROLES,
        "description": "Multidisciplinary founder, learning designer, and executive function coach with 20+ years designing human-centered systems.",
        "address": {"@type": "PostalAddress", "addressRegion": "California", "addressCountry": "US"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Columbia College Chicago"},
        "knowsAbout": ["People", "Ideas", "Brands", "Technology", "Experiences", "Places",
                       "AI evaluation", "Learning design", "Executive function coaching",
                       "Event production", "Product development"],
        "email": "mailto:" + EMAIL,
    }
    same = [COACHING_URL] + ([LINKEDIN_URL] if LINKEDIN_URL else [])
    person["sameAs"] = same
    graph = [
        person,
        {"@type": "WebSite", "@id": BASE_URL + "/#website", "name": NAME, "url": BASE_URL,
         "description": description, "publisher": {"@id": BASE_URL + "/#greg"}},
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title,
         "description": description, "isPartOf": {"@id": BASE_URL + "/#website"},
         "about": {"@id": BASE_URL + "/#greg"}},
    ]
    if extra_ld:
        graph.extend(extra_ld)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"))
    theme_color = area_color or "#0d2740"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta name="author" content="{NAME}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{NAME}">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{BASE_URL}/assets/images/og-image.png">
  <meta property="og:image:width" content="1774">
  <meta property="og:image:height" content="887">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(description, quote=True)}">
  <meta name="twitter:image" content="{BASE_URL}/assets/images/og-image.png">
  <meta name="theme-color" content="{theme_color}">
  <link rel="icon" href="assets/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="preload" as="style" href="assets/styles.css">
  <link rel="stylesheet" href="assets/styles.css">
  <script>(function(){{var d=document.documentElement;d.classList.add('js');try{{var t=localStorage.getItem('gc-theme');if(t==='dark'||t==='light'){{d.setAttribute('data-theme',t);}}}}catch(e){{}}}})();</script>
  <script type="application/ld+json">{ld}</script>
</head>"""

def header(active):
    def _link(label, href):
        cur = ' aria-current="page"' if href == active else ""
        return '<a href="' + href + '"' + cur + '>' + label + '</a>'
    links = "".join(_link(label, href) for label, href in NAV)
    return f"""  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <a class="brand" href="index.html" aria-label="{NAME} — home">
      {BRAND_MARK}
      <span class="brand-word"><strong>Gregory Castellanos</strong><small>People · Ideas · Brands · Technology · Experiences · Places</small></span>
    </a>
    <nav class="site-nav" id="site-nav" aria-label="Primary">
      {links}
    </nav>
    <div class="header-actions">
      <button class="theme-toggle" type="button" aria-label="Switch to dark theme" aria-pressed="false">{ICON_SUN}{ICON_MOON}</button>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open navigation">Menu</button>
    </div>
  </header>"""

def footer():
    ventures = "".join(
        f'<a href="{a["url"] or a["slug"] + ".html"}">{a["venture"]}</a>' for a in AREAS)
    areas = "".join(f'<a href="{a["slug"]}.html">{a["name"]}</a>' for a in AREAS)
    linkedin = f'<a href="{LINKEDIN_URL}">LinkedIn</a>' if LINKEDIN_URL else ""
    return f"""  <footer class="site-footer">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="index.html" aria-label="{NAME} — home">
          {BRAND_MARK}
          <span class="brand-word"><strong>Gregory Castellanos</strong><small>One practice, six lanes</small></span>
        </a>
        <p>A multidisciplinary practice for people, ideas, brands, technology, experiences, and places — based in the Bay Area and Sonoma County, California.</p>
      </div>
      <div class="footer-grid">
        <div>
          <h2>Areas</h2>
          {areas}
        </div>
        <div>
          <h2>Ventures</h2>
          {ventures}
        </div>
        <div>
          <h2>Connect</h2>
          <a href="work.html">Work</a>
          <a href="speaking.html">Speaking &amp; teaching</a>
          <a href="contact.html">Contact</a>
          <a href="mailto:{EMAIL}">Email</a>
          {linkedin}
          <a href="privacy.html">Privacy</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> {NAME}. All rights reserved.</span>
      <span>Bay Area / Sonoma County, California</span>
    </div>
  </footer>
  <script src="assets/site.js" defer></script>
</body>
</html>"""

def page(path, title, description, body, active=None, extra_ld=None, area_color=None, body_class=""):
    active = active or path
    cls = f' class="{body_class}"' if body_class else ""
    doc = head(title, description, path, extra_ld, area_color) + "\n<body" + cls + ">\n" + \
        header(active) + "\n  <main id=\"main\">\n" + body + "\n  </main>\n" + footer()
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(doc)
    return path

# Reusable section builders -------------------------------------------------
def proof_bar():
    stats = "".join(
        f'<div class="stat"><span class="num">{n}</span><span class="label">{l}</span></div>'
        for n, l in STATS)
    return f'<section class="proof-bar"><div class="proof-grid">{stats}</div></section>'

def cta_band(full=False, heading=None, text=None):
    heading = heading or "Bring the unusual project, the half-formed idea, or the place with hidden potential."
    text = text or "Coaching, strategy, brand, technology, events, teaching, and place work are all welcome. Start with a simple note."
    cls = "cta-band full" if full else "cta-band"
    inner = f"""<p class="eyebrow">Contact</p>
      <h2>{heading}</h2>
      <p>{text}</p>
      <div class="cta-row">
        <a class="button primary" href="contact.html">Start a conversation</a>
        <a class="button secondary" href="mailto:{EMAIL}">Email Greg</a>
      </div>"""
    if full:
        return f'<section class="section reveal"><div class="{cls}">{inner}</div></section>'
    return f'<section class="section"><div class="container reveal"><div class="{cls}">{inner}</div></div></section>'

def area_card(a):
    venture = f'<span class="venture">{a["venture"]}</span>'
    return f"""<a class="area-card reveal" href="{a['slug']}.html" style="--area:{a['color']}">
        <span class="area-index">0{AREAS.index(a)+1}</span>
        {area_glyph(a['slug'])}
        {venture}
        <h3>{a['name']}</h3>
        <p class="purpose">{a['purpose']}</p>
        <p class="detail">{a['detail']}</p>
        <span class="card-cta">Explore {a['name']} &rsaquo;</span>
      </a>"""

def case_card(c, filterable=True):
    color = AREA_COLOR.get(c["areas"][0], "#0d2740")
    tags = "".join(f"<span>{t}</span>" for t in c["tags"])
    link = ""
    if c.get("link"):
        link = f'<a class="text-link" href="{c["link"]}" style="margin-top:1rem">{c.get("link_label","Visit")}</a>'
    data = f' data-areas="{" ".join(c["areas"])}"' if filterable else ""
    return f"""<article class="case-card reveal"{data} style="--area:{color}">
        <div class="mark" aria-hidden="true">&#9679;</div>
        <div class="case-body">
          <p class="kicker">{c['kicker']}</p>
          <h3>{c['name']}</h3>
          <p>{c['blurb']}</p>
          <p class="role"><strong>Greg's role:</strong> {c['role']}</p>
          <div class="tag-row">{tags}</div>
        </div>
        <div class="case-meta">
          <p class="status">{c['status']}</p>
          {link}
        </div>
      </article>"""

# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_home():
    roles = "".join(f"<span>{r}</span>" for r in ROLES)
    area_cards = "".join(area_card(a) for a in AREAS)
    method = "".join(
        f'<div class="process-step reveal"><span class="step-num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(METHOD))
    home_cases = "".join(case_card(CASE_BY_NAME[n], filterable=False) for n in
                         ["Convergence 2026", "Recreation Sound Systems", "TechShop STEAM Program", "Castellanos Coaching"])
    current = "".join(f'<div class="process-step reveal"><p>{c}</p></div>' for c in CURRENT)

    extra = [{
        "@type": "ProfessionalService", "name": NAME, "url": BASE_URL,
        "areaServed": "United States", "provider": {"@id": BASE_URL + "/#greg"},
        "knowsAbout": [a["name"] for a in AREAS],
    }]
    body = f"""    <section class="hero">
      <div class="hero-copy reveal">
        <p class="eyebrow">Gregory Castellanos · Bay Area &amp; Sonoma County</p>
        <h1>The one to call when the work is complicated and human.</h1>
        <p class="lede">Founder, learning designer, and executive-function coach. AI evaluator, live-event producer, and two-time U.S. patent holder. Twenty years, one throughline: see the whole system, understand the people inside it, and build the next step they can actually use.</p>
        <div class="cta-row">
          <a class="button primary" href="#ecosystem">Explore the work</a>
          <a class="button secondary" href="contact.html">Start a conversation</a>
        </div>
        <div class="identity-line">{roles}</div>
      </div>
      <div class="hero-art reveal">{ecosystem_art()}</div>
    </section>
    {proof_bar()}
    <section class="section" id="ecosystem">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Six-part ecosystem</p>
          <h2>Six lanes, one practice.</h2>
          <p>Each area has its own focus and a shared way of working: understand the people, shape the system, and make the next step usable.</p>
        </div>
        <div class="ecosystem-grid">{area_cards}</div>
      </div>
    </section>
    <section class="section band">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">How it connects</p>
          <h2>Scattered parts, turned into a working whole.</h2>
          <p>The coaching practice uses Clarity, Alignment, Foundation, and Expansion. The broader practice keeps the same respect for sequence.</p>
        </div>
        <div class="process-grid">{method}</div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Selected work</p>
          <h2>Real proof across the ecosystem.</h2>
          <p>Public anchors and named productions — described without inventing outcomes or exposing details that should stay private.</p>
        </div>
        <div class="case-list">{home_cases}</div>
        <div class="cta-row reveal"><a class="button secondary" href="work.html">View all work &amp; case studies</a></div>
      </div>
    </section>
    <section class="section band-alt">
      <div class="container">
        <div class="feature-split reveal">
          <figure class="hero-figure portrait" style="margin:0;border-radius:0">
            <img src="assets/images/greg-production.jpg" alt="Greg Castellanos running graphics and playback from the production desk at a live gala." width="1200" height="1600" style="object-position:62% 55%" loading="lazy" decoding="async">
          </figure>
          <div class="copy">
            <p class="eyebrow">About Greg</p>
            <h2>Different fields, one consistent skill.</h2>
            <p>Education, coaching, AI, invention, events, and community programs all point to the same throughline: make ideas useful in real life. Greg's work is strongest when a project has people, moving parts, and a need for good judgment.</p>
            <a class="text-link" href="about.html">Read the full narrative</a>
          </div>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Current focus</p>
          <h2>What is active now.</h2>
        </div>
        <div class="process-grid" style="grid-template-columns:repeat(3,minmax(0,1fr))">{current}</div>
      </div>
    </section>
    {cta_band(full=True)}"""
    return page("index.html", f"{NAME} | People, Ideas, Brands, Technology, Experiences, Places",
                "The umbrella site for Gregory Castellanos — a Bay Area founder, learning designer, executive function coach, AI evaluation specialist, event producer, and inventor.",
                body, active="index.html", extra_ld=extra, body_class="home")

def build_area(a):
    idx = "".join(
        f'<span><strong>0{i+1}</strong>{t}</span>' for i, t in enumerate(a["index"]))
    copy = "".join(f'<article><h2>{h}</h2><p>{p}</p></article>' for h, p in a["copy"])
    includes = "".join(f"<li>{i}</li>" for i in a["includes"])
    related = "".join(
        case_card(CASE_BY_NAME[n], filterable=False) for n in a["related"] if n in CASE_BY_NAME)
    cta_primary = f'<a class="button primary" href="{a["cta_href"]}">{a["cta"]}</a>'
    hero_img = a.get("hero_image")
    if hero_img:
        hero_class = "hero page-hero"
        hero_fig = (f'<figure class="hero-figure reveal"><img src="assets/images/{hero_img}" '
                    f'alt="{a.get("hero_alt", "")}" width="1200" height="1600" '
                    f'style="aspect-ratio:3/4" loading="eager" decoding="async"></figure>')
    else:
        hero_class = "hero page-hero text-hero"
        hero_fig = ""

    extra = [{
        "@type": "Service", "serviceType": a["name"], "name": a["venture"],
        "provider": {"@id": BASE_URL + "/#greg"}, "areaServed": "United States",
        "description": a["purpose"],
    }]
    body = f"""    <section class="{hero_class}" style="--area:{a['color']}">
      <div class="hero-copy reveal">
        <p class="eyebrow">{a['name']} · {a['venture']}</p>
        <h1>{a['hero_h1']}</h1>
        <p class="lede">{a['hero_lede']}</p>
        <div class="cta-row">{cta_primary}<a class="button secondary" href="work.html">See related work</a></div>
      </div>
      {hero_fig}
    </section>
    <section class="section tight">
      <div class="container">
        <div class="split">
          <div class="stacked reveal">{copy}</div>
          <aside class="reveal">
            <p class="eyebrow">Includes</p>
            <ul class="rule-list">{includes}</ul>
          </aside>
        </div>
      </div>
    </section>
    <section class="section band">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Related work</p>
          <h2>{a['name']} connects with the wider ecosystem.</h2>
          <p>A few anchors from the broader practice.</p>
        </div>
        <div class="case-list">{related}</div>
      </div>
    </section>
    <section class="section reveal">
      <div class="cta-band split-cta full" style="border-radius:0">
        <h2 style="margin:0">Have a {a['name'].lower()} question that needs judgment and shape?</h2>
        <div class="cta-row"><a class="button secondary" href="contact.html">Talk with Greg</a></div>
      </div>
    </section>"""
    return page(f"{a['slug']}.html", f"{a['name']} | {NAME}", a["purpose"], body,
                active=f"{a['slug']}.html", extra_ld=extra, area_color=a["color"],
                body_class=f"area-page {a['slug']}")

def build_work():
    filters = '<span class="filter-label">Filter</span><button class="filter is-active" type="button" data-filter="all">All</button>' + \
        "".join(f'<button class="filter" type="button" data-filter="{a["slug"]}">{a["name"]}</button>' for a in AREAS)
    cases = "".join(case_card(c) for c in CASES)
    item_list = [{"@type": "ListItem", "position": i + 1, "name": c["name"]} for i, c in enumerate(CASES)]
    extra = [{"@type": "ItemList", "name": "Selected work", "itemListElement": item_list}]
    body = f"""    <section class="hero page-hero text-hero">
      <div class="hero-copy reveal">
        <p class="eyebrow">Work &amp; case studies</p>
        <h1>Selected work across six connected practices.</h1>
        <p class="lede">Projects often cross more than one lane. This index shows the range with real detail — without turning private work into a public case study.</p>
      </div>
    </section>
    <section class="section tight">
      <div class="container">
        <div class="filter-panel reveal" aria-label="Filter work by area">{filters}</div>
        <div class="case-list">{cases}</div>
      </div>
    </section>
    {cta_band(full=True, heading="See a lane that fits your project?", text="Tell Greg what you are building, changing, or trying to solve.")}"""
    return page("work.html", f"Work &amp; Case Studies | {NAME}",
                "Selected work across Gregory Castellanos's six connected practices — coaching, strategy, brand, technology, events, and places.",
                body, extra_ld=extra)

def build_about():
    tl = "".join(f'<span><strong>{y}</strong>{t}</span>' for y, t in TIMELINE)
    rec = "".join(f"<li>{r}</li>" for r in RECOGNITION)
    cred = "".join(f"<li>{c}</li>" for c in CREDENTIALS)
    domains = "".join(f"<span>{d}</span>" for d in SKILL_DOMAINS)
    narrative = [
        ("The throughline",
         "This is not a random sequence of pivots. Greg sees the system, understands the people inside it, connects disciplines, and makes the next move practical. Twenty years, one skill."),
        ("Learning, technology, and making",
         "A B.A. in Interactive Multimedia and a Master of Arts in Teaching (both with Honors), a STEAM program adopted across TechShop locations nationwide, and AI-literacy teaching today all point to one question: how do people learn, adapt, and make better decisions with better tools?"),
        ("Sound, events, and operations",
         "Two U.S. patents for resonance-based audio and a decade of live production built technical fluency and calm under pressure — from a sold-out 250-person production to supporting corporate shows for the world's leading technology companies."),
        ("People, place, and systems",
         "Castellanos Coaching, consulting, creative direction, and Common Ground Works sit under one umbrella because they all involve people, environments, and decisions that need to become usable."),
    ]
    narr = "".join(f'<article><h2>{h}</h2><p>{p}</p></article>' for h, p in narrative)
    quotes = "".join(
        f'<figure class="quote-card reveal" style="margin:0"><blockquote>&ldquo;{q}&rdquo;</blockquote>'
        f'<figcaption class="attr">{name} · {role}</figcaption></figure>'
        for q, name, role in TESTIMONIALS)
    extra = [{
        "@type": "AboutPage", "@id": BASE_URL + "/about.html#about",
        "mainEntity": {"@id": BASE_URL + "/#greg"},
    }]
    body = f"""    <section class="hero page-hero">
      <div class="hero-copy reveal">
        <p class="eyebrow">About</p>
        <h1>A multidisciplinary career built around making complicated things workable.</h1>
        <p class="lede">Greg has worked across education, coaching, technology, events, entrepreneurship, strategy, and place. The fields change. The pattern stays consistent.</p>
        <div class="chip-list" style="margin-top:1.75rem">{domains}</div>
      </div>
      <figure class="hero-figure portrait reveal">
        <img src="assets/images/greg-headshot.jpg" alt="Portrait of Gregory Castellanos." width="514" height="738" loading="eager" decoding="async" fetchpriority="high">
        <figcaption>Greg Castellanos · Bay Area / Sonoma County, CA</figcaption>
      </figure>
    </section>
    <section class="section tight">
      <div class="container">
        <div class="split">
          <div class="stacked reveal">{narr}</div>
          <aside class="reveal">
            <p class="eyebrow">Selected milestones</p>
            <div class="hero-index" style="border-top:0">{tl}</div>
          </aside>
        </div>
      </div>
    </section>
    <section class="section band">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <p class="eyebrow">Recognition</p>
            <ul class="rule-list">{rec}</ul>
          </div>
          <div class="reveal">
            <p class="eyebrow">Education &amp; credentials</p>
            <ul class="rule-list">{cred}</ul>
          </div>
        </div>
      </div>
    </section>
    <section class="section tight">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <p class="eyebrow">Beyond the work</p>
            <h2>Bay Area born, happiest with a project and a mountain nearby.</h2>
            <p style="color:var(--muted);margin-top:1rem">Greg lives and works between the Bay Area and Sonoma County. Snowboarding, radio, music, and time outdoors keep the ideas moving as much as the work does — and keep the practice grounded in real life.</p>
          </div>
          <figure class="hero-figure reveal" style="margin:0">
            <img src="assets/images/greg-outdoors.jpg" alt="Greg Castellanos in the snow-covered Sierra." width="1200" height="1600" style="aspect-ratio:3/4" loading="lazy" decoding="async">
          </figure>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">In their words</p>
          <h2>Voices from the coaching work.</h2>
          <p>Real words from Castellanos Coaching clients. Nothing here is invented, and testimonials are shared only with permission.</p>
        </div>
        <div class="quote-grid">{quotes}</div>
      </div>
    </section>
    <section class="section band-alt">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Speaking &amp; teaching</p>
          <h2>Topics for schools, parent groups, organizations, retreats, and panels.</h2>
        </div>
        <div class="chip-list reveal">{"".join(f"<span>{t}</span>" for t in SPEAKING_TOPICS)}</div>
        <div class="cta-row reveal"><a class="button secondary" href="speaking.html">View speaking topics</a></div>
      </div>
    </section>
    {cta_band(full=True)}"""
    return page("about.html", f"About | {NAME}",
                "The narrative behind Gregory Castellanos — two decades across education, coaching, invention, AI, events, and community, with the credentials and milestones behind the work.",
                body, extra_ld=extra)

def build_speaking():
    topics = "".join(f'<span><strong>0{i+1}</strong>{t}</span>' for i, t in enumerate(SPEAKING_TOPICS[:6]))
    formats = "".join(f"<span>{f}</span>" for f in SPEAKING_FORMATS)
    body = f"""    <section class="hero page-hero">
      <div class="hero-copy reveal">
        <p class="eyebrow">Speaking &amp; teaching</p>
        <h1>Talks and workshops that make complex ideas practical.</h1>
        <p class="lede">Greg teaches where human development, creativity, technology, entrepreneurship, and community meet — backed by a Master of Arts in Teaching and twenty years in classrooms, makerspaces, and community programs.</p>
        <div class="cta-row"><a class="button primary" href="contact.html">Ask about availability</a></div>
      </div>
      <aside class="hero-index reveal">{topics}</aside>
    </section>
    <section class="section band">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Formats</p>
          <h2>Useful in rooms where people need language, structure, and next steps.</h2>
          <p>Formats can be shaped around the audience and setting.</p>
        </div>
        <div class="chip-list reveal">{formats}</div>
      </div>
    </section>
    {cta_band(full=True, heading="Invite Greg for a workshop, class, panel, conference, or retreat.", text="Share the audience, setting, and goal, and Greg will shape something that fits.")}"""
    return page("speaking.html", f"Speaking &amp; Teaching | {NAME}",
                "Speaking and teaching topics from Gregory Castellanos — executive function, AI literacy, education, entrepreneurship, community, and experience design.",
                body)

def build_contact():
    options = "".join(f"<option>{a['name']}</option>" for a in AREAS)
    faq = "".join(
        f'<details class="reveal"><summary>{q}</summary><div class="faq-body">{ans}</div></details>'
        for q, ans in FAQ)
    faq_ld = [{
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": html.unescape(q).replace("<a href=\"" + COACHING_URL + "\">castellanoscoaching.com</a>", "castellanoscoaching.com"),
             "acceptedAnswer": {"@type": "Answer", "text": _strip_tags(a)}}
            for q, a in FAQ
        ],
    }]
    body = f"""    <section class="hero page-hero text-hero">
      <div class="hero-copy reveal">
        <p class="eyebrow">Contact</p>
        <h1>Tell Greg what you are building, changing, or trying to solve.</h1>
        <p class="lede">Start with a simple note. Coaching, strategy, brand, technology, events, teaching, place work, and unusual collaborations are all welcome.</p>
      </div>
    </section>
    <section class="section tight">
      <div class="container">
        <div class="contact-layout">
          <form class="contact-form reveal" id="contact-form" novalidate>
            <input class="honeypot" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
            <input type="hidden" name="startedAt" id="startedAt">
            <label>Name <input name="name" required autocomplete="name"></label>
            <label>Email <input name="email" type="email" required autocomplete="email"></label>
            <label>Organization <span style="font-weight:400;color:var(--muted)">(optional)</span> <input name="organization" autocomplete="organization"></label>
            <label>Area of interest
              <select name="area" required>
                <option value="">Select one</option>
                {options}
                <option>Speaking &amp; teaching</option>
                <option>General collaboration</option>
              </select>
            </label>
            <label>Brief description <textarea name="message" rows="6" required></textarea></label>
            <label>Desired timing <span style="font-weight:400;color:var(--muted)">(optional)</span> <input name="timing"></label>
            <label>How you heard about Greg <span style="font-weight:400;color:var(--muted)">(optional)</span> <input name="referral"></label>
            <button class="button primary" type="submit">Prepare email inquiry</button>
            <p class="form-note" id="form-note" aria-live="polite"></p>
          </form>
          <aside class="contact-aside reveal">
            <div class="contact-block">
              <p class="eyebrow">Direct email</p>
              <a href="mailto:{EMAIL}">{EMAIL}</a>
              <p style="margin-top:.75rem;color:var(--muted)">For coaching specifically, visit <a href="{COACHING_URL}">castellanoscoaching.com</a>.</p>
            </div>
            <div class="contact-block">
              <h2>Reach out for</h2>
              <ul>
                <li>Coaching fit or family support</li>
                <li>Strategy, brand, or creative direction</li>
                <li>AI, education, or technology projects</li>
                <li>Events, retreats, speaking, or place work</li>
              </ul>
            </div>
          </aside>
        </div>
      </div>
    </section>
    <section class="section band">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Questions</p>
          <h2>Good to know before you write.</h2>
        </div>
        <div class="faq">{faq}</div>
      </div>
    </section>"""
    return page("contact.html", f"Contact | {NAME}",
                "Contact Gregory Castellanos about coaching, consulting, brand, technology, experiences, places, speaking, teaching, and collaboration.",
                body, extra_ld=faq_ld)

def build_privacy():
    blocks = [
        ("Private by design",
         "This site intentionally avoids publishing private client, family, student, venue, property-owner, address, medical, legal, financial, or confidential business information."),
        ("Honest claims only",
         "Private work is described at a high level. Outcomes, figures, awards, testimonials, and partnerships are never invented, and estimates are phrased conservatively. Client productions are credited through the production companies Greg worked with."),
        ("Contact and forms",
         "The contact form runs entirely in your browser and simply prepares an email draft — no inquiry data is stored or sent to a third party without you clicking send. Any future server-side form handling would use spam protection and clear consent."),
        ("Analytics",
         "No third-party analytics or tracking scripts are loaded on this site. Your theme preference is stored locally in your browser only."),
    ]
    inner = "".join(f'<article><h2>{h}</h2><p>{p}</p></article>' for h, p in blocks)
    body = f"""    <section class="hero page-hero text-hero">
      <div class="hero-copy reveal">
        <p class="eyebrow">Privacy</p>
        <h1>Privacy and accuracy matter here.</h1>
        <p class="lede">A short, plain-language note on how this site handles information — and how Greg describes private work.</p>
      </div>
    </section>
    <section class="section tight">
      <div class="container">
        <div class="stacked reveal" style="max-width:52rem">{inner}</div>
      </div>
    </section>"""
    return page("privacy.html", f"Privacy | {NAME}",
                "Privacy and accuracy notes for gregcastellanos.com.", body)

def build_404():
    body = f"""    <section class="hero page-hero text-hero" style="min-height:50vh">
      <div class="hero-copy reveal">
        <p class="eyebrow">404</p>
        <h1>This page is not here.</h1>
        <p class="lede">The work may have moved, been renamed, or not been published yet.</p>
        <div class="cta-row">
          <a class="button primary" href="index.html">Return home</a>
          <a class="button secondary" href="work.html">View the work</a>
        </div>
      </div>
    </section>"""
    return page("404.html", f"Page Not Found | {NAME}",
                "The requested page could not be found.", body)

def _strip_tags(s):
    import re
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

# --------------------------------------------------------------------------
def build_sitemap():
    urls = ["/"] + ["/" + href for _l, href in NAV if href != "index.html"] + ["/speaking.html", "/privacy.html"]
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        body += f"  <url><loc>{BASE_URL}{u}</loc></url>\n"
    body += "</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(body)

def main():
    written = [build_home()]
    for a in AREAS:
        written.append(build_area(a))
    written.append(build_work())
    written.append(build_about())
    written.append(build_speaking())
    written.append(build_contact())
    written.append(build_privacy())
    written.append(build_404())
    build_sitemap()
    print("Generated:", ", ".join(written), "+ sitemap.xml")

if __name__ == "__main__":
    main()
