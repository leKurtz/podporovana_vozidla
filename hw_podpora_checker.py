import pandas as pd

# Název souboru s tabulkou (musí být ve stejné složce jako tento skript)
EXCEL_FILE = "podporovana_vozidla.xlsx"

# Načtení Excelu
df = pd.read_excel(EXCEL_FILE)

while True:
    # Zadání od uživatele
    hw = input("Zadej typ HW (např. 818, 820, Teltonika 150): ").strip()
    vyrobce = input("Zadej výrobce vozidla: ").strip()
    model = input("Zadej model vozidla: ").strip()

    # Filtrování tabulky
    filtrovano = df[
        (df['HW'].astype(str).str.strip().str.lower() == hw.lower()) &
        (df['Vyrobce'].astype(str).str.strip().str.lower() == vyrobce.lower()) &
        (df['Model'].astype(str).str.strip().str.lower() == model.lower())
    ]

    if not filtrovano.empty:
        print("Ano, HW je podporován pro uvedeného výrobce a model vozidla.")

        # Projdeme všechny nalezené řádky (např. různé roky)
        for idx, radek in filtrovano.iterrows():
            if 'Rok' in df.columns and pd.notna(radek.get('Rok')):
                print(f"Rok: {radek['Rok']}")
            if 'CMD' in df.columns and pd.notna(radek.get('CMD')):
                print(f"  CMD příkaz: {radek['CMD']}")
            if 'NKP' in df.columns and pd.notna(radek.get('NKP')):
                print(f"  NKP příkaz: {radek['NKP']}")
            if 'Zapojeni' in df.columns and pd.notna(radek.get('Zapojeni')):
                print(f"  Zapojení: {radek['Zapojeni']}")
            print("-")
    else:
        print("Ne, zadaná kombinace HW, výrobce a modelu nebyla nalezena.")

    # Dotaz, zda pokračovat
    pokracovat = input("Chceš hledat znovu? (ano/ne): ").strip().lower()
    if pokracovat != "ano":
        print("Ukončuji program.")
        break
