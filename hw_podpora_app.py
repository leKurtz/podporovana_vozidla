import pandas as pd
import streamlit as st

# Název souboru s tabulkou (musí být ve stejné složce jako tento skript)
CSV_FILE = "podporovana_vozidla.csv"

# Načtení CSV (zkusí UTF-8, pokud selže použije CP1250)
try:
    df = pd.read_csv(CSV_FILE, sep=';', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(CSV_FILE, sep=';', encoding='cp1250')

st.title("Kontrola podporovaných vozidel dle typu HW")

# Formulář pro zadání vstupů
with st.form("hledani_form"):
    hw = st.radio("Vyber typ HW:", ["820", "FMX150", "FMX003"])
    vyrobce = st.text_input("Zadej výrobce vozidla").strip()
    model = st.text_input("Zadej model vozidla").strip()
    submitted = st.form_submit_button("Hledat")

if submitted:
    if hw and vyrobce and model:
        filtrovano = df[
            (df['HW'].astype(str).str.strip().str.lower() == hw.lower()) &
            (df['Vyrobce'].astype(str).str.strip().str.lower().str.contains(vyrobce.lower(), na=False)) &
            (df['Model'].astype(str).str.strip().str.lower().str.contains(model.lower(), na=False))
        ]

        if not filtrovano.empty:
            st.success("Ano, HW je podporován pro výrobce a model.")

            for _, radek in filtrovano.iterrows():
                st.write("---")
                if 'Model' in df.columns and pd.notna(radek.get('Model')):
                    st.write(f"**Model:** {radek['Model']}")
                if 'Rok_od' in df.columns and 'Rok_do' in df.columns:
                    if pd.notna(radek.get('Rok_od')) or pd.notna(radek.get('Rok_do')):
                        st.write(f"**Rok:** {radek.get('Rok_od', '')} - {radek.get('Rok_do', '')}")
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
                if 'Spotreba' in df.columns and pd.notna(radek.get('Spotreba')):
                    st.write(f"**Spotřeba:** {radek['Spotreba']}")
        else:
            st.error("Ne, zadaná kombinace HW, výrobce a modelu nebyla nalezena.")
    else:
        st.warning("Vyplň prosím všechny vstupy.")
