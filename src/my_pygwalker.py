from pygwalker.api.streamlit import StreamlitRenderer
import streamlit as st
import myfunc, os
# https://github.com/Kanaries/pygwalker

def app():
    # Set title and subtitle
    # st.title('Consultas Gerais')
    st.subheader('Totalizacoes por criterios diversos')

    # relacao_venda_produtos = myfunc.load_relacao_venda_produtos( os.path.getmtime('csv/totvenda_prod.csv')  ) 
    relacao_venda_cliente_vendedor_produto = myfunc.load_relacao_venda_cliente_vendedor_produto( os.path.getmtime('csv/totvenda_cli_prod.csv')  ) 

    # You should cache your pygwalker renderer, if you don't want your memory to explode
    @st.cache_resource
    def get_pyg_renderer() -> "StreamlitRenderer":
        return StreamlitRenderer(relacao_venda_cliente_vendedor_produto, spec="./my_pygconfig.json", spec_io_mode="rw")

    renderer = get_pyg_renderer()

    tab1, tab2 = st.tabs(["Criar/Alterar", "Visualizar Consulta"])

    with tab1:
        # o renderer.explorer() permite criar/alterar graficos... se passar o parametro default_tab="data" ele entraria visualizando dados 
        renderer.explorer()

    with tab2:
        renderer.viewer()

