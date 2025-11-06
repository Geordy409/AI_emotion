from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Charger la clé depuis le fichier .env
load_dotenv()
openai_key = "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"


# Vérifier que la clé est bien chargée
if openai_key is None:
    raise ValueError("La clé OPENAI_API_KEY n'est pas définie. Vérifie ton .env ou passe la clé directement.")

# Initialiser le modèle ChatOpenAI
chat = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,
    api_key=openai_key
)

# Créer le prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un expert en psychiatrie qui utilise le DSM-5 pour diagnostiquer et expliquer les troubles mentaux. Base toutes tes réponses sur les critères du DSM-5."),
    ("human", "{question}")
])

# Créer la chaîne avec l'opérateur pipe (|)
chain = prompt | chat

# Exécuter la chaîne
response = chain.invoke({"question": "Quels sont les critères du trouble anxieux généralisé?"})

# Afficher la réponse
print(response.content)