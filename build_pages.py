#!/usr/bin/env python3
"""Generates one landing page per service (/<slug>/index.html) and sitemap.xml.

A single homepage can only rank for a handful of searches. Each page here
targets what customers actually type into Google ("sewage tanker dubai",
"sweet water tanker dubai", "tse water supply dubai", ...) the same way the
competitors that rank for those searches do.

To change the copy, edit SERVICES below and re-run:

    python build_pages.py
"""
import datetime, hashlib, html, json, os
from urllib.parse import quote

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://salmanmohammadtransport.ae'
PHONE, PHONE_DISPLAY = '+971559449223', '+971 55 944 9223'
PHONE2, PHONE2_DISPLAY = '+97145806482', '04 580 6482'
EMAIL = 'info@salmanmohammadtransport.ae'
WHATSAPP = 'https://wa.me/message/RNEF42WRMKX4E1'
INSTAGRAM = 'https://www.instagram.com/smt.dxb/'

AREAS = [
    'Al Qusais', 'Deira', 'Bur Dubai', 'Al Nahda', 'Muhaisnah', 'Mirdif',
    'Al Quoz', 'Jebel Ali', 'Dubai Investment Park', 'Dubai Silicon Oasis',
    'International City', 'Business Bay', 'Downtown Dubai', 'Jumeirah',
    'Al Barsha', 'JVC', 'Dubai Marina', 'Palm Jumeirah',
]

