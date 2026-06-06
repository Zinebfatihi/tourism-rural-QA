# Framework QA Automation — Plateforme de Tourisme Rural

Framework de tests automatisés pour la plateforme de tourisme rural (frontend React + backend Spring Boot).
Construit en **Python / Selenium / Pytest** selon le patron **Page Object Model (POM)**.

> Ce dépôt contient le *squelette* du framework et une première suite de tests **smoke**.
> Les suites de régression et E2E (par rôle) sont ajoutées progressivement.

## Pile technique

- **Selenium WebDriver** — pilotage du navigateur
- **Pytest** — exécution des tests, fixtures, marqueurs
- **Page Object Model** — une classe par page, pour un code maintenable
- **pytest-html** — rapport HTML
- **python-dotenv** — configuration par variables d'environnement

## Structure du projet

```
tourisme-rural-qa/
├── pages/              # Page Objects (1 classe par page)
│   ├── base_page.py    #   actions communes (clic, saisie, attentes)
│   ├── login_page.py   #   page /login
│   └── home_page.py    #   page d'accueil
├── tests/
│   └── smoke/          # suite smoke (P0)
│       └── test_login.py
├── utilities/
│   ├── driver_factory.py   # création/config du navigateur
│   └── logger.py           # logs centralisés
├── config/
│   ├── config.py           # paramètres globaux
│   └── .env.example        # modèle de configuration
├── test_data/          # données de test (data-driven)
├── reports/            # rapports HTML générés
├── screenshots/        # captures automatiques en cas d'échec
├── logs/               # journaux d'exécution
├── conftest.py         # fixtures globales + hook captures
├── pytest.ini          # configuration Pytest
└── requirements.txt
```

## Prérequis

- Python 3.10+
- Google Chrome (ou Firefox) installé
- La plateforme lancée en local : **backend** sur `http://localhost:8080`, **frontend** sur `http://localhost:5173`

> Selenium 4 télécharge automatiquement le bon driver navigateur : aucune installation manuelle de chromedriver n'est nécessaire.

## Installation

```bash
# 1. Créer et activer un environnement virtuel
python -m venv venv
# Windows :
venv\Scripts\activate
# Linux / Mac :
source venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer le fichier de configuration local
#    (copier le modèle, puis adapter si besoin)
# Windows :
copy config\.env.example .env
# Linux / Mac :
cp config/.env.example .env
```

## Exécution

```bash
# Tous les tests
pytest

# Uniquement la suite smoke
pytest -m smoke

# En mode headless (sans fenêtre de navigateur, comme en CI)
# -> mettre HEADLESS=true dans .env, puis :
pytest -m smoke
```

Le rapport HTML est généré dans `reports/report.html`.
En cas d'échec, une capture d'écran est automatiquement enregistrée dans `screenshots/`.

## Configuration

Les paramètres se règlent dans le fichier `.env` (voir `config/.env.example`) :

| Variable        | Rôle                                   | Défaut                  |
|-----------------|----------------------------------------|-------------------------|
| `BASE_URL`      | URL du frontend                        | `http://localhost:5173` |
| `BROWSER`       | `chrome` ou `firefox`                  | `chrome`                |
| `HEADLESS`      | navigateur invisible (`true`/`false`)  | `false`                 |
| `EXPLICIT_WAIT` | délai max d'attente d'un élément (s)   | `10`                    |
| `ADMIN_EMAIL`   | identifiant de test                    | `admin@saih.com`        |
| `ADMIN_PASSWORD`| mot de passe de test                   | `Admin123!`             |

## Suites de tests

| Suite        | Marqueur       | État         |
|--------------|----------------|--------------|
| Smoke        | `-m smoke`     | ✅ en place  |
| Régression   | `-m regression`| à venir      |
| E2E          | `-m e2e`       | à venir      |

## À venir (roadmap)

- Page Objects du catalogue, des réservations et des espaces hôte/guide/admin
- Suites de régression et parcours E2E multi-rôles
- Intégration CI/CD via GitHub Actions (exécution headless sur chaque push / pull request)
