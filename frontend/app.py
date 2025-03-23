import streamlit as st
import requests

# FastAPI server URL
API_URL = "http://127.0.0.1:8000"

# Streamlit App
st.set_page_config(layout="wide", page_title="FitAura Bot")

# Session State Initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # Store previous prompts and responses

# Disable fields based on login status
disable_fields = st.session_state.logged_in

def reset_fields():
    st.session_state.logged_in = False
    st.session_state.name = ""
    st.session_state.email = ""
    st.session_state.gender = "Select"
    st.session_state.age = 1
    st.session_state.chat_history = []  # Clear chat history on logout

def login_action():
    st.session_state.logged_in = True

def logout_action():
    reset_fields()

# Left Sidebar for User Input
with st.sidebar:
    st.image("utils/logo.png", use_container_width=True)  # Add your bot's logo image
    st.title("Welcome to FitAura Bot!")
    st.subheader("User Details")
    
    name = st.text_input("Name", disabled=disable_fields, key="name")
    email = st.text_input("Email", disabled=disable_fields, key="email")
    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"], disabled=disable_fields, key="gender")
    age = st.number_input("Age", min_value=1, max_value=120, step=1, disabled=disable_fields, key="age")
    
    login = st.button("Login", disabled=st.session_state.logged_in, on_click=login_action)
    logout = st.button("Logout", disabled=not st.session_state.logged_in, on_click=logout_action)
    
    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.name}!")

# Right-Hand Side Content
col1, col2, col3 = st.columns([1, 10, 2])
with col2:
    if st.session_state.logged_in:
        # Chat UI when logged in
        st.subheader(f"Hello {st.session_state.name}, Welcome to FitAura! 👋")
        st.write("Let me know how I can help you today.")

        # Keep input field at the top
        with st.container():
            user_query = st.text_area("Type your question here...", height=100)
            submit_button = st.button("Submit")

        # Chat history container (newest at the top)
        with st.container():
            for index, chat in enumerate(reversed(st.session_state.chat_history)):  # Reverse order
                with st.chat_message("user"):
                    st.write(chat["query"])
                with st.chat_message("assistant"):
                    st.write(chat["response"])

                # Show "Yes" button if an intent_response exists
                if "intent_response" in chat and chat["intent_response"]:
                    if chat["intent_response"] == "common":
                        st.write("Could you clarify? Are you asking about skincare, exercise, or nutrition?")
                        
                        col1, col2, col3 = st.columns(3)  # Create three buttons side by side
                        
                        with col1:
                            if st.button("Excerise", key=f"fitness_button_{index}"):
                                input_query = f"My question: {chat['query']}. User clarified: Fitness."
                                response = requests.post(f"{API_URL}/send_message", json={
                                    "query": input_query,
                                    "name": st.session_state.name,
                                    "email": st.session_state.email,
                                    "age": st.session_state.age,
                                    "gender": st.session_state.gender
                                })
                                bot_response = response.json()["response"]
                                st.session_state.chat_history.append({"query": "Exercise - "+chat["query"], "response": bot_response})
                                st.rerun()

                        with col2:
                            if st.button("Skincare", key=f"skincare_button_{index}"):
                                input_query = f"My question: {chat['query']}. User clarified: Skincare."
                                response = requests.post(f"{API_URL}/send_message", json={
                                    "query": input_query,
                                    "name": st.session_state.name,
                                    "email": st.session_state.email,
                                    "age": st.session_state.age,
                                    "gender": st.session_state.gender
                                })
                                bot_response = response.json()["response"]
                                st.session_state.chat_history.append({"query": "Skincare - "+chat["query"], "response": bot_response})
                                st.rerun()

                        with col3:
                            if st.button("Nutrition", key=f"nutrition_button_{index}"):
                                input_query = f"My question: {chat['query']}. User clarified: Nutrition."
                                response = requests.post(f"{API_URL}/send_message", json={
                                    "query": input_query,
                                    "name": st.session_state.name,
                                    "email": st.session_state.email,
                                    "age": st.session_state.age,
                                    "gender": st.session_state.gender
                                })
                                bot_response = response.json()["response"]
                                st.session_state.chat_history.append({"query": "Nutrition - "+chat["query"], "response": bot_response})
                                st.rerun()
                    
                    else:
                        if st.button("Yes", key=f"yes_button_{index}"):
                            input_query = f"My question: {chat['intent_response']} User responded Yes. So provide information."
                            response = requests.post(f"{API_URL}/send_message", json={
                                "query": input_query,
                                "name": st.session_state.name,
                                "email": st.session_state.email,
                                "age": st.session_state.age,
                                "gender": st.session_state.gender
                            })
                            bot_response = response.json()["response"]
                            st.session_state.chat_history.append({"query": chat["intent_response"] + " Yes!", "response": bot_response})
                            st.rerun()


        # Process user input after rendering UI
        if submit_button and user_query.strip():
            # Call FastAPI endpoint
            response = requests.post(f"{API_URL}/send_message", json={
                "query": user_query,
                "name": st.session_state.name,
                "email": st.session_state.email,
                "age": st.session_state.age,
                "gender": st.session_state.gender
            })

            # Extract response
            bot_response = response.json()["response"]
            intent_response = response.json().get("intent_response", "")

            # Store query and response in session state
            if intent_response:
                st.session_state.chat_history.append({"query": user_query, "response": intent_response, "intent_response": intent_response})

            st.session_state.chat_history.append({"query": user_query, "response": bot_response})

            # Rerun script to update UI
            st.rerun()

    else:
        # Default content when logged out
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            st.title(response.json()["message"])
            st.write(
                "### Your AI companion for a balanced lifestyle!\n"
                "**FitAura Bot** offers expert guidance in three key areas:\n"
                "- **Exercise:** Personalized workouts for your fitness goals.\n"
                "- **Skin & Hair Care:** Tips for healthy skin and hair.\n"
                "- **Nutrition:** Balanced diet recommendations tailored to your needs."
            )
            st.markdown("### Stay fit, stay glowing, stay nourished!")
        else:
            st.error("Failed to fetch data from FastAPI.")