# form_name must match an <option> in the quote form on index.html, so the
# "Request a Quote" button can pre-select it (/#quote=<form_name>).
SERVICES = [
    dict(
        slug='sewage-tanker-dubai',
        name='Sewage Removal',
        form_name='Sewage Removal',
        category='env',
        title='Sewage Tanker Service in Dubai | 24/7 Removal | SMT',
        description='Sewage tanker service in Dubai for septic tank, sewage and wastewater removal. Municipality-compliant disposal, one-off or monthly, 24/7.',
        h1='Sewage Tanker Service in Dubai',
        lead='Septic tank full or sewage backing up? We send a sewage tanker to your site anywhere in Dubai, day or night, and dispose of the waste in line with Dubai Municipality rules.',
        image='/assets/about/about-2-sewage.jpg', image_size=(1000, 700),
        image_alt='SMT sewage tanker on site in Dubai',
        cta='Need a sewage tanker in Dubai today?',
        area_intro='Our sewage tankers operate across Dubai, including:',
        body='''
<h2>Sewage and wastewater removal, handled properly</h2>
<p>Our tankers collect sewage, septic waste and wastewater from villas, residential buildings, labour accommodation, construction sites, restaurants, warehouses and industrial units. Every load goes to an authorised disposal point, so you're never exposed to fines for improper disposal.</p>
<h2>Who we work with</h2>
<ul>
  <li>Villas and buildings on septic tanks or without a sewer connection</li>
  <li>Construction sites and labour camps</li>
  <li>Restaurants, hotels and commercial kitchens</li>
  <li>Warehouses, factories and industrial areas</li>
  <li>Facilities management companies running multiple sites</li>
</ul>
<h2>One-off pickups or a scheduled contract</h2>
<p>Need a single tank emptied? Call us and we'll dispatch a tanker. If your tank fills regularly, a monthly contract puts it on a fixed collection schedule so it never overflows. That's ideal for camps, sites and buildings that aren't connected to the sewer network.</p>
<h2>How it works</h2>
<ol>
  <li>Tell us the location, the approximate tank size and how soon you need it.</li>
  <li>We confirm the price and send the right size tanker.</li>
  <li>Our crew empties the tank and leaves the area clean.</li>
  <li>The waste is taken to an authorised disposal facility.</li>
</ol>
''',
        faqs=[
            ('How quickly can you send a sewage tanker?',
             'Our fleet runs 24/7. Call <a href="tel:+971559449223">+971 55 944 9223</a> with your location and we\'ll give you an arrival time straight away. Urgent jobs are prioritised.'),
            ('How much does sewage removal cost in Dubai?',
             'The price depends on the volume to be removed, your location and how urgent the job is. Tell us those three things and we\'ll quote before we dispatch, with no surprises afterwards.'),
            ('Is the sewage disposed of legally?',
             'Yes. All waste goes to authorised disposal facilities in line with Dubai Municipality requirements.'),
            ('Do you offer monthly sewage collection contracts?',
             'Yes. Many of our clients, including construction sites, labour camps and buildings without a sewer connection, are on scheduled collections. Choose "Monthly / Recurring" in the quote form and we\'ll call to set it up.'),
            ('Which areas do you cover?',
             'We\'re based in Al Qusais and serve the whole Emirate of Dubai. Our services are available within the Emirate of Dubai only.'),
        ],
    ),
    dict(
        slug='sweet-water-tanker-dubai',
        name='Sweet Water Tanker',
        form_name='Sweet Water Supply',
        category='env',
        title='Sweet Water Tanker Dubai | Pool & Site Delivery | SMT',
        description='Sweet water tanker delivery across Dubai for swimming pools, villas, building tanks and construction sites. Fast 24/7 delivery, one-off or monthly supply.',
        h1='Sweet Water Tanker Supply in Dubai',
        lead='Clean sweet water delivered by tanker to your pool, villa, building or site anywhere in Dubai, as a one-off or on a regular schedule, 24/7.',
        image='/assets/services/sweet-water.jpg', image_size=(566, 184),
        image_alt='Sweet water tanker delivering in Dubai',
        cta='Need a sweet water tanker in Dubai?',
        area_intro='We deliver sweet water across Dubai, including:',
        body='''
<h2>What sweet water is used for</h2>
<p>Sweet water is fresh, low-salinity water. It's the right choice for filling swimming pools, topping up villa and building water tanks, and for construction work such as concrete mixing and curing.</p>
<ul>
  <li>Swimming pool filling and top-ups</li>
  <li>Villa and building water tanks</li>
  <li>Construction sites: concrete mixing, curing and site use</li>
  <li>Landscaping, gardens and vehicle washing</li>
  <li>Events and temporary sites</li>
</ul>
<h2>Swimming pool filling</h2>
<p>Filling a pool from a garden hose can take days and push up your water bill. A sweet water tanker fills it in one visit. Tell us the pool size and we'll work out how much water you need.</p>
<h2>Daily or monthly supply for sites</h2>
<p>Construction and industrial sites that use water every day can set up a scheduled supply. We deliver on the days you need, so work never stops waiting for water.</p>
<h2>How it works</h2>
<ol>
  <li>Tell us where the water is going and roughly how much you need.</li>
  <li>We confirm the price and a delivery time.</li>
  <li>The tanker arrives and fills your pool, tank or site storage.</li>
</ol>
''',
        faqs=[
            ('How much does a sweet water tanker cost in Dubai?',
             'The price depends on how much water you need, your location and the delivery time. Share those details and we\'ll quote you upfront.'),
            ('How much water do I need to fill my pool?',
             'Multiply length × width × average depth in metres to get cubic metres. One cubic metre is 1,000 litres (about 220 imperial gallons). Send us your pool size and we\'ll calculate it for you.'),
            ('Is sweet water the same as drinking water?',
             'No. Sweet water is fresh water for pools, tanks and construction. If you need water that\'s fit to drink, see our <a href="/drinking-water-supply-dubai/">drinking water supply</a>.'),
            ('Can you deliver today?',
             'Our fleet runs 24/7, so urgent deliveries are often possible. Call <a href="tel:+971559449223">+971 55 944 9223</a> to check availability.'),
            ('Which areas do you cover?',
             'We serve the whole Emirate of Dubai. Our services are available within the Emirate of Dubai only.'),
        ],
    ),
    dict(
        slug='salt-water-tanker-dubai',
        name='Salt Water Tanker',
        form_name='Salt Water Supply',
        category='env',
        title='Salt Water Tanker Supply in Dubai | SMT Transport',
        description='Salt water tanker supply in Dubai for soil compaction, backfilling, piling and construction groundworks. Reliable daily or monthly delivery to your site.',
        h1='Salt Water Tanker Supply in Dubai',
        lead='Bulk salt water delivered to construction and infrastructure sites across Dubai, for compaction, piling and other groundworks where fresh water isn\'t required.',
        image='/assets/services/salt-water.jpg', image_size=(566, 184),
        image_alt='Salt water tanker for construction in Dubai',
        cta='Need salt water delivered to your site?',
        area_intro='We supply salt water to sites across Dubai, including:',
        body='''
<h2>Why contractors use salt water</h2>
<p>Many earthworks don't need fresh water. Where the project specification allows it, using salt water for soil compaction, backfilling and piling keeps costs down and saves fresh water for where it's really needed.</p>
<ul>
  <li>Soil compaction and backfilling</li>
  <li>Piling works</li>
  <li>Road and infrastructure earthworks</li>
  <li>Site preparation and groundworks</li>
</ul>
<h2>Supply that keeps pace with your site</h2>
<p>Groundworks get through a lot of water. We set up daily or weekly deliveries matched to your programme, and you can call any time to add an extra load.</p>
<h2>How it works</h2>
<ol>
  <li>Tell us the site location, the volume you need and how often.</li>
  <li>We agree a price and a delivery schedule.</li>
  <li>Our tankers deliver on schedule, and extra loads are one call away.</li>
</ol>
''',
        faqs=[
            ('What is salt water used for in construction?',
             'Mainly soil compaction, backfilling and piling, where the project specification allows it. Check with your consultant if you\'re unsure.'),
            ('How much does a salt water tanker cost?',
             'It depends on the quantity, how often you need deliveries and where the site is. Tell us and we\'ll quote upfront.'),
            ('Can you supply salt water every day?',
             'Yes. Choose "Monthly / Recurring" in the quote form and we\'ll set up a schedule that matches your works.'),
            ('Can you supply sweet water to the same site?',
             'Yes, many sites need both. See our <a href="/sweet-water-tanker-dubai/">sweet water tanker service</a> and we can combine them on one schedule.'),
        ],
    ),
    dict(
        slug='drinking-water-supply-dubai',
        name='Drinking Water Supply',
        form_name='Potable Water Supply',
        category='env',
        title='Drinking Water Tanker Supply in Dubai | SMT Transport',
        description='Potable (drinking) water supply by tanker across Dubai for buildings, labour camps and sites. Scheduled or one-off delivery, available 24/7.',
        h1='Drinking Water (Potable Water) Supply in Dubai',
        lead='Potable water delivered by tanker to buildings, labour accommodation, sites and facilities across Dubai when the mains supply is interrupted, unavailable or not enough.',
        image='/assets/services/sweet-water.jpg', image_size=(566, 184),
        image_alt='Potable water tanker in Dubai',
        cta='Need drinking water delivered in Dubai?',
        area_intro='We deliver potable water across Dubai, including:',
        body='''
<h2>When you need potable water by tanker</h2>
<ul>
  <li>Buildings and villas during a supply interruption</li>
  <li>Labour accommodation and camps</li>
  <li>Construction sites and site offices</li>
  <li>Farms and locations without a mains connection</li>
  <li>Events and temporary facilities</li>
</ul>
<h2>Regular supply for camps and sites</h2>
<p>Accommodation and sites that rely on tanker water need it to arrive on time, every time. We schedule deliveries around your consumption so storage tanks never run dry.</p>
<h2>Potable water or sweet water?</h2>
<p>Potable water is water that's fit to drink. Sweet water is fresh water for pools, tanks and construction and isn't intended for drinking. If you're not sure which you need, tell us what the water is for and we'll advise. For pools and site use, see our <a href="/sweet-water-tanker-dubai/">sweet water tanker service</a>.</p>
<h2>How it works</h2>
<ol>
  <li>Tell us the location, the volume and how often you need it.</li>
  <li>We confirm the price and a delivery time or schedule.</li>
  <li>The tanker fills your storage tank on site.</li>
</ol>
''',
        faqs=[
            ('What\'s the difference between potable water and sweet water?',
             'Potable water is fit for drinking. Sweet water is fresh water for pools, tanks and construction. It isn\'t intended for drinking.'),
            ('How much does potable water delivery cost?',
             'It depends on the volume, the location and how often you need deliveries. Share those details and we\'ll quote upfront.'),
            ('Can you set up a daily delivery to our camp or site?',
             'Yes. Choose "Monthly / Recurring" in the quote form and we\'ll call to plan a schedule around your usage.'),
            ('Which areas do you cover?',
             'We serve the whole Emirate of Dubai. Our services are available within the Emirate of Dubai only.'),
        ],
    ),
    dict(
        slug='tse-water-supply-dubai',
        name='TSE Water Supply',
        form_name='TSE Water Supply',
        category='env',
        title='TSE Water Supply in Dubai | Irrigation Water | SMT',
        description='TSE (treated sewage effluent) water supply by tanker in Dubai for irrigation, landscaping, parks and farms. Scheduled delivery, available 24/7.',
        h1='TSE Water Supply in Dubai',
        lead='TSE (treated sewage effluent) is recycled water that\'s ideal for irrigation and landscaping. We deliver it by tanker to villas, parks, farms and project sites across Dubai.',
        image='/assets/services/sweet-water.jpg', image_size=(566, 184),
        image_alt='TSE irrigation water tanker in Dubai',
        cta='Need TSE water for irrigation?',
        area_intro='We deliver TSE water across Dubai, including:',
        body='''
<h2>What is TSE water?</h2>
<p>TSE is wastewater that has been treated to a standard suitable for reuse in irrigation and other non-drinking uses. It isn't for drinking or swimming pools, but for watering landscapes it's a sensible, lower-cost alternative to fresh water that puts treated water back to use.</p>
<h2>Where TSE is used</h2>
<ul>
  <li>Landscaping and garden irrigation</li>
  <li>Parks, green belts and open spaces</li>
  <li>Farms and plantations</li>
  <li>Construction uses where the specification allows it</li>
</ul>
<h2>Scheduled irrigation supply</h2>
<p>Landscaping needs water every day, especially in summer. We set up recurring deliveries that match your irrigation cycle, so planting never goes without.</p>
<h2>How it works</h2>
<ol>
  <li>Tell us the location, the volume and how often you irrigate.</li>
  <li>We agree a price and a delivery schedule.</li>
  <li>Our tankers deliver on schedule, all year round.</li>
</ol>
''',
        faqs=[
            ('What is TSE water used for?',
             'Mainly irrigation: landscaping, parks, green belts and farms. It\'s also used in some construction applications where the specification allows it.'),
            ('Is TSE water safe?',
             'TSE is treated for reuse in irrigation and similar non-drinking applications. It must not be used for drinking, cooking or swimming pools.'),
            ('Is TSE cheaper than sweet water?',
             'For irrigation it\'s usually the more economical choice. Tell us your volume and schedule and we\'ll quote both so you can compare.'),
            ('Can you deliver TSE on a monthly contract?',
             'Yes. Choose "Monthly / Recurring" in the quote form and we\'ll set up a schedule with you.'),
        ],
    ),
    dict(
        slug='waste-management-dubai',
        name='Waste Management',
        form_name='Waste Management',
        category='env',
        title='Waste Management & Collection in Dubai | SMT Transport',
        description='Waste collection and disposal in Dubai for construction sites, businesses and industrial units. Municipality-compliant, one-off clearances or scheduled pickups.',
        h1='Waste Management Services in Dubai',
        lead='Waste collection and disposal for construction sites, commercial premises and industrial operators across Dubai, collected on your schedule and disposed of in line with Dubai Municipality rules.',
        image='/assets/services/waste-management.jpg', image_size=(566, 184),
        image_alt='Waste collection and skip loading in Dubai',
        cta='Need waste collected in Dubai?',
        area_intro='We collect waste across Dubai, including:',
        body='''
<h2>End-to-end waste handling</h2>
<p>From one-off site clearances to regular collections, we take care of loading, transport and disposal so you don't have to. Tell us what you need to get rid of. If it's something we don't handle, we'll say so straight away.</p>
<ul>
  <li>General commercial waste</li>
  <li>Construction and demolition debris</li>
  <li>Sludge and liquid waste (see our <a href="/sewage-tanker-dubai/">sewage tanker service</a>)</li>
  <li>Non-hazardous industrial waste</li>
</ul>
<h2>One-off clearances and scheduled collections</h2>
<p>Clearing a site at handover, or generating waste every week? We handle both, with collections timed around your operation so waste never piles up.</p>
<h2>Compliant disposal</h2>
<p>Everything we collect goes to authorised disposal facilities. You get a reliable partner and no risk of penalties for improper disposal.</p>
''',
        faqs=[
            ('How much does waste collection cost in Dubai?',
             'It depends on the type and volume of waste, your location and how often you need collections. Tell us and we\'ll quote upfront.'),
            ('How often can you collect?',
             'As often as you need, from a single clearance to daily or weekly pickups. Choose "Monthly / Recurring" in the quote form for a schedule.'),
            ('Do you handle liquid waste and sludge?',
             'Yes. Our <a href="/sewage-tanker-dubai/">sewage tankers</a> collect sewage, sludge and wastewater.'),
            ('Is disposal compliant with Dubai Municipality rules?',
             'Yes. All waste goes to authorised facilities.'),
        ],
    ),
    dict(
        slug='container-transport-dubai',
        name='Container Transport',
        form_name='Container Hauling',
        category='freight',
        title='Container Transport & Haulage in Dubai | SMT Transport',
        description='Container transport and haulage across the Emirate of Dubai. Port, free zone, warehouse and site moves for 20ft and 40ft containers. Get a fast quote.',
        h1='Container Transport &amp; Haulage in Dubai',
        lead='Reliable container haulage between ports, free zones, warehouses and project sites across the Emirate of Dubai.',
        image='/assets/about/about-1-fleet.jpg', image_size=(1000, 700),
        image_alt='SMT container haulage truck on the highway',
        cta='Need a container moved?',
        area_intro='We move containers across Dubai, including:',
        body='''
<h2>What we move</h2>
<ul>
  <li>20ft and 40ft shipping containers</li>
  <li>Port and free zone container moves</li>
  <li>Warehouse and project site deliveries</li>
  <li>Heavy haulage within Dubai</li>
</ul>
<h2>Planned around your schedule</h2>
<p>Containers have free-time windows and sites have delivery slots. We plan pick-ups and drop-offs to fit, keep you updated, and deliver to the gate on time.</p>
<h2>Dubai-wide coverage</h2>
<p>From our base in Al Qusais, we run container transport throughout the Emirate of Dubai, covering port, free zone, industrial area and site moves.</p>
<h2>How it works</h2>
<ol>
  <li>Tell us the container size, the pick-up and drop-off points, and your dates.</li>
  <li>We confirm the price and book the move.</li>
  <li>We collect and deliver on schedule, keeping you updated along the way.</li>
</ol>
''',
        faqs=[
            ('How much does container transport cost in Dubai?',
             'It depends on the container size, the distance and any waiting time. Send us the details and we\'ll quote upfront.'),
            ('Which container sizes do you move?',
             'Standard 20ft and 40ft containers. If you have something non-standard, call us to discuss.'),
            ('Which areas do you cover?',
             'We move containers anywhere in the Emirate of Dubai, including Jebel Ali, Dubai Investment Park and Al Quoz. Our services are available within the Emirate of Dubai only.'),
            ('Can we set up a regular haulage contract?',
             'Yes. Choose "Monthly / Recurring" in the quote form and we\'ll call to plan it with you.'),
        ],
    ),
    dict(
        slug='diesel-supply-dubai',
        name='Diesel Supply',
        form_name='Diesel Supply',
        category='freight',
        title='Diesel Supply in Dubai | On-Site Fuel Delivery | SMT',
        description='On-site diesel delivery in Dubai for generators, construction plant and vehicle fleets. Scheduled or on-demand refuelling, available 24/7.',
        h1='Diesel Supply &amp; On-Site Fuel Delivery in Dubai',
        lead='We deliver diesel directly to your generators, machinery and fleet, on site and on schedule, so your operation never stops for fuel.',
        image='/assets/about/about-3-diesel.jpg', image_size=(1000, 700),
        image_alt='SMT diesel bowser refuelling on site in Dubai',
        cta='Need diesel delivered to your site?',
        area_intro='We deliver diesel across Dubai, including:',
        body='''
<h2>Who we refuel</h2>
<ul>
  <li>Generators on construction sites, events and facilities</li>
  <li>Construction plant and heavy equipment</li>
  <li>Vehicle and truck fleets</li>
  <li>Industrial and backup power systems</li>
</ul>
<h2>Scheduled or on demand</h2>
<p>Set up regular refuelling so tanks are topped up before they run low, or call when you need an urgent delivery. Our fleet runs 24/7.</p>
<h2>Why on-site delivery?</h2>
<p>Driving equipment to a fuel station costs time and money, and some machines can't move at all. On-site delivery keeps machines working and takes fuel runs off your team's day.</p>
<h2>How it works</h2>
<ol>
  <li>Tell us the location, the equipment and roughly how much diesel you need.</li>
  <li>We confirm the price and a delivery time or schedule.</li>
  <li>Our bowser refuels your equipment on site.</li>
</ol>
''',
        faqs=[
            ('How much does diesel delivery cost in Dubai?',
             'The price follows the current diesel price plus delivery, and depends on quantity and location. Call or request a quote for today\'s rate.'),
            ('Can you refuel our generators on a schedule?',
             'Yes. Choose "Monthly / Recurring" in the quote form and we\'ll set up regular top-ups.'),
            ('Do you deliver at night or at weekends?',
             'Our fleet runs 24/7. Call <a href="tel:+971559449223">+971 55 944 9223</a> to arrange a delivery time.'),
            ('Which areas do you cover?',
             'We serve the whole Emirate of Dubai. Our services are available within the Emirate of Dubai only.'),
        ],
    ),
]

