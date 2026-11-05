# Northwest Water Polo Club — unofficial preview

A mock-up of [northwestwaterpoloclub.com](https://www.northwestwaterpoloclub.com) (Home, Our Schedule, a page per team, Our Facilities,
Tournaments) in the look of the club's SportsEngine site, with its practices on live [Pool Relay](https://www.poolrelay.com) calendars.
Not operated by, endorsed by or affiliated with Northwest Water Polo Club. No NWPC logo or photos are used.

No schedule is typed into the pages. Practice days, times, pools, "next practice", "this week" and how far the season runs are filled
by `finder.js` from the live Pool Relay views; `build.py` holds only prices, ages, program descriptions and coaches, plus quotes of the
club's schedule that are labeled as quotes. `check.py` fails if a time, weekday or date appears outside a script or a labeled quote.

- `build.py`: generates the pages (`python3 build.py && python3 check.py`).
- `finder.js`: `data-live` elements (`today`, `week`, `when`, `next`, `through`, `closures`) and the **Follow your team** form, which
  posts to Pool Relay's double opt-in subscribe endpoint and offers Google / Apple / Outlook calendar links for the team's feed.
- Pool Relay views: `GLtzZAMK32smkH6Y8wGHhw` (whole club, week; feeds the club-wide text and the Follow form). Team tabs, each locked
  to the team's group: HS Girls & 14u Girls `orz6Web4Pj1MEfpoxOgA1T`, HS Boys & 14u `4g9FthSAAnr3nI8vKQynQN`, 12u 3x-a-week
  `aCHMsuDRoUxUjactVoVqQE`, 12u Beginner-Intermediate `wgplZKVicja5wSW9z8xZ6v`, Splashball `yeKdvNIFXa6TUNDcuKHmJ8`.
- Data: entered 2026-11-05 from the club's Our Schedule page (2026 Fall Session) and its 2026-2027 tournament schedule (start dates,
  Labor Day, Thanksgiving break). Lanes are Pool Relay's estimate. HS Boys & 14u Mon/Wed has no pool in the source; Phantom Lake is an estimate.
- The Kap7 Holiday Cup is run by SET Water Polo Club and Irvine Youth Water Polo Corporation; NWPC is attending, not hosting.
- Sister previews: [Phantom Lake Club](https://psmoore.github.io/pool_phantomlake/), [Woodridge Swim Club](https://psmoore.github.io/pool_woodridge/).
