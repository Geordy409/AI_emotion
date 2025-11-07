import streamlit as st
page_title="Chatbot DSM-5",
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# Configuration de la page
st.set_page_config(
    page_icon="🧠",
    layout="wide"
)

# Charger la clé depuis le fichier .env
load_dotenv()

openai_key ="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"

# Initialiser l'historique de conversation dans session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_model" not in st.session_state:
    st.session_state.chat_model = None

# Titre
st.title("💬 Chatbot Psychiatrique DSM-5")
st.markdown("---")

# Sidebar pour les paramètres
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Vérifier si la clé API est configurée
    if not openai_key:
        st.error("⚠️ Clé API OpenAI non configurée")
        openai_key = st.text_input(
            "Entrez votre clé API OpenAI:",
            type="password",
            help="Obtenez une clé sur https://platform.openai.com/api-keys"
        )
    else:
        st.success("✅ Clé API configurée")
    
    # Paramètres du modèle
    temperature = st.slider(
        "🌡️ Température",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Contrôle la créativité des réponses"
    )
    
    model = st.selectbox(
        "🤖 Modèle",
        ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0
    )
    
    st.markdown("---")
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer l'historique", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Compteur de messages
    st.info(f"📊 Messages: {len(st.session_state.messages)}")
    
    st.markdown("---")
    st.markdown("### 💡 Exemples")
    st.markdown("""
    - Quels sont les critères du TAG?
    - Explique-moi le trouble bipolaire
    - Différence entre anxiété et dépression?
    - Symptômes du TDAH
    """)
    
    st.markdown("---")
    st.warning("⚠️ Ceci est un outil éducatif. Ne remplace pas un diagnostic médical.")

# Zone de chat principale
if openai_key:
    try:
        # Initialiser le modèle
        if st.session_state.chat_model is None or st.session_state.get("last_model") != model:
            st.session_state.chat_model = ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=openai_key
            )
            st.session_state.last_model = model
        
        # Afficher l'historique des messages
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(message["content"])
                else:
                    with st.chat_message("assistant", avatar="🧠"):
                        st.markdown(message["content"])
        
        # Zone de saisie du message
        user_input = st.chat_input("💬 Posez votre question sur le DSM-5...")
        
        if user_input:
            # Ajouter le message de l'utilisateur à l'historique
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Afficher le message de l'utilisateur
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)
            
            # Préparer le contexte de conversation
            messages_for_ai = [
                ("system", """Tu es un expert en psychiatrie spécialisé dans le DSM-5 (Manuel diagnostique et statistique des troubles mentaux, 5e édition). 

Tes missions:
- Répondre avec précision selon les critères diagnostiques du DSM-5
- Être pédagogique et structuré dans tes explications
- Utiliser des exemples concrets quand c'est approprié
- Toujours rappeler que tu fournis des informations éducatives, pas de diagnostic

Réponds de manière conversationnelle et professionnelle.""")
            ]
            
            # Ajouter l'historique de conversation
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    messages_for_ai.append(("human", msg["content"]))
                else:
                    messages_for_ai.append(("ai", msg["content"]))
            
            # Créer le prompt et la chaîne
            prompt = ChatPromptTemplate.from_messages(messages_for_ai)
            chain = prompt | st.session_state.chat_model
            
            # Générer la réponse avec animation
            with st.chat_message("assistant", avatar="🧠"):
                with st.spinner("🔍 Analyse en cours..."):
                    try:
                        response = chain.invoke({})
                        assistant_response = response.content
                        
                        # Afficher la réponse
                        st.markdown(assistant_response)
                        
                        # Ajouter la réponse à l'historique
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": assistant_response
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
            
            # Forcer le rafraîchissement pour afficher le nouveau message
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ Erreur d'initialisation: {str(e)}")
        st.info("💡 Vérifiez votre clé API et votre connexion internet")

else:
    # Message si pas de clé API
    st.warning("⚠️ Configurez votre clé API OpenAI dans la barre latérale pour commencer")
    
    st.markdown("### 🚀 Pour commencer:")
    st.markdown("""
    1. Créez un fichier `.env` à la racine du projet
    2. Ajoutez: `OPENAI_API_KEY=votre-clé-ici`
    3. Ou entrez votre clé dans la barre latérale
    4. Relancez l'application
    """)

# Footerl
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    🧠 Chatbot DSM-5 | Développé avec LangChain & Streamlit | 
    Données basées surfV  
      r le DSM-5 (2013)
</div>
""", unsafe_allow_html=True)