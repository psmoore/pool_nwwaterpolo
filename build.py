#!/usr/bin/env python3
"""Build the Northwest Water Polo Club preview: Home, Our Schedule, one page per team, Our Facilities and Tournaments,
in the look of northwestwaterpoloclub.com, with every practice day, time and pool read live from Pool Relay by finder.js.

Nothing about WHEN a team practices is typed here: only prices, ages, program descriptions, coaches and facts about the
pools. The club's own schedule text appears only as labeled quotes.
Run: python3 build.py   (then python3 check.py)"""
import hashlib, html

E = html.escape
CLUB = "GLtzZAMK32smkH6Y8wGHhw"  # Pool Relay tab: Northwest Water Polo Club, week (every team; feeds the club-wide live text)
NW = "https://www.northwestwaterpoloclub.com"
SCHED_SRC = NW + "/page/show/7521405-our-schedule"
TOURN_SRC = NW + "/page/show/7398082-2024-2025-season-tournament-schedule"
REG_SRC = NW + "/page/show/7177616-tournament-registration"
PROGRAM_SRC = NW + "/page/show/7177677-our-program"
KAP7 = "https://www.kahunaevents.com/competitions/6acfb8d869a4bae19366f753/details"
PL_SITE = "https://psmoore.github.io/pool_phantomlake/"
WR_SITE = "https://psmoore.github.io/pool_woodridge/"
VER = hashlib.sha1((open("finder.js").read() + open("style.css").read()).encode()).hexdigest()[:8]

# Each team page embeds a tab locked to that team's group, and its Follow form is preset to that group.
TEAMS = [
    dict(slug="hs-girls", name="HS Girls & 14u Girls", group="grp:hs-girls-14u-girls", token="orz6Web4Pj1MEfpoxOgA1T", color="#D4A10A",
         coach="Emily Hernandez and Alicia Nordal", price="$350/month", level="Gold (for California tournaments)",
         who="Girls in 14u and high school.",
         about="Two-hour practices for motivated and experienced players, building toward Junior Olympics, varsity high school water "
               "polo, national competitions and NCAA water polo. The first half is conditioning with swimming and egg-beater drills "
               "while working on passing and body position; the second half is usually shooting drills, front court work and "
               "counter attack drills."),
    dict(slug="hs-boys", name="HS Boys & 14u", group="grp:hs-boys-14u", token="4g9FthSAAnr3nI8vKQynQN", color="#2B2B2B",
         coach="Adam Jacobson, Keegan Klein, Topher Lacrampe, Daniel Kavesh and Vee Valle", price="$350/month",
         level="Gold (for California tournaments)", who="Boys in 14u and high school.",
         about="Two-hour practices that develop athletes for varsity high school water polo, national competitions and NCAA water "
               "polo, plus a scrimmage or weekend tournament. The first half is conditioning with swimming and egg-beater drills; "
               "the second half is usually shooting drills, front court work and counter attack drills.",
         note="The club's schedule names no pool for two of this team's four practice days. Pool Relay shows Phantom Lake for "
              "those, as an estimate, until the club enters the real pool."),
    dict(slug="12u", name="12u 3x-a-week", group="grp:12u-3x-a-week", token="aCHMsuDRoUxUjactVoVqQE", color="#2E7D4F",
         coach="Andrew Falaniko and Daniel Kavesh", price="$250/month",
         level="Bronze (local scrimmages), Silver (travel tournaments, not Jr. Olympics) or Gold (travel tournaments and Jr. Olympics)",
         who="12u boys and girls, intermediate to advanced, three practices a week.",
         about="Hour-and-a-half practices twice a week plus a shorter weekend practice, for motivated novice through experienced "
               "players. Conditioning with swimming and egg-beater drills first, then shooting drills, front court work and counter "
               "attack drills."),
    dict(slug="12u-beginner", name="12u Beginner-Intermediate", group="grp:12u-beginner-intermediate", token="wgplZKVicja5wSW9z8xZ6v",
         color="#4F9A6E", coach="Andrew Falaniko and Daniel Kavesh", price="$150/month",
         level="Bronze (local scrimmages), Silver (travel tournaments, not Jr. Olympics) or Gold (travel tournaments and Jr. Olympics)",
         who="6th grade and younger, once a week. No water polo experience needed; a basic swimming ability is.",
         about="Water polo basics (swimming with the ball, egg-beater, passing and shooting), then scrimmage games and half-court "
               "drills. The goal is to introduce young athletes to water polo, build water safety skills and have fun with friends. "
               "To move up: swim 50 yards without stopping or using the bottom, egg-beater with hands out of the water for 10 "
               "seconds, and a coach's recommendation."),
    dict(slug="splashball", name="Splashball", group="grp:splashball", token="yeKdvNIFXa6TUNDcuKHmJ8", color="#1E88C8",
         coach="Andrew Falaniko and Daniel Kavesh", price="$100/month", level="Splashball (practice only) or Bronze (plus local scrimmages)",
         who="Boys and girls ages 5 to 10. No water polo experience needed; must be comfortable in the water.",
         about="A fun, introductory program. Athletes start in the shallow end swimming with the ball, passing and shooting, then "
               "play short games to wrap up. To move up to Coed Beginner: swim across the pool without stopping, be developing "
               "egg-beater and treading water, and a coach's recommendation."),
]


def out(href, label, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{E(href)}" target="_blank" rel="noopener noreferrer">{label}</a>'


def live(mode, token=CLUB, **kw):
    attrs = "".join(f' data-{k.replace("_", "-")}="{E(str(v))}"' if v is not True else f' data-{k.replace("_", "-")}' for k, v in kw.items())
    return f'data-live="{mode}" data-view="{token}"{attrs}'


def frame(token, title, height=760):
    return (f'<div class="frame"><iframe src="https://www.poolrelay.com/embed/{token}" height="{height}" title="{E(title)}" '
            f'loading="lazy"></iframe></div><p class="credit">Schedule by {out("https://www.poolrelay.com/", "Pool Relay")}</p>')


def quote(lines, src, label, who="NWPC's own text"):
    body = "".join(f"<p>{E(l)}</p>" for l in lines)
    return f'<blockquote class="quote"><span class="qh">{E(who)}, quoted from {out(src, label)}</span>{body}</blockquote>'


LIVE = '<span class="live-tag">Live</span>'

BALL = """<svg class="ball" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="47" fill="#f2c811" stroke="#000" stroke-width="4"/>
<path d="M8 40 Q50 22 92 40 M14 24 Q50 50 50 96 M86 24 Q50 50 50 96" fill="none" stroke="#000" stroke-width="3.5"/>
<path d="M6 70 L16 52 L26 70 Z M20 74 L32 50 L44 74 Z M38 78 L50 54 L62 78 Z M56 74 L68 50 L80 74 Z M74 70 L84 52 L94 70 Z" fill="#000"/></svg>"""
TREES = """<svg class="trees" viewBox="0 0 800 44" preserveAspectRatio="none" aria-hidden="true"><path fill="#000" d="M0 44 L20 14 L40 44 L55 20 L70 44 L90 6 L110 44 L130 22 L150 44 L175 10 L200 44 L220 24 L240 44 L265 8 L290 44 L310 20 L330 44 L355 12 L380 44 L400 26 L420 44 L445 6 L470 44 L490 18 L510 44 L535 10 L560 44 L580 22 L600 44 L625 8 L650 44 L670 20 L690 44 L715 12 L740 44 L760 24 L780 44 L800 16 L800 44 Z"/></svg>"""

MENU = [
    ("Home", "index.html"),
    ("About Us", [("Our Program", PROGRAM_SRC), ("Our Schedule", "schedule.html"), ("Our Facilities", "facilities.html"),
                  ("Our Coaches", NW + "/page/show/7177679-our-coaches"), ("Our Board", NW + "/board"),
                  ("For Parents", NW + "/forparents"), ("Alumni", NW + "/almuni"), ("Media", NW + "/media")]),
    ("Teams", [(t["name"], t["slug"] + ".html") for t in TEAMS]),
    ("Registration", NW + "/signup"),
    ("Tournaments", "tournaments.html"),
    ("Free Trial", NW + "/page/show/8161185-free-trial-information"),
    ("Calendar", "schedule.html#calendar"),
    ("Team Store", NW + "/page/show/7154292-team-store"),
]
SUB = ("About Us", [("Our Program", PROGRAM_SRC), ("Our Schedule", "schedule.html"), ("Our Facilities", "facilities.html"),
                    ("Our Coaches", NW + "/page/show/7177679-our-coaches"), ("Our Board", NW + "/board"),
                    ("For Parents", NW + "/forparents"), ("Alumni", NW + "/almuni"), ("Media", NW + "/media")])


def link(label, href, here):
    if href.startswith("http"):
        return out(href, E(label))
    cls = ' class="here"' if href.split("#")[0] == here else ""
    return f'<a href="{href}"{cls}>{E(label)}</a>'


def follow(selected=None, heading="Follow your team", lead=None):
    opts = "".join(f'<option value="{t["group"]}"{" selected" if t["group"] == selected else ""}>{E(t["name"])}</option>' for t in TEAMS)
    lead = lead or ("Pick your athlete's team. Pool Relay emails you when its practices change (a moved pool, a canceled night, a "
                    "new session), and the links below put the team's practices in your own calendar app, where they stay current.")
    return f"""<form class="follow" data-follow data-view="{CLUB}">
  <h2>{E(heading)}</h2>
  <p>{E(lead)}</p>
  <div class="row"><select aria-label="Team">{opts}</select>
    <input type="email" required placeholder="Parent email" aria-label="Email" autocomplete="email">
    <button class="btn y" type="submit">Follow</button></div>
  <p class="msg" aria-live="polite"></p>
  <div class="cal-links"></div>
  <p class="small" style="margin:10px 0 0;color:#999">One confirmation email first; every update has a one-click stop link. No account, no app to install.</p>
</form>"""


def page(file, title, body, sub=False):
    nav = ""
    for label, target in MENU:
        if isinstance(target, list):
            here = " here" if any(h == file for _, h in target) else ""
            nav += (f'<div class="dd{here}"><button type="button" aria-haspopup="true">{E(label)}</button><div class="panel">'
                    + "".join(link(l, h, file) for l, h in target) + "</div></div>")
        else:
            nav += link(label, target, file)
    mnav = ""
    for label, target in MENU:
        if isinstance(target, list):
            mnav += f"<h5>{E(label)}</h5>" + "".join(link(l, h, file) for l, h in target)
        else:
            mnav += link(label, target, file)
    subnav = (f'<div class="sub"><div class="in"><b>{E(SUB[0])} ›</b>' + "".join(link(l, h, file) for l, h in SUB[1]) + "</div></div>") if sub else ""
    doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a Northwest Water Polo Club website. A mock-up of {NW}
     with the practice schedule on live Pool Relay calendars. Built to demonstrate Pool Relay; not affiliated with NWPC. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{E(title)} | Northwest Water Polo Club (unofficial preview)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700&family=Lato:wght@400;700&family=Arvo:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER}">
