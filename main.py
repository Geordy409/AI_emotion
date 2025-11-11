import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Chatbot DSM-5",
    page_icon="🧠",
    layout="wide"
)

# Initialiser l'historique de conversation dans session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "processing" not in st.session_state:
    st.session_state.processing = False 

# Titre
st.title("💬 Chatbot Psychiatrique DSM-5")
st.markdown("---")

# Sidebar pour les paramètres
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Récupérer la clé API
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        st.error("⚠️ Clé API OpenAI non configurée")
        openai_key = st.text_input(
            "Entrez votre clé API OpenAI:",
            type="password",
            help="Obtenez une clé sur https://platform.openai.com/api-keys"
        )
    else:
        st.success("✅ Clé API configurée")
        # Afficher les premiers caractères pour debug
        st.caption(f"Clé: {openai_key[:10]}...")
    
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
        ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
        help="gpt-4o-mini est recommandé (rapide et économique)"
    )
    
    st.markdown("---")
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer l'historique", use_container_width=True):
        st.session_state.messages = []
        st.session_state.processing = False
        st.rerun()
    
    # Compteur de messages
    st.info(f"📊 Messages: {len(st.session_state.messages)}")
    
    # Debug info
    if st.session_state.processing:
        st.warning("⏳ En cours de traitement...")
    
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
        # Afficher l'historique des messages
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🧠"):
                    st.markdown(message["content"])
        
        # Zone de saisie du message - TOUJOURS affichée
        prompt = st.chat_input(
            "💬 Posez votre question sur le DSM-5...",
            disabled=st.session_state.processing
        )
        
        # Traiter le message utilisateur
        if prompt and not st.session_state.processing:
            st.session_state.processing = True
            
            # Ajouter le message de l'utilisateur
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Afficher le message de l'utilisateur immédiatement
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            # Préparer les messages pour l'IA
            messages_for_ai = [
                ("system", """Tu es un expert en psychiatrie spécialisé dans le DSM-5 (Manuel diagnostique et statistique des troubles mentaux, 5e édition). 

Tes missions:
- Répondre avec précision selon les critères diagnostiques du DSM-5
- Être pédagogique et structuré dans tes explications
- Utiliser des exemples concrets quand c'est approprié
- Toujours rappeler que tu fournis des informations éducatives, pas de diagnostic

Réponds de manière conversationnelle et professionnelle.""")
            ]
            
            # Ajouter l'historique complet
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    messages_for_ai.append(("human", msg["content"]))
                else:
                    messages_for_ai.append(("ai", msg["content"]))
            
            # Générer la réponse
            with st.chat_message("assistant", avatar="🧠"):
                message_placeholder = st.empty()
                
                try:
                    # Initialiser le modèle
                    chat_model = ChatOpenAI(
                        model=model,
                        temperature=temperature,
                        api_key=openai_key,
                        streaming=False
                    )
                    
                    # Créer la chaîne
                    prompt_template = ChatPromptTemplate.from_messages(messages_for_ai)
                    chain = prompt_template | chat_model
                    
                    # Message de chargement
                    message_placeholder.markdown("🔍 _Réflexion en cours..._")
                    
                    # Invoquer le modèle
                    response = chain.invoke({})
                    assistant_response = response.content
                    
                    # Afficher la réponse
                    message_placeholder.markdown(assistant_response)
                    
                    # Sauvegarder dans l'historique
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
                    
                    st.session_state.processing = False
                    
                except Exception as e:
                    error_msg = f"❌ **Erreur:** {str(e)}"
                    message_placeholder.markdown(error_msg)
                    st.error(f"Détails de l'erreur: {type(e).__name__}")
                    
                    # Sauvegarder l'erreur dans l'historique
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
                    
                    st.session_state.processing = False
    
    except Exception as e:
        st.error(f"❌ Erreur d'initialisation: {str(e)}")
        st.error(f"Type d'erreur: {type(e).__name__}")
        st.info("💡 Vérifiez votre clé API et votre connexion internet")

else:
    # Message si pas de clé API
    st.warning("⚠️ Configurez votre clé API OpenAI dans la sidebar")
    
    st.markdown("### 🚀 Pour commencer:")
    st.markdown("""
    1. **Option 1 - Fichier .env (recommandé)**
       - Créez un fichier `.env` à la racine du projet
       - Ajoutez: `OPENAI_API_KEY=sk-votre-clé-ici`
       - Relancez: `streamlit run app.py`
    
    2. **Option 2 - Saisie manuelle**
       - Entrez votre clé dans la sidebar →
       - Commencez à discuter !
    """)
    
    st.info("🔑 Obtenez une clé API sur: https://platform.openai.com/api-keys")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    🧠 Chatbot DSM-5 | Développé avec LangChain & Streamlit | 
    Données basées sur le DSM-5 (2013)
</div>
""", unsafe_allow_html=True)