esc = html.escape


def nav_links(current_slug):
    groups = [('env', 'Environmental'), ('freight', 'Freight')]
    out = []
    for key, label in groups:
        out.append('        <div class="dd-group">\n          <span class="dd-label">%s</span>' % label)
        for s in SERVICES:
            if s['category'] != key:
                continue
            cur = ' aria-current="page"' if s['slug'] == current_slug else ''
            out.append('          <a href="/%s/"%s>%s</a>' % (s['slug'], cur, s['name']))
        out.append('        </div>')
    return '\n'.join(out)


def json_ld(svc):
    url = '%s/%s/' % (SITE, svc['slug'])
    data = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Service',
                'name': html.unescape(svc['h1']),
                'serviceType': svc['name'],
                'description': svc['description'],
                'url': url,
                'areaServed': {'@type': 'City', 'name': 'Dubai'},
                'provider': {
                    '@type': 'LocalBusiness',
                    '@id': SITE + '/#business',
                    'name': 'Salman Mohammad Transport LLC',
                    'url': SITE + '/',
                    'telephone': PHONE,
                    'image': SITE + '/assets/about/about-1-fleet.jpg',
                    'address': {
                        '@type': 'PostalAddress',
                        'streetAddress': 'Shop No. 36, Speedex Center, Al Qusais Industrial Area 4',
                        'addressLocality': 'Dubai',
                        'addressCountry': 'AE',
                    },
                },
            },
            {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': svc['name'], 'item': url},
                ],
            },
        ],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def render(svc, css_version):
    url = '%s/%s/' % (SITE, svc['slug'])
    quote_href = '/#quote=' + quote(svc['form_name'])
    w, h = svc['image_size']
    badge = ('env', 'Environmental Services') if svc['category'] == 'env' else ('freight', 'Freight Services')
    related = '\n'.join(
        '          <li><a href="/%s/">%s</a></li>' % (s['slug'], s['name'])
        for s in SERVICES if s['slug'] != svc['slug'])
    footer_services = '\n'.join(
        '        <li><a href="/%s/">%s</a></li>' % (s['slug'], s['name']) for s in SERVICES)
    areas = '\n'.join('  <li>%s</li>' % a for a in AREAS)
    faqs = '\n'.join(
        '  <details>\n    <summary>%s</summary>\n    <p>%s</p>\n  </details>' % (esc(q), a)
        for q, a in svc['faqs'])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(svc['title'])}</title>
