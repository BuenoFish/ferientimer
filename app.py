import streamlit as st
from datetime import date, datetime
import math

# ── Seitenkonfiguration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lunas Ferienkalender - Sachsen",
    page_icon="🐱",
    layout="centered",
)

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Hintergrund */
  .stApp { background: linear-gradient(135deg, #fdf6e3 0%, #fce4ec 100%); }

  /* Karten */
  .card {
      background: white;
      border-radius: 18px;
      padding: 1.2rem 1.6rem;
      margin-bottom: 0.8rem;
      box-shadow: 0 4px 14px rgba(0,0,0,0.08);
      border-left: 6px solid #f48fb1;
  }
  .card.next {
      border-left: 6px solid #ff6090;
      background: linear-gradient(90deg, #fff0f5, #fff);
  }
  .days-big {
      font-size: 3.2rem;
      font-weight: 800;
      color: #e91e63;
      line-height: 1;
  }
  .ferien-name {
      font-size: 1.3rem;
      font-weight: 700;
      color: #333;
  }
  .ferien-dates {
      font-size: 0.95rem;
      color: #777;
  }
  .ferienzeit {
      font-size: 1rem;
      color: #e91e63;
      font-weight: 600;
  }
  .luna-quote {
      background: #fff8e1;
      border-radius: 16px;
      padding: 1rem 1.4rem;
      margin: 1.2rem 0;
      font-style: italic;
      color: #555;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      border-left: 5px solid #ffca28;
  }
  .progress-bar-bg {
      background: #f3f3f3;
      border-radius: 10px;
      height: 12px;
      margin-top: 0.5rem;
  }
  .progress-bar-fill {
      background: linear-gradient(90deg, #ff6090, #ff8fab);
      border-radius: 10px;
      height: 12px;
  }
</style>
""", unsafe_allow_html=True)

# ── Feriendaten (Quelle: sachsen.de, offizielle VwV) ──────────────────────────
ferien_alle = [
    # 2025/2026
    {"name": "🎄 Weihnachtsferien",   "von": date(2025, 12, 22), "bis": date(2026,  1,  2)},
    {"name": "❄️ Winterferien",        "von": date(2026,  2,  9), "bis": date(2026,  2, 21)},
    {"name": "🐣 Osterferien",         "von": date(2026,  4,  3), "bis": date(2026,  4, 10)},
    {"name": "☀️ Sommerferien",         "von": date(2026,  7,  4), "bis": date(2026,  8, 14)},
    # 2026/2027
    {"name": "🍂 Herbstferien",        "von": date(2026, 10, 12), "bis": date(2026, 10, 24)},
    {"name": "🎄 Weihnachtsferien",    "von": date(2026, 12, 23), "bis": date(2027,  1,  2)},
    {"name": "❄️ Winterferien",         "von": date(2027,  2,  8), "bis": date(2027,  2, 19)},
    {"name": "🐣 Osterferien",          "von": date(2027,  3, 26), "bis": date(2027,  4,  2)},
    {"name": "🌸 Pfingstferien",        "von": date(2027,  5, 15), "bis": date(2027,  5, 18)},
    {"name": "☀️ Sommerferien",          "von": date(2027,  7, 10), "bis": date(2027,  8, 20)},
]

# ── Lunas Sprüche (von der Katze 😂) ──────────────────────────────────────────
luna_sprueche_countdown = [
    "Ich hab genau nachgezählt – mit meinen Schwanzklopfern.",
    "Solange noch Schule ist, benutze ich deinen Platz auf dem Sofa.",
    "Ich trainiere schon mal Schnurren für die Ferienzeit. Wird toll.",
    "Mein Fell liegt bereit. Beeil dich mit den Ferien.",
    "Ferien bedeuten: mehr Streicheln und Besuch bei Annas Katzen.",
    "Jeden Tag, den du arbeitest, stirbt ein Knäuel Wolle.",
    "Ich esse jetzt deine Pflanzen. Das ist keine Drohung. Es ist ein Countdown.",
]
luna_sprueche_ferien = [
    "ES SIND FERIEN! Ich hab dir schon deinen Kuschelpatz reserviert.",
    "Ferien! Endlich kann ich dich bei jeder Gelegenheit anschnurren. Der Plan läuft.",
    "Ferien!! Mein Schnurrmotor läuft auf Hochtouren. Du wurdest gewarnt.",
    "FERIEN. Ich lasse die Legoblumen diesmal stehen. Als Zeichen des guten Willens.",
]

# ── Logik ──────────────────────────────────────────────────────────────────────
heute = date.today()

def tage_bis(d: date) -> int:
    return (d - heute).days

# Nächste Ferien finden
naechste = None
aktuelle = None
for f in ferien_alle:
    if f["von"] <= heute <= f["bis"]:
        aktuelle = f
        break
    if f["von"] > heute and naechste is None:
        naechste = f

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("## 🐱 Lunas Schulferienkalender")
st.markdown("#### Sachsen – Countdown für Lehrerinnen, die es verdienen 🎓")

st.write("")

# ── Luna-Bild (ASCII-Art als Platzhalter, da kein Upload) ─────────────────────
st.markdown("""
```
   /\\_____/\\
  /  o   o  \\      Hi! Ich bin Luna! 🐾
 ( ==  ^  == )     Britisch Kurzhaar, Expertin für
  )         (      Ferienplanung und Sofabelegung.
 (           )
  \\ .___._ /
   \\       /
```
""")

# ── Heute ─────────────────────────────────────────────────────────────────────
st.markdown(f"📅 **Heute ist der {heute.strftime('%d.%m.%Y')}**")
st.write("")

# ── Aktuell Ferien? ────────────────────────────────────────────────────────────
if aktuelle:
    rest = tage_bis(aktuelle["bis"])
    import random
    spruch = random.choice(luna_sprueche_ferien)
    st.markdown(f"""
    <div class="card next">
        <div class="ferienzeit">🎉 Es sind gerade Ferien!</div>
        <div class="ferien-name">{aktuelle['name']}</div>
        <div class="ferien-dates">
            {aktuelle['von'].strftime('%d.%m.%Y')} – {aktuelle['bis'].strftime('%d.%m.%Y')}
        </div>
        <div style="margin-top:0.5rem; color:#777;">
            Noch <strong>{rest} Tag{"e" if rest != 1 else ""}</strong> Ferien verbleibend 🎊
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="luna-quote">🐾 <strong>Luna sagt:</strong> „{spruch}"</div>', unsafe_allow_html=True)

# ── Nächste Ferien Countdown ────────────────────────────────────────────────────
if naechste and not aktuelle:
    tage = tage_bis(naechste["von"])
    import random
    spruch = random.choice(luna_sprueche_countdown)

    # Fortschrittsbalken (wie viel % bis zur nächsten Ferien vergangen?)
    # Einfache Schätzung: max 100 Tage als Referenz
    prozent = max(0, min(100, int((1 - tage / max(tage, 1)) * 100)))

    st.markdown(f"""
    <div class="card next">
        <div class="ferienzeit">⏳ Nächste Ferien:</div>
        <div class="ferien-name">{naechste['name']}</div>
        <div class="ferien-dates">
            {naechste['von'].strftime('%d.%m.%Y')} – {naechste['bis'].strftime('%d.%m.%Y')}
        </div>
        <div class="days-big" style="margin-top:0.6rem;">{tage}</div>
        <div style="color:#888; font-size:1rem;">Tag{"e" if tage != 1 else ""} noch bis zur Freiheit 🚀</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="luna-quote">🐾 <strong>Luna sagt:</strong> „{spruch}"</div>', unsafe_allow_html=True)

# ── Alle kommenden Ferien ──────────────────────────────────────────────────────
st.write("")
st.markdown("### 📆 Alle kommenden Ferien auf einen Blick")

zukuenftige = [f for f in ferien_alle if f["bis"] >= heute]

for i, f in enumerate(zukuenftige):
    tage = tage_bis(f["von"])
    laenge = (f["bis"] - f["von"]).days + 1

    if f["von"] <= heute <= f["bis"]:
        status = "🟢 Gerade jetzt!"
        tage_str = "Jetzt genießen! 🎉"
    elif tage == 0:
        status = "🔔 Morgen geht's los!"
        tage_str = "Morgen!"
    elif tage < 0:
        tage_str = "Läuft gerade"
        status = ""
    else:
        tage_str = f"in {tage} Tag{'en' if tage != 1 else ''}"
        status = ""

    is_next = (naechste and f == naechste and not aktuelle)
    card_class = "card next" if is_next else "card"

    dauer_info = f"{laenge} Tag{'e' if laenge != 1 else ''}" if laenge > 1 else "1 Tag"

    st.markdown(f"""
    <div class="{card_class}">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="ferien-name">{f['name']}</div>
                <div class="ferien-dates">
                    {f['von'].strftime('%d.%m.%Y')} – {f['bis'].strftime('%d.%m.%Y')}
                    &nbsp;·&nbsp; {dauer_info}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:1.6rem; font-weight:800; color:#e91e63;">{tage_str}</div>
                <div style="font-size:0.85rem; color:#aaa;">{status}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Schuljahr 2027+ Hinweis ────────────────────────────────────────────────────
st.write("")
with st.expander("📋 Noch mehr Ferien: Schuljahre 2027/28, 2028/29, 2029/30"):
    weitere = [
        # 2027/2028
        {"name": "🍂 Herbstferien 27/28",  "von": date(2027, 10, 11), "bis": date(2027, 10, 23)},
        {"name": "🎄 Weihnachtsferien",    "von": date(2027, 12, 23), "bis": date(2028,  1,  1)},
        {"name": "❄️ Winterferien",         "von": date(2028,  2, 14), "bis": date(2028,  2, 26)},
        {"name": "🐣 Osterferien",          "von": date(2028,  4, 14), "bis": date(2028,  4, 22)},
        {"name": "☀️ Sommerferien",          "von": date(2028,  7, 22), "bis": date(2028,  9,  1)},
        # 2028/2029
        {"name": "🍂 Herbstferien 28/29",  "von": date(2028, 10, 23), "bis": date(2028, 11,  3)},
        {"name": "🎄 Weihnachtsferien",    "von": date(2028, 12, 23), "bis": date(2029,  1,  3)},
        {"name": "❄️ Winterferien",         "von": date(2029,  2,  5), "bis": date(2029,  2, 16)},
        {"name": "🐣 Osterferien",          "von": date(2029,  3, 29), "bis": date(2029,  4,  6)},
        {"name": "🌸 Pfingstferien",        "von": date(2029,  5, 19), "bis": date(2029,  5, 22)},
        {"name": "☀️ Sommerferien",          "von": date(2029,  7, 21), "bis": date(2029,  8, 31)},
    ]
    for f in weitere:
        tage = tage_bis(f["von"])
        if tage >= 0:
            st.markdown(f"**{f['name']}**: {f['von'].strftime('%d.%m.%Y')} – {f['bis'].strftime('%d.%m.%Y')} *(in {tage} Tagen)*")
        else:
            st.markdown(f"**{f['name']}**: {f['von'].strftime('%d.%m.%Y')} – {f['bis'].strftime('%d.%m.%Y')}")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.write("")
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#aaa; font-size:0.85rem;">
    🐾 Gemacht mit Liebe (und Lunas Pfoten) &nbsp;·&nbsp;
    Daten: <a href="https://www.schule.sachsen.de/schuljahrestermine-4793.html" target="_blank" style="color:#f48fb1;">sachsen.de (offiziell)</a>
    <br>Luna genehmigt diese App 😺
</div>
""", unsafe_allow_html=True)
