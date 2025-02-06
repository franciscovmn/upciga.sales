import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import numpy as np
import os
import myfunc
from streamlit_extras.metric_cards import style_metric_cards
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from millify import millify
# st.set_option('deprecation.showPyplotGlobalUse', False)

def app():

    produtos = myfunc.load_produtos(os.path.getmtime('csv/produto.csv'))
    venda_itens = myfunc.load_venda_itens(os.path.getmtime('csv/venda_itens.csv'))
    clientes = myfunc.load_table('csv/cliente.csv')
    venda_cliente_produto = myfunc.load_table('csv/venda.csv')
    # ,'IDSETOR', 'IDVENDEDOR'
    venda_cliente_produto = pd.merge(venda_cliente_produto[['IDPEDIDO','IDCLI','FDATAEMI','HORA','FVAL']], clientes[['IDCLI','NOMECLI','UF','CIDADE']], how='left', left_on='IDCLI', right_on='IDCLI')
    venda_cliente_produto = pd.merge(venda_cliente_produto[['IDPEDIDO','IDCLI','NOMECLI','UF','CIDADE','FDATAEMI']],venda_itens[['IDPEDIDO','PCOD','QTDVENDA','VLVENDA']],on='IDPEDIDO')
    venda_cliente_produto = pd.merge(venda_cliente_produto[['IDPEDIDO','IDCLI','NOMECLI','UF','CIDADE','FDATAEMI','PCOD','QTDVENDA','VLVENDA']],produtos[['PCOD','PREF','PDESC','PUNIDADE']],on='PCOD')

    # Convertendo FDATAEMI para datetime e formatando para dia/mês/ano
    venda_cliente_produto['FDATAEMI'] = pd.to_datetime(venda_cliente_produto['FDATAEMI'], format='%m/%d/%Y')

    # Agrupando e somando os valores de vendas para cada cliente
    # clientes_mais_compra = venda_cliente_produto.groupby(['IDCLI','NOMECLI','UF','CIDADE'])['FVAL'].sum().reset_index()
    # clientes_mais_compra = clientes_mais_compra.sort_values(by='FVAL', ascending=False)

    search_term = st.text_input("CIDADE, NOME OU CODIGO DO CLIENTE:")
    if search_term != "":           # search_term != "" eh o mesmo que: not search_term == "":
        try:
            if ',' in search_term:
                codigos = [int(codigo.strip()) for codigo in search_term.split(',') if codigo.strip().isdigit()]
                venda_cliente_produto = venda_cliente_produto[ venda_cliente_produto['IDCLI'].isin(codigos) ]
            elif search_term.isdigit():
                venda_cliente_produto = venda_cliente_produto[ venda_cliente_produto['IDCLI'] == int(search_term) ]
            else:
                venda_cliente_produto = venda_cliente_produto[ venda_cliente_produto['NOMECLI'].str.contains(search_term, case=False) | venda_cliente_produto['CIDADE'].str.contains(search_term, case=False) ].copy()
        except KeyError:  # Tratar KeyError caso a coluna não exista no DataFrame
            st.write("Erro: Coluna não encontrada. Verifique se os dados estão corretos.")
        except ValueError:  # Tratar ValueError caso a conversão de tipo falhe
            st.write("Erro: Valor inválido. Verifique se os dados estão corretos.")
        except Exception as e:  # Tratar outras exceções genéricas
            st.write(f"Ocorreu um erro: {e}")

    venda_cliente_produto['VLVENDA'] = venda_cliente_produto['VLVENDA'].map(lambda x: f'R$ {x:,.0f}')
    venda_cliente_produto = venda_cliente_produto.sort_values(by=['QTDVENDA', 'VLVENDA'], ascending=False)
    venda_cliente_produto = venda_cliente_produto.rename(columns={'FDATAEMI': 'DATA VENDA', 'IDCLI': 'COD CLIENTE', 'NOMECLI': 'CLIENTE', 'PCOD': 'COD PRODUTO', 'PDESC': 'PRODUTO', 'PUNIDADE': 'UND', 'QTDVENDA': 'QUANTIDADE VENDIDA', 'VLVENDA': 'VENDA', 'PREF': 'REFERENCIA'})

    # Configurando AgGrid para filtrar as colunas de data e texto
    gb = GridOptionsBuilder.from_dataframe(venda_cliente_produto)
    gb.configure_column('DATA VENDA', type=['dateColumnFilter', 'customDateTimeFormat'], custom_format_string='dd/MM/yyyy')
    gb.configure_column('CLIENTE', filter='agTextColumnFilter')
    gb.configure_column('UF', filter='agTextColumnFilter')
    gb.configure_column('CIDADE', filter='agTextColumnFilter')
    gb.configure_column('REFERENCIA', filter='agTextColumnFilter')
    gb.configure_column('PRODUTO', filter='agTextColumnFilter')
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    grid_options = gb.build()

    # Mostra o dataframe com AgGrid e Captura dados filtrados pelo AgGrid
    grid_response = AgGrid(venda_cliente_produto, gridOptions=grid_options, update_mode=GridUpdateMode.FILTERING_CHANGED, use_container_width=True)

    # Converte os dados filtrados no grid para um dataFrame novamente
    venda_cliente_produto_aggrid = pd.DataFrame(grid_response['data'])

    # Atualizar métricas com base nos dados filtrados
    soma_qtd_venda_aggrid = venda_cliente_produto_aggrid['QUANTIDADE VENDIDA'].sum()
    soma_venda_aggrid = venda_cliente_produto_aggrid['VENDA'].replace({'R\$ ': '', ',': ''}, regex=True).astype(float).sum()
    num_vendas_aggrid = venda_cliente_produto_aggrid.shape[0]
    ticket_medio_venda_aggrid = (soma_venda_aggrid / num_vendas_aggrid) if num_vendas_aggrid != 0 else 0

    col = st.columns(3)
    with col[0]:
        st.metric('QUANTIDADE VENDIDA', f'{soma_qtd_venda_aggrid:.0f}')
    with col[1]:
        st.metric('VALOR VENDIDO', f'R${soma_venda_aggrid:,.0f}')
        # st.metric('VALOR VENDIDO', f'R${millify(soma_venda_aggrid,precision=2)}')
    with col[2]:
        st.metric('TICKET MEDIO', f'R${ticket_medio_venda_aggrid:,.0f}')
    
    style_metric_cards(border_radius_px=12, border_left_color='#AA00DD')


    # # soma_qtd_venda = venda_cliente_produto['QTDVENDA'].sum()
    # valor_venda = venda_cliente_produto['VLVENDA'].sum()
    # num_vendas = venda_cliente_produto.shape[0]
    # ticket_medio_venda = valor_venda / num_vendas

    # # Formatando os valores para reais
    # valor_venda = f'R${valor_venda:,.0f}'
    # ticket_medio_venda = f'R${ticket_medio_venda:,.0f}'
    # # quantidade_vendida = f'{soma_qtd_venda:.0f}'