</head>
<body>
<div class="forest" aria-hidden="true"></div>
<div class="preview-note"><b>Unofficial preview — not a Northwest Water Polo Club website.</b> A mock-up of {out(NW, "northwestwaterpoloclub.com")} with its practice schedule on live {out("https://www.poolrelay.com/", "Pool Relay")} calendars.</div>
<div class="se-bar"><span>sportsengine</span>{out(NW + "/login", "Sign In")}</div>
<header class="top"><div class="in">
  <a href="index.html" aria-label="NWPC preview home">{BALL}</a>
  <nav class="nav" aria-label="Main">{nav}</nav>
  <details class="mnav"><summary>MENU</summary><div class="mpanel">{mnav}</div></details>
</div></header>
{subnav}
<div class="col">
  <div class="banner">{BALL}<div class="wm"><b>Northwest</b><span>Water Polo Club</span></div>{TREES}</div>
  <main>
{body}
  </main>
</div>
<footer>
  <p><b style="color:#fff">Have questions? Contact Adam</b><br>Executive Director Adam Jacobson · <a href="mailto:adam@northwestwaterpoloclub.com">adam@northwestwaterpoloclub.com</a> · 206-234-8350</p>
  <p class="disc"><b>Unofficial preview.</b> Built to demonstrate embedded {out("https://www.poolrelay.com/", "Pool Relay")} schedules. Not operated by,
    endorsed by or affiliated with Northwest Water Polo Club, Phantom Lake Club or Woodridge Swim Club. Practices were entered from the
    club's {out(SCHED_SRC, "Our Schedule")} page, with season start, holiday and break dates from its {out(TOURN_SRC, "tournament schedule")} page.
    The club publishes no lanes, so which lanes each team holds is Pool Relay's estimate. Prices and program details are copied from
    {out(NW, "northwestwaterpoloclub.com")}, which remains the official source. No NWPC logo or photos are used.</p>
