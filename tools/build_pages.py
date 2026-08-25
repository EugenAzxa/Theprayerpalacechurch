#!/usr/bin/env python3
"""Generate the flat pages from one set of partials.

index.html is hand-written because it carries the scene. Everything after it is
an ordinary document, and those four share a head, a navigation and a footer.
Writing them once here means a change to the phone number or a new item in the
menu cannot land on three pages and miss the fourth.

Run from the repo root:  python3 tools/build_pages.py
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

PHONE_HREF = "+14162411100"
PHONE = "416 241 1100"
ADDRESS = "1111 Arrow Road, Toronto, Ontario M9M 3B3"
PUSHPAY = "https://pushpay.com/g/theprayerpalace"
FORMS = "https://theprayerpalace.com/contact-us"

NAV = [
    ("index.html#threshold", "New here"),
    ("index.html#sanctuary", "About"),
    ("events.html", "Events"),
    ("connect.html", "Connect &amp; Serve"),
    ("contact.html", "Visit"),
]


def head(title, desc, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>The Prayer Palace | {title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#060A13">
<link rel="icon" href="assets/mark.webp" type="image/webp">
<meta property="og:title" content="The Prayer Palace | {title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/sanctuary-wall.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300&family=Inter:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="site.css">{extra}
</head>
<body class="flat">
"""


def nav(current):
    rows = []
    for href, label in NAV:
        mark = ' aria-current="page"' if href == current else ""
        rows.append('      <a href="%s"%s>%s</a>\n' % (href, mark, label))
    links = "".join(rows)
    return f"""<nav id="nav" aria-label="Primary">
  <a class="brand" href="index.html" aria-label="The Prayer Palace, home"><img src="assets/logo.webp" alt="The Prayer Palace"></a>
  <div class="spacer"></div>
  <div class="links">
{links}  </div>
  <div class="nav-cta"><a class="btn btn-gold" href="give.html">Give</a></div>
  <button id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
  </button>
</nav>

<div id="drawer" aria-label="Menu" role="dialog" aria-modal="true">
  <button class="close" aria-label="Close menu">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
  </button>
  <a href="index.html#threshold">New here</a>
  <a href="index.html#sanctuary">Who we are</a>
  <a href="index.html#word">Prayer</a>
  <a href="events.html">Events</a>
  <a href="connect.html">Connect &amp; Serve</a>
  <a href="contact.html">Visit us</a>
  <div class="drawer-cta">
    <a class="btn btn-gold" href="give.html">Give</a>
    <a class="btn" href="contact.html">Plan a visit</a>
  </div>
</div>
"""


def top(num, label, h1, lede, cta=""):
    return f"""<header class="page-top">
  <div class="wrap"><div class="col wide">
    <div class="mark-line"><span class="num">{num}</span><span class="rule"></span><span class="lbl">{label}</span></div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    {cta}
  </div></div>
</header>
"""


