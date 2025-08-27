import pandas as pd
import streamlit as st

# Název souboru s tabulkou (musí být ve stejné složce jako tento skript)
EXCEL_FILE = "podporovana_vozidla.xlsx"

# Načtení Excelu
df = pd.read_excel(EXCEL_FILE)

st.title("Kontrola podpory HW pro vozidla")

# Formulář pro zadání vstupů
with st.form("hledani_form"):
    hw = st.text_input("Zadej typ HW (818, 820, Teltonika 150)").strip()
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
                if 'Rok' in df.columns and pd.notna(radek.get('Rok')):
                    st.write(f"**Rok:** {radek['Rok']}")
                if 'CMD' in df.columns and pd.notna(radek.get('CMD')):
                    st.write(f"**CMD příkaz:** {radek['CMD']}")
                if 'NKP' in df.columns and pd.notna(radek.get('NKP')):
                    st.write(f"**NKP příkaz:** {radek['NKP']}")
                if 'Zapojeni' in df.columns and pd.notna(radek.get('Zapojeni')):
                    st.write(f"**Zapojení:** {radek['Zapojeni']}")
            print("-")
        else:
            st.error("Ne, zadaná kombinace HW, výrobce a modelu nebyla nalezena.")
    else:
        st.warning("Vyplň prosím všechny vstupy.")
