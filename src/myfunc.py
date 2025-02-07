import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from streamlit_extras.metric_cards import style_metric_cards
from millify import millify
from aggrid_com_pesquisa_generica import aggrid_com_pesquisa
from streamlit_option_menu import option_menu
# from user_agents import parse
# from streamlit_user_agent import UserAgent

#from streamlit_javascript import st_javascript
import re

# st.set_option('deprecation.showPyplotGlobalUse', False)

# def my_progress_bar(pg_caption, pg_int_percentage, pg_colour, pg_bgcolour):
# # def CreateProgressBar(pg_caption, pg_int_percentage, pg_colour, pg_bgcolour):
# #     pg_int_percentage = str(pg_int_percentage).zfill(2)
# #     pg_html = f"""<table style="width:50%; border-style: none;">
# #                         <tr style='font-weight:bold;'>
# #                             <td style='background-color:{pg_bgcolour};'>{pg_caption}: <span style='accent-color: {pg_colour}; bgcolor: transparent;'>
# #                                 <progress value='{pg_int_percentage}' max='100'>{pg_int_percentage}%</progress> </span>{pg_int_percentage}% 
# #                             </td>
# #                         </tr>
# #                     </table><br>"""
# #     return pg_html

# # st.markdown(CreateProgressBar("Positive", 62, "#A5D6A7", "#B2EBF2"), True)
# # st.markdown(CreateProgressBar("Neutral", 40, "#FFD54F", "#B2EBF2"), True)
# # st.markdown(CreateProgressBar("Negative", 65, "red", "#B2EBF2"), True)

def exiba_menu(OpcoesDoMenu, icones=["house", "dashboard", "eye", "person", "person"], Titulo_do_Menu='UpCiga BI'):
    escolha_do_menu = option_menu(
            menu_title=Titulo_do_Menu,
            options=OpcoesDoMenu,
            icons=icones,
            menu_icon='cast',
            default_index=0,
            styles={
                "container": {"padding": "5px!important", "background-color": "white", "border-radius": "10px"},
                "icon": {"color": "#6A0DAD", "font-size": "15px"},
                "nav-link": {"color": "#6A0DAD", "font-size": "17px", "text-align": "left", "margin": "0px", "--hover-color": "#32CD32"},
                "nav-link-selected": {"background-color": "#32CD32", "color": "white"}
            }
        )
    return escolha_do_menu

def get_tipo_de_dispositivo_se_mobile_ou_desktop():
    # r'(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-', re.I
    #  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) isMobile = true;})(navigator.userAgent||navigator.vendor||window.opera);
    # # def check_device(cTipoDeNavegador):
    # #     mobile_pattern = re.compile( r'Android|iPhone|iPod|BlackBerry|IEMobile|Opera Mini', re.I )
    # #     if mobile_pattern.match(cTipoDeNavegador):
    # #         check = True
    # #     else:
    # #         check = False
    # #     return check

    # navigator_userAgent = st_javascript(""" navigator.userAgent """)
    # is_mobile = check_device(navigator_userAgent)

    # Exemplo de uso
    # cTipoDeNavegador = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    # is_mobile = check_device(cTipoDeNavegador)
    # print(f"Is mobile: {is_mobile}")

    # st.subheader("Javascript API call")
    navigator_userAgent = st_javascript(""" navigator.userAgent """)    # any(): A função any() retorna True se qualquer um dos elementos no iterável for verdadeiro.
    is_mobile = any(agent in navigator_userAgent.lower() for agent in ["android", "iphone", "blackberry", "mobile", "iemobile", "opera m"])
    device_type = 'mobile' if is_mobile else 'desktop'

    # st.markdown(f"is_mobile={is_mobile} navigator.userAgent was: {navigator_userAgent}", unsafe_allow_html=True)
    # # Verificando o tipo de dispositivo
    # if device_type == 'mobile':
    #     st.write("Você está usando um dispositivo móvel.")
    # else:
    #     st.write("Você está usando um desktop.")

    # return_value = st_javascript(""" window.innerWidth """)
    # st.markdown(f"window.innerWidth was: {return_value}", unsafe_allow_html=True)

    return device_type

def mostra_progress_bar_venda_meta(venda_total, meta_total):
    style_metric_cards(border_radius_px=12, border_left_color='#AA00DD')
    col = st.columns(3)
    with col[0]:
        st.metric('VENDA R$', f'{millify(venda_total,precision=0)}') # st.metric('VENDA TOTAL', f'R${venda_total:,.0f}')
    with col[1]:
        st.metric('META R$', f'{millify(meta_total,precision=2)}')  # st.metric('Meta', f'R${millify( df_totais_empresa['V_META'].sum() ,precision=2)}')
    with col[2]:
        st.metric('%Meta (%)', f'{millify(100*venda_total/meta_total,precision=1)} %') # st.metric('Projecao', f'R${millify( df_totais_empresa['V_PROJ'].sum() ,precision=2)}')

    # Mostra uma progress bar with the current percentage
    progress_bar = st.empty()               # Create a placeholder for the progress bar and text
    percentage = venda_total / meta_total   # Calculate the percentage for the progress bar
    progress_bar.progress(percentage)
    
    # mostra the text under the progress bar to show min, current, and max values
    min_val = 0
    progress_style = f"""
    <div style="
        display: flex;
        justify-content: space-between;
        width: 100%;">
        <span>{min_val}</span>
        <span style="position: absolute; left: {percentage * 100}%; transform: translateX(-50%);">
            {venda_total} ({percentage * 100:.1f}%)
        </span>
        <span>{meta_total}</span>
    </div>
    """
    progress_text = st.empty()
    progress_text.markdown(progress_style, unsafe_allow_html=True)