FOOTER = f"""<footer>
  <div class="fwrap">
    <div>
      <img class="flogo" src="assets/logo.webp" alt="The Prayer Palace">
      <p class="small" style="max-width:36ch">A non-profit Christian organization blanketing the world with the Gospel of Jesus Christ to meet the needs of mankind.</p>
      <p class="small" style="margin-top:18px">Licensed and recognized by The Evangelical Association in Canada.</p>
    </div>
    <div>
      <h4>The house</h4>
      <ul>
        <li><a href="index.html#threshold">New here</a></li>
        <li><a href="index.html#sanctuary">Who we are</a></li>
        <li><a href="index.html#word">Prayer</a></li>
        <li><a href="index.html#ascent">Heaven is real</a></li>
        <li><a href="events.html">Events</a></li>
        <li><a href="connect.html">Connect &amp; Serve</a></li>
      </ul>
    </div>
    <div>
      <h4>Get in touch</h4>
      <ul>
        <li><a href="contact.html">{ADDRESS}</a></li>
        <li><a href="tel:{PHONE_HREF}">{PHONE}</a></li>
        <li><a href="mailto:info@theprayerpalace.com">info@theprayerpalace.com</a></li>
        <li><a href="give.html">Give</a></li>
        <li><a href="contact.html#prayer">Prayer requests</a></li>
      </ul>
    </div>
  </div>
  <div class="base">
    <span>Sundays 10:30 am &nbsp;|&nbsp; Fridays 7:30 pm &nbsp;|&nbsp; Saturday prayer 7:30 pm</span>
    <span>&copy; 2026 The Prayer Palace</span>
  </div>
</footer>

<script>
/* The menu is the only behaviour these pages need. */
(function () {{
  var burger = document.getElementById('burger');
  var drawer = document.getElementById('drawer');
  var closeBtn = drawer.querySelector('.close');
  function set(open) {{
    drawer.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
    (open ? closeBtn : burger).focus();
  }}
  burger.addEventListener('click', function () {{ set(!drawer.classList.contains('open')); }});
  closeBtn.addEventListener('click', function () {{ set(false); }});
  drawer.querySelectorAll('a').forEach(function (a) {{ a.addEventListener('click', function () {{ set(false); }}); }});
  document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape' && drawer.classList.contains('open')) set(false); }});
}})();
</script>
</body>
</html>
"""


def write(name, title, desc, body, extra_head="", extra_tail=""):
    html = head(title, desc, extra_head) + nav(name) + body + FOOTER
    if extra_tail:
        html = html.replace("</body>", extra_tail + "\n</body>")
    with open(os.path.join(ROOT, name), "w") as f:
        f.write(html)
    print(f"{name:16} {len(html) // 1024} KB")


