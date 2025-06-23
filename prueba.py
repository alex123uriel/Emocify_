import streamlit as st
import tweepy
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import nltk
import re
import qrcode
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta
import time
import random
import pyttsx3
import base64
import speech_recognition as sr
import threading
from emciones import detectar_emocion

nltk.download('punkt')

# --- CREDENCIALES ---
SPOTIFY_CLIENT_ID = 'a64730f41d9a4b97851f683ed0a6209b'
SPOTIFY_CLIENT_SECRET = 'bfacefaaefa14cdab8f86dc8a37ac69c'
TWITTER_BEARER_TOKEN = [
    "AAAAAAAAAAAAAAAAAAAAAI8l0gEAAAAAhDU8NLwbQ0BbxE8aPNLBv2GQTrY%3Dw5GtzwfYwGBIA01ABfZK6aesqUXtouDtwiDz4IPiK6y52L8m2B",
    "AAAAAAAAAAAAAAAAAAAAAMXI2gEAAAAAQ7YFcY27thZbmxzB3IJqxuch2Po%3DiNZuKn094gpFASHAX42hCOOLMZgbdIzuNERu0eVk8ekCDCKojh",
    "AAAAAAAAAAAAAAAAAAAAAM0v0gEAAAAAno%2FatFXd9ze2bELvHGDy0R0LAYA%3Dy14atlHub78cbGz6Bhx7cK6qMVE82PNUBcIdZO9CIF92aGok9k",
    "AAAAAAAAAAAAAAAAAAAAAEdv0QEAAAAA%2BoxEbgLwfzrneu9E54KbH12qp5M%3Dob5CKvptYRJQh6fRPScDgfVgafwBNDja9hcX1BLetEja9Mja0S",
    "AAAAAAAAAAAAAAAAAAAAAAN72AEAAAAA0OBe%2FC4tgCJ0B8OiAK5hvdF%2FJEg%3DpSrqzEKO4yIbGiD2Z1sopE4w9IdA7pfusNiDJ6ODgjmqBVdD7l",
    "AAAAAAAAAAAAAAAAAAAAANbI2gEAAAAA%2FPLwyvodUcc%2BcjpQnICWi%2F2kkGo%3DtyFBqzg1YT1uF3LNuiU24cTtns9sV9dx3xchaE4trrl6PzloOe"
]

# --- AUTENTICACIÓN ---
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))
# --- FUNCIÓN PARA ROTAR CLIENTE TWITTER ---
def get_twitter_client():
    for token in TWITTER_BEARER_TOKEN:
        try:
            client = tweepy.Client(bearer_token=token)
            client.get_user(username="Twitter")  # Test silencioso
            return client
        except tweepy.TooManyRequests:
            continue
        except Exception:
            continue
    return None

# --- CLIENTE DE TWITTER FUNCIONAL ---
twitter_client = get_twitter_client()

# --- FUNCIONES ---
def decir(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Velocidad de habla
    engine.setProperty('volume', 1.0)  # Volumen (0.0 a 1.0)
    engine.say(texto)
    engine.runAndWait()

def limpiar_texto(texto):
    texto = re.sub(r"http\S+", "", texto)          # quitar URLs
    texto = re.sub(r"@\w+", "", texto)             # quitar menciones
    texto = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]", "", texto)  # quitar emojis y símbolos
    return texto.lower().strip()


def emocion_a_genero(emocion):
    return {
        'euforia': 'electronic',
        'entusiasmo': 'dance',
        'alegría': 'pop',
        'serenidad': 'classical',
        'neutral': 'chill',
        'melancolía': 'jazz',
        'tristeza': 'acoustic',
        'enojo': 'metal',
        'frustración': 'grunge',
        'amor': 'romantic',
        'celos': 'blues',
        'envidia': 'hip-hop',
        'indefinida': 'world'
    }.get(emocion, 'pop')


def buscar_artista(texto):
    palabras = texto.split()
    posibles_nombres = [p for p in palabras if p.istitle()]
    if not posibles_nombres:
        return None
    artista = posibles_nombres[0]
    try:
        time.sleep(1)
        resultados = sp.search(q=artista, type='artist', limit=1)
        if resultados and resultados.get('artists') and resultados['artists']['items']:
            return resultados['artists']['items'][0]['name']
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 429:
            st.error("Spotify está rechazando demasiadas solicitudes. Intenta más tarde.")
            return None
    return None

