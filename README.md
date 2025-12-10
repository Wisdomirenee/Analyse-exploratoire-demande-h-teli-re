 Mini-Projet : Analyse exploratoire de la demande hôtelière
🎯 Objectif du projet

Ce projet a pour objectif de réaliser une analyse exploratoire de données (EDA) complète sur un jeu de données réel de réservations hôtelières couvrant la période 2015–2017, pour deux types d’établissements :

City Hotel (hôtel urbain)

Resort Hotel (hôtel de villégiature)

L’analyse vise à identifier les facteurs influençant la demande, la saisonnalité des prix (ADR) et les tendances d’annulation, afin de formuler des recommandations stratégiques en matière de Revenue Management et d’optimisation du taux d’occupation.

🧩 Données

Source : Hotel Booking Demand Dataset – Kaggle

Période : 2015 à 2017

Variables principales :

hotel → type d’hôtel

is_canceled → statut de réservation

lead_time → délai entre réservation et arrivée

adr → prix moyen journalier

arrival_date_year, arrival_date_month → période d’arrivée

customer_type → type de client

total_of_special_requests → niveau d’engagement client

⚙️ 1. Prérequis

Avant d’exécuter le projet, assurez-vous de disposer de :

Python 3.8+

pip (gestionnaire de paquets Python)

🧰 2. Installation des dépendances

Toutes les bibliothèques nécessaires sont listées dans le fichier requirements.txt
Elles incluent : pandas, numpy, matplotlib, seaborn, plotly, streamlit, kagglehub.

pip install -r requirements.txt

🚀 3. Exécution de l’application

L’application web interactive est développée avec Streamlit.

À la racine du dépôt, exécutez :

streamlit run app/app.py


Le tableau de bord s’ouvrira automatiquement dans votre navigateur à l’adresse :
👉 http://localhost:8501

🧱 Structure du projet
hotel-demand-analysis/
│
├── data/
│   └── hotel_bookings.csv             # Jeu de données Kaggle
│
├── notebooks/
│   └── hotel_analysis.ipynb           # Notebook Jupyter complet (EDA)
│
├── app/
│   └── app.py                         # Application Streamlit interactive
│
├── reports/
│   ├── rapport.pdf                    # Rapport exécutif (1–2 pages)
│   └── figures/                       # Graphiques exportés
│
├── requirements.txt                   # Librairies nécessaires
├── .gitignore                         # Fichiers exclus de Git
└── README.md                          # Présentation du projet

📊 Résultats clés

City Hotel → 66 % des réservations totales, taux d’annulation plus élevé (~45 %).

Resort Hotel → ADR moyen plus haut (~120 €), séjours plus longs (4 nuits).

Saisonnalité → forte demande entre juin et août.

Lead time long → corrélé à un risque accru d’annulation.

🧠 Recommandations stratégiques

Réduire le risque d’annulation : appliquer des dépôts non remboursables pour les réservations à long terme.

Optimiser l’ADR : politique de tarification dynamique pendant la haute saison.

Engager la clientèle : encourager les demandes spéciales pour renforcer l’intention de séjour.

🧠 Technologies utilisées
Outil / Librairie	Rôle
Python	Base du projet
Pandas / NumPy	Manipulation et nettoyage des données
Seaborn / Matplotlib / Plotly	Visualisations statistiques
Streamlit	Interface web interactive
GitHub