# ============================================================
# GIVE
# ============================================================
GIVE = top("07", "Give", "Your seed<br>has a purpose",
  "Giving through tithes and offerings is not just a donation. You are sowing into the furtherance of the gospel, locally and internationally, and into the families this house feeds and clothes every week.",
  f'<div class="cta-row"><a class="btn btn-solid" href="{PUSHPAY}" target="_blank" rel="noopener">Give online now</a>'
  f'<a class="btn" href="#ways">Other ways to give</a></div>') + f"""
<main>
<section id="ways">
  <div class="wrap">
    <div class="mark-line"><span class="num">01</span><span class="rule"></span><span class="lbl">Ways to give</span></div>
    <h2>Six ways, one purpose</h2>
    <div class="ways">
      <div class="way">
        <h3>Online, once or recurring</h3>
        <p>Set up a single gift or a giving schedule through Pushpay, our online giving platform. You can create a profile, manage your schedule and pull your statements at any time.</p>
        <span class="go"><a class="btn btn-solid" href="{PUSHPAY}" target="_blank" rel="noopener">Open the giving portal</a></span>
      </div>
      <div class="way">
        <h3>Interac e-Transfer</h3>
        <p>Send directly from your Canadian bank. No fees are deducted from a gift sent this way.</p>
        <span class="big">give@theprayerpalace.com</span>
      </div>
      <div class="way">
        <h3>By text</h3>
        <p>Text the word below to the number below from your mobile and follow the reply.</p>
        <span class="big">Text TPP to 77977</span>
      </div>
      <div class="way">
        <h3>In person</h3>
        <p>Give during any service. You may also request your own tithing box with envelopes at the main office.</p>
        <span class="big">Sundays 10:30 am</span>
      </div>
      <div class="way">
        <h3>By mail</h3>
        <p>Cheques must be received or postmarked by 31 December to appear on that year's giving statement.</p>
        <span class="big">The Prayer Palace<br>{ADDRESS}</span>
      </div>
      <div class="way">
        <h3>Non-cash gifts</h3>
        <p>Vehicles, real estate, stocks and other assets can be given to further the work. Contact the office and we will walk you through it.</p>
        <span class="big">info@theprayerpalace.com</span>
      </div>
    </div>
    <p class="small" style="margin-top:26px">Outside Canada: give through the portal if you are in a Pushpay-supported country, otherwise call the office during business hours to give by credit card, or use PayPal.</p>
  </div>
</section>

<section id="missions">
  <div class="wrap">
    <div class="mark-line"><span class="num">02</span><span class="rule"></span><span class="lbl">Global missions</span></div>
    <h2>Mission: raise the roof</h2>
    <div class="duo" style="margin-top:34px;align-items:start">
      <div>
        <p class="body">Hurricane Melissa struck Jamaica on 28 October 2025, making landfall as a category five storm with sustained winds up to 295 km/h. It is the most powerful hurricane ever to hit the island directly.</p>
        <p class="body">Among the hardest hit was Clarendon, where a local church lost its roof entirely, leaving the sanctuary open to the sky and its congregation displaced. We have committed to rebuilding it, and to reinforcing it against the next storm.</p>
        <ul class="values" style="margin-top:30px">
          <li><span>I</span><p>The full rebuilding of the church roof.</p></li>
          <li><span>II</span><p>Structural reinforcement against future storms.</p></li>
          <li><span>III</span><p>Materials, labour and transportation.</p></li>
          <li><span>IV</span><p>Restoring a safe and sacred place for worship.</p></li>
        </ul>
        <p class="small" style="margin-top:24px;font-style:italic">"God is our refuge and strength, a very present help in trouble." Psalm 46:1</p>
        <div class="cta-row"><a class="btn btn-gold" href="{PUSHPAY}" target="_blank" rel="noopener">Give to the rebuild</a></div>
      </div>
      <figure class="plate">
        <img src="assets/jamaica.webp" alt="The damaged roof of the church in Clarendon, Jamaica" loading="lazy" width="900" height="620">
        <figcaption><b>Clarendon, Jamaica</b><span>October 2025</span></figcaption>
      </figure>
    </div>
  </div>
</section>

<section id="accountability">
  <div class="wrap">
    <div class="mark-line"><span class="num">03</span><span class="rule"></span><span class="lbl">Accountability</span></div>
    <h2>Where it goes,<br>and who checks</h2>
    <p class="lede">The ministry is committed to financial integrity, transparency and accountability in accordance with CRA guidelines and applicable accounting and regulatory standards.</p>
    <div class="stats">
      <div><b>Zeifmans LLP</b><span>Annual external audit</span></div>
      <div><b>CRA</b><span>Registered charitable receipts</span></div>
      <div><b>PCI L1</b><span>Payment security certification</span></div>
    </div>
    <h3 style="margin-top:64px">Questions people ask</h3>
    <div style="margin-top:22px;max-width:76ch">
      <details class="q"><summary>What is registered tithing?</summary>
        <p>Registered tithers receive a year-end official donation receipt recording their total giving for that year, with name and address. You can use it to claim a tax credit in accordance with the Canada Revenue Agency.</p></details>
      <details class="q"><summary>How do I calculate my tithe?</summary>
        <p>If you are new to tithing, start with the biblical principle of giving ten per cent of your gross income. See Malachi 3:10.</p></details>
      <details class="q"><summary>What are the processing fees?</summary>
        <p>The online platform charges approximately 2.2 per cent plus 30 cents each time you give, deducted from the gift when the church receives it. You have the option of covering that fee yourself at the time of giving. An Interac e-Transfer carries no such fee.</p></details>
      <details class="q"><summary>What is the deadline for a given year?</summary>
        <p>Cash and cheque donations must be received or postmarked by 31 December. Online donations must be completed by 11:59 pm Eastern on 31 December to be included in that year's statement.</p></details>
      <details class="q"><summary>How secure is online giving?</summary>
        <p>The platform uses Stripe as its payment processor, certified by a PCI-qualified auditor to PCI Service Provider Level 1, the most stringent certification available in the payments industry. The account dashboard supports SMS, time-based one-time passwords, hardware security keys and passkeys for multi-factor authentication.</p></details>
      <details class="q"><summary>How do I change my giving or my contact details?</summary>
        <p>Log in to the giving portal to edit your profile and schedule at any time. If you give in person, call the main office on <a href="tel:{PHONE_HREF}">{PHONE}</a> and speak to reception. For help with an online account, email media@theprayerpalace.com.</p></details>
    </div>
  </div>
</section>
</main>
"""

