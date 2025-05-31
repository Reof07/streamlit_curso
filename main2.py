# Importamos librerías necesarias
import streamlit as st  # Streamlit para crear la interfaz web
from dotenv import load_dotenv  # Para cargar las variables de entorno
from langchain_cohere import ChatCohere  # Nuestro modelo de chat usando Cohere
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage  # Tipos de mensajes que maneja LangChain

# Cargamos las variables de entorno (.env), como claves API
load_dotenv()

# Inicializamos el modelo de lenguaje que vamos a usar
model = ChatCohere()

# Configuramos el título que aparecerá en nuestra app de Streamlit
st.title("🧠 Mi Chat con LangChain + Streamlit")

# Definimos un mensaje inicial del sistema para dar contexto al asistente
initial_message = SystemMessage(
    content="""
        You are a specialized assistant named LangChain Assistant . Your sole purpose is to answer user questions related exclusively to the LangChain framework .

        Only respond to questions directly about the LangChain framework .
        If the question is unrelated to LangChain, politely respond:
        "This question is outside the scope of the LangChain framework. Please ask something related to LangChain."
        If you do not know the answer to a LangChain-related question, say:
        "I don't know."
        Do not provide any additional information beyond what is explicitly asked.
        Do not engage in discussions or answer questions about other topics, frameworks, or tools.

        """)

# Usamos session_state para mantener la conversación entre interacciones
if "messages" not in st.session_state:
    st.session_state.messages = [initial_message]  # Si no hay historial, lo inicializamos con el mensaje de sistema

# Función auxiliar para convertir los tipos de mensajes en roles de Streamlit
def get_role(message):
    if isinstance(message, HumanMessage):
        return "user"  # El usuario es quien envía preguntas
    elif isinstance(message, AIMessage):
        return "assistant"  # El asistente es quien responde
    elif isinstance(message, SystemMessage):
        return "system"  # Mensajes internos del sistema (normalmente ocultos)
    else:
        return "user"  # Por defecto, lo tratamos como usuario

# Recorremos el historial de mensajes para mostrarlos en pantalla
for msg in st.session_state.messages:
    role = get_role(msg)  # Obtenemos el rol del mensaje
    if role != "system":  # Si es un mensaje de sistema, podemos decidir no mostrarlo
        with st.chat_message(role):  # Creamos un bloque de chat según el rol (user o assistant)
            st.markdown(msg.content)  # Mostramos el contenido del mensaje

# Creamos el input de texto donde el usuario escribe su pregunta
if prompt := st.chat_input("¿Qué quieres saber?"):
    # Cuando el usuario envía algo, lo convertimos en un objeto HumanMessage
    user_message = HumanMessage(content=prompt)
    st.session_state.messages.append(user_message)  # Lo agregamos al historial

    # Mostramos inmediatamente el mensaje del usuario en pantalla
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generamos la respuesta del asistente
    with st.chat_message("assistant"):
        # Usamos el modelo para responder basándonos en el último input
        #response = model.invoke(prompt)
        response = model.invoke(st.session_state.messages)
        assistant_message = AIMessage(content=response.content)  # Guardamos la respuesta como un AIMessage
        st.markdown(assistant_message.content)  # Mostramos la respuesta en pantalla

    # Añadimos la respuesta del asistente al historial para futuras referencias
    st.session_state.messages.append(assistant_message)
