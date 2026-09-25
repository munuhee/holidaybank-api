"""
Services, FAQs, testimonials, blog posts and demo operations data.

Services restate what the original website says the company does, so they are
not flagged as samples. FAQ answers describe how booking works in general terms
and avoid specific policies (deposit percentages, cancellation windows) the
business has not published; they are flagged `sample` so staff review them.

Testimonials, blog posts, staff accounts and enquiries are entirely demo
content. Testimonials in particular are shown on the public site with a
"sample review" label until real reviews replace them: presenting invented
quotes as genuine customer reviews would be misleading.
"""

SERVICES = [
    {
        'title': 'Kenyan Holiday Packages', 'icon': 'leaf', 'image': 'diani-beach-palms.jpg', 'order': 1,
        'summary': "Weekend escapes and longer breaks across Kenya, built for locals who want the country's best without the guesswork.",
        'body': 'Beach breaks at Diani, lake weekends at Naivasha, a day in Nairobi or a few days at Ol Pejeta: short trips with the transport, stays and activities arranged.',
        'highlights': ['Diani, Naivasha, Nairobi and Nanyuki', 'Weekend and longer options', 'Priced in Kenya shillings'],
        'cta': ('See Kenyan packages', '/tours?category=kenyan-packages'),
    },
    {
        'title': 'East African Safaris', 'icon': 'compass', 'image': 'mara-leopard-branch.jpg', 'order': 2,
        'summary': 'From a weekend in the Mara to a full circuit across four countries, built around the migration calendar and your budget.',
        'body': 'Kenyan safaris in the Maasai Mara, Amboseli and Tsavo, and cross-border trips into Tanzania, Uganda and Rwanda, including gorilla trekking.',
        'highlights': ['Kenya, Tanzania, Uganda and Rwanda', 'Timed to the migration', 'Gorilla and chimpanzee permits arranged'],
        'cta': ('See safaris', '/tours?category=safaris'),
    },
    {
        'title': 'International Holidays', 'icon': 'globe', 'image': 'santorini-oia-lane.jpg', 'order': 3,
        'summary': 'Curated routes across Europe for travellers ready to go further.',
        'body': 'City breaks in Paris, Greece and Spain, rail journeys through Italy and Switzerland, and an eighteen-day Grand European Tour.',
        'highlights': ['France, Greece, Italy, Switzerland and Spain', 'Rail routes and city breaks', 'From five days to eighteen'],
        'cta': ('See international trips', '/tours?category=international'),
    },
    {
        'title': 'Visas and Flights', 'icon': 'receipt', 'image': 'paris-eiffel-tower.jpg', 'order': 4,
        'summary': 'International packages come with visas and flights sorted.',
        'body': 'For European trips we prepare the Schengen visa application with you and arrange the flights to match the itinerary.',
        'highlights': ['Schengen visa application support', 'Flights matched to your itinerary'],
        'cta': ('Ask about a trip', '/contact'),
    },
]

FAQS = [
    ('general', 'Where is Holidaybank Expeditions based?', 'We are based in Nairobi, Kenya, and plan trips across Kenya, East Africa and Europe.'),
    ('general', 'Who are the Kenyan packages for?', "They are built for locals: weekend escapes and longer breaks across Kenya for people who want the country's best without the guesswork. Prices are shown in Kenya shillings."),
    ('booking', 'Are the prices per person?', 'Yes. Prices are shown "from" a per-person rate, based on the standard room or tent and sharing. Your quote will reflect your dates, group size and room choice.'),
    ('booking', 'How do I book a package?', 'Send a booking request from the package page or the contact form. We confirm availability for your dates and send a written quote before anything is paid.'),
    ('booking', 'Can a package be changed or tailor-made?', 'Yes. Any package can be shortened, extended or combined with another, and we can plan a trip from scratch around your dates and budget.'),
    ('travel', 'When is the best time for the migration?', 'The herds are usually in the Maasai Mara from about July to October, and in the Serengeti for much of the rest of the year. We time each safari to where the migration is likely to be.'),
    ('travel', 'Do you help with visas for Europe?', 'Yes. International packages include help preparing the Schengen visa application. Visa fees themselves are paid to the embassy or visa centre.'),
    ('travel', 'How fit do I need to be for gorilla trekking?', 'Treks can take from one to several hours over steep, muddy forest paths. A reasonable level of fitness helps; porters can be hired to carry bags and give a hand on the climbs.'),
    ('payment', 'Which currencies do you quote in?', 'Kenyan packages are quoted in Kenya shillings. Safaris and international holidays are quoted in US dollars.'),
    ('payment', 'When do I pay?', 'A deposit confirms the booking and the balance is due before travel. The exact amounts and dates are set out in your written quote.'),
]