# ============================================================
# EVENTS
# ============================================================
def ev(date, day, title, body, act=""):
    return f"""    <div class="entry">
      <div class="when"><b>{date}</b>{day}</div>
      <div><h3>{title}</h3><p>{body}</p></div>
      <div class="act">{act}</div>
    </div>
"""

EVENTS = top("08", "Events", "What is<br>coming up",
  "We look forward to you joining in and being a part of the body of Christ here at The Prayer Palace, where all are welcome.") + f"""
<main>
<section>
  <div class="wrap">
    <div class="mark-line"><span class="num">01</span><span class="rule"></span><span class="lbl">Dated</span></div>
    <h2>On the calendar</h2>
    <div style="margin-top:40px">
""" + ev("30 August", "Sunday, 10:30 am", "Back to school service",
      "Prayer and anointing for the new season. Students and educators of all ages are encouraged and dedicated for the year ahead. Pre-register for a gift, ages twelve and under.",
      f'<a class="btn" href="{FORMS}" target="_blank" rel="noopener">Register</a>') \
+ ev("5 September", "Saturday, 6:30 to 9 am", "Sunrise prayer",
      "A morning given entirely to corporate prayer, before the day starts.") \
+ ev("12 September", "Saturday, 12 to 3 pm", "Guys grill and gather at the park",
      "Good food, games, sport and real conversation. Bring a dish to share, your game face and a lawn chair. For men of all ages. Free admission, please register.",
      f'<a class="btn" href="{FORMS}" target="_blank" rel="noopener">Register</a>') \
+ ev("19 September", "Saturday, 5 pm", "Couples date night",
      "Dinner and a movie for dating and married couples. A buffet dinner and an inspiring feature film, with time to actually talk to each other.",
      f'<a class="btn" href="{FORMS}" target="_blank" rel="noopener">Tickets</a>') \
+ ev("26 September", "Saturday, 1 to 4 pm", "Young adults praise cruise",
      "A private yacht along Toronto Harbour with skyline views, live praise, hors d'oeuvres and board games. Take advantage of the early bird price.",
      f'<a class="btn" href="{FORMS}" target="_blank" rel="noopener">Tickets</a>') + """    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="mark-line"><span class="num">02</span><span class="rule"></span><span class="lbl">Every week</span></div>
    <h2>Things that happen<br>on repeat</h2>
    <div style="margin-top:40px">
""" + ev("Sundays", "10:15 to 11:15 am", "Children's Sunday church",
      "Wing 1, with an all new Bible-based curriculum. Ages nought to twelve. Check in from 10:15.") \
+ ev("Fridays", "7:30 pm", "Palace Kidz fun Fridays",
      "A night of faith-filled activities and treats, built to give kids a joyful reason to be at church.") \
+ ev("Fridays", "8 pm", "Palace youth",
      "Youth services weekly for ages thirteen and up, in the Wing 1 Chapel.") \
+ ev("Saturdays", "All day", "Samaritan: city-wide evangelism",
      "Evangelism re-imagined. Join a team reaching the city in a way that has not been done here before.",
      '<a class="btn" href="connect.html">Sign me up</a>') \
+ ev("Sundays", "Before and after 10:30", "Bibles and gifts bookstore",
      "Open before and after the Sunday morning service. There is a free gift with purchase at the moment, while stocks last.") + """    </div>
    <div class="cta-row" style="margin-top:46px">
      <a class="btn btn-solid" href="connect.html">Find a group to belong to</a>
      <a class="btn" href="contact.html">Ask us about an event</a>
    </div>
  </div>
</section>
</main>
"""