<meta name="description" content="{esc(svc['description'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Salman Mohammad Transport LLC">
<meta property="og:title" content="{esc(svc['title'])}">
<meta property="og:description" content="{esc(svc['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{svc['image']}">
<meta property="og:locale" content="en_AE">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/assets/favicon/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/favicon/apple-touch-icon.png">
<link rel="manifest" href="/assets/favicon/site.webmanifest">
<meta name="theme-color" content="#BB0408">
<link rel="preload" href="/fonts/Montserrat-VariableFont_wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/pages.css?v={css_version}">
<script type="application/ld+json">
{json_ld(svc)}
</script>
</head>
<body>

<header class="site-header">
  <a class="brand" href="/" aria-label="Salman Mohammad Transport LLC, home">
    <img src="/assets/logo.svg" alt="Salman Mohammad Transport LLC" width="155" height="30">
    <span class="divider"></span>
    <span class="brand-text"><span>SALMAN MOHAMMAD</span><span>TRANSPORT LLC</span></span>
  </a>
  <nav class="main-nav" id="mainNav" aria-label="Main">
    <a href="/">Home</a>
    <div class="nav-services">
      <a href="/#services">Services ▾</a>
      <div class="nav-dropdown">
{nav_links(svc['slug'])}
      </div>
    </div>
    <a href="/#clients">Our Clients</a>
    <a href="/#quote">Contact</a>
  </nav>
  <a href="tel:{PHONE}" class="call-btn">📞 {PHONE_DISPLAY}</a>
  <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mainNav">
    <span></span><span></span><span></span>
  </button>
