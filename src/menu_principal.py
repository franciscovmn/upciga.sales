import requests
import json
import streamlit as st
import os
#from streamlit_navigation_bar import st_navbar
#import pages as pg
import myfunc

# st.set_page_config(page_title="UpCiga BI", layout='wide', initial_sidebar_state="collapsed")
# from teste_popover import teste_popover

import inicio, produtos_vendidos, venda_por_cliente, venda_por_vendedor, venda_por_empresa, my_pygwalker

class MyApp:
    def __init__(self):
        # self.device_type = myfunc.get_tipo_de_dispositivo_se_mobile_ou_desktop()
        self.df_totais_empresa = myfunc.load_table('csv/totvenda_empresa.csv')
        self.df_data_hora_ultima_atualizacao = myfunc.load_table('csv/ultima_atualizacao.csv')
        
        self.produtos=self.fornecedores=None
        self.df_totais_emp_produtos=self.df_totais_emp_fornecedores=self.df_totais_emp_marcas=self.df_totais_emp_divisoes=self.df_totais_emp_gprecos=self.df_totais_emp_giro=self.df_totais_emp_gen=self.df_totais_emp_produtos_e_clientes=None
        
        self.clientes=self.setores=self.segmentos=self.vendedores=None
        self.df_totais_por_clientes=self.df_totais_por_vendedores=self.df_totais_por_setores=self.df_totais_por_cidades=self.df_totais_por_segmento=self.df_totais_por_uf=None

        self.opcoes_da_navbar = ["Home", "Periodo", "Recarregar", "Config"]
        self.styles = {
            "nav": {
                "background-color": "rgb(123, 209, 146)",
            },
            "div": {
                "max-width": "32rem",
            },
            "active": {
                "background-color": "rgba(255, 255, 255, 0.25)",
            },
            "hover": {
                "background-color": "rgba(255, 255, 255, 0.35)",
            },
        }
    
    def recarregar_dados(self):
        API_URL = os.getenv("API_URL", "http://localhost:80/api/updatebi")
        with st.spinner("Recarregando periodo atual..."):
            try:
                request = requests.get(API_URL)
                request.raise_for_status()
                response = json.loads(request.content)
                st.info(f"Dados atualizados em {response['result']}hs ... Clique Home...")
            except requests.exceptions.RequestException as e:
                st.error(f"Falha conectando retaguarda: {e}")

    # def toggle_sidebar_state(self):
    #     st.session_state.sidebar_state = "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"

    def run(self):

        # escolha_da_navbar = st_navbar(self.opcoes_da_navbar, styles=self.styles)
        # if escolha_da_navbar == 'Recarregar':
        #     self.recarregar_dados()
        #     return

        st.write(f"De {self.df_totais_empresa['DTINI'].iloc[0]} a {self.df_totais_empresa['DTFIM'].iloc[0]}... Recarga: {self.df_data_hora_ultima_atualizacao['DTHRUPDATE'].iloc[0]}")

        with st.sidebar:
            if st.session_state.grupo in ["admin", "super-admin"]:
                escolha_do_menu_principal = myfunc.exiba_menu(['Totais e Filtros Gerais', 'Totais por Produtos', 'Produtos por Vendedores', 'Produtos por Clientes', 'CONSULTAS LIVRES'])
            elif st.session_state.grupo == "vendedor":
                escolha_do_menu_principal = myfunc.exiba_menu(['Totais e Filtros Gerais', 'Totais por Produtos', 'Produtos por Vendedores', 'Produtos por Clientes', 'CONSULTAS LIVRES'])
            else:
                escolha_do_menu_principal = myfunc.exiba_menu(['Produtos por Vendedores', 'Produtos por Clientes', 'CONSULTAS LIVRES'])
            
            # # st.session_state.escolha_do_menu_principal = escolha_do_menu_principal
            # st.button(f'Sidebar Status: {st.session_state.sidebar_state}', on_click=self.toggle_sidebar_state)

        cFiltrosAtivos = myfunc.monta_botoes_limpar_filtros_ativos()
        if cFiltrosAtivos:
            st.write(f"Filtros Ativos: {cFiltrosAtivos}")

        # escolha_do_menu_principal = st.session_state.get('escolha_do_menu_principal', 'Totais e Filtros Gerais')

        self.clientes,self.setores,self.segmentos,self.vendedores,self.df_totais_por_clientes,self.df_totais_por_vendedores,self.df_totais_por_setores,self.df_totais_por_cidades,self.df_totais_por_segmento,self.df_totais_por_uf = myfunc.load_table('load_totalizacoes_por_clientes')

        if escolha_do_menu_principal == 'Totais e Filtros Gerais':
            inicio.app(self)
        else:
            self.produtos, self.fornecedores, self.df_totais_emp_produtos, self.df_totais_emp_fornecedores, self.df_totais_emp_marcas, self.df_totais_emp_divisoes, self.df_totais_emp_gprecos, self.df_totais_emp_giro, self.df_totais_emp_gen, self.df_totais_emp_produtos_e_clientes = myfunc.load_table('load_totalizacoes_por_produtos')
            if escolha_do_menu_principal == "Totais por Produtos":
                produtos_vendidos.app()
            elif escolha_do_menu_principal == "Produtos por Vendedores":
                venda_por_vendedor.app(self.df_totais_empresa, self.df_totais_por_clientes, self.df_totais_por_vendedores, self.df_totais_por_setores, self.df_totais_por_cidades, self.df_totais_por_segmento, self.df_totais_por_uf, self.clientes, self.setores, self.segmentos, self.vendedores)
            elif escolha_do_menu_principal == "Produtos por Clientes":
                venda_por_cliente.app()
            # elif escolha_do_menu_principal == "CONSULTAS LIVRES":
            #     my_pygwalker.app()


def app():
    app = MyApp()
    app.run()


# /       # def app():
            
#         #     device_type = myfunc.get_tipo_de_dispositivo_se_mobile_ou_desktop()
                
#         #     opcoes_da_navbar = [ "Home", "Periodo", "Recarregar", "Config"]
#         #     styles = {
#         #         "nav": {
#         #             "background-color": "rgb(123, 209, 146)",
#         #         },
#         #         "div": {
#         #             "max-width": "32rem",
#         #         },
#         #         "active": {
#         #             "background-color": "rgba(255, 255, 255, 0.25)",
#         #         },
#         #         "hover": {
#         #             "background-color": "rgba(255, 255, 255, 0.35)",
#         #         },
#         #     }
#         #     escolha_da_navbar = st_navbar(opcoes_da_navbar, styles=styles)
#         #     if escolha_da_navbar=='Recarregar':
#         #         # st.write("vai "+page)
#         #         API_URL = os.getenv("API_URL", "http://localhost:80/api/updatebi")
#         #         with st.spinner("Recarregando periodo atual..."):
#         #             try:
#         #                 request = requests.get(API_URL)
#         #                 request.raise_for_status()
#         #                 response = json.loads(request.content)
#         #                 # st.info(f"""response: {response}""")
#         #                 st.info(f"""Dados atualizados em {response['result']}hs ... Clique Home... """)
#         #                 return None
#         #             except requests.exceptions.RequestException as e:
#         #                 st.error(f"Falha conectando retaguarda: {e}")
#         #                 return None
#         #     # else:
#         #     #     st.write(page)

#         #     df_totais_empresa = myfunc.load_table('csv/totvenda_empresa.csv')  # DTINI;DTFIM;QCLIPOSIT;QCLICAD;QCLIVISIT;QC_AMAIS;QC_AMENOS;QPRDCOMSLD;QPRDNAOVND;QTDPROD;QTDPRODCAD;QP_AMAIS;QP_AMENOS;VB1;VB2;V_AMAIS;V_AMENOS;V_META;V_PROJ;FVAL;FCREDDEVOL;QPEDIDOS;FVALPROD;FDESCONTO;TENDENCIA;A1A2;Q1;Q2;Q3;Q4;Q1A;Q2A;Q3A;Q4A;V1;V2;V3;V4;V1A;V2A;V3A;V4A
#         #     df_data_hora_ultima_atualizacao = myfunc.load_table('csv/ultima_atualizacao.csv') # DATAHORA
#         #     st.write(f"De {df_totais_empresa['DTINI'].iloc[0]} a {df_totais_empresa['DTFIM'].iloc[0]}... Recarga: {df_data_hora_ultima_atualizacao['DTHRUPDATE'].iloc[0]}")
#         #     myfunc.debugalert(f""" na menu principal ...  """)

#         #     # usando "from streamlit_navigation_bar import st_navbar" em combinacao com o st.sidebar o streamlit buga: desaparece o 'X' (close da sidebar)

#         #     # st.sidebar.image('http://localhost/images/ASSINATURA.png', caption="")
#         #     with st.sidebar:
#         #         # Substituímos o título pela logo da empresa
#         #         # st.logo("https://utfs.io/f/18abf710-06d8-4938-9028-196e77c16bea-5nx6en.png",icon_image="https://utfs.io/f/28e6820b-f340-40bb-a74e-0d7a8bf54b87-1njz0s.png")
#         #         if st.session_state.grupo in ["admin", "super-admin"]:
#         #             escolha_do_menu_principal = myfunc.exiba_menu(['Totais e Filtros Gerais', 'Totais por Produtos', 'Produtos por Vendedores', 'Produtos por Clientes', 'CONSULTAS LIVRES'])
#         #         elif st.session_state.grupo == "vendedor":
#         #             escolha_do_menu_principal = myfunc.exiba_menu(['Totais e Filtros Gerais', 'Totais por Produtos', 'Produtos por Vendedores', 'Produtos por Clientes', 'CONSULTAS LIVRES'])
#         #         else:
#         #             escolha_do_menu_principal = myfunc.exiba_menu(['Produtos por Vendedores', 'Produtos por Clientes', 'CONSULTAS LIVRES'])

#         #         clientes, setores, segmentos, vendedores, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf = myfunc.load_table('load_totalizacoes_por_clientes')
#         #         cFiltrosAtivos = myfunc.monta_botoes_limpar_filtros_ativos()

#         #         if device_type != 'mobile':
#         #             def change():
#         #                 st.session_state.sidebar_state = "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
#         #                 # st.session_state.sidebar_state = "auto" if  st.session_state.sidebar_state=="collapsed" else "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
#         #             st.button(f'Sidebar Status: {st.session_state.sidebar_state}', on_click=change)

#         #     if not cFiltrosAtivos is None and cFiltrosAtivos!='':
#         #         st.write(f"Filtros Ativos: {cFiltrosAtivos}")

#         #     if escolha_do_menu_principal == 'Totais e Filtros Gerais':
#         #         inicio.app(df_totais_empresa, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf, clientes, setores, segmentos, vendedores)
#         #     else:
#         #         produtos,fornecedores, df_totais_emp_produtos,df_totais_emp_fornecedores,df_totais_emp_marcas,df_totais_emp_divisoes,df_totais_emp_gprecos,df_totais_emp_giro,df_totais_emp_gen,df_totais_emp_produtos_e_clientes = myfunc.load_table('load_totalizacoes_por_produtos')
#         #         if escolha_do_menu_principal == "Produtos por Vendedores":
#         #             venda_por_vendedor.app(df_totais_empresa, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf, clientes, setores, segmentos, vendedores)
#         #         elif escolha_do_menu_principal == "Produtos por Clientes":
#         #             venda_por_cliente.app()
#         #         elif escolha_do_menu_principal == "Totais por Produtos":
#         #             produtos_vendidos.app()
#         #         elif escolha_do_menu_principal == "CONSULTAS LIVRES":
#         #             my_pygwalker.app()

# elif app == 'TESTE':
#     teste_popover()

    # # st.header(f"Vendas de {df_totais_empresa['DTINI'].iloc[0]} a {df_totais_empresa['DTFIM'].iloc[0]} :bar_chart:", divider='rainbow')
    # st.subheader('Totais Gerais das Vendas :bar_chart:', divider='rainbow')
    # # st.info(f"""Periodo de {df_totais_empresa['DTINI'].iloc[0]} a {df_totais_empresa['DTFIM'].iloc[0]}  \n atualizado em {df_data_hora_ultima_atualizacao['DATAHORA'].iloc[0]} """)


    # # page = st_navbar(["Home", "Documentation", "Examples", "Community", "About"])
    # # st.write(page)
    # # opcoes_da_navbar = ["Home", "Library", "Tutorials", "Development", "Download"]
        # "span": {
        #     "border-radius": "0.5rem",
        #     "color": "rgb(49, 51, 63)",
        #     "margin": "0 0.125rem",
        #     "padding": "0.4375rem 0.625rem",
        # },




# import os
# import streamlit as st

# # Função para listar arquivos CSV e extrair anos e meses
# def listar_anos_meses(pasta):
#     arquivos = os.listdir(pasta)
#     anos = []
#     meses = []
    
#     for arquivo in arquivos:
#         if arquivo.endswith('.csv'):
#             # Supondo que o nome do arquivo esteja no formato "ano-mes-nome.csv"
#             partes = arquivo.split('-')
#             ano = partes[0]
#             mes = partes[1]
            
#             if ano not in anos:
#                 anos.append(ano)
#             if mes not in meses:
#                 meses.append(mes)
    
#     return sorted(anos), sorted(meses)

# # Diretório onde os arquivos CSV estão armazenados
# pasta_diretorio = 'caminho/para/sua/pasta'

# # Obter listas de anos e meses
# anos, meses = listar_anos_meses(pasta_diretorio)

# # Criar selectboxes no Streamlit
# ano_selecionado = st.selectbox('Selecione o ano', anos)
# mes_selecionado = st.selectbox('Selecione o mês', meses)

# st.write(f'Você selecionou o ano: {ano_selecionado} e o mês: {mes_selecionado}')


# from datetime import datetime

# # Obter a data atual
# data_atual = datetime.now()

# # Formatando a data no formato YYMM
# ano_mes = data_atual.strftime('%y%m')

# print(ano_mes)