</footer>
<script src="finder.js?v={VER}"></script>
</body>
</html>
"""
    open(file, "w").write(doc)


def team_card(t):
    return (f'<a class="team" href="{t["slug"]}.html" style="--c:{t["color"]}"><b>{E(t["name"])}</b>'
            f'<div {live("when", t["token"], show_fac=True)}>…</div><span class="go">Team page ›</span></a>')


# ── Home ─────────────────────────────────────────────────────────────────────
page("index.html", "Home", f"""
<h1 class="pt">Welcome to Northwest Water Polo Club</h1>
<div class="two"><div>
  <p><b>Welcome!</b> Northwest Water Polo Club (NWPC) is the premier water polo organization serving Seattle, Bellevue, Mercer Island,
    and the Greater Seattle area. A non-profit, our mission is to develop young athletes through year-round training, competitive
    tournaments, and a commitment to excellence both in and out of the pool.</p>
  <p><b>Programs for All Ages and Skill Levels</b> We offer inclusive programs for boys and girls ages 5 and up, welcoming athletes at
    every stage, from beginners to elite competitors.</p>
  <p><b>Excellence in Athletics and Academics</b> NWPC athletes consistently stand out in the classroom and in competition, with a
    strong tradition of Academic All-American honorees (minimum 3.5 GPA).</p>
</div><div class="side">
  <h2>Registration now open</h2>
  {out(NW + "/signup", "Register: Team Registration", "btn")}
  <p class="small">Still deciding? {out(NW + "/page/show/8161185-free-trial-information", "Learn about our free trial")}.</p>
  <h3>Next practice {LIVE}</h3>
  <p class="small"><span {live("next", show_title=True)}>…</span></p>
</div></div>

{follow()}

<h2>This week's practices {LIVE}</h2>
<p class="small muted">Every team, from the same calendar the coaches keep. When a practice moves, this list, each team page and every
  follower's calendar change together.</p>
<div class="week" {live("week", show_fac=True)}><p class="muted">Loading the week…</p></div>

<h2>Find your team</h2>
<div class="teams">{"".join(team_card(t) for t in TEAMS)}</div>

<div class="trip"><span class="tag">Travel tournament</span>
  <h2>Kap 7 Holiday Cup, Orange County</h2>
  <p>HS Boys, HS Girls and 14u are traveling to the Kap7 Holiday Cup, run by SET Water Polo Club and Irvine Youth Water Polo Corporation.
    Trip details, fees and packing list are on the {link("Tournaments", "tournaments.html", "index.html")} page.</p>
</div>

<h2 id="calendar">The whole club on one calendar {LIVE}</h2>
<p class="small muted">Every team's practices, each block naming its pool. Tap a team in the filter row to see only that team; its
  <b>Subscribe</b> button does the same thing as Follow above.</p>
{frame(CLUB, "Northwest Water Polo Club practices", 780)}

<h2>What's different in this preview</h2>
<div class="ba">
  <div><h3>Today on northwestwaterpoloclub.com</h3><ul>
    <li>The practice schedule is a paragraph per team on the Our Schedule page, and one team's line names no pool for two of its days.</li>
    <li>Start dates, holidays and breaks are on a different page (the tournament schedule), so a parent reads both.</li>
    <li>The site's Calendar page shows no practices.</li>
    <li>When a night moves, parents hear by message, and the page has to be edited by hand.</li></ul></div>
  <div class="a"><h3>In this preview</h3><ul>
    <li>One calendar, kept by the coaches, with each practice in its pool and lanes, holidays and breaks already left out.</li>
    <li>Each team has its own page and calendar, and every day and time on the site is read from that calendar.</li>
    <li>Parents follow their team: a change email, and the practices in Google, Apple or Outlook Calendar, always current.</li>
    <li>The pools see the same bookings: see the {out(PL_SITE, "Phantom Lake")} and {out(WR_SITE, "Woodridge")} previews.</li></ul></div>
