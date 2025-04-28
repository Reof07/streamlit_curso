import streamlit as st

# Set page title
st.title('Chatbot basico con streamlit') 

side_bar_provider_list = [
    ["OpenAI", "OpenAI"],
    ["Azure", "Azure"],
    ["Cohere", "Cohere"]
]

# Set sidebar
add_selectbox = st.sidebar.selectbox(
    "Seleciona un modelo",
    side_bar_provider_list,
    format_func=lambda x: x[0],
)

api_key = st.sidebar.text_input(
        "Api key",
        type="password",
        placeholder="Inserta tu api key",
    )


history = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = history
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("¿Qué te gustaría saber?"):
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
response = f"Echo: {prompt}"
# Display assistant response in chat message container
with st.chat_message("assistant"):
    st.markdown(response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})