def my_aggrid(df, cTitulo1, cTextoDoInputDePesquisa='', conteudo_do_placeholder='', CHelpText='', cColunaId='', cColunaNome='', cColunasAgGrid='', fg_permite_rerun=False):
    return aggrid_com_pesquisa(df, cTitulo1, cTextoDoInputDePesquisa, conteudo_do_placeholder, CHelpText, cColunaId, cColunaNome, cColunasAgGrid, fg_permite_rerun)

def mostra_grafico_barras_e_pizza(df, cColunaXComValor, cColunaYComNome, cTitulo1, nFaixasToShow=0, cTextoDoInputDePesquisa='', conteudo_do_placeholder='', CHelpText='', cColunaId='', cColunaNome='', cColunasAgGrid=''):
    if nFaixasToShow>0:
        cTituloGrafico = f"TOP {nFaixasToShow} {cTitulo1}"
    else:
        cTituloGrafico = "Venda por "+cTitulo1

    tab1, tab2 = st.tabs([cTituloGrafico, "Filtrar "+cTitulo1 ])
    with tab1:
        if nFaixasToShow>0:
            dataframe_to_show = df.sort_values(cColunaXComValor,ascending=False).head(nFaixasToShow) # pega as maiores nFaixasToShow 
            dataframe_to_show = dataframe_to_show.sort_values(by=[cColunaXComValor],ascending=True)
        else:
            dataframe_to_show = df.sort_values(cColunaXComValor,ascending=True)

        col1, col2= st.columns([1.5, 1])   # Divide a tela em duas colunas, com proporções 1.5, 1
        with col1:
            # Cria o gráfico de barras
            fig = px.bar(dataframe_to_show, x=cColunaXComValor, y=cColunaYComNome, orientation='h') # , color="FVAL"
            st.plotly_chart(fig, use_container_width=True)
        with col2: 
            # Cria o gráfico de pizza
            fig = px.pie(dataframe_to_show, values=cColunaXComValor, names=cColunaYComNome)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if cTextoDoInputDePesquisa != "":           # search_term != "" eh o mesmo que: not search_term == "":
            aggrid_com_pesquisa(df, cTitulo1, cTextoDoInputDePesquisa, conteudo_do_placeholder, CHelpText, cColunaId, cColunaNome, cColunasAgGrid, True)
        else:
            st.dataframe(df)

def monta_botoes_limpar_filtros_ativos():
    def monta_botao_limpa_filtro(cNomeDaTabela, cFiltrosAtivos=''):
        cFiltroAtivo = ''
        cNomeDaVariavelDeSessao = 'psq'+cNomeDaTabela
        if cNomeDaVariavelDeSessao in st.session_state and not getattr(st.session_state, cNomeDaVariavelDeSessao) is None:
            cFiltroAtivo = cNomeDaTabela+': '+getattr(st.session_state, cNomeDaVariavelDeSessao)
            cTextoDoBotao = 'Limpar '+cFiltroAtivo
            div_limpar_filtro = st.sidebar.empty()               # Create a placeholder for the st.sidebar.button(cTextoDoBotao)
            chk_botao_limpar = div_limpar_filtro.button(cTextoDoBotao, key='limpar_filtro_'+cNomeDaVariavelDeSessao) # precisa indicar a key=... senao o streamlit buga ja que os botoes estarao sendo criados com o mesmo nome de variavel... para ver o problema, retire a key=...
            if chk_botao_limpar:
                setattr(st.session_state, cNomeDaVariavelDeSessao, None)
                setattr(st.session_state, 'df_'+cNomeDaVariavelDeSessao, None)
                div_limpar_filtro.empty()
                st.rerun()
            cFiltrosAtivos = cFiltrosAtivos+' ; '+cFiltroAtivo if cFiltrosAtivos!='' and cFiltroAtivo!='' else cFiltroAtivo if cFiltroAtivo!='' else ''
        return cFiltrosAtivos
    cFiltrosAtivos = ''
    cFiltrosAtivos = monta_botao_limpa_filtro("Vendedores", cFiltrosAtivos)
    cFiltrosAtivos = monta_botao_limpa_filtro("Setores", cFiltrosAtivos)
    cFiltrosAtivos = monta_botao_limpa_filtro("Segmentos", cFiltrosAtivos)
    cFiltrosAtivos = monta_botao_limpa_filtro("Cidades", cFiltrosAtivos)
    cFiltrosAtivos = monta_botao_limpa_filtro("Clientes", cFiltrosAtivos)
    cFiltrosAtivos = monta_botao_limpa_filtro("UFs", cFiltrosAtivos)
    return cFiltrosAtivos

def get_filtros_ativos():
    def get_filtro(cNomeDaTabela, cFiltrosAtivos=''):
        cFiltroAtivo = ''
        cNomeDaVariavelDeSessao = 'psq'+cNomeDaTabela
        if cNomeDaVariavelDeSessao in st.session_state and not getattr(st.session_state, cNomeDaVariavelDeSessao) is None:
            cFiltroAtivo = cNomeDaTabela+': '+getattr(st.session_state, cNomeDaVariavelDeSessao)
            cFiltrosAtivos = cFiltrosAtivos+' ; '+cFiltroAtivo if cFiltrosAtivos!='' and cFiltroAtivo!='' else cFiltroAtivo if cFiltroAtivo!='' else ''
        return cFiltrosAtivos
    cFiltrosAtivos = ''
    cFiltrosAtivos = get_filtro("Vendedores", cFiltrosAtivos)
    cFiltrosAtivos = get_filtro("Setores", cFiltrosAtivos)
    cFiltrosAtivos = get_filtro("Segmentos", cFiltrosAtivos)
    cFiltrosAtivos = get_filtro("Cidades", cFiltrosAtivos)
    cFiltrosAtivos = get_filtro("Clientes", cFiltrosAtivos)
    cFiltrosAtivos = get_filtro("UFs", cFiltrosAtivos)
    return cFiltrosAtivos