</div>
""")

# ── Our Schedule ─────────────────────────────────────────────────────────────
rows = "".join(f'<div class="pool"><h3>{link(t["name"], t["slug"] + ".html", "")}</h3><div {live("when", t["token"], show_fac=True)}>…</div>'
               f'<p class="small" style="margin:0">Next: <span {live("next", t["token"])}>…</span></p></div>' for t in TEAMS)
page("schedule.html", "Our Schedule", f"""
<h1 class="pt">Our Schedule</h1>
<p>Each team's practice days, times and pool, read live from the club's calendar. Holidays and breaks are already left out. The
  published practices run <b><span {live("through")}>…</span></b>.</p>
{rows}
{follow(heading="Get your team's changes by email")}
<h2 id="calendar">Club calendar {LIVE}</h2>
{frame(CLUB, "Northwest Water Polo Club practices", 780)}
<h2>As published today</h2>
{quote(["2026 FALL SESSION - SEPTEMBER 1 TO NOVEMBER 22",
        "HS Girls/14u Girls: Mon & Wed 7:30pm-9:30pm @ Phantom Lake; Tue 8:00-9:30pm @ Woodridge; Thu 8:00pm-9:30pm @ Phantom Lake",
        "HS Boys/14u: Mon & Wed 7:30pm -9:30pm; Tue & Thu 8:00-9:30pm @ Phantom Lake",
        "12u Boys/Girls 3x-a-week: Tue & Thu 7:30-9:00pm @ Woodridge; Sun 10:30am-12pm @ Woodridge",
        "12u boys/girls (beginner/intermediate): Sun 10:30am-12pm @ Woodridge",
        "Splashball: Sun 10-11am @ Woodridge"], SCHED_SRC, "Our Schedule")}
{quote(["Sept 1 - HS & 14u practices start", "NO Practice Sun 9/6 & Mon 9/7 due to Labor Day",
        "Sept 8 - 12u, 10u, and Splashball practices start", "11/20 - 11/29 NO PRACTICE THANKSGIVING BREAK", "11/30 - Winter Session Starts"],
       TOURN_SRC, "2026-2027 Season Tournament Schedule")}
<p class="small muted">The holiday break on the tournament schedule starts before the session end date on the Our Schedule page; the
  calendar follows the break. The winter session's practice times are not published yet, so the calendar has none.</p>
""", sub=True)

# ── Team pages ───────────────────────────────────────────────────────────────
for t in TEAMS:
    note = f'<p class="small muted">{E(t["note"])}</p>' if t.get("note") else ""
    page(t["slug"] + ".html", t["name"], f"""
<h1 class="pt">{E(t["name"])}</h1>
<div class="two"><div>
  <p>{E(t["who"])}</p>
  <p>{E(t["about"])}</p>
  <ul class="facts"><li><b>Cost:</b> <span class="price">{E(t["price"])}</span></li>
    <li><b>USAWP membership level:</b> {E(t["level"])}</li><li><b>Coaches:</b> {E(t["coach"])}</li></ul>
</div><div class="side">
  <h2>Practices {LIVE}</h2>
  <div {live("when", t["token"], show_fac=True)}>…</div>
  <h3>Next practice</h3><p><span {live("next", t["token"])}>…</span></p>
  <p class="small muted">Published practices run <span {live("through", t["token"])}>…</span>.</p>
  {out(NW + "/signup", "Register", "btn")}