def recomendar_playlist_personalizada(emocion, texto):
    artista = buscar_artista(texto)
    
    if emocion == "amor" and artista:
        q = f"{artista} amor"
    else:
        genero = emocion_a_genero(emocion)
        q = f"{genero} mood"

    try:
        time.sleep(1)
        resultados = sp.search(q=q, type='playlist', limit=10)
        playlists = resultados.get('playlists', {}).get('items', [])
        urls = [
            p.get('external_urls', {}).get('spotify')
            for p in playlists if p and 'spotify' in p.get('external_urls', {})
        ]
        return random.choice(urls) if urls else None
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 429:
            st.error("⚠️ Límite de solicitudes alcanzado en Spotify. Intenta de nuevo en unos segundos.")
        else:
            st.error(f"Error con Spotify: {str(e)}")
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
    return None


def obtener_tweet(usuario):
    try:
        user = twitter_client.get_user(username=usuario)
        tweets = twitter_client.get_users_tweets(id=user.data.id, max_results=5, exclude=['retweets', 'replies'])
        return tweets.data[0].text if tweets.data else "No se encontró ningún tweet reciente."
    except tweepy.TooManyRequests:
        hora_reintento = datetime.now() + timedelta(minutes=15)
        return f"⚠️ Has hecho muchas solicitudes. Intenta de nuevo a las {hora_reintento.strftime('%H:%M:%S')}"
    except Exception as e:
        return f"Error: {str(e)}"


def generar_qr_url(url):
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return Image.open(buf)

def escuchar_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        decir("Estoy escuchando. Dime cómo te sientes.")
        st.info("🎙️ Esperando tu voz... habla ahora.")
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        st.success(f"🔊 Has dicho: {texto}")
        return texto
    except sr.UnknownValueError:
        st.warning("No entendí lo que dijiste.")
        decir("Lo siento, no entendí lo que dijiste.")
    except sr.RequestError:
        st.error("No se pudo conectar al servicio de reconocimiento de voz.")
        decir("No se pudo conectar al servicio de reconocimiento de voz.")
    
    return ""


# --- INTERFAZ STREAMLIT ---
st.title("🎧 Emocify")

# Fondo con imagen
def set_background_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background_image("C:/Users/alexc/Downloads/Necesitas ayuda Habla con Urissa, nuestra aitente virtual! 1.png") # Asegúrate que exista esta imagen

# Estilo para widgets
st.markdown(
    """
    <style>
    .stTextInput, .stTextArea, .stSelectbox, .stButton {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 10px;
        padding: 0.5em;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Botón para activar el asistente de voz Urissa
if st.button("Activar Asistente Urissa"):
    intro = (
        "¡Hola! Soy Urissa, tu asistente de emociones y música. "
        "Esta aplicación te ayuda a detectar emociones en textos de Twitter o que tú escribas, "
        "y te recomienda playlists en Spotify para mejorar tu estado de ánimo. "
        "Puedes ingresar un usuario de Twitter para analizar su último tweet, o escribir un texto manualmente. "
        "Luego te diré cuál es la emoción detectada y te daré una playlist para que la escuches. "
        "¡Vamos a empezar!"
    )
    decir(intro)
    st.info("Urissa ha comenzado a guiarte por la app con voz.")

# Selección de fuente del texto
opcion = st.radio("¿Desde dónde quieres analizar el texto?", ("Twitter", "Facebook (manual)"))

# Botón para pedir ayuda a Urissa según la opción elegida
if st.button("Pedir ayuda a Urissa"):
    if opcion == "Twitter":
        ayuda_twitter = (
            "Has elegido analizar un tweet de Twitter. "
            "Por favor, ingresa el nombre del usuario sin la arroba y luego presiona 'Analizar y recomendar'."
        )
        decir(ayuda_twitter)
        st.info(ayuda_twitter)
    else:
        ayuda_manual = (
            "Has elegido analizar un texto manualmente. "
            "Pega o escribe el texto en el área que aparece y luego presiona 'Analizar manual'."
        )
        decir(ayuda_manual)
        st.info(ayuda_manual)

# Flujo para opción Twitter
if opcion == "Twitter":
    usuario = st.text_input("Ingresa el nombre de usuario de Twitter (sin @):")
    
    if st.button("Analizar y recomendar"):
        st.info("Obteniendo tweet...")
        decir("Obteniendo tweet del usuario.")
        tweet = obtener_tweet(usuario)

        if tweet.startswith("Error") or tweet.startswith("⚠️"):
            st.error(tweet)
            decir("Hubo un problema al obtener el tweet. Por favor intenta más tarde o revisa el usuario.")
        else:
            st.success("Tweet obtenido correctamente.")
            texto = limpiar_texto(tweet)
            emocion = detectar_emocion(texto)
            url = recomendar_playlist_personalizada(emocion, texto)

            st.markdown(f"**Texto original:** {tweet}")
            st.markdown(f"**Emoción detectada:** {emocion}")
            decir(f"Detectamos la emoción {emocion}. Aquí tienes una playlist recomendada.")

            if url:
                st.markdown(f"[🎧 Escuchar playlist recomendada]({url})")
                st.image(generar_qr_url(url), caption="Escanea el QR para abrir la playlist")
            else:
                st.warning("No se pudo generar la playlist para este texto.")
                decir("Lo siento, no pude generar una playlist para este texto.")

# Flujo para texto manual
else:
    texto_manual = st.text_area("Pega aquí tu texto:")
    if st.button("Analizar manual"):
        if not texto_manual.strip():
            st.warning("Por favor, ingresa algún texto para analizar.")
            decir("Por favor, ingresa algún texto para analizar.")
        else:
            st.info("Analizando texto...")
            decir("Analizando el texto que ingresaste.")
            texto = limpiar_texto(texto_manual)
            emocion = detectar_emocion(texto)
            url = recomendar_playlist_personalizada(emocion, texto)

            st.markdown(f"**Emoción detectada:** {emocion}")
            decir(f"Detectamos la emoción {emocion}. Aquí tienes una playlist recomendada.")

            if url:
                st.markdown(f"[🎧 Escuchar playlist recomendada]({url})")
                st.image(generar_qr_url(url), caption="Escanea el QR para abrir la playlist")
            else:
                st.warning("No se pudo generar la playlist para este texto.")
                decir("No pude generar una playlist para este texto.")

# --- FLUJO POR VOZ ---
st.markdown("---")
st.header("🗣️ Dime cómo te sientes")

# Función para escuchar por micrófono
def escuchar_voz():
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        decir("Estoy escuchando. Dime cómo te sientes.")
        st.info("🎙️ Esperando tu voz... habla ahora.")
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        st.success(f"🔊 Has dicho: {texto}")
        return texto
    except sr.UnknownValueError:
        st.warning("No entendí lo que dijiste.")
        decir("Lo siento, no entendí lo que dijiste.")
    except sr.RequestError:
        st.error("No se pudo conectar al servicio de reconocimiento de voz.")
        decir("No se pudo conectar al servicio de reconocimiento de voz.")
    return ""

# Botón para activar micrófono
if st.button("🎙️ Hablar ahora"):
    texto_voz = escuchar_voz()
    if texto_voz:
        texto = limpiar_texto(texto_voz)
        emocion = detectar_emocion(texto)
        url = recomendar_playlist_personalizada(emocion, texto)

        # Mensaje empático según emoción
        respuestas = {
            'alegría': "¡Qué gusto saber que estás feliz!",
            'tristeza': "Lo siento mucho. Aquí hay música que podría ayudarte.",
            'amor': "¡El amor es hermoso!",
            'enojo': "Respira profundo, la música puede ayudarte a calmarte.",
            'frustración': "Sé que es difícil. Escucha esto, puede levantar tu ánimo.",
            'euforia': "¡Wow, qué emoción! Celebra con esta música.",
            'melancolía': "Los recuerdos a veces duelen. Esta música puede acompañarte.",
            'serenidad': "Qué bonito sentirse en paz. Aquí tienes algo tranquilo.",
            'sorpresa': "¡Qué inesperado! Acompáñalo con buena música.",
            'gratitud': "La gratitud es poderosa. Te dejo algo especial.",
            'esperanza': "Nunca pierdas la fe. Esta playlist es para ti.",
            'miedo': "No estás solo. Esta música puede reconfortarte.",
            'celos': "Es normal sentir eso a veces. Aquí tienes música para despejarte.",
            'envidia': "Recuerda que cada uno tiene su momento. Escucha esto.",
            'orgullo': "¡Felicidades por tu logro!",
            'vergüenza': "Todos cometemos errores. Esta música puede ayudarte.",
            'neutral': "Aquí tienes algo relajado para acompañarte.",
        }

        mensaje = respuestas.get(emocion, "Aquí tienes algo para acompañar tu estado de ánimo.")
        st.markdown(f"**Emoción detectada:** {emocion}")
        decir(f"{mensaje} Te recomiendo esta playlist.")

        if url:
            st.markdown(f"[🎧 Escuchar playlist recomendada]({url})")
            st.image(generar_qr_url(url), caption="Escanea el QR para abrir la playlist")
        else:
            st.warning("No se pudo generar la playlist para este texto.")
            decir("No pude generar una playlist para este texto.")