</header>

<main>
  <section class="svc-hero">
    <div class="wrap hero-grid">
      <div>
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/#services">Services</a> › {svc['name']}</nav>
        <span class="cat-badge {badge[0]}">{badge[1]}</span>
        <h1>{svc['h1']}</h1>
        <p class="lead">{esc(svc['lead'])}</p>
        <div class="hero-ctas">
          <a class="btn btn-primary" href="{quote_href}">Request a Quote</a>
          <a class="btn btn-outline" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
          <a class="btn btn-wa" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp</a>
        </div>
        <ul class="hero-points">
          <li>Available 24/7</li>
          <li>Municipality compliant</li>
          <li>10+ years in operation</li>
        </ul>
      </div>
      <figure class="hero-img">
        <img src="{svc['image']}" alt="{esc(svc['image_alt'])}" width="{w}" height="{h}">
      </figure>
    </div>
  </section>

  <section class="content">
    <div class="wrap content-grid">
      <article class="prose">
{svc['body'].strip()}

<h2>Why choose Salman Mohammad Transport</h2>
<div class="stats">
  <div><div class="num">10+</div><div class="label">Years in operation</div></div>
  <div><div class="num">24/7</div><div class="label">Fleet availability</div></div>
  <div><div class="num">100%</div><div class="label">Municipality compliant</div></div>
  <div><div class="num">8</div><div class="label">Services, one partner</div></div>
