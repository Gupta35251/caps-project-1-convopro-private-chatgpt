import streamlit as st

from services.chat_utilities import get_answer
from services.get_model_list import get_ollama_model_list
from services.get_title import get_chat_title
from db.conversations import (
    create_new_services,
    add_message,
    get_conversation,
    get_all_conversations
)

st.set_page_config(page_title = "ChatGPT Clone",page_icon = "💬",layout = "centered")
st.title("🤖 Local ChatGPT Clone")

# -- Models --  
if "OLLAMA_MODELS" not in st.session_state:
    st.session_state.OLLAMA_MODELS = get_ollama_model_list()

selected_model = st.selectbox("Select Model",st.session_state.OLLAMA_MODELS)

#  ---Session States --- 
st.session_state.setdefault("conversation_id",None)
# same as if conversation_id not in st.session_state:
# st.session_state.conversation_id = None
# st.session_state preser
st.session_state.setdefault("converasation_title",None)
st.session_state.setdefault("chat_history",[])
# st.session_state will preserve the previous data on every rerun

# --- Sidebar Conversations --- 
with st.sidebar:
    st.header("💬 Chat History")
    conversations = get_all_conversations()

    if st.button("➕ New Chat"):
        st.session_state.conversation_id= None
        st.session_state.converasation_title = None
        st.session_state.chat_history = []
        
    for cid,title in conversations.items():
        is_current = cid == st.session_state.conversation_id
        label = f"**{title}**" if is_current else title
        if st.button(label,key = f"conv_{cid}"):
            doc = get_conversation(cid) or {}
            st.session_state.conversation_id = cid
            st.session_state.conversation_title = doc.get("title","untitled") 
            # .get() is used to get the value of key in a dictionary
            st.session_state.chat_history = [
                {"role" : m["role"], "content" : m["content"]} for m in doc.get("messages",[])
            ]

#  --- Show chat so far ---

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#  ---Chat Input ---
user_query = st.chat_input("Ask AI ...")
if user_query:
    #1). Show + store user query in chat
    st.chat_message("user").markdown(user_query)
    st.session_state.chat_history.append({"role":"user","content":user_query})


    # 2) Persist to DB (create convo on first message, else append)
    if st.session_state.conversation_id is None:
        try:
            title = get_chat_title(selected_model,user_query) or "New Chat"
        except Exception:
            title = "New Chat"
        conv_id = create_new_services(role = "user",title = title,content = user_query)
        st.session_state.conversation_id = conv_id
        st.session_state.title = title
    else: 
        add_message(conv_id=st.session_state.conversation_id,role="user",content = user_query)


    # 3) Get assistant response (direct service)
    try:
        assistant_text = get_answer(selected_model,st.session_state.chat_history)
    except Exception as e:
        assistant_text = f"[Error getting response : {e}]"

    # 4). Show + store assistant message
    st.chat_message("assistant").markdown(assistant_text)
    st.session_state.chat_history.append({"role":"assistant","content":assistant_text})

    # 5). assistant_text
    if st.session_state.conversation_id:
        add_message(st.session_state.conversation_id,"assistant",assistant_text)