# Demo reviews: first name and initial only, no invented surnames or employers.
TESTIMONIALS = [
    ('Wanjiru M.', 'Nairobi', 'Diani Beach Escape', 5, 'The dhow cruise at sunset was the highlight. Everything was arranged before we arrived, so we just went to the beach.'),
    ('Daniel O.', 'Kisumu', 'Lake Naivasha Weekend', 5, 'Easy weekend away with the family. The kids loved walking among the giraffes on Crescent Island.'),
    ('Amina K.', 'Mombasa', 'Maasai Mara, 3 Days', 5, 'Our guide found a leopard on the first drive. Short trip but we saw so much.'),
    ('Peter N.', 'Nakuru', 'Mara–Serengeti Migration', 5, 'We timed it for the river crossings and saw two in one morning. Worth every shilling.'),
    ('Grace W.', 'Nairobi', 'Paris City Break', 4, 'The visa help made all the difference. Hotel was a short walk from the Eiffel Tower.'),
    ('Brian K.', 'Eldoret', 'Volcanoes NP Gorilla Trek', 5, 'Hard walk up, unforgettable hour with the family group. Would do it again tomorrow.'),
    ('Faith A.', 'Nairobi', 'Santorini & Athens', 5, 'The catamaran sunset sail was magical. Well paced between Athens and the island.'),
    ('Samuel M.', 'Thika', 'Amboseli & Kilimanjaro Views', 4, 'Clear morning and the mountain came out behind the elephants. Lodge was comfortable.'),
]

BLOG_POSTS = [
    {
        'title': 'When to see the Great Migration in the Maasai Mara',
        'image': 'mara-zebra-river-crossing.jpg', 'tags': ['safari', 'kenya', 'migration'], 'days_ago': 12, 'featured': True,
        'excerpt': 'The herds follow the rain, not the calendar. Here is how we plan migration safaris, month by month.',
        'content': (
            '## Following the rain\n\nThe wildebeest migration is a loop between Tanzania and Kenya driven by grazing. '
            'In a typical year the herds reach the Maasai Mara around July and stay until October.\n\n'
            '## The river crossings\n\nThe Mara River crossings are the moment most people come for. They are unpredictable: '
            'herds can gather on the bank for hours and then turn away. Giving yourself at least two full days in the Mara '
            'makes a crossing far more likely.\n\n'
            '## Outside the migration months\n\n- **January to March:** calving season in the southern Serengeti\n'
            '- **April to June:** the long rains; quieter, greener, often cheaper\n'
            '- **November and December:** the herds head south again\n\n'
            'The Mara has resident wildlife all year, so a safari outside migration season is still rewarding.'
        ),
    },
    {
        'title': 'A first-timer’s guide to the Schengen visa from Kenya',
        'image': 'paris-eiffel-tower.jpg', 'tags': ['europe', 'visas', 'planning'], 'days_ago': 26,
        'excerpt': 'What to prepare before applying for a European holiday visa, and how early to start.',
        'content': (
            '## Start early\n\nAppointments at visa centres fill up, especially before the European summer. Starting two to '
            'three months before travel gives you room.\n\n'
            '## What you will usually need\n\n- A passport valid for at least three months after you leave Europe\n'
            '- Travel insurance covering the whole trip\n- Flight and hotel bookings\n- Bank statements\n\n'
            '## Which country to apply to\n\nYou normally apply to the country where you will spend the most nights. On a '
            'multi-country route like our Grand European Tour, we will tell you which one that is.\n\n'
            'Requirements change, so always check the current list for the embassy you are applying to.'
        ),
    },
    {
        'title': 'Gorilla trekking in Rwanda or Uganda: how to choose',
        'image': 'gorilla-silverback-rwanda.jpg', 'tags': ['safari', 'gorillas', 'rwanda', 'uganda'], 'days_ago': 41,
        'excerpt': 'Both countries offer unforgettable treks. The differences are in access, terrain and what else you want to see.',
        'content': (
            '## Rwanda: Volcanoes National Park\n\nA short drive from Kigali, which makes it the easier choice for a short '
            'trip. The terrain is bamboo and open slopes on the volcanoes.\n\n'
            '## Uganda: Bwindi Impenetrable Forest\n\nFurther to reach, in steep, dense rainforest. It pairs naturally with '
            'chimpanzee tracking in Kibale.\n\n'
            '## Either way\n\n- Permits are limited and should be booked well ahead\n- Treks can be long and muddy; good boots help\n'
            '- Time with the gorillas is limited to about an hour'
        ),
    },
    {
        'title': 'Five Kenyan weekend escapes from Nairobi',
        'image': 'naivasha-hippos-pelicans.jpg', 'tags': ['kenya', 'weekend'], 'days_ago': 58,
        'excerpt': 'Lakes, rhinos and white sand, all within a short trip of the capital.',
        'content': (
            '## Lake Naivasha\n\nTwo hours from Nairobi: boat rides among hippos and a walk on Crescent Island.\n\n'
            '## Nanyuki and Ol Pejeta\n\nRhinos, the equator, and Mt. Kenya on clear mornings.\n\n'
            '## Diani\n\nA short flight or train and road trip to the south coast for reef snorkelling.\n\n'
            '## Amboseli\n\nElephants and Kilimanjaro, best on a clear morning.\n\n'
            '## Nairobi itself\n\nThe elephant orphanage, the Giraffe Centre and the national park make a full day without leaving the city.'
        ),
    },
    {
        'title': 'Italy by train: Rome, Florence and Venice',
        'image': 'venice-grand-canal.jpg', 'tags': ['europe', 'italy', 'rail'], 'days_ago': 73,
        'excerpt': 'Why we route Italy by rail, and how long to spend in each city.',
        'content': (
            '## Why the train\n\nHigh-speed trains link the three cities in a few hours, city centre to city centre, '
            'with no airport transfers.\n\n'
            '## How long in each\n\n- **Rome:** three nights for the ancient city and the Vatican\n'
            '- **Florence:** three nights, including a day in Tuscany\n- **Venice:** three nights; stay over to see it after the day-trippers leave\n\n'
            'That is the shape of our ten-day Rome, Florence & Venice route.'
        ),
    },
]

# Demo staff: cannot sign in (unusable passwords). They exist so the enquiry
# pipeline has owners to show.
STAFF = [
    {'email': 'amani.consultant@example.com', 'name': 'Amani (demo consultant)', 'role': 'Travel Consultant'},
    {'email': 'lena.consultant@example.com', 'name': 'Lena (demo consultant)', 'role': 'Travel Consultant'},
    {'email': 'joseph.editor@example.com', 'name': 'Joseph (demo editor)', 'role': 'Editor'},
]

# Demo enquiries across every pipeline stage. Emails use example.com.
ENQUIRIES = [
    {'type': 'booking', 'name': 'Mercy Wambui', 'email': 'mercy.w@example.com', 'phone': '+254 700 000 101', 'tour': 'Diani Beach Escape',
     'travel_in_days': 30, 'guests': {'adults': 2, 'children': 1, 'infants': 0}, 'status': 'new', 'days_ago': 1,
     'message': 'Is the dhow cruise suitable for a seven-year-old?'},
    {'type': 'contact', 'name': 'James Otieno', 'email': 'j.otieno@example.com', 'phone': '+254 700 000 102', 'interest': 'East Africa Safaris',
     'budget': 3000, 'budget_currency': 'USD', 'status': 'new', 'days_ago': 2,
     'message': 'Looking at a migration safari for two in August, possibly with a few days in Zanzibar after.'},
    {'type': 'booking', 'name': 'Aisha Hassan', 'email': 'aisha.h@example.com', 'tour': 'Paris City Break', 'travel_in_days': 75,
     'guests': {'adults': 2, 'children': 0, 'infants': 0}, 'status': 'assigned', 'assignee': 0, 'days_ago': 3,
     'message': 'Honeymoon trip. We have not applied for visas yet.'},
    {'type': 'booking', 'name': 'Kevin Mutua', 'email': 'kevin.m@example.com', 'phone': '+254 700 000 104', 'tour': 'Maasai Mara, 3 Days',
     'travel_in_days': 21, 'guests': {'adults': 4, 'children': 0, 'infants': 0}, 'status': 'in_progress', 'assignee': 1, 'days_ago': 5,
     'follow_up_in_days': -1, 'message': 'Group of four friends, flexible on dates.'},
    {'type': 'contact', 'name': 'Susan Achieng', 'email': 'susan.a@example.com', 'interest': 'Kenyan Packages', 'budget': 60000,
     'budget_currency': 'KES', 'status': 'quoted', 'assignee': 0, 'days_ago': 8, 'follow_up_in_days': 2,
     'message': 'Family weekend for five somewhere within four hours of Nairobi.'},
    {'type': 'booking', 'name': 'Tom Kiprono', 'email': 'tom.k@example.com', 'tour': 'Santorini & Athens', 'travel_in_days': 120,
     'guests': {'adults': 2, 'children': 0, 'infants': 0}, 'status': 'won', 'assignee': 1, 'days_ago': 20,
     'message': 'Anniversary trip in May.'},
    {'type': 'booking', 'name': 'Linda Njeri', 'email': 'linda.n@example.com', 'tour': 'Grand European Tour', 'travel_in_days': 150,
     'guests': {'adults': 2, 'children': 2, 'infants': 0}, 'status': 'lost', 'assignee': 0, 'days_ago': 35,
     'message': 'Would the tour work with two teenagers?'},
    {'type': 'contact', 'name': 'Omar Abdi', 'email': 'omar.a@example.com', 'interest': 'International Holidays', 'status': 'new', 'days_ago': 0,
     'message': 'Do you arrange trips to Switzerland in December for skiing?'},
    {'type': 'booking', 'name': 'Rose Chebet', 'email': 'rose.c@example.com', 'tour': 'Bwindi Gorillas & Chimps', 'travel_in_days': 90,
     'guests': {'adults': 1, 'children': 0, 'infants': 0}, 'status': 'in_progress', 'assignee': 1, 'days_ago': 9, 'follow_up_in_days': 1,
     'message': 'Solo traveller; how early do permits need booking?'},
    {'type': 'booking', 'name': 'David Ochieng', 'email': 'david.o@example.com', 'tour': 'Nairobi City & Nature', 'travel_in_days': 10,
     'guests': {'adults': 2, 'children': 2, 'infants': 1}, 'status': 'quoted', 'assignee': 0, 'days_ago': 4, 'follow_up_in_days': -2,
     'message': 'Visiting family from abroad, one day free in Nairobi.'},
]