</div>
<p>Contractors, facilities managers and industrial operators across Dubai rely on our fleet, including Larsen &amp; Toubro, Emirates Transport, Belhasa and the UAE Football Association. One call covers water, sewage, waste, containers and diesel.</p>

<h2>Areas we cover</h2>
<p>{esc(svc['area_intro'])}</p>
<ul class="areas">
{areas}
</ul>
<p>Please note: our services are available within the Emirate of Dubai only.</p>

<h2>Frequently asked questions</h2>
<div class="faq">
{faqs}
</div>
      </article>

      <aside class="side">
        <div class="side-card quote-card">
          <p class="side-title">Get a quote</p>
          <p>Tell us what you need and where. We'll confirm the price before anything is dispatched.</p>
          <a class="btn btn-primary" href="{quote_href}">Request a Quote</a>
          <a class="btn btn-call" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
          <a class="btn btn-wa" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp us</a>
        </div>
        <div class="side-card">
          <p class="side-title">Other services</p>
          <ul class="side-links">
{related}
          </ul>
        </div>
      </aside>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap">
      <div><h2>{esc(svc['cta'])}</h2><p>Our fleet is ready 24/7 to handle your requirements.</p></div>
      <a href="tel:{PHONE}" class="cta-call">📞 {PHONE_DISPLAY}</a>
    </div>
  </section>