# ============================================================
# CONNECT AND SERVE
# ============================================================
CONNECT = top("09", "Connect &amp; Serve", "There is a place<br>for every part<br>of the family",
  "Life is not meant to be lived alone, and neither is faith. Whatever age you are and whatever season you are in, there are people here already expecting you.") + f"""
<main>
<section>
  <div class="wrap">
    <div class="mark-line"><span class="num">01</span><span class="rule"></span><span class="lbl">Connect groups</span></div>
    <h2>Find your people</h2>
    <figure class="plate" style="max-width:520px;margin:36px 0 0">
      <img src="assets/congregation.webp" alt="Members of the congregation together after a service" loading="lazy" width="900" height="900">
      <figcaption><b>Over fifty nationalities</b><span>One body</span></figcaption>
    </figure>
    <div class="ways">
      <div class="way">
        <h3>Palace Kidz, nought to twelve</h3>
        <p>Nursery care from birth to thirty-six months during the 10:30 service, in a loving environment that teaches life lessons on a biblical model. Ages four to twelve get age-appropriate Bible stories, games and leaders who are genuinely glad to see them.</p>
        <span class="big">Sundays 10:30, check in 9:45</span>
      </div>
      <div class="way">
        <h3>Youth, thirteen and up</h3>
        <p>Amazing young people who love God and know they are a chosen generation who can make a difference in this world. Peer groups and leaders who stay in it with them.</p>
        <span class="big">Fridays 7:30 pm, Wing 1 Chapel</span>
      </div>
      <div class="way">
        <h3>CREW, young adults</h3>
        <p>Christian, ready, equipped and willing. A place to connect, laugh and grow together: Bible-themed question nights, game nights with refreshments, outdoor adventures. Roughly eighteen to thirty-five.</p>
        <span class="big">Regular socials, ask about the channel</span>
      </div>
      <div class="way">
        <h3>Women's</h3>
        <p>Women of all ages coming together to make new friendships, grow in their relationship with God, and be empowered to use the gifts they have been given.</p>
        <span class="big">Ask at the Connect Cafe</span>
      </div>
      <div class="way">
        <h3>Men's</h3>
        <p>Established by men for men. Fellowship, praise and service to people in need, with a view to becoming the fathers, husbands and men of integrity they are called to be.</p>
        <span class="big">Saturday mornings, off site</span>
      </div>
      <div class="way">
        <h3>Seniors</h3>
        <p>Lunches, trips, Bible studies and themed events, and real support for one another through these golden years.</p>
        <span class="big">2nd and 4th Wednesdays, Wing 1</span>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="mark-line"><span class="num">02</span><span class="rule"></span><span class="lbl">Serve teams</span></div>
    <h2>Everyone is called<br>for a purpose</h2>
    <p class="lede">A kingdom model mindset is about serving and multiplying. If you are ready to give some of your week to the house, there is a team that needs exactly what you can do.</p>
    <ul class="values" style="margin-top:38px">
      <li><span>01</span><p>Welcome and hospitality, including the Welcome Reception in the Connect Cafe.</p></li>
      <li><span>02</span><p>Palace Kidz and youth, for those who are good with children and cleared to work with them.</p></li>
      <li><span>03</span><p>Worship, media and the seven projection screens that carry the scriptures every service.</p></li>
      <li><span>04</span><p>Multilingual translation, offered free to visitors every Sunday.</p></li>
      <li><span>05</span><p>The food and clothing distribution hub, serving local families facing hardship.</p></li>
      <li><span>06</span><p>Samaritan, the city-wide evangelism teams that go out on Saturdays.</p></li>
    </ul>
    <figure class="plate" style="max-width:520px;margin:38px 0 0">
      <img src="assets/welcome.webp" alt="A visitor being welcomed at the door" loading="lazy" width="900" height="900">
      <figcaption><b>Welcome Reception</b><span>Every Sunday, after the service</span></figcaption>
    </figure>
    <div class="cta-row" style="margin-top:40px">
      <a class="btn btn-solid" href="{FORMS}" target="_blank" rel="noopener">Serve team form</a>
      <a class="btn" href="contact.html">Talk to someone first</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="mark-line"><span class="num">03</span><span class="rule"></span><span class="lbl">Start here</span></div>
    <h2>Connect Class</h2>
    <p class="lede">A Sunday course on the DNA and vision of The Prayer Palace: our ministries, the children's programs, baptism, serving, and how to become a member. Thirty minutes, before the morning service.</p>
    <div class="stats">
      <div><b>9:45</b><span>Every Sunday morning</span></div>
      <div><b>30 min</b><span>Before the 10:30 service</span></div>
      <div><b>Wing 2</b><span>The chapel</span></div>
    </div>
    <p class="body">Once you have finished Connect, there is an eight-week study that takes you through the key biblical principles and foundations for healthy Christian living.</p>
  </div>
</section>
</main>
"""