</div></div>
{note}
{follow(t["group"], heading=f"Follow {t['name']}", lead="Get an email when this team's practices change, and put its practices in your own calendar app. Families with athletes on more than one team can follow each.")}
<h2>This week {LIVE}</h2>
<div class="week" {live("week", t["token"], show_fac=True, skip_empty=True)}><p class="muted">Loading…</p></div>
<h2>{E(t["name"])} calendar {LIVE}</h2>
{frame(t["token"], t["name"] + " practices", 700)}
""")

# ── Our Facilities ───────────────────────────────────────────────────────────
POOLS = [
    ("Woodridge Swim Club", "12320 SE 14th St, Bellevue, WA 98005", WR_SITE, "Woodridge Swim Club",
     "Six-lane, 25-yard pool with a deep end and diving board; a member-owned club in the Woodridge neighborhood."),
    ("Phantom Lake Club", "15810 SE 24th St, Bellevue, WA 98008", PL_SITE, "Phantom Lake Club",
     "Six-lane, 25-yard competition pool (44 by 75 feet) with a dive board, on the shore of Phantom Lake; a member-owned club."),
]
pools = "".join(f"""<div class="pool"><h3>{E(n)}</h3><p class="small">{E(a)} · {out("https://maps.google.com/?q=" + a.replace(" ", "+"), "Map")}</p>
<p>{E(d)}</p><p><b>NWPC practices here {LIVE}</b></p><div {live("when", fac=f, by_title=True)}>…</div>
<p class="small">{out(s, "See this pool's own schedule (preview)")}</p></div>""" for n, a, s, f, d in POOLS)
page("facilities.html", "Our Facilities", f"""
<h1 class="pt">Our Facilities</h1>
<p>Which team is in which pool, read live from the club calendar.</p>
{pools}
<div class="pool"><h3>Mercer Island Beach Club</h3><p class="small">8326 Avalon Dr, Mercer Island, WA 98040</p>
  <p class="muted small">Listed by the club; no practices there on the current schedule.</p></div>
<div class="pool"><h3>Medgar Evers</h3><p class="small">500 23rd Ave, Seattle, WA 98122</p>
  <p class="muted small">Listed by the club; no practices there on the current schedule.</p></div>
""", sub=True)

# ── Tournaments ──────────────────────────────────────────────────────────────
page("tournaments.html", "Tournaments", f"""
<h1 class="pt">Tournaments</h1>
<div class="trip"><span class="tag">Next travel tournament</span>
  <h2>Kap7 Holiday Cup, Orange County</h2>
  <p>NWPC is traveling to the Kap7 Holiday Cup, a tournament run by SET Water Polo Club and Irvine Youth Water Polo Corporation in
    Orange County. NWPC does not run it; the host publishes the game schedule and venues.</p>
  {quote(["Register: Kap 7 Holiday Cup Dec 12 - Dec 13 HS Boys/Girls/14u Boys"], REG_SRC, "Tournament Registration")}
  {quote(["12/12-12/13 (HS Boys, HS Girls, 14u Boys/Girls) K7 Holiday Invite @ Irvine, CA"], TOURN_SRC, "2026-2027 Season Tournament Schedule")}
  {quote(["13TH ANNUAL KAP7 HOLIDAY CUP", "December 12 & 13, 2026", "Orange County"], KAP7, "Kahuna Events", who="The host's event listing")}
  <p>{out(REG_SRC, "Tournament registration", "btn")} {out(KAP7, "Host's event page", "btn")}</p>
  <p class="small muted">The host's listing shows 14U Girls but no 16U or 18U girls division, while the club lists HS Girls as going;
    the coaches will confirm which girls' teams travel.</p>
</div>
<h2>Trip planning</h2>
<ul class="facts">
  <li><b>14u and up, travel tournaments:</b> fees include tournament entry, hotels and team vans at the destination. Families book
    flights, with direction from the coaches so the team can travel together. Estimated fee $400 per athlete per tournament.</li>
  <li><b>Meals:</b> athletes pay for their own, around $40–60 per day. Tell the coach about allergies or dietary needs.</li>
  <li><b>Meeting:</b> at the airline's check-in counter, usually about an hour and a half before the flight.</li>
  <li><b>Pack light:</b> one swim/water polo bag. NWPC suit (or an all-black polo suit), NWPC shirt or hoodie, towel, running shoes,
    water bottle, goggles, medications, phone charger.</li>
  <li><b>Coming home:</b> meet your athlete at the gate (with the airline's escort pass) or outside security.</li>
</ul>
<p class="small">Full details on the club's {out(NW + "/page/show/7181436-tournament-information", "Tournament Travel Information")} page.</p>
<h2>Practice while the team travels {LIVE}</h2>
<p class="small muted">Practices for each team come from the club calendar; a canceled night shows here and in followers' calendars as soon as a coach removes it.</p>
<div class="week" {live("week", days=14, show_fac=True, skip_empty=True)}><p class="muted">Loading…</p></div>
""")
print("built", len(TEAMS) + 4, "pages")
