# app.py
from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

app = Flask(__name__)

# Historique des messages stocké en mémoire (simple)
chat_history = []

# Route principale pour la page web
@app.route("/")
def index():
    return render_template("index.html", messages=chat_history)

# Route pour traiter les messages utilisateur
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("prompt", "")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not openai_key:
        return jsonify({"error": "Clé API OpenAI non configurée"}), 400

    # Ajouter le message utilisateur à l'historique
    chat_history.append({"role": "user", "content": user_message})

    # Préparer les messages pour l'IA
    messages_for_ai = [
        ("system", """Tu es un expert en psychiatrie spécialisé dans le DSM-5.
- Réponds avec précision selon les critères diagnostiques du DSM-5
- Sois pédagogique et structuré
- Utilise des exemples concrets
- Rappelle que ce n'est qu'à titre éducatif""")
    ]

    for msg in chat_history:
        if msg["role"] == "user":
            messages_for_ai.append(("human", msg["content"]))
        else:
            messages_for_ai.append(("ai", msg["content"]))

    try:
        # Initialiser le modèle
        chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=openai_key,
            streaming=False
        )

        # Créer la chaîne
        prompt_template = ChatPromptTemplate.from_messages(messages_for_ai)
        chain = prompt_template | chat_model

        # Générer la réponse
        response = chain.invoke({})
        assistant_response = response.content

        # Ajouter la réponse à l'historique
        chat_history.append({"role": "assistant", "content": assistant_response})

        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour effacer l'historique
@app.route("/reset", methods=["POST"])
def reset():
    chat_history.clear()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
