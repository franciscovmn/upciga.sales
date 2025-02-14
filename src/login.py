import streamlit as st
import requests
import json
import time
import os

class LoginClass:
    def __init__(self):
        self.apps = []

    # def get_button_style(self):
    #     return """
    #     <style>
    #         .stButton > button {
    #             color: #FFFFFF; 
    #             background-color:#6A0DAD; /* Roxo */
    #             font-size: 20px;
    #             height:60px;
    #             width:100%;
    #             border: 2px solid #32CD32; /* Verde */
    #         } 
    #         .stButton > button:hover {
    #             color: #FFFFFF; 
    #             background-color:#520B8E; /* Roxo escuro */
    #             border-color:#228B22; /* Verde escuro */
    #             font-size: 20px;
    #             height:60px;
    #             width:100%
    #         }
    #     </style>
    #     """

    # def display_login_form(self):
    #     with st.form("login"):
    #         st.markdown(self.get_button_style(), unsafe_allow_html=True)
    #         # Título com a logo ao lado
    #         st.markdown(
    #             """
    #             <div style="display: flex; align-items: center;">
    #             <img src="https://utfs.io/f/28e6820b-f340-40bb-a74e-0d7a8bf54b87-1njz0s.png" width="auto" height="auto">
    #             <h2 style="margin: auto;">UpcigaSales</h2>
    #             </div>
    #             """, unsafe_allow_html=True)
    #         username = st.text_input("Usuario", placeholder="Entre seu usuario")
    #         password = st.text_input("Senha", placeholder="Digite sua senha", type="password")
    #         botaosubmit = st.form_submit_button("Login")
    #     return username, password, botaosubmit

    def authenticate_user(self, username, password):
        API_URL = os.getenv("API_URL", "http://192.168.15.195:85/api/login")
        with st.spinner("Checando usuario e senha..."):
            try:
                resposta_da_retaguarda = requests.post(API_URL, json={'user': username, 'senha': password, 'sessionid': ''})
                resposta_da_retaguarda.raise_for_status()
                return json.loads(resposta_da_retaguarda.content)
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the login service: {e}")
                return None

    def handle_login_response(self, response):
        if response['result'] == 'ok':
            st.session_state.usuario = response['usuario']
            if response['isAdmin'] and response['isComprador']:
                st.session_state.grupo = 'super-admin'
            elif response['isAdmin']:
                st.session_state.grupo = 'admin'
            else:
                st.session_state.grupo = 'vendedor'
            st.session_state.sys_usuario = response['usuario'] # dadosDoLogin.vendedor
            st.session_state.idvendedor = response['vendedor'] # dadosDoLogin.vendedor
            # time.sleep(6)
            # st.write(f"usuario: {st.session_state.sys_usuario} vendedor={st.session_state.idvendedor}  ")
            st.success("Bem-vindo, " + st.session_state.usuario)
            time.sleep(1)
            # st.balloons()
            st.rerun()
        else:
            st.error("Usuario ou senha Invalidos! Repita Login")

    def login(self):
        placeholder = st.empty()
        with placeholder.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # username, password, botaosubmit = self.display_login_form()
                with st.form("login"):
                    # st.markdown(self.get_button_style(), unsafe_allow_html=True)
                    # Título com a logo ao lado
                    st.markdown(
                        """
                        <style>
                            .stButton > button {
                                color: #FFFFFF; 
                                background-color:#6A0DAD; /* Roxo */
                                font-size: 20px;
                                height:60px;
                                width:100%;
                                border: 2px solid #32CD32; /* Verde */
                            } 
                            .stButton > button:hover {
                                color: #FFFFFF; 
                                background-color:#520B8E; /* Roxo escuro */
                                border-color:#228B22; /* Verde escuro */
                                font-size: 20px;
                                height:60px;
                                width:100%
                            }
                        </style>
                        <div style="display: flex; align-items: center;">
                        <img src="https://utfs.io/f/28e6820b-f340-40bb-a74e-0d7a8bf54b87-1njz0s.png" width="auto" height="auto">
                        <h2 style="margin: auto;">UpcigaSales</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    username = st.text_input("Usuario", placeholder="Entre seu usuario")
                    password = st.text_input("Senha", placeholder="Digite sua senha", type="password")
                    botaosubmit = st.form_submit_button("Login")

                if botaosubmit:
                    if username.strip() == "" or password.strip() == "":
                        st.error("Por favor, indique usuario e senha")
                    else:
                        resposta_de_pedido_de_login_na_retaguarda = self.authenticate_user(username, password)
                        if resposta_de_pedido_de_login_na_retaguarda:
                            self.handle_login_response(resposta_de_pedido_de_login_na_retaguarda)

def app():
    app = LoginClass()
    app.login()