def load_df_totais_por_clientes_e_vendedores(oQueRetornar='cli_vend'):
    if 'df_psqClientes' in st.session_state and not st.session_state.df_psqClientes is None:
        clientes = load_table( 'csv/cliente.csv' ) # IDCLI;NOMECLI;IDVENDEDOR;IDSETOR;CIDADE;UF;IDSEGMENTO
        df_totais_por_clientes = st.session_state.df_psqClientes
    else:
        clientes, df_totais_por_clientes = load_df_totais_por_clientes( os.path.getmtime('csv/totvenda_cli.csv') ) 

    if 'df_psqVendedores' in st.session_state and not st.session_state.df_psqVendedores is None:
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['IDVENDEDOR'].isin( st.session_state.df_psqVendedores['IDVENDEDOR']) ]
    if 'df_psqSetores'   in st.session_state and not st.session_state.df_psqSetores is None:
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['IDSETOR'].isin( st.session_state.df_psqSetores['IDSETOR']) ]
    if 'df_psqSegmentos' in st.session_state and not st.session_state.df_psqSegmentos is None:
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['IDSEGMENTO'].isin( st.session_state.df_psqSegmentos['IDSEGMENTO']) ]
    if 'df_psqCidades'   in st.session_state and not st.session_state.df_psqCidades is None:
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['CIDADE'].isin( st.session_state.df_psqCidades['CIDADE']) ]
    if 'df_psqUFs'       in st.session_state and not st.session_state.df_psqUFs is None:
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['UF'].isin( st.session_state.df_psqUFs['UF']) ]
    if 'df_psqMovnfProdutos'  in st.session_state and not st.session_state.df_psqMovnfProdutos is None:
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['IDCLI'].isin( st.session_state.df_psqMovnfProdutos['IDCLI']) ]

    if oQueRetornar=='cli_vend':
        if 'df_psqVendedores' in st.session_state and not st.session_state.df_psqVendedores is None:
            vendedores = load_table('csv/vendedor.csv')  # st.write('df_psqVendedores:') st.dataframe(st.session_state.df_psqVendedores)
            df_totais_por_vendedores = st.session_state.df_psqVendedores 
        else:
            vendedores, df_totais_por_vendedores = load_df_totais_por_vendedores( os.path.getmtime('csv/totvenda_vendedor.csv') )
        df_totais_por_vendedores = df_totais_por_vendedores[ df_totais_por_vendedores['IDVENDEDOR'].isin( df_totais_por_clientes['IDVENDEDOR']) ]            
        return clientes, df_totais_por_clientes, vendedores, df_totais_por_vendedores
    else:
        return clientes, df_totais_por_clientes

def existem_filtros_salvos_na_session_state():
    return ( 'df_psqClientes' in st.session_state or 'df_psqVendedores' in st.session_state or 'df_psqSetores' in st.session_state or 'df_psqSegmentos' in st.session_state or 'df_psqCidades' in st.session_state or 'df_psqUFs' in st.session_state )

