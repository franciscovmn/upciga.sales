import streamlit as st

def app():
    # usando "from streamlit_navigation_bar import st_navbar" no menu_principal.py em combinacao com o st.sidebar, o streamlit buga: desaparece o 'X' (close da sidebar) ... por isso passei a colocar o sidebar_state en session_state
    if 'sidebar_state' not in st.session_state:
        st.session_state.sidebar_state = 'expanded'

    st.set_page_config(page_title="UpCiga BI", layout='wide', initial_sidebar_state=st.session_state.sidebar_state, page_icon="📈")
    # st.title("UpCiga BI")

    st.markdown("<style>.stDeployButton {visibility: hidden;}#MainMenu {visibility: hidden;}</style>", unsafe_allow_html=True)

    # # se ativar qualquer das configuracoes seguintes, a navbar deforma:
    # st.markdown("<style>.stDeployButton {visibility: hidden;}</style>", unsafe_allow_html=True)
    # st.markdown("<style>#MainMenu {visibility: hidden;}</style>", unsafe_allow_html=True)
    # st.markdown("<style>#MainMenu {visibility: hidden;}header {visibility: hidden;}</style>", unsafe_allow_html=True)

    # df_totais_empresa, df_data_hora_ultima_atualizacao, clientes, setores, segmentos, vendedores, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf = None, None, None, None, None, None, None, None, None, None, None, None
    
    # Check session state for login status
    if "grupo" not in st.session_state or st.session_state.grupo is None:
        if "a" in st.query_params:
            st.session_state.grupo = 'admin'
            st.session_state.usuario = st.query_params["a"]
            st.rerun()
        elif "s" in st.query_params:
            st.session_state.grupo = 'super-admin'
            st.session_state.usuario = st.query_params["s"]
            st.rerun()
        elif "v" in st.query_params:
            st.session_state.grupo = 'vendedor'
            st.session_state.usuario = st.query_params["v"]
            st.rerun()
        else:
            import login
            login.app()
    else:
        import menu_principal
        menu_principal.app()




# import streamlit as st
# from streamlit import session_state as ss
# if 'sidebar_state' not in ss:
#     ss.sidebar_state = 'collapsed'
# st.set_page_config(initial_sidebar_state=ss.sidebar_state)
# def change():
#     ss.sidebar_state = (
#         "collapsed" if ss.sidebar_state == "expanded" else "expanded"
#     )
# st.sidebar.button('Click to toggle sidebar state', on_click=change)

# if "grupo" not in st.session_state or st.session_state.grupo is None:
#     # Initialize st.session_state.grupo 
#     # st.write(st.query_params)
#     if "a" in st.query_params:
#         st.session_state.grupo = 'admin'
#         st.session_state.usuario = st.query_params["a"]
#     elif "s" in st.query_params:
#         st.session_state.grupo = 'super-admin'
#         st.session_state.usuario = st.query_params["s"]
#     elif "v" in st.query_params:
#         st.session_state.grupo = 'vendedor'
#         st.session_state.usuario = st.query_params["v"]
#     else:
#         # st.session_state.grupo = 'admin'
#         # st.session_state.usuario = 'admin'
#         # st.session_state.grupo = None
#         # st.session_state.usuario = None
#         st.switch_page("login.py")
#         """Programmatically switch the current page in a multipage app.

#         When ``st.switch_page`` is called, the current page execution stops and
#         the specified page runs as if the user clicked on it in the sidebar
#         navigation. The specified page must be recognized by Streamlit's multipage
#         architecture (your main Python file or a Python file in a ``pages/``
#         folder). Arbitrary Python scripts cannot be passed to ``st.switch_page``.

#         Parameters
#         ----------
#         page: str
#             The file path (relative to the main script) of the page to switch to.

#         Example
#         -------
#         Consider the following example given this file structure:

#         >>> your-repository/
#         >>> ├── pages/
#         >>> │   ├── page_1.py
#         >>> │   └── page_2.py
#         >>> └── your_app.py

