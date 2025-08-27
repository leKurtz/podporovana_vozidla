import pandas as pd
import streamlit as st

# CSV soubor (ve stejné složce jako skript)
CSV_FILE = "podporovana_vozidla.csv"

# Načtení CSV – české CSV často používá středník a kódování cp1250
try:
    df = pd.read_csv(CSV_FILE, sep=';', encoding='cp1250')
except FileNotFoundError:
    st.error(f"Soubor {CSV_FILE} nebyl nalezen. Zkontrolujte cestu.")
    st.stop()
except Exception as e:
    st.error(f"Chyba při načítání CSV: {e}")
    st.stop()

st.title("Kontrola podpory HW pro vozidla")

# Formulář pro zadání vstupů
with st.form("hledani_form"):
    hw = st.text_input("Zadej typ HW (820, FMX003, FMX150)").strip()
    vyrobce = st.text_input("Zadej výrobce vozidla").strip()
    model = st.text_input("Zadej model vozidla").strip()
    submitted = st.form_submit_button("Hledat")

if submitted:
    if hw and vyrobce and model:
        filtrovano = df[
            (df['HW'].astype(str).str.strip().str.lower() == hw.lower()) &
            (df['Vyrobce'].astype(str).str.strip().str.lower() == vyrobce.lower()) &
            (df['Model'].astype(str).str.strip().str.lower() == model.lower())
        ]

        if not filtrovano.empty:
            st.success("Ano, HW je podporován pro výrobce a model.")

            for _, radek in filtrovano.iterrows():
                st.write("---")
                if 'Model_+' in df.columns and pd.notna(radek.get('Model_+')):
                    st.write(f"** ** {radek['Model_+']}")
                if 'Rok' in df.columns and pd.notna(radek.get('Rok')):
                    st.write(f"**Rok:** {radek['Rok']}")
                if 'CMD' in df.columns and pd.notna(radek.get('CMD')):
                    st.write(f"**CMD příkaz:** {radek['CMD']}")
                if 'NKP' in df.columns and pd.notna(radek.get('NKP')):
                    st.write(f"**NKP příkaz:** {radek['NKP']}")
                if 'Zapojeni' in df.columns and pd.notna(radek.get('Zapojeni')):
                    st.write(f"**Zapojení:** {radek['Zapojeni']}")
                if 'Tachometr' in df.columns and pd.notna(radek.get('Tachometr')):
                    st.write(f"**Tachometr:** {radek['Tachometr']}")
                if 'Nadrz litry' in df.columns and pd.notna(radek.get('Nadrz litry')):
                    st.write(f"**Nádrž litry:** {radek['Nadrz litry']}")
                if 'Nadrz %' in df.columns and pd.notna(radek.get('Nadrz %')):
                    st.write(f"**Nádrž %:** {radek['Nadrz %']}")
        else:
            st.error("Ne, zadaná kombinace HW, výrobce a modelu nebyla nalezena.")
    else:
        st.warning("Vyplň prosím všechny vstupy.")
