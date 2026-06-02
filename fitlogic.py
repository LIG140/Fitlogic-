import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="FitLogic", page_icon="🏋️‍♂️", layout="wide")

# --- HARDCORE DESIGN-TRICK: Dunkles Bodybuilding Theme ---
hintergrund_url = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070&auto=format&fit=crop"

st.markdown(
    f"""
    <style>
    /* Haupt-Hintergrund */
    .stApp {{
        background-image: url("{hintergrund_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Dunkler, harter Glaseffekt für den Container */
    .stMainBlockContainer {{
        background-color: rgba(10, 10, 10, 0.92); /* Fast schwarz */
        padding: 50px !important;
        border-radius: 20px;
        border: 1px solid rgba(255, 50, 50, 0.3); /* Roter Rand */
        box-shadow: 0px 0px 30px rgba(255, 0, 0, 0.2); /* Roter Schein */
    }}
    
    /* Sidebar anpassen */
    [data-testid="stSidebar"] {{
        background-color: rgba(15, 15, 15, 0.95);
        border-right: 1px solid rgba(255, 50, 50, 0.3);
    }}
    
    /* Überschriften in Gold/Rot */
    h1, h2, h3 {{
        color: #ff4b4b !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    
    /* Metric Werte hervorheben */
    [data-testid="stMetricValue"] {{
        color: #ffd700 !important; /* Gold */
        font-weight: 900 !important;
        font-size: 1.8em !important;
    }}
    
    /* Buttons anpassen */
    .stButton>button {{
        background-color: #ff4b4b;
        color: white;
        border: none;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #ff0000;
        box-shadow: 0px 0px 15px rgba(255, 0, 0, 0.5);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- SIDEBAR: EINGABEN ---
with st.sidebar:
    st.title("⚙️ DEIN PROFIL")
    st.write("Gib deine Daten ein, Krieger.")
    
    name = st.text_input("Name:", placeholder="Gib deinen Namen ein...")
    alter = st.number_input("Alter:", min_value=16, max_value=80, value=25)
    gewicht = st.number_input("Gewicht (kg):", min_value=40.0, max_value=200.0, value=85.0, step=0.5)
    groesse = st.number_input("Größe (cm):", min_value=140.0, max_value=220.0, value=180.0, step=1.0)
    geschlecht = st.selectbox("Geschlecht:", ["Männlich", "Weiblich"])
    
    st.markdown("---")
    ziel = st.selectbox("Wähle deine Mission:", [
        "🔥 Fat Loss (Definition)", 
        "💪 Lean Mass (Aufbau ohne Fett)", 
        "🐻 Mass Gain (Masse & Kraft)", 
        "🏆 Pro-Bodybuilding (Elite)"
    ])
    
    aktivitaet = st.selectbox("Aktivitätslevel:", [
        "Sitzend (Büro)", 
        "Leicht aktiv (3x/Woche)", 
        "Sehr aktiv (6x hartes Training)", 
        "Extrem (Profi-Level + körperlicher Job)"
    ])

# --- HAUPTBEREICH ---
st.title("🏋️‍♂️ FITLOGIC")
st.caption("Fortschritt um jeden Preis")  # <--- HIER IST DEINE NEUE CAPTION
st.markdown(f"### Willkommen, **{name if name else 'Krieger'}**. Zeit zu schmieden.")

if st.button("⚡ PLAN GENERIEREN ⚡"):
    
    # --- 1. KALORIEN & MAKRO BERECHNUNG ---
    if geschlecht == "Männlich":
        bmr = (10 * gewicht) + (6.25 * groesse) - (5 * alter) + 5
    else:
        bmr = (10 * gewicht) + (6.25 * groesse) - (5 * alter) - 161
        
    # Aktivitätsfaktor
    aktiv_faktor = {"Sitzend (Büro)": 1.2, "Leicht aktiv (3x/Woche)": 1.4, "Sehr aktiv (6x hartes Training)": 1.6, "Extrem (Profi-Level + körperlicher Job)": 1.8}
    tdee = bmr * aktiv_faktor[aktivitaet]
    
    # Ziel-Kalorien & Makros
    if ziel == "🔥 Fat Loss (Definition)":
        kalorien_ziel = tdee - 500
        protein_faktor = 2.4 # Sehr hoch zum Muskelerhalt
        fat_faktor = 0.8
    elif ziel == "💪 Lean Mass (Aufbau ohne Fett)":
        kalorien_ziel = tdee + 200
        protein_faktor = 2.2
        fat_faktor = 1.0
    elif ziel == "🐻 Mass Gain (Masse & Kraft)":
        kalorien_ziel = tdee + 500
        protein_faktor = 2.0
        fat_faktor = 1.2
    elif ziel == "🏆 Pro-Bodybuilding (Elite)":
        kalorien_ziel = tdee + 400 # Clean Bulk auf Pro-Level
        protein_faktor = 2.5 # Extrem hohe Proteinzufuhr
        fat_faktor = 1.0

    # Makro-Berechnung (1g Protein = 4kcal, 1g Fat = 9kcal, Rest Carbs = 4kcal)
    protein_g = round(gewicht * protein_faktor)
    fat_g = round(gewicht * fat_faktor)
    carb_kcal = kalorien_ziel - (protein_g * 4) - (fat_g * 9)
    carb_g = round(carb_kcal / 4)
    if carb_g < 0: carb_g = 50 # Fallback

    # --- 2. ERNÄHRUNGS-DASHBOARD ---
    st.header("🥩 DEIN ERNÄHRUNGSPLAN")
    
    col_k1, col_k2, col_k3 = st.columns(3)
    with col_k1:
        st.metric(label="BMR (Grundumsatz)", value=f"{round(bmr)} kcal")
    with col_k2:
        st.metric(label="TDEE (Gesamtumsatz)", value=f"{round(tdee)} kcal")
    with col_k3:
        st.metric(label="ZIEL-KALORIEN", value=f"{round(kalorien_ziel)} kcal")

    st.markdown("---")
    st.subheader("📊 Makronährstoff-Verteilung (Daily Target)")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Protein", value=f"{protein_g} g", delta="Muskelaufbau")
    with col_m2:
        st.metric(label="Kohlenhydrate", value=f"{carb_g} g", delta="Energie")
    with col_m3:
        st.metric(label="Fette", value=f"{fat_g} g", delta="Hormone")

    # --- 3. TRAININGSPLAN ---
    st.header("🗡️ TRAININGS PROTOKOLL")

    if ziel == "🔥 Fat Loss (Definition)":
        st.write("**Modus:** Zirkeltraining & High-Intensity Interval Training (HIIT)")
        st.write("4x pro Woche. 40 Sek Arbeit, 20 Sek Pause. 4 Runden.")
        exercises = ["Burpees", "Kettlebell Swings", "Sprungkniebeugen", "Mountain Climbers", "Battle Ropes"]
        for ex in exercises:
            st.markdown(f"- ⚡ **{ex}**")
            
    elif ziel == "💪 Lean Mass (Aufbau ohne Fett)":
        st.write("**Modus:** Upper/Lower Split (Oberkörper/Unterkörper) - 4x pro Woche")
        st.write("Fokus auf progressive Überlastung. 3 Sätze à 8-12 Wdh.")
        exercises = ["Bankdrücken (Langhantel)", "Kurzhantel-Flyes", "Latzug zur Brust", "Beinpresse", "Rudern vorgebeugt"]
        for ex in exercises:
            st.markdown(f"- 💪 **{ex}**")

    elif ziel == "🐻 Mass Gain (Masse & Kraft)":
        st.write("**Modus:** Push/Pull/Legs - 6x pro Woche. Heavy Compound Lifts!")
        st.write("5 Sätze à 5-8 Wdh. bei 80-90% 1RM (One Rep Max).")
        exercises = ["Schwere Kniebeugen", "Kreuzheben", "Bankdrücken", "Militärdücken (OHP)", "Rudern T-Bar"]
        for ex in exercises:
            st.markdown(f"- 🐻 **{ex}**")

    elif ziel == "🏆 Pro-Bodybuilding (Elite)":
        st.write("**Modus:** Bro-Split / Hypertrophie-Spezialisierung - 5-6x pro Woche")
        st.write("Intensitätstechniken: Drop-Sets, Supersätze, Faszien-Training (FST-7). 4 Sätze à 10-15 Wdh.")
        exercises = ["Brust: Schrägbank Kurzhantel + Flyes (Supersatz)", "Rücken: Rudern + Latzug (Supersatz)", "Beine: Hackenschmidt + Beinstrecker (Drop-Set)", "Schultern: Seitheben FST-7 (7 Sätze à 12 Wdh.)"]
        for ex in exercises:
            st.markdown(f"- 🏆 **{ex}**")

    # --- 4. SUPPLEMENTE & ADVANCED PROTOCOLS ---
    st.header("🧪 SUPPLEMENTE & ADVANCED STACKS")

    if ziel != "🏆 Pro-Bodybuilding (Elite)":
        st.subheader("Natty (Natürliche) Basis-Supplemente")
        st.info(
            f"**1. Kreatin Monohydrat:** 5g täglich (Immer!)\n\n"
            f"**2. Whey Isolat:** Zur Erreichung der {protein_g}g Protein.\n\n"
            f"**3. Omega-3 (Fischöl):** 2-3g EPA/DHA für Gelenke & Entzündungshemmer.\n\n"
            f"**4. Pre-Workout (Koffein):** 200-400mg vor dem Training."
        )
    
    else: # PRO BODYBUILDING STACK
        st.subheader("🏆 Pro-Level Nährstoffoptimierung")
        st.info(
            f"**Basis:** Kreatin (10g/Tag), Whey Isolat, EAA's während dem Training, Citrullin Malate (8g Pre-Workout für den Pump)."
        )
        
        st.markdown("---")
        st.subheader("☢️ ADVANCED: Aufklärung zu PEDs (Performance Enhancing Drugs)")
        st.error("⚠️ **MEDIZINISCHE WARNUNG & RECHTLICHER HINWEIS:** Die folgenden Informationen dienen ausschließlich der **Harm Reduction (Schadensminderung)** und Aufklärung. Anabolika sind in Deutschland/D/A/CH ohne Rezept illegal (BTM-Gesetz) und verursachen schwere Organschäden, Herz-Kreislauf-Erkrankungen, Hormonabsturz und psychiatrische Probleme. **Nutze dies NICHT als Anleitung, sondern um zu verstehen, was im Pro-Bereich passiert.**")
        
        with st.expander("🔬 Klicke hier für die wissenschaftliche Aufklärung (Der sogenannte 'Safestack')"):
            st.warning(
                "**Was im Pro-Bereich als 'Safestack' (Einsteiger-Kur) bezeichnet wird:**\n\n"
                "Ein sogenannter 'Safestack' existiert nicht im Sinne von 'ungefährlich'. Gefährlichkeit ist nur eine Frage des Ausmaßes. "
                "In Bodybuilding-Foren wird oft eine reine Testosteron-Kur (Testosterone Only Cycle) als das 'sicherste' Einstiegsprotokoll diskutiert, "
                "da der Körper Testosteron kennt und man nicht mehrere unbekannte Substanzen mischt.\n\n"
                "**Das hypothetische (und illegal anwendbare) Protokoll lautet meistens:**\n"
                "- **Substanz:** Testosteron Enantate (Testo E)\n"
                "- **Dosis:** 250mg - 500mg pro Woche (Der natürliche Mann produziert ca. 50-70mg/Woche!)\n"
                "- **Dauer:** 10-12 Wochen\n"
                "- **Begleitmedikation (WICHTIG):** Ein Aromatasehemmer (z.B. Arimidex/Exemestan), um die Umwandlung in Östrogen (Gynäkomastie/Wassereinlagerungen) zu verhindern.\n\n"
                "**Nach der Kur (PCT - Post Cycle Therapy):**\n"
                "Da die eigene Hormonproduktion komplett eingeschlafen ist, MUSS eine PCT erfolgen, um den natürlichen Testosteronspiegel wiederherzustellen (z.B. mit HCG, Clomid, Tamoxifen). Ohne PCT droht der 'Crash' (Depression, Muskelverlust, Impotenz).\n\n"
                "**Risiken selbst bei 'nur' Testo:**\n"
                "- Haarverlust (falls genetisch bedingt)\n"
                "- Akne\n"
                "- Erhöhte Blutwerte (Hämatokrit -> Blutverdickung -> Schlaganfallrisiko)\n"
                "- Bluthochdruck\n"
                "- Ständige Blutkontrollen (Bilder) sind zwingend notwendig."
            )
            
            st.error("**Fazit:** Auch der 'Safestack' greift massiv in das Endokrine System ein. Wenn du nicht als Profi vom Leben leben musst, lass es. Naturals haben den längeren Atem und eine intakte Gesundheit.")

    st.markdown("---")
    st.caption("FITLOGIC 💀 Fortschritt um jeden Preis.") # <--- FOOTER AUCH ANGEPASST