def load_table(cFileCsv):
    # return load_table_csv(cFileCsv, os.path.getmtime(cFileCsv))  nao posso usar simplesmente assim, pois todas as vezes que fosse feita uma chamada a essa funcao mudando o nome do cfilecsv, ele recarraria tudo
   
    if (cFileCsv == 'load_totalizacoes_por_clientes' or cFileCsv == 'load_df_totais_por_clientes_e_vendedores' or cFileCsv == 'load_df_pedidos_itens' or cFileCsv == 'csv/totvenda_cli.csv' or cFileCsv == 'csv/totvenda_vendedor.csv') and existem_filtros_salvos_na_session_state():
        debugalert(f""" passando na load_table COM ST.SESSION_STATE: {cFileCsv} """)
       
        if cFileCsv == 'load_totalizacoes_por_clientes':
            debugalert(f""" VAI CARREGAR CLIENTES e seus groupby DO ST.SESSION_STATE """)
            clientes, df_totais_por_clientes, vendedores, df_totais_por_vendedores = load_df_totais_por_clientes_e_vendedores()

            setores = load_table('csv/setor.csv') # IDSETOR;NOME
            if 'df_psqSetores' in st.session_state and not st.session_state.df_psqSetores is None:
                df_totais_por_setores = st.session_state.df_psqSetores
                df_totais_por_setores = df_totais_por_setores[ df_totais_por_setores['IDSETOR'].isin( df_totais_por_clientes['IDSETOR']) ]
            else:
                df_totais_por_setores = df_totais_por_clientes.groupby('IDSETOR')['FVAL'].sum().reset_index()
                df_totais_por_setores = pd.merge(df_totais_por_setores,setores,on='IDSETOR',how='left')
                df_totais_por_setores = df_totais_por_setores.sort_values(by='FVAL',ascending=False)

            segmentos = load_table('csv/segmento.csv') # IDSEGMENTO;SEGMENTO
            if 'df_psqSegmentos' in st.session_state and not st.session_state.df_psqSegmentos is None:
                df_totais_por_segmento = st.session_state.df_psqSegmentos
                df_totais_por_segmento = df_totais_por_segmento[ df_totais_por_segmento['IDSEGMENTO'].isin( df_totais_por_clientes['IDSEGMENTO']) ]
            else:
                df_totais_por_segmento = df_totais_por_clientes.groupby('IDSEGMENTO')['FVAL'].sum().reset_index()  
                df_totais_por_segmento = pd.merge(df_totais_por_segmento,segmentos,on='IDSEGMENTO',how='left')
                df_totais_por_segmento = df_totais_por_segmento.sort_values(by='FVAL',ascending=False)

            if 'df_psqCidades' in st.session_state and not st.session_state.df_psqCidades is None:
                df_totais_por_cidades = st.session_state.df_psqCidades
                df_totais_por_cidades = df_totais_por_cidades[ df_totais_por_cidades['CIDADE'].isin( df_totais_por_clientes['CIDADE']) ]
            else:
                df_totais_por_cidades = df_totais_por_clientes.groupby('CIDADE')['FVAL'].sum().reset_index()  
                df_totais_por_cidades = df_totais_por_cidades.sort_values(by='FVAL',ascending=False)   # df_totais_por_cidades = df_totais_por_cidades[ df_totais_por_cidades['FVAL'] > 0 ]
            
            if 'df_psqUFs' in st.session_state and not st.session_state.df_psqUFs is None:
                df_totais_por_uf = st.session_state.df_psqUFs
                df_totais_por_uf = df_totais_por_uf[ df_totais_por_uf['UF'].isin( df_totais_por_clientes['UF']) ]
            else:
                df_totais_por_uf = df_totais_por_clientes.groupby('UF')['FVAL'].sum().reset_index()  
                df_totais_por_uf = df_totais_por_uf.sort_values(by='FVAL',ascending=False)

            return clientes, setores, segmentos, vendedores, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf 

        elif cFileCsv == 'load_totalizacoes_por_produtos':

            produtos,fornecedores, df_totais_emp_produtos,df_totais_emp_fornecedores,df_totais_emp_marcas,df_totais_emp_divisoes,df_totais_emp_gprecos,df_totais_emp_giro,df_totais_emp_gen,df_totais_emp_produtos_e_clientes = load_totalizacoes_por_produtos(os.path.getmtime('csv/totvenda_cli_prod.csv')) 

            # produtos = load_produtos(os.path.getmtime('csv/produto.csv')) #PCOD;IDGRUPO;IDSUBGRUPO;IDFORN;IDGPRECO;PABCFISICA;PGENERICO;MARCA;MODELO;PDESC;PUNIDADE;PVLUVEN3;PVLUVENDA;SALDO
            # fornecedores = load_table('csv/fornecedores.csv') # IDFORN;NOMEFORN;CP_CIDADE;UF

            # df_totais_emp_produtos = pd.merge(df_totais_emp_produtos,produtos,on='PCOD',how='left', suffixes=('', '_y')) 
            # df_totais_emp_fornecedores = df_totais_emp_produtos.groupby('IDFORN')['VLVENDA'].sum().reset_index()
            # df_totais_emp_marcas = df_totais_emp_produtos.groupby('MARCA')['VLVENDA'].sum().reset_index()  
            # df_totais_emp_divisoes = df_totais_emp_produtos.groupby('IDSUBGRUPO')['VLVENDA'].sum().reset_index()  
            # df_totais_emp_gprecos = df_totais_emp_produtos.groupby('IDGPRECO')['VLVENDA'].sum().reset_index()  
            # df_totais_emp_giro = df_totais_emp_produtos.groupby('PABCFISICA')['VLVENDA'].sum().reset_index()  
            # df_totais_emp_gen = df_totais_emp_produtos.groupby('PGENERICO')['VLVENDA'].sum().reset_index()  
            # df_totais_emp_produtos_e_clientes = load_relacao_venda_cliente_vendedor_produto(file_update_timestamp) # csv/totvenda_cli_prod.csv

            # if 'df_psqFornecedores' in st.session_state and not st.session_state.df_psqFornecedores is None:
            #     df_totais_emp_fornecedores = st.session_state.df_psqFornecedores
            #     df_totais_emp_fornecedores = df_totais_emp_fornecedores[ df_totais_emp_fornecedores['IDFORN'].isin( df_totais_por_clientes['IDFORN']) ]
            # else:
            #     df_totais_por_setores = df_totais_por_clientes.groupby('IDSETOR')['FVAL'].sum().reset_index()
            #     df_totais_por_setores = pd.merge(df_totais_por_setores,setores,on='IDSETOR',how='left')
            #     df_totais_por_setores = df_totais_por_setores.sort_values(by='FVAL',ascending=False)

            return produtos,fornecedores, df_totais_emp_produtos,df_totais_emp_fornecedores,df_totais_emp_marcas,df_totais_emp_divisoes,df_totais_emp_gprecos,df_totais_emp_giro,df_totais_emp_gen,df_totais_emp_produtos_e_clientes

        elif cFileCsv == 'load_df_pedidos_itens':
            clientes, df_totais_por_clientes = load_df_totais_por_clientes_e_vendedores(oQueRetornar='apenas_clientes')
            if 'df_psqPedidosItens' in st.session_state and not st.session_state.df_psqPedidosItens is None:
                df_pedidos_itens = st.session_state.df_psqPedidosItens
            else:
                df_pedidos_itens = load_df_pedidos_itens(os.path.getmtime('csv/venda_itens.csv'))  # df_pedidos_itens
            df_pedidos_itens = df_pedidos_itens[ df_pedidos_itens['IDCLI'].isin( df_totais_por_clientes['IDCLI']) ]

        elif cFileCsv == 'load_df_totais_por_clientes_e_vendedores':
            return load_df_totais_por_clientes_e_vendedores() # clientes, df_totais_por_clientes, vendedores, df_totais_por_vendedores

        elif cFileCsv == 'csv/totvenda_cli.csv':
            return load_df_totais_por_clientes_e_vendedores(oQueRetornar='apenas_clientes')

        elif cFileCsv == 'csv/totvenda_vendedor.csv':
            vendedores = load_table('csv/vendedor.csv')
            df_totais_por_vendedores = st.session_state.df_psqVendedores # getattr(st.session_state, 'df_'+cNomeDaVariavelDeSessao)
            return vendedores, df_totais_por_vendedores
        
    else:
        debugalert(f""" passando na load_table SEM ST.SESSION_STATE: {cFileCsv} """)

        if cFileCsv == 'load_totalizacoes_por_clientes':
            return load_totalizacoes_por_clientes( os.path.getmtime('csv/totvenda_cli.csv') ) # clientes, setores, segmentos, vendedores, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf 

        elif cFileCsv == 'load_totalizacoes_por_produtos':
            return load_totalizacoes_por_produtos(os.path.getmtime('csv/totvenda_cli_prod.csv'))

        elif cFileCsv == 'load_df_pedidos_itens':
            return load_df_pedidos_itens(os.path.getmtime('csv/venda_itens.csv'))  # df_pedidos_itens

        else:
            file_update_timestamp = os.path.getmtime(cFileCsv)
            if cFileCsv == 'csv/totvenda_cli.csv':
                return load_df_totais_por_clientes(file_update_timestamp) # st.write('df_totais_por_clientes apos filtro antes de retornar:') # st.dataframe(df_totais_por_clientes) # time.sleep(4) # return clientes, df_totais_por_clientes
            elif cFileCsv == 'csv/totvenda_vendedor.csv':
                return load_df_totais_por_vendedores(file_update_timestamp)  # vendedores, df_totais_por_vendedores
            elif cFileCsv == 'csv/vendedor.csv':
                return load_vendedores(file_update_timestamp)      
            elif cFileCsv == 'csv/produto.csv':
                return load_produtos(file_update_timestamp)
            elif cFileCsv == 'csv/venda.csv':
                return load_vendas(file_update_timestamp)
            elif cFileCsv == 'csv/venda_itens.csv':
                return load_venda_itens(file_update_timestamp)
            elif cFileCsv == 'csv/cliente.csv':
                return load_clientes(file_update_timestamp)
            elif cFileCsv == 'csv/fornecedores.csv':
                return load_fornecedores(file_update_timestamp)
            elif cFileCsv == 'csv/totvenda_prod.csv':
                return load_relacao_venda_produtos(file_update_timestamp)
            elif cFileCsv == 'csv/totvenda_cli_prod.csv':
                return load_relacao_venda_cliente_vendedor_produto(file_update_timestamp)
            elif cFileCsv == 'csv/clientes_setores.csv':
                return load_setores(file_update_timestamp)
            elif cFileCsv == 'csv/segmento.csv':
                return load_segmentos(file_update_timestamp)
            elif cFileCsv == 'csv/totvenda_empresa.csv':
                return load_totais_empresa(file_update_timestamp)
            elif cFileCsv == 'csv/ultima_atualizacao.csv':
                return load_ultima_atualizacao(file_update_timestamp)
            else:
                return load_table_csv(file_update_timestamp,cFileCsv)


@st.cache_data(ttl=24*60*60)
def load_table_csv(file_update_timestamp,cFileCsv):                    # recarregara se o cFileCsv ou o timestamp mudar entre uma chamada e outra
    debugalert("CSV DA GENERICA: "+cFileCsv)
    return pd.read_csv(cFileCsv, delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_df_totais_por_clientes(file_update_timestamp):
    clientes = load_table( 'csv/cliente.csv' ) # IDCLI;NOMECLI;IDVENDEDOR;IDSETOR;CIDADE;UF;IDSEGMENTO
    debugalert('csv/totvenda_cli.csv')
    df_totais_por_clientes = pd.read_csv('csv/totvenda_cli.csv', delimiter=';',encoding='latin-1') # [['IDCLI', 'IDVENDEDOR', 'FVAL', 'V_META', 'A1A2', 'V_PROJ', 'TENDENCIA', 'QCLIPOSIT', 'QCLICAD']] # IDCLI;IDVENDEDOR;QCLIPOSIT;QCLICAD;FVAL3;FVAL;FCREDDEVOL;FVALDEV;QPEDIDOS;LUCRO;FVALPROD;FDESCONTO;QCLIVISIT;QTDPROD;QC_AMAIS;QC_AMENOS;V_AMAIS;V_AMENOS;QP_AMAIS;QP_AMENOS;V_AMAIS;V_AMENOS;V_META;V_PROJ;TENDENCIA;A1A2;Q1;Q2;Q3;Q4;Q1A;Q2A;Q3A;Q4A;V1;V2;V3;V4;V1A;V2A;V3A;V4A
    # st.write('df_totais_por_clientes antes do merge')
    # st.dataframe(df_totais_por_clientes)
    df_totais_por_clientes = pd.merge(df_totais_por_clientes,clientes,on='IDCLI',how='left', suffixes=('', '_y')) # o suffixes eh porque a coluna IDVENDEDOR esta repetida nas duas tabelas, na csv/cliente.csv e na csv/totvenda_cli.csv
    if st.session_state.grupo == 'vendedor':
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['IDVENDEDOR'] == int(st.session_state.idvendedor) ]

    # st.write('df_totais_por_clientes depois do merge')
    # st.dataframe(df_totais_por_clientes)

    # df_totais_por_clientes.drop(df_totais_por_clientes.filter(regex='_y$').columns, axis=1, inplace=True)
    # st.write('df_totais_por_clientes depois de eliminar a idvendedor_y')
    # st.dataframe(df_totais_por_clientes)
    # time.sleep(4)
    # df_totais_por_clientes = df_totais_por_clientes.sort_values(by='FVAL',ascending=False).reset_index()
    return clientes, df_totais_por_clientes

@st.cache_data(ttl=24*60*60)
def load_df_totais_por_vendedores(file_update_timestamp):
    vendedores = load_table('csv/vendedor.csv')
    debugalert('csv/totvenda_vendedor.csv')
    df_totais_por_vendedores = pd.read_csv('csv/totvenda_vendedor.csv', delimiter=';',encoding='latin-1') # [['IDVENDEDOR','FVAL', 'V_META', 'A1A2', 'V_PROJ', 'TENDENCIA', 'QCLIPOSIT', 'QCLICAD']] # IDVENDEDOR;QCLIPOSIT;QCLICAD;QCLIVISIT;QC_AMAIS;QC_AMENOS;QPRDCOMSLD;QPRDNAOVND;QTDPROD;QTDPRODCAD;V_AMAIS;V_AMENOS;QP_AMAIS;QP_AMENOS;V_AMAIS;V_AMENOS;V_META;V_PROJ;FVAL;FCREDDEVOL;QPEDIDOS;FVALPROD;FDESCONTO;TENDENCIA;A1A2;Q1;Q2;Q3;Q4;Q1A;Q2A;Q3A;Q4A;V1;V2;V3;V4;V1A;V2A;V3A;V4A
    if st.session_state.grupo == 'vendedor':
        # st.subheader(f'Vendas de {st.session_state.sys_usuario} (Cod{st.session_state.idvendedor}) :bar_chart:', divider='rainbow')
        #  df_filtrado = df[ df[cColunaId] == int(search_term) ]
        df_totais_por_vendedores = df_totais_por_vendedores[ df_totais_por_vendedores['IDVENDEDOR'] == int(st.session_state.idvendedor) ]
    df_totais_por_vendedores = pd.merge(df_totais_por_vendedores,vendedores,on='IDVENDEDOR',how='left')
    df_totais_por_vendedores = df_totais_por_vendedores.sort_values(by='FVAL',ascending=False)
    return vendedores, df_totais_por_vendedores

@st.cache_data(ttl=24*60*60)
def load_df_pedidos_itens(file_update_timestamp):
    df_vendas = load_vendas( os.path.getmtime('csv/venda.csv') ) # 'csv/venda.csv': # venda.csv FLOJA;IDPEDIDO;IDCLI;FVENDEDOR;FDATAEMI;HORA;FVAL
    df_venda_itens = load_venda_itens( file_update_timestamp  )[['IDPEDIDO','PCOD', 'QTDVENDA', 'VLVENDA']] # venda_itens.csv IDPEDIDO;PCOD;QTDVENDA;VLVENDA;PCFOP;MFGES
    df_pedidos_itens = pd.merge(df_venda_itens, df_vendas, on='IDPEDIDO', how='left')
    clientes = load_table( 'csv/cliente.csv' ) # csv/cliente.csv: IDCLI;NOMECLI;IDVENDEDOR;IDSETOR;CIDADE;UF;IDSEGMENTO
    df_pedidos_itens = pd.merge(df_venda_itens, clientes, on='IDCLI', how='left') 
    if st.session_state.grupo == 'vendedor':
        df_pedidos_itens = df_pedidos_itens[ df_pedidos_itens['IDVENDEDOR'] == int(st.session_state.idvendedor) ]
    return df_pedidos_itens

@st.cache_data(ttl=24*60*60)
def load_totalizacoes_por_clientes(file_update_timestamp):
    clientes, df_totais_por_clientes = load_df_totais_por_clientes(file_update_timestamp)
    vendedores, df_totais_por_vendedores = load_df_totais_por_vendedores( os.path.getmtime('csv/totvenda_vendedor.csv') )

    setores = load_table('csv/setor.csv') # IDSETOR;NOME
    df_totais_por_setores = df_totais_por_clientes.groupby('IDSETOR')['FVAL'].sum().reset_index()
    df_totais_por_setores = pd.merge(df_totais_por_setores,setores,on='IDSETOR',how='left')
    df_totais_por_setores = df_totais_por_setores.sort_values(by='FVAL',ascending=False)

    df_totais_por_cidades = df_totais_por_clientes.groupby('CIDADE')['FVAL'].sum().reset_index()  
    df_totais_por_cidades = df_totais_por_cidades.sort_values(by='FVAL',ascending=False)   # df_totais_por_cidades = df_totais_por_cidades[ df_totais_por_cidades['FVAL'] > 0 ]

    segmentos = load_table('csv/segmento.csv') # IDSEGMENTO;SEGMENTO
    df_totais_por_segmento = df_totais_por_clientes.groupby('IDSEGMENTO')['FVAL'].sum().reset_index()  
    df_totais_por_segmento = pd.merge(df_totais_por_segmento,segmentos,on='IDSEGMENTO',how='left')
    df_totais_por_segmento = df_totais_por_segmento.sort_values(by='FVAL',ascending=False)

    df_totais_por_uf = df_totais_por_clientes.groupby('UF')['FVAL'].sum().reset_index()  
    df_totais_por_uf = df_totais_por_uf.sort_values(by='FVAL',ascending=False)
    return clientes, setores, segmentos, vendedores, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf 