#         >>> import streamlit as st
#         >>>
#         >>> if st.button("Home"):
#         >>>     st.switch_page("your_app.py")
#         >>> if st.button("Page 1"):
#         >>>     st.switch_page("pages/page_1.py")
#         >>> if st.button("Page 2"):
#         >>>     st.switch_page("pages/page_2.py")

#         .. output ::
#             https://doc-switch-page.streamlit.app/
#             height: 350px

#         """

# # Retrieve the grupo from Session State to initialize the widget
# st.session_state._grupo = st.session_state.grupo

# def set_grupo():
#     # Callback function to save the grupo selection to Session State
#     st.session_state.grupo = st.session_state._grupo

# # Selectbox to choose grupo
# st.selectbox("Select your grupo:",[None, "vendedor", "admin", "super-admin"],
#     key="_grupo",on_change=set_grupo,)

# https://your_app.streamlit.app/?first_key=1&second_key=two&third_key=true
# st.query_params: {"first_key" : "1","second_key" : "two","third_key" : "true"}

# # You can read query params using key notation
# if st.query_params["first_key"] == "1":
#     do_something()

# # ...or using attribute notation
# if st.query_params.second_key == "two":
#     do_something_else()

# # And you can change a param by just writing to it 
# st.query_params.first_key = 2  # This gets converted to str automatically

# st.session_state.grupo = "admin"

# print(json_retorno[0]['titulo'])

# self.mydb = Connection()
# user = self.mydb.register(self.username, self.email, self.password)
# if user:
#     st.success("Registration Successful")
# else:
#     st.error("Registration Failed")
# st.session_state.grupo = 'admin'
# st.session_state.usuario = username.strip()
# st.write('chamou api st.session_state.usuario= '+st.session_state.usuario)


# if not st.sidebar.checkbox(“Live Data”, True):
#     st.sidebar.markdown(“Choose the data file csv”)
#     folder_path = path_script = os.path.abspath(os.getcwd())
#     filenames = os.listdir(folder_path )
#     selected_filename = st.selectbox(‘Select a file’, filenames)
#     DATA_URL=os.path.join(folder_path + ‘\’ + selected_filename)

#     st.write('You selected `%s`' % DATA_URL)
# else:
#     list_of_files = glob.glob(’*.csv’)
#     #print(list_of_files)
#     LASTEST_FILE = max(list_of_files, key=os.path.getctime)
#     #print(latest_file)
#     path_script = os.path.abspath(os.getcwd())
#     DATA_URL = path_script + ‘\’+ LASTEST_FILE

# def load_data():
#     update_timestamp = time.ctime(os.path.getmtime(DATA_URL))
#     st.write(update_timestamp)
#     return cached_data_load(update_timestamp)

# @st.cache(ttl=60)
#     def cached_data_load(timestamp):
#     data = pd.read_csv(DATA_URL)
#     return data

# data = load_data()

# How to Hide Streamlit Branding
# To hide the Streamlit branding, you can use custom CSS within your Streamlit app. Here are a few methods:

# To hide the footer that says “Hosted with Streamlit,” you can use the following CSS:
# hide_footer_style = """
# .reportview-container .main footer {visibility: hidden;}
# """
# st.markdown(hide_footer_style, unsafe_allow_html=True)

# To remove the hamburger menu, you can use:
# hide_menu_style = """
# #MainMenu {visibility: hidden;}
# """
# st.markdown(hide_menu_style, unsafe_allow_html=True)

# To hide the footer completely, you can use:
# hide_footer_style = """
# .reportview-container .main footer {visibility: hidden;}
# """
# st.markdown(hide_footer_style, unsafe_allow_html=True)

# To hide the stDecoration, you can use:  #stDecoration {display:none;}

# RUN sed -i 's/Streamlit<\/title>/&lt;title&gt;Your App Title&lt;\/title&gt;/g' /usr/local/lib/python3.10/site-packages/streamlit/static/index.html

# import subprocess
#     import sys
#     import streamlit as st

#     from activity_check import high_count
#     act_lev = ""

#     def start_capture():
#         subprocess.run([f"{sys.executable}", "activity_check.py"])

#     if st.button("Start Capturing"):
#         st.write(start_capture())

#     st.write(high_count)