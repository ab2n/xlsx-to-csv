import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Convertisseur XLSX → CSV")

st.title("Convertisseur XLSX vers CSV")

uploaded_file = st.file_uploader(
    "Déposez votre fichier Excel (.xlsx)",
    type=["xlsx"]
)

if uploaded_file is not None:
    try:
        # Lire les feuilles disponibles
        xls = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Choisissez la feuille :", xls.sheet_names)

        # Lire la feuille sélectionnée
        df = pd.read_excel(xls, sheet_name=sheet_name)

        st.success("Fichier chargé avec succès ✅")
        st.dataframe(df)

        # Choix du séparateur
        separator = st.selectbox(
            "Choisissez le séparateur CSV :",
            options=[",", ";", "\t"],
            format_func=lambda x: {
                ",": "Virgule (,)",
                ";": "Point-virgule (;)",
                "\t": "Tabulation (\\t)"
            }[x]
        )

        # Conversion en CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, sep=separator)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="📥 Télécharger le fichier CSV",
            data=csv_data,
            file_name="conversion.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Erreur lors du traitement : {e}")