</main>

<footer>
  <div class="foot-grid">
    <div>
      <div class="foot-brand"><img src="/assets/logo.svg" alt="Salman Mohammad Transport LLC" width="155" height="30"></div>
      <p class="foot-name">SALMAN MOHAMMAD TRANSPORT LLC</p>
      <p>Experts you can trust. From waste &amp; sludge management to supplying water tanks, we are your reliable partner in Dubai.</p>
      <div class="foot-social">
        <a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C8.8 3 3 8.8 3 16c0 2.3.6 4.5 1.7 6.4L3 29l6.8-1.8C11.6 28.4 13.8 29 16 29c7.2 0 13-5.8 13-13S23.2 3 16 3zm0 23.6c-2 0-4-.5-5.7-1.6l-.4-.2-4 1.1 1.1-3.9-.3-.4A10.5 10.5 0 015.4 16C5.4 10.2 10.2 5.4 16 5.4S26.6 10.2 26.6 16 21.8 26.6 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.6 8.6 0 01-2.5-1.6 9.6 9.6 0 01-1.8-2.2c-.2-.3 0-.5.1-.7l.5-.6.3-.5v-.5c0-.2-.7-1.7-1-2.3s-.5-.5-.7-.5h-.6a1.2 1.2 0 00-.9.4A3.6 3.6 0 009.4 14a6.3 6.3 0 001.3 3.3 14.3 14.3 0 005.5 4.9c.8.3 1.4.5 1.8.7a4.4 4.4 0 002 .1 3.3 3.3 0 002.1-1.5 2.7 2.7 0 00.2-1.5c-.1-.2-.3-.2-.5-.3z"/></svg></a>
        <a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.2A6.6 6.6 0 1018.6 12 6.6 6.6 0 0012 5.4zm0 10.9A4.3 4.3 0 1116.3 12 4.3 4.3 0 0112 16.3zm6.8-11.1a1.5 1.5 0 11-1.5-1.5 1.5 1.5 0 011.5 1.5z"/></svg></a>
      </div>
    </div>
    <div>
      <p class="foot-title">Quick Links</p>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/#about">About Us</a></li>
        <li><a href="/#services">Our Services</a></li>
        <li><a href="/#clients">Our Clients</a></li>
        <li><a href="/#quote">Request a Quote</a></li>
      </ul>
    </div>
    <div>
      <p class="foot-title">Our Services</p>
      <ul>
{footer_services}
      </ul>
    </div>
    <div>
      <p class="foot-title">Contact Information</p>
      <ul class="foot-contact">
        <li><span>📍</span><span>Shop No. 36, Speedex Center<br>Al Qusais Industrial Area 4<br>Dubai, UAE</span></li>
        <li><span>📞</span><span><a href="tel:{PHONE}">{PHONE_DISPLAY}</a><br><a href="tel:{PHONE2}">{PHONE2_DISPLAY}</a></span></li>
        <li><span>✉️</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul>
    </div>
  </div>
  <div class="foot-bottom">© {datetime.date.today().year} Salman Mohammad Transport LLC. All rights reserved.</div>
</footer>

<div class="mobile-bar">
  <a class="mb-call" href="tel:{PHONE}">Call</a>
  <a class="mb-wa" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp</a>
  <a class="mb-quote" href="{quote_href}">Get Quote</a>
</div>

<script>
  (function () {{
    var burger = document.getElementById('burger');
    var nav = document.getElementById('mainNav');
    burger.addEventListener('click', function () {{
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }});
  }})();
</script>
</body>
</html>
'''


def main():
    css = open(os.path.join(BASE, 'assets', 'css', 'pages.css'), 'rb').read()
    css_version = hashlib.md5(css).hexdigest()[:8]  # busts the browser cache when the CSS changes

    for svc in SERVICES:
        out_dir = os.path.join(BASE, svc['slug'])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(render(svc, css_version))
        print('written /%s/' % svc['slug'])

    today = datetime.date.today().isoformat()
    urls = ['/'] + ['/%s/' % s['slug'] for s in SERVICES]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines += ['  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>' % (SITE, u, today) for u in urls]
    lines.append('</urlset>')
    with open(os.path.join(BASE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('written sitemap.xml (%d URLs)' % len(urls))


if __name__ == '__main__':
    main()
