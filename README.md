# 🧠 Chatbot Psychiatrique DSM-5

Un chatbot intelligent spécialisé dans le Manuel Diagnostique et Statistique des troubles mentaux (DSM-5), développé avec Streamlit et LangChain.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![LangChain](https://img.shields.io/badge/langchain-latest-green.svg)

## 📋 Description

Ce chatbot éducatif permet d'obtenir des informations précises sur les critères diagnostiques du DSM-5. Il utilise les modèles GPT d'OpenAI via LangChain pour fournir des réponses structurées et pédagogiques.

### ⚠️ Avertissement Important

**Cet outil est à but éducatif uniquement.** Il ne remplace en aucun cas :
- Une consultation médicale
- Un diagnostic professionnel
- L'avis d'un psychiatre ou psychologue

## ✨ Fonctionnalités

- 💬 **Interface conversationnelle** intuitive
- 🔄 **Historique des conversations** persistant
- 🎛️ **Paramètres personnalisables** (modèle, température)
- 🤖 **Support de plusieurs modèles GPT** (GPT-4o, GPT-4o-mini, GPT-3.5-turbo)
- 📊 **Compteur de messages**
- 🗑️ **Effacement de l'historique**
- 🔒 **Gestion sécurisée des clés API**

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Une clé API OpenAI ([obtenir une clé](https://platform.openai.com/api-keys))

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone https://github.com/votre-username/ai_emotion.git
cd ai_emotion
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv

# Activation sur Windows
venv\Scripts\activate

# Activation sur macOS/Linux
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la clé API**

Créez un fichier `.env` à la racine du projet :
```env
OPENAI_API_KEY=sk-votre-clé-api-ici
```

## 📦 Dépendances

Créez un fichier `requirements.txt` avec le contenu suivant :

```txt
streamlit>=1.28.0
langchain>=0.1.0
langchain-openai>=0.0.2
langchain-core>=0.1.0
python-dotenv>=1.0.0
openai>=1.0.0
```

## 🎮 Utilisation

### Lancement local

```bash
streamlit run main.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Configuration

Dans la sidebar, vous pouvez :
- ✅ Vérifier le statut de votre clé API
- 🌡️ Ajuster la température (0.0 = précis, 1.0 = créatif)
- 🤖 Choisir le modèle GPT à utiliser
- 🗑️ Effacer l'historique de conversation

### Exemples de questions

```
- Quels sont les critères diagnostiques du TAG (Trouble Anxieux Généralisé) ?
- Explique-moi le trouble bipolaire de type 1
- Quelle est la différence entre anxiété et dépression ?
- Quels sont les symptômes du TDAH chez l'adulte ?
- Critères du trouble de stress post-traumatique ?
```

## 🌐 Déploiement sur Streamlit Cloud

1. **Pusher votre code sur GitHub**

2. **Créer une application sur [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Configurer les secrets**

Dans les paramètres de votre app, ajoutez :
```toml
OPENAI_API_KEY = "sk-votre-clé-api-ici"
```

4. **Déployer** : L'application sera accessible via une URL publique

## 📁 Structure du projet

```
ai_emotion/
├── main.py              # Application principale
├── requirements.txt     # Dépendances Python
├── .env                 # Variables d'environnement (à créer)
├── .gitignore          # Fichiers à ignorer
└── README.md           # Ce fichier
```

## 🔧 Configuration avancée

### Changer le modèle par défaut

Dans `main.py`, ligne 58 :
```python
model = st.selectbox(
    "🤖 Modèle",
    ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    index=0,  # Modifiez cet index
)
```

### Ajuster le prompt système

Dans `main.py`, ligne 132-142, modifiez le message système pour personnaliser le comportement du chatbot.

## 🐛 Résolution des problèmes

### Erreur : `ModuleNotFoundError: No module named 'langchain_openai'`

**Solution** :
```bash
pip install langchain-openai
```

### Erreur : `name 'ChatOpenAI' is not defined`

**Solution** : Vérifiez que l'import est présent en ligne 2 de `main.py` :
```python
from langchain_openai import ChatOpenAI
```

### Erreur : Clé API non configurée

**Solution** : 
- Créez un fichier `.env` avec votre clé API
- OU entrez la clé manuellement dans la sidebar

### L'application est lente

**Recommandations** :
- Utilisez `g