# ============================================================
# VISIT AND CONTACT
# ============================================================
CONTACT = top("10", "Visit us", "Come and see",
  "The main office welcomes members and visitors, in person or over the phone. Come for a service, or come by during the week.",
  '<div class="cta-row"><a class="btn btn-solid" href="https://maps.google.com/?q=1111+Arrow+Road,+Toronto,+ON+M9M+3B3" target="_blank" rel="noopener">Get directions</a>'
  f'<a class="btn" href="tel:{PHONE_HREF}">{PHONE}</a></div>') + f"""
<main>
<section>
  <div class="wrap">
    <div class="visit">
      <div>
        <div class="mark-line"><span class="num">01</span><span class="rule"></span><span class="lbl">When</span></div>
        <h2>Times</h2>
        <ul class="times">
          <li><b>Sunday</b><span>10:30 am<br>Worship &amp; Word</span></li>
          <li><b>Friday</b><span>7:30 pm<br>Bible study &amp; prayer</span></li>
          <li><b>Saturday</b><span>7:30 pm<br>Prayer</span></li>
          <li><b>Office hours</b><span>Tue to Fri, 9 am to 5 pm<br>Closed Sat to Mon</span></li>
        </ul>
        <p class="small" style="margin-top:24px">A Sunday service usually runs from 10:30 to about 12:30. On Friday nights the sanctuary is open from 7 pm to 9:30 pm, so come any time.</p>
      </div>
      <div>
        <div class="mark-line"><span class="num">02</span><span class="rule"></span><span class="lbl">Where</span></div>
        <h2>The house</h2>
        <address>
          The Prayer Palace<br>
          1111 Arrow Road<br>
          Toronto, Ontario<br>
          M9M 3B3, Canada<br><br>
          <a href="tel:{PHONE_HREF}">{PHONE}</a><br>
          <a href="mailto:info@theprayerpalace.com">info@theprayerpalace.com</a><br>
          <a href="mailto:media@theprayerpalace.com">media@theprayerpalace.com</a>
        </address>
        <p class="small" style="margin-top:24px">Parking is free. Security personnel are on the premises at all times. Nursery is in Wing 2, Palace Kidz in Wing 1, and the Connect Cafe sits between the north main entrance and the gymnasium.</p>
      </div>
    </div>
  </div>
</section>

<section id="prayer">
  <div class="wrap">
    <div class="mark-line"><span class="num">03</span><span class="rule"></span><span class="lbl">Prayer</span></div>
    <h2>Send us a prayer request<br>or a praise report</h2>
    <p class="lede">We firmly believe in the power of prayer and will stand with you as you petition the Father. We covenant with you that we will lift your request to Jesus, our High Priest, with the full expectation that the thing you are believing for will come to pass.</p>
    <p class="small" style="max-width:60ch;margin-top:18px;font-style:italic">"If two of you shall agree on earth as touching any thing that they shall ask, it shall be done for them of my Father which is in heaven." Matthew 18:19</p>
    <figure class="plate" style="max-width:440px;margin:38px 0 0">
      <img src="assets/cross.webp" alt="Hands raised before a cross at first light" loading="lazy" width="900" height="900">
      <figcaption><b>We will stand with you</b><span>Matthew 18:19</span></figcaption>
    </figure>
    <form class="form" id="prayerForm">
      <label>Your name<input name="name" type="text" autocomplete="name" required></label>
      <label>Your email<input name="email" type="email" autocomplete="email" required></label>
      <label>This is a
        <select name="kind">
          <option>Prayer request</option>
          <option>Praise report</option>
        </select>
      </label>
      <label>What would you like us to stand with you for?<textarea name="body" required></textarea></label>
      <div class="cta-row" style="margin-top:4px"><button class="btn btn-solid" type="submit">Send to the prayer team</button></div>
      <p class="note">This opens your own mail application with the message ready to send, so nothing is stored on this site. If you would rather speak to someone, call <a href="tel:{PHONE_HREF}">{PHONE}</a> during office hours.</p>
    </form>
  </div>
</section>

<section id="forms">
  <div class="wrap">
    <div class="mark-line"><span class="num">04</span><span class="rule"></span><span class="lbl">Registration</span></div>
    <h2>Take the next step</h2>
    <div class="ways">
      <div class="way" id="baptism">
        <h3>Water baptism</h3>
        <p>An outward expression of an inward change, practised here by immersion. If you have accepted Jesus and have not been baptized in water, this is for you. Families are welcome to re-declare their faith together.</p>
        <span class="go"><a class="btn btn-solid" href="{FORMS}" target="_blank" rel="noopener">Register for baptism</a></span>
      </div>
      <div class="way">
        <h3>Baby and child dedication</h3>
        <p>To have your baby or child dedicated to the Lord here, start with the dedication form and we will be in touch about dates.</p>
        <span class="go"><a class="btn" href="{FORMS}" target="_blank" rel="noopener">Dedication form</a></span>
      </div>
      <div class="way">
        <h3>Connect card</h3>
        <p>Update your contact details, or sign up to receive ongoing biblical resources from the house.</p>
        <span class="go"><a class="btn" href="{FORMS}" target="_blank" rel="noopener">Connect card</a></span>
      </div>
      <div class="way">
        <h3>Hospital notice</h3>
        <p>If you or someone you love is in hospital, send us a notice so the pastoral team knows to visit and to pray.</p>
        <span class="go"><a class="btn" href="{FORMS}" target="_blank" rel="noopener">Send a notice</a></span>
      </div>
      <div class="way">
        <h3>Serve team</h3>
        <p>Interested in volunteering in an area of ministry? Tell us what you are drawn to and we will find the team.</p>
        <span class="go"><a class="btn" href="{FORMS}" target="_blank" rel="noopener">Serve team form</a></span>
      </div>
      <div class="way">
        <h3>Just visiting</h3>
        <p>You do not need to fill in anything at all to come on a Sunday. Meet us at the Welcome Reception afterwards and we will take it from there.</p>
        <span class="go"><a class="btn" href="index.html#threshold">What to expect</a></span>
      </div>
    </div>
  </div>
</section>
</main>
"""

PRAYER_JS = """
<script>
/* The form composes a message in the sender's own mail client. Nothing is
   posted anywhere, which is the honest behaviour for a site with no backend. */
(function () {
  var f = document.getElementById('prayerForm');
  if (!f) return;
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(f);
    var subject = d.get('kind') + ' from ' + d.get('name');
    var body = d.get('body') + '\\n\\n' + d.get('name') + '\\n' + d.get('email');
    window.location.href = 'mailto:info@theprayerpalace.com?subject=' +
      encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  });
})();
</script>"""


if __name__ == "__main__":
    write("give.html", "Give",
          "Tithes, offerings and missions giving to The Prayer Palace, Toronto. Online, e-transfer, text, in person or by mail.", GIVE)
    write("events.html", "Events",
          "What is coming up at The Prayer Palace, Toronto: sunrise prayer, youth nights, couples date night and the young adults praise cruise.", EVENTS)
    write("connect.html", "Connect &amp; Serve",
          "Palace Kidz, youth, young adults, women's, men's and seniors, plus every serve team in the house.", CONNECT)
    write("contact.html", "Visit us",
          "1111 Arrow Road, Toronto. Service times, office hours, prayer requests and registration for baptism and dedication.", CONTACT,
          extra_tail=PRAYER_JS)
