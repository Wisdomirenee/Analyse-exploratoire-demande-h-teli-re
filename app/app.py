# ============================================================
# 🏨 Application Streamlit : Analyse de la demande hôtelière
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np # Ajout de numpy pour le nettoyage
from pathlib import Path

# NOUVEL IMPORT
import kagglehub 
import os # Utile pour joindre les chemins

# ... (Le reste de la configuration de la page) ...

# --- Chargement du dataset (MIS À JOUR) ---

@st.cache_data
def load_data():
    DATASET_NAME = "jessemostipak/hotel-booking-demand"
    FILE_NAME = "hotel_bookings.csv"
    
    try:
        # Télécharge le dataset et retourne le chemin du répertoire local de cache
        # Exemple de chemin: C:\Users\user\.kaggle\hub\datasets\jessemostipak\hotel-booking-demand\files
        download_path = kagglehub.dataset_download(DATASET_NAME)
        
        # Construit le chemin complet vers le fichier CSV à l'intérieur du dossier téléchargé
        file_path = os.path.join(download_path, FILE_NAME)
        
        # Charge les données
        df = pd.read_csv(file_path)
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données. Assurez-vous d'être connecté à Internet et que 'kagglehub' est installé. Détail: {e}")
        st.stop()
        return pd.DataFrame() 

    # --- Nettoyage minimal (RÉPÉTER LES ÉTAPES DU NOTEBOOK) ---
    
    # 1. Suppression des doublons
    df.drop_duplicates(inplace=True)

    # 2. Gestion des valeurs manquantes essentielles (enfants)
    df['children'].fillna(0, inplace=True)
    df['children'] = df['children'].astype(int)
    
    # 3. Filtrage des ADR aberrants (pour la fiabilité du Prix Moyen)
    df = df[df['adr'] > 0]
    df = df[df['adr'] < 5000]

    # 4. Création de la variable 'total_nights'
    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_week_nights"]
    
    # 5. Remplacement des types d'hôtels pour la lisibilité
    df['hotel'] = df['hotel'].replace({
        'City Hotel': 'Hôtel de Ville',
        'Resort Hotel': 'Hôtel de Villégiature'
    })
    
    return df



df = load_data()

# --- Titre principal ---
st.title("🏨 Analyse exploratoire de la demande hôtelière")
st.markdown(
    """
    Cette mini-application permet d’explorer les données de réservations des deux hôtels :
    **City Hotel** et **Resort Hotel**.
    """
)

# --- Filtres interactifs ---
st.sidebar.header("🔎 Filtres")

hotel_type = st.sidebar.selectbox(
    "Type d'hôtel",
    df["hotel"].unique(),
    index=0
)

year = st.sidebar.multiselect(
    "Années d'arrivée",
    sorted(df["arrival_date_year"].unique()),
    default=sorted(df["arrival_date_year"].unique())
)

month = st.sidebar.multiselect(
    "Mois d'arrivée",
    sorted(df["arrival_date_month"].unique()),
    default=sorted(df["arrival_date_month"].unique())
)

# --- Filtrage du dataset ---
filtered_df = df[
    (df["hotel"] == hotel_type) &
    (df["arrival_date_year"].isin(year)) &
    (df["arrival_date_month"].isin(month))
]

st.markdown(f"### 📊 Aperçu du dataset filtré ({len(filtered_df)} réservations)")
st.dataframe(filtered_df.head())

# ============================================================
# 1️⃣ Visualisation : Réservations par mois
# ============================================================
st.subheader("📅 Nombre de réservations par mois")

reservations = (
    filtered_df.groupby("arrival_date_month")["hotel"].count().reset_index(name="count")
)
fig1 = px.bar(
    reservations,
    x="arrival_date_month",
    y="count",
    title=f"Nombre de réservations par mois — {hotel_type}",
    color_discrete_sequence=["#5DADE2"]
)
st.plotly_chart(fig1, use_container_width=True)

# ============================================================
# 2️⃣ Visualisation : Prix moyen (ADR)
# ============================================================
st.subheader("💰 Prix moyen (ADR) par mois")

adr_month = (
    filtered_df.groupby("arrival_date_month")["adr"].mean().reset_index()
)
fig2 = px.line(
    adr_month,
    x="arrival_date_month",
    y="adr",
    title=f"Évolution du prix moyen (ADR) — {hotel_type}",
    markers=True,
    color_discrete_sequence=["#E67E22"]
)
st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# 3️⃣ Visualisation : Taux d'annulation
# ============================================================
st.subheader("❌ Taux d'annulation")

cancel_rate = filtered_df["is_canceled"].mean() * 100
st.metric(label="Taux d'annulation (%)", value=f"{cancel_rate:.2f}")

cancel_by_year = (
    filtered_df.groupby("arrival_date_year")["is_canceled"].mean().reset_index()
)
fig3 = px.bar(
    cancel_by_year,
    x="arrival_date_year",
    y="is_canceled",
    title="Taux d'annulation par année",
    text_auto=".1%",
    color_discrete_sequence=["#EC7063"]
)
fig3.update_yaxes(title_text="Taux d'annulation", tickformat=".0%")
st.plotly_chart(fig3, use_container_width=True)

# ============================================================
# 4️⃣ Visualisation : Répartition des types de clients
# ============================================================
st.subheader("👨‍👩‍👧 Types de clients")

client_counts = (
    filtered_df["customer_type"].value_counts().reset_index()
)
client_counts.columns = ["Type de client", "Nombre"]
fig4 = px.pie(
    client_counts,
    values="Nombre",
    names="Type de client",
    title="Répartition des types de clients",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# 🧾 Synthèse
# ============================================================
st.markdown("---")
st.markdown("### 🧠 Synthèse rapide")
st.write(
    f"""
    - Le type d'hôtel sélectionné est **{hotel_type}**.  
    - Taux d'annulation moyen : **{cancel_rate:.2f}%**.  
    - Le prix moyen (ADR) varie selon les mois et la saisonnalité.  
    - Les types de clients les plus fréquents peuvent être observés dans le graphique ci-dessus.  
    """
)

st.success("✅ Application Streamlit exécutée avec succès !")