@st.cache_data(ttl=24*60*60)
def load_totalizacoes_por_produtos(file_update_timestamp):
    # df_totais_emp_produtos, df_totais_emp_fornecedores, df_totais_emp_divisoes, df_totais_emp_marcas, df_totais_emp_gprecos, df_totais_emp_giro, df_totais_emp_gen
    produtos = load_produtos(os.path.getmtime('csv/produto.csv')) #PCOD;IDGRUPO;IDSUBGRUPO;IDFORN;IDGPRECO;PABCFISICA;PGENERICO;MARCA;MODELO;PDESC;PUNIDADE;PVLUVEN3;PVLUVENDA;SALDO
    df_totais_emp_produtos = load_relacao_venda_produtos(os.path.getmtime('csv/totvenda_prod.csv')) # PCOD;QTDVENDA;MVALOR3;VLVENDA;TENDENCIA;QP_AMAIS;QP_AMENOS;VB1;VB2;V_AMAIS;V_AMENOS;V_META;V_PROJ;TENDENCIA;A1A2;Q1;Q2;Q3;Q4;Q1A;Q2A;Q3A;Q4A;V1;V2;V3;V4;V1A;V2A;V3A;V4A
    df_totais_emp_produtos = pd.merge(df_totais_emp_produtos,produtos,on='PCOD',how='left', suffixes=('', '_y')) 

    fornecedores = load_table('csv/fornecedores.csv') # IDFORN;NOMEFORN;CP_CIDADE;UF
    df_totais_emp_fornecedores = df_totais_emp_produtos.groupby('IDFORN')['VLVENDA'].sum().reset_index()
    df_totais_emp_fornecedores = pd.merge(df_totais_emp_fornecedores,fornecedores[['NOMEFORN']],on='IDFORN',how='left')
    df_totais_emp_fornecedores = df_totais_emp_fornecedores.sort_values(by='VLVENDA',ascending=False)

    df_totais_emp_marcas = df_totais_emp_produtos.groupby('MARCA')['VLVENDA'].sum().reset_index()  
    df_totais_emp_marcas = df_totais_emp_marcas.sort_values(by='VLVENDA',ascending=False)   

    df_totais_emp_divisoes = df_totais_emp_produtos.groupby('IDSUBGRUPO')['VLVENDA'].sum().reset_index()  
    df_totais_emp_divisoes = df_totais_emp_divisoes.sort_values(by='VLVENDA',ascending=False)   

    df_totais_emp_gprecos = df_totais_emp_produtos.groupby('IDGPRECO')['VLVENDA'].sum().reset_index()  
    df_totais_emp_gprecos = df_totais_emp_gprecos.sort_values(by='VLVENDA',ascending=False)   

    df_totais_emp_giro = df_totais_emp_produtos.groupby('PABCFISICA')['VLVENDA'].sum().reset_index()  
    df_totais_emp_giro = df_totais_emp_giro.sort_values(by='VLVENDA',ascending=False)   

    df_totais_emp_gen = df_totais_emp_produtos.groupby('PGENERICO')['VLVENDA'].sum().reset_index()  
    df_totais_emp_gen = df_totais_emp_gen.sort_values(by='VLVENDA',ascending=False)   

    df_totais_emp_produtos_e_clientes = load_relacao_venda_cliente_vendedor_produto(file_update_timestamp) # csv/totvenda_cli_prod.csv
    return produtos,fornecedores, df_totais_emp_produtos,df_totais_emp_fornecedores,df_totais_emp_marcas,df_totais_emp_divisoes,df_totais_emp_gprecos,df_totais_emp_giro,df_totais_emp_gen,df_totais_emp_produtos_e_clientes


@st.cache_data(ttl=24*60*60)
def load_vendedores(file_update_timestamp):
    debugalert('csv/vendedor.csv')
    return pd.read_csv('csv/vendedor.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_totais_empresa(file_update_timestamp):
    debugalert('csv/totvenda_empresa.csv')
    return pd.read_csv('csv/totvenda_empresa.csv', delimiter=';',encoding='latin-1') # df_totais_empresa = myfunc.load_table('csv/totvenda_empresa.csv')[['FVAL', 'V_META', 'V_PROJ', 'A1A2', 'TENDENCIA', 'QCLIPOSIT', 'QCLICAD','QTDPRODCAD','QTDPROD','QPRDNAOVND']]  

@st.cache_data(ttl=24*60*60)
def load_produtos(file_update_timestamp):
    debugalert('csv/produto.csv')
    return pd.read_csv('csv/produto.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_clientes(file_update_timestamp):
    debugalert('csv/cliente.csv')
    return pd.read_csv('csv/cliente.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_fornecedores(file_update_timestamp):
    debugalert('csv/fornecedores.csv')
    return pd.read_csv('csv/fornecedores.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_vendas(file_update_timestamp):
    debugalert('csv/venda.csv')
    return pd.read_csv('csv/venda.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_venda_itens(file_update_timestamp):
    debugalert('csv/venda_itens.csv')
    return pd.read_csv('csv/venda_itens.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_relacao_venda_produtos(file_update_timestamp):
    debugalert('csv/totvenda_prod.csv')
    return pd.read_csv('csv/totvenda_prod.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_relacao_venda_cliente_vendedor_produto(file_update_timestamp):
    debugalert('csv/totvenda_cli_prod.csv')
    df_totais_emp_produtos_e_clientes = pd.read_csv('csv/totvenda_cli_prod.csv', delimiter=';',encoding='latin-1') 
    if st.session_state.grupo == 'vendedor':
        df_totais_emp_produtos_e_clientes = df_totais_emp_produtos_e_clientes[ df_totais_emp_produtos_e_clientes['IDVENDEDOR'] == int(st.session_state.idvendedor) ]
    return df_totais_emp_produtos_e_clientes

@st.cache_data(ttl=24*60*60)
def load_setores(file_update_timestamp):
    debugalert('csv/clientes_setores.csv')
    return pd.read_csv('csv/clientes_setores.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_segmentos(file_update_timestamp):
    debugalert('csv/segmento.csv')
    return pd.read_csv('csv/segmento.csv', delimiter=';',encoding='latin-1')

@st.cache_data(ttl=24*60*60)
def load_ultima_atualizacao(file_update_timestamp):
    debugalert('csv/ultima_atualizacao.csv')
    return pd.read_csv('csv/ultima_atualizacao.csv', delimiter=';',encoding='latin-1')

def debugalert(cFileCsv):
    if False:
        st.info(f""" DO CSV: {cFileCsv} { time.time() } """)
        time.sleep(3)


# There isn't an option to filter the rows before the CSV file is loaded into a pandas object.
# You can either load the file and then filter using df[df['field'] > constant], or if you have a very large file and you are worried about memory running out, then use an iterator and apply the filter as you concatenate chunks of your file e.g.:

# import pandas as pd
# iter_csv = pd.read_csv('file.csv', iterator=True, chunksize=1000)
# df = pd.concat([chunk[chunk['field'] > constant] for chunk in iter_csv])


    # # Na abordagem seguinte, que nao deu certo, foi assim: Captura do Tipo de Dispositivo: Usamos st.text_input para capturar o valor do campo oculto criado pelo JavaScript e definir a chave key='device-type' para associá-lo ao campo correto.
    # # JavaScript para detectar o tipo de dispositivo
    # device_type_js = """
    # <script>
    # function detectDeviceType() {
    #     const ua = navigator.userAgent;
    #     if (/Mobi|Android/i.test(ua)) {
    #         return 'mobile';
    #     }
    #     return 'desktop';
    # }
    # document.write('<input type="hidden" id="device-type" value="' + detectDeviceType() + '">');
    # </script>
    # """
    # # Injetando o JavaScript no Streamlit
    # st.markdown(device_type_js, unsafe_allow_html=True)
    # # Obtendo o valor do tipo de dispositivo
    # device_type = st.text_input('Tipo de dispositivo:', value="", key='device-type')
    # st.write(f"\nVocê está usando um {device_type}")
    # if device_type == 'mobile':
    #     st.write("Você está usando um dispositivo móvel.")
    # else:
    #     st.write("Você está usando um desktop.")

    # dessa outra maneira tambem nao funcionou, pois o streamlit nao alimentou a sessao com a variavel: st.session_state.user_agent
    # # Obter informações do user agent
    # user_agent = parse(st.session_state.user_agent)
    # st.write(f"\nVocê está usando um {user_agent}")

    # # Verificar se o dispositivo é móvel ou desktop
    # if user_agent.is_mobile:
    #     st.write("Você está usando um dispositivo móvel.")
    # elif user_agent.is_tablet:
    #     st.write("Você está usando um tablet.")
    # else:
    #     st.write("Você está usando um desktop.")

    # # user_agent = st.session_state.user_agent # UserAgent()

    # device_type = 'mobile' if user_agent.is_mobile else 'desktop'

    # esse formato tambem nao funcionou:
    # // Check if the user is accessing the page on a mobile device
    # var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    # if (isMobile) {
    # // User is accessing the page on a mobile device
    # console.log("Mobile device detected");
    # return "mobile";
    # } 
    # // User is accessing the page on a desktop device
    # console.log("Desktop device detected");
    # return "desktop";


    # if (/Mobi|Android/i.test(ua)) {
    #     return 'mobile';
    # }
    # return 'desktop';

    # # JavaScript para detectar o tipo de dispositivo e retornar o resultado
    # funcao_js_a_inserir = """
    # function getdevice_type_js() {
    #         // Check if the user is accessing the page on a mobile device
    #         // var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    #         let isMobile = false;
    #         alert("===> estou na device_type_js ");
    #         (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) isMobile = true;})(navigator.userAgent||navigator.vendor||window.opera);
    #         if (isMobile) {
    #             // User is accessing the page on a mobile device
    #             alert("chicoooo Mobile device detected");
    #             console.log("chicoooo Mobile device detected");
    #             return "mobile";
    #         } 
    #         // User is accessing the page on a desktop device
    #         alert("chicoooo Desktop device detected");
    #         console.log("chicoooo Desktop device detected");
    #         return "desktop";
    # };
    # getdevice_type_js()
    # """

    # # st.markdown(funcao_js_a_inserir, unsafe_allow_html=True)

    # # device_type = st_javascript(funcao_js_a_inserir)
    # # st.markdown(f"getdevice_type_js: {device_type}", unsafe_allow_html=True)

    # # # return_value = st_javascript("""await fetch("http://localhost:85/api/ping").then(function(response) {return response.json();}) """)
    
    # # # return_value = st_javascript(""" () => { return window.location.href; } """)

    # # return_value = st_javascript("""alert('ola ...') """)
    # # st.markdown(f"chico was: {return_value}", unsafe_allow_html=True)


    # # # JavaScript para obter a largura da janela
    # # width_js = """
    # # () => {
    # #     return window.innerWidth;
    # # }
    # # """

    # # # Executando o JavaScript e capturando o retorno
    # # width = st_javascript(width_js)

    # # # Exibindo a largura da janela
    # # st.write(f"A largura da janela é: {width} pixels")

    # # Executando o JavaScript e capturando o retorno
    # st.write(f"O device-type foi: {device_type}")

    # # # #     mobile_pattern = re.compile( r'Android|iPhone|iPod|BlackBerry|IEMobile|Opera Mini', re.I )
    # # mobile_agents = [ "android", "iphone", "blackberry", "mobile", "iemobile", "opera m"]

    # # # Verificar se o user agent corresponde a qualquer um dos agentes móveis
    # # for agent in mobile_agents:
    # #     if agent in navigator_userAgent.lower():
    # #         is_mobile = True
    # #         break

    # # if is_mobile:
    # #     print("Mobile device detected")
    # #     return "mobile"
    # # else:
    # #     print("Desktop device detected")
    # #     return "desktop"

    # # # Exemplo de uso
    # # user_agent_string = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    # # device_type = get_device_type(user_agent_string)
    # # print(f"Device type: {device_type}")



    # # trechos_de_nav_mobiles = re.compile( r'(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-', re.I )
    # # is_mobile = trechos_de_nav_mobiles.match(navigator_userAgent[:4])

    # is_mobile = check_device(navigator_userAgent)
