import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import numpy as np
from plotly.subplots import make_subplots
import os
from streamlit_kpi import streamlit_kpi
import myfunc
from streamlit_extras.metric_cards import style_metric_cards
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from millify import millify
# st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>", unsafe_allow_html=True)
# def set_page_config():
#     st.set_page_config(
#         page_title="Sales Dashboard",
#         page_icon=":bar_chart:",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

def app():
    # Carregando os dados
    # vendedores = myfunc.load_vendedores( os.path.getmtime('csv/vendedores.csv')  ) # print(os.path.getmtime('data/temp/test.txt')) resulta em algo como: 1549094615.9723485
    produtos = myfunc.load_produtos( os.path.getmtime('csv/produto.csv')  ) 
    venda_itens = myfunc.load_venda_itens( os.path.getmtime('csv/venda_itens.csv')  ) 
    clientes = myfunc.load_clientes( os.path.getmtime('csv/clientes.csv')  ) 
    # fornecedores = myfunc.load_fornecedores( os.path.getmtime('csv/fornecedores.csv')  ) 
    vendas = myfunc.load_vendas( os.path.getmtime('csv/venda.csv')  ) 
    # relacao_vendedor = myfunc.load_relacao_vendedor( os.path.getmtime('csv/totvenda_vendedor.csv')  ) 
    relacao_venda_produtos = myfunc.load_relacao_venda_produtos( os.path.getmtime('csv/totvenda_prod.csv')  ) 
    relacao_venda_cliente_vendedor_produto = myfunc.load_relacao_venda_cliente_vendedor_produto( os.path.getmtime('csv/totvenda_cli_prod.csv')  ) 

    # Mesclando as tabelas vendas e clientes
    # venda_cliente = pd.merge(vendas[['IDPEDIDO','IDCLI','FDATAEMI','HORA','FVAL']],clientes[['IDCLI','NOMECLI']],how='left',left_on='IDCLI',right_on='IDCLI')

    def lista_produtos_vendidos():
        # st.title("Venda por produtos")
        st.subheader('Venda por produtos :bar_chart:', divider='rainbow')
        # st.subheader('_Streamlit_ is :blue[cool] :sunglasses:')
        # Criando tabela dos produtos que mais venderam
        produto_mais_venda = venda_itens.groupby('PCOD')[['VLVENDA','QTDVENDA']].sum().reset_index()
        # Localizando os produtos que mais venderam
        produto_mais_venda = produto_mais_venda.sort_values(by='VLVENDA', ascending=False)
        # Selecionando os top 5 produtos que mais venderam
        top_produtos_mais_vendidos = produto_mais_venda.head(5)
        # Agora mesclando para saber o nome dos produtos
        verifica_nome_produtos_vendas = top_produtos_mais_vendidos.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')
        # Criando o gráfico de pizza valor venda
        fig = px.pie(verifica_nome_produtos_vendas, values='VLVENDA', names='PDESC', title='TOP 5 PRODUTOS MAIS VENDIDOS')

        # Unir os dataframes
        vendas_relacao_produtos = pd.merge(produtos[['PCOD','PDESC','PVLUVEN3','PVLUVENDA']],venda_itens[['PCOD','QTDVENDA','VLVENDA']],right_on='PCOD',left_on='PCOD')
        vendas_relacao_produtos = vendas_relacao_produtos.groupby(['PCOD','PDESC','PVLUVEN3','PVLUVENDA'])[['QTDVENDA','VLVENDA']].sum().reset_index()
        vendas_relacao_produtos = vendas_relacao_produtos.sort_values(by='VLVENDA',ascending=False)
        vendas_relacao_produtos['CUSTOCMV'] = vendas_relacao_produtos['PVLUVEN3'] * vendas_relacao_produtos['QTDVENDA']
        vendas_relacao_produtos['MARGEM'] = vendas_relacao_produtos['VLVENDA'] - vendas_relacao_produtos['CUSTOCMV']
        vendas_relacao_produtos['LUCRO'] = ((vendas_relacao_produtos['MARGEM']) / (vendas_relacao_produtos['VLVENDA'])) * 100
        vendas_relacao_produtos['MARKUP'] = (((vendas_relacao_produtos['VLVENDA']) / (vendas_relacao_produtos['CUSTOCMV'])) * 100) -100
        vendas_relacao_produtos = vendas_relacao_produtos[['PCOD','PDESC','QTDVENDA','VLVENDA','CUSTOCMV','MARGEM','LUCRO','MARKUP']]


        # Construção das variaveis
        soma_quantidade = vendas_relacao_produtos['QTDVENDA'].sum()
        soma_valor_venda = vendas_relacao_produtos['VLVENDA'].sum() # R$
        soma_custo_cmv = vendas_relacao_produtos['CUSTOCMV'].sum() # R$
        soma_margem = vendas_relacao_produtos['MARGEM'].sum() # R$
        percentual_lucro_final = (soma_margem / soma_valor_venda) * 100
        percentual_markup_final = ((soma_valor_venda / soma_custo_cmv) * 100) - 100

        # Pesquisa por código ou nome do produto
        search_term = st.text_input("Digite o nome ou código do produto:")

        try:
            # Verifica se o termo de pesquisa contém vírgulas para separar os códigos
            if ',' in search_term:
                # Divide os códigos de produto
                codigos = [int(codigo.strip()) for codigo in search_term.split(',') if codigo.strip().isdigit()]
                # Filtra os dados para incluir apenas os códigos de produto presentes na lista
                filtered_data = vendas_relacao_produtos[vendas_relacao_produtos['PCOD'].isin(codigos)]
            # Filtrar os dados de acordo com o termo de pesquisa
            elif search_term.isdigit():
                # Pesquisa pelo código do produto
                filtered_data = vendas_relacao_produtos[vendas_relacao_produtos['PCOD'] == int(search_term)]
            else:
                # Pesquisa pelo nome do produto
                filtered_data = vendas_relacao_produtos[vendas_relacao_produtos['PDESC'].str.contains(search_term, case=False)]

            # Exibir as métricas
            if search_term == "":
                quantidade = soma_quantidade
                valor_venda = f'R${soma_valor_venda:,.0f}'
                custo_cmv = f'R${soma_custo_cmv:,.0f}'
                margem = f'R${soma_margem:,.0f}'
            else:
                quantidade = filtered_data['QTDVENDA'].sum()
                valor_venda = filtered_data['VLVENDA'].sum()
                custo_cmv = filtered_data['CUSTOCMV'].sum()
                margem = filtered_data['MARGEM'].sum()

                valor_venda = float(valor_venda)
                margem = float(margem)
                custo_cmv = float(custo_cmv)

                percentual_lucro_final = (margem / valor_venda) * 100
                percentual_markup_final = ((valor_venda / custo_cmv) * 100) - 100

                percentual_lucro_final = (margem / valor_venda) * 100
                percentual_markup_final = ((valor_venda / custo_cmv) * 100) - 100

                # Formatando os valores para reais
                valor_venda = f'R${valor_venda:,.0f}'
                margem = f'R${margem:,.0f}'
                custo_cmv = f'R${custo_cmv:,.0f}'
                
        except KeyError:  # Tratar KeyError caso a coluna não exista no DataFrame
            st.write("Erro: Coluna não encontrada. Verifique se os dados estão corretos.")
        except ValueError:  # Tratar ValueError caso a conversão de tipo falhe
            st.write("Erro: Valor inválido. Verifique se os dados estão corretos.")
        except Exception as e:  # Tratar outras exceções genéricas
            st.write(f"Ocorreu um erro: {e}")
            
        percentual_lucro_final = f'{percentual_lucro_final:.0f}%'
        percentual_markup_final = f'{percentual_markup_final:.0f}%'

        # Formatação dos dados
        filtered_data['VLVENDA'] = filtered_data['VLVENDA'].map(lambda x: f'R$ {x:,.0f}')
        filtered_data['CUSTOCMV'] = filtered_data['CUSTOCMV'].map(lambda x: f'R$ {x:,.0f}')
        filtered_data['MARGEM'] = filtered_data['MARGEM'].map(lambda x: f'R$ {x:,.0f}')
        filtered_data['LUCRO'] = filtered_data['LUCRO'].map(lambda x: f'{x:,.0f}%')
        filtered_data['MARKUP'] = filtered_data['MARKUP'].map(lambda x: f'{x:,.0f}%')

        # Renomear as colunas
        filtered_data_r = filtered_data.rename(columns={'PCOD': 'CODIGO', 'PDESC': 'DESCRIÇÃO', 'QTDVENDA': 'QUANTIDADE', 'VLVENDA': 'VENDA'})

        # Configuração do AgGrid para filtragem
        gb = GridOptionsBuilder.from_dataframe(filtered_data_r)
        gb.configure_column('DESCRIÇÃO', filter='agTextColumnFilter')
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        grid_options = gb.build()

        grid_response = AgGrid(filtered_data_r, gridOptions=grid_options, update_mode=GridUpdateMode.FILTERING_CHANGED, use_container_width=True)

        filtered_data_aggrid = pd.DataFrame(grid_response['data'])

        # Atualizar métricas com base nos dados filtrados
        soma_quantidade_aggrid = filtered_data_aggrid['QUANTIDADE'].sum()
        soma_valor_venda_aggrid = filtered_data_aggrid['VENDA'].replace({'R\$ ': '', ',': ''}, regex=True).astype(float).sum()
        soma_custo_cmv_aggrid = filtered_data_aggrid['CUSTOCMV'].replace({'R\$ ': '', ',': ''}, regex=True).astype(float).sum()
        soma_margem_aggrid = filtered_data_aggrid['MARGEM'].replace({'R\$ ': '', ',': ''}, regex=True).astype(float).sum()
        percentual_lucro_final_aggrid = (soma_margem_aggrid / soma_valor_venda_aggrid) * 100 if soma_valor_venda_aggrid != 0 else 0
        percentual_markup_final_aggrid = ((soma_valor_venda_aggrid / soma_custo_cmv_aggrid) * 100) - 100 if soma_custo_cmv_aggrid != 0 else 0

        cols = st.columns(4)
        with cols[0]:
            st.metric('Valor VENDA', f'R${millify(soma_valor_venda_aggrid,precision=2)}')
        with cols[1]:
            st.metric('Custo CMV', f'R${millify(soma_custo_cmv_aggrid,precision=2)}')
        with cols[2]:
            st.metric('Margem', f'R${millify(soma_margem_aggrid,precision=2)}')
        with cols[3]:
            st.metric('Quantidade',f'{soma_quantidade_aggrid:.0f}')

        cols = st.columns(4)
        with cols[0]:
            st.metric('LUCRO', f'{percentual_lucro_final_aggrid:.0f}%')
        with cols[1]:
            st.metric('MARKUP', f'{percentual_markup_final_aggrid:.0f}%')
        style_metric_cards(border_radius_px=12, border_left_color='#AA00DD')

        # # Renomear as colunas
        # filtered_data_r = filtered_data.rename(columns={'PCOD': 'CODIGO','PDESC':'DESCRIÇÃO', 'QTDVENDA': 'QUANTIDADE','VLVENDA':'VENDA'})

        # AgGrid(filtered_data_r,use_container_width=True)
        # # Exibir os dados filtrados


    def top_produtos_mais_vendidos():
        # Mesclando as tabelas vendas e clientes
        venda_cliente = pd.merge(vendas[['FLOJA','IDPEDIDO','IDCLI','SI_CAIXA','FDATAEMI','HORA','FVAL']],clientes[['IDCLI','NOMECLI']],how='left',left_on='IDCLI',right_on='IDCLI')
        venda_cliente.rename(columns= {'NOMEFORN': 'NOMECLI'},inplace=True)

        # Substituindo NaN por Consumidor Final
        venda_cliente['NOMECLI'].fillna('Consumidor Final', inplace=True)

        # Criando tabela dos produtos que mais venderam
        produto_mais_venda = venda_itens.groupby('PCOD')[['VLVENDA','QTDVENDA']].sum().reset_index()

        # Localizando os produtos que mais venderam
        produto_mais_venda = produto_mais_venda.sort_values(by='VLVENDA', ascending=False)

        # Selecionando os top 5 produtos que mais venderam
        top_produtos_mais_vendidos = produto_mais_venda.head(5)
        # Agora mesclando para saber o nome dos produtos
        verifica_nome_produtos_vendas = top_produtos_mais_vendidos.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')

        # Criando o gráfico de pizza valor venda
        fig = px.pie(verifica_nome_produtos_vendas, values='VLVENDA', names='PDESC', title='TOP 5 PRODUTOS MAIS VENDIDOS')

        # Criando a tabela que vai ficar os dados do codigo que teve mais unidades vendidas
        produto_mais_venda_qtd = venda_itens.groupby('PCOD')[['QTDVENDA','VLVENDA']].sum().reset_index()

        # Localizando os produtos que mais sairam em quantidade
        produto_mais_venda_qtd = produto_mais_venda_qtd.sort_values(by='QTDVENDA', ascending=False)

        # Selecionando os top 5 produtos que mais venderam
        top_produtos_mais_vendidos_qtd = produto_mais_venda_qtd.head(5)

        # Agora mesclando para saber o nome dos produtos
        verifica_nome_produtos_vendas_qtd = top_produtos_mais_vendidos_qtd.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')

        # Criando o gráfico de pizza qtd
        fig_qtd = px.pie(verifica_nome_produtos_vendas_qtd, values='QTDVENDA', names='PDESC', title='TOP 5 PRODUTOS QUE MAIS FORAM VENDIDOS')

        # Adicionando o selectbox para o usuário escolher entre top 5, 10 ou 20
        selected_option = st.selectbox("Selecione a quantidade de produtos mais vendidos:",
                                        ["Top 5", "Top 10", "Top 20"])

        # Determinando o número de produtos a serem exibidos com base na seleção do usuário
        if selected_option == "Top 5":
            top_produtos = 5
        elif selected_option == "Top 10":
            top_produtos = 10
        else:
            top_produtos = 20

        # Redefinindo as variáveis com base na escolha do usuário
        top_produtos_mais_vendidos = produto_mais_venda.head(top_produtos)
        top_produtos_mais_vendidos_qtd = produto_mais_venda_qtd.head(top_produtos)

        # Atualizando os gráficos com as novas informações
        verifica_nome_produtos_vendas = top_produtos_mais_vendidos.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')
        verifica_nome_produtos_vendas_qtd = top_produtos_mais_vendidos_qtd.merge(produtos[['PCOD', 'PDESC', 'PUNIDADE', 'PVLUVENDA' , 'PVLUVEN3']], on='PCOD')

        # Passo 1: Extrair os dois primeiros e os dois últimos nomes
        def get_short_desc(desc):
            words = desc.split()
            if len(words) <= 4:
                return desc
            else:
                return ' '.join(words[:2] + words[-2:])

        verifica_nome_produtos_vendas['PDESC_SHORT'] = verifica_nome_produtos_vendas['PDESC'].apply(get_short_desc)
        verifica_nome_produtos_vendas_qtd['PDESC_SHORT'] = verifica_nome_produtos_vendas_qtd['PDESC'].apply(get_short_desc)

        # Passo 2: Atualizar os gráficos para usar a nova coluna
        if selected_option == "Top 5":
            fig = px.bar(verifica_nome_produtos_vendas, x='VLVENDA', y='PDESC_SHORT', orientation='h', title=f'TOP {top_produtos} PRODUTOS EM VALOR DE VENDA')
            fig_qtd = px.bar(verifica_nome_produtos_vendas_qtd, x='QTDVENDA', y='PDESC_SHORT', orientation='h', title=f'TOP {top_produtos} PRODUTOS EM QUANTIDADES')
        else:
            fig = px.bar(verifica_nome_produtos_vendas, y='PDESC_SHORT', x='VLVENDA', orientation='h', title=f'TOP {top_produtos} PRODUTOS EM VALOR DE VENDA')
            fig_qtd = px.bar(verifica_nome_produtos_vendas_qtd, y='PDESC_SHORT', x='QTDVENDA', orientation='h', title=f'TOP {top_produtos} PRODUTOS EM QUANTIDADES')

        # Resetar o índice de verifica_nome_produtos_vendas
        verifica_nome_produtos_vendas.reset_index(drop=True, inplace=True)

        # Formatar 'VLVENDA' para moeda brasileira real
        verifica_nome_produtos_vendas['VLVENDA'] = verifica_nome_produtos_vendas['VLVENDA'].map(lambda x: f'R${x:,.0f}')
        verifica_nome_produtos_vendas['PVLUVENDA'] = verifica_nome_produtos_vendas['PVLUVENDA'].map(lambda x: f'R${x:,.0f}')

        # Selecione as colunas relevantes para verifica_nome_produtos_vendas_qtd
        verifica_nome_produtos_vendas_qtd = verifica_nome_produtos_vendas_qtd[['PCOD', 'PDESC', 'QTDVENDA', 'VLVENDA']]
        verifica_nome_produtos_vendas = verifica_nome_produtos_vendas[['PCOD', 'PDESC', 'VLVENDA', 'QTDVENDA']]

        verifica_nome_produtos_vendas_qtd['VLVENDA'] = verifica_nome_produtos_vendas_qtd['VLVENDA'].map(lambda x: f'R${x:,.0f}')

        # Renomear colunas
        verifica_nome_produtos_vendas = verifica_nome_produtos_vendas.rename(columns={'PCOD': 'CODIGO', 'PDESC': 'NOME', 'VLVENDA': 'SOMA VENDAS', 'QTDVENDA': 'QUANTIDADE VENDIDA'})
        verifica_nome_produtos_vendas_qtd = verifica_nome_produtos_vendas_qtd.rename(columns={'PCOD': 'CODIGO', 'PDESC': 'NOME', 'VLVENDA': 'SOMA VENDAS', 'QTDVENDA': 'QUANTIDADE VENDIDA'})
        

        gb = GridOptionsBuilder.from_dataframe(verifica_nome_produtos_vendas)
        gq = GridOptionsBuilder.from_dataframe(verifica_nome_produtos_vendas_qtd)
        gb.configure_default_column(filterable=True)
        gq.configure_default_column(filterable=True)
        gb.configure_column("NOME", filter="agTextColumnFilter")
        gq.configure_column("NOME", filter="agTextColumnFilter")
        grid_options = gb.build()
        grid_optionsq = gq.build()
     
        cols = st.columns(2)
        with cols[0]:
            st.plotly_chart(fig,use_container_width=True)
            AgGrid(verifica_nome_produtos_vendas, gridOptions=grid_options, use_container_width=True)
        with cols[1]:
            st.plotly_chart(fig_qtd,use_container_width=True)
            AgGrid(verifica_nome_produtos_vendas_qtd, gridOptions=grid_optionsq, use_container_width=True)
    def produtos_em_alta():
        produtos_alta = pd.merge(relacao_venda_produtos[['PCOD','QTDVENDA','MVALOR3','VLVENDA','TENDENCIA','QP_AMAIS','QP_AMENOS','V_AMAIS','V_AMENOS']],produtos[['PCOD','PDESC','PUNIDADE','PVLUVENDA','SALDO','PREF']],on='PCOD')

        produtos_clientes_alta = pd.merge(relacao_venda_cliente_vendedor_produto[['IDCLI','PCOD','QTDVENDA','VLVENDA','QP_AMAIS','QP_AMENOS','V_AMAIS','V_AMENOS']],produtos_alta[['PCOD','PDESC','PREF']],on='PCOD')
        produtos_clientes_alta = pd.merge(produtos_clientes_alta[['IDCLI','QP_AMAIS','QP_AMENOS','QTDVENDA','VLVENDA','PCOD','PDESC','PREF','V_AMAIS','V_AMENOS']],clientes[['IDCLI','NOMECLI','CIDADE']],on='IDCLI')
        produtos_clientes_alta = produtos_clientes_alta[['IDCLI','NOMECLI','CIDADE','PCOD','PDESC','QP_AMAIS','V_AMAIS','QP_AMENOS','V_AMENOS','QTDVENDA','VLVENDA','PREF']]

        opcoes_selecionadas = st.selectbox("Selecione uma opção:", ["Produto em alta que foi recomprado", "Produto que foi reativado (não estava sendo vendido)"])

        # Filtro baseado na opção selecionada
        #if opcoes_selecionadas == "Produto em alta que foi recomprado":
        #    filtro_tendencia = produtos_alta['TENDENCIA'] == "2"
        #else:
        #    filtro_tendencia = produtos_alta['TENDENCIA'] == "3"


        filtro_tendencia = produtos_alta['TENDENCIA'] == ("2" if opcoes_selecionadas == "Produto em alta que foi recomprado" else "3")
        produtos_filtrados = produtos_alta[filtro_tendencia]

        # organizando as variaveis
        produtos_filtrados['MARGEM'] = produtos_filtrados['VLVENDA'] - produtos_filtrados['MVALOR3']
        produtos_filtrados['LUCRO'] = ((produtos_filtrados['MARGEM']) / (produtos_filtrados['VLVENDA'])) * 100
        # Construção das variaveis
        soma_quantidade_amais = produtos_filtrados['QP_AMAIS'].sum()
        soma_quantidade_menos = produtos_filtrados['QP_AMENOS'].sum()
        soma_valor_venda_amais = produtos_filtrados['V_AMAIS'].sum() # R$
        soma_valor_venda_menos = produtos_filtrados['V_AMENOS'].sum() # R$
        soma_custo = produtos_filtrados['MVALOR3'].sum()
        soma_margem = (produtos_filtrados['VLVENDA'].sum()) - soma_custo
        soma_valor_venda = produtos_filtrados['VLVENDA'].sum()
        lucro_final = soma_valor_venda - soma_custo
        produtos_filtrados = produtos_filtrados[['PCOD','PDESC','PUNIDADE','VLVENDA','QTDVENDA','QP_AMAIS','V_AMAIS','QP_AMENOS','V_AMENOS','TENDENCIA','PVLUVENDA','MVALOR3','SALDO','MARGEM','LUCRO','PREF']]

        # Pesquisa por código ou nome do produto
        search_term = st.text_input("Digite o nome, referencia ou código do produto:")

        try:
            # Verifica se o termo de pesquisa contém vírgulas para separar os códigos
            if ',' in search_term:
                # Divide os códigos de produto
                codigos = [int(codigo.strip()) for codigo in search_term.split(',') if codigo.strip().isdigit()]
                # Filtra os dados para incluir apenas os códigos de produto presentes na lista
                produtos_filtrados_cliente = produtos_clientes_alta[produtos_clientes_alta['PCOD'].isin(codigos)]
                produtos_filtrados = produtos_filtrados[produtos_filtrados['PCOD'].isin(codigos)]
            elif search_term.isdigit():
                # Pesquisa por um único código de produto
                produtos_filtrados = produtos_filtrados[produtos_filtrados['PCOD'] == int(search_term)]
                produtos_filtrados_cliente = produtos_clientes_alta[produtos_clientes_alta['PCOD'] == int(search_term)]
            else:
                # Pesquisa pelo nome do produto
                produtos_filtrados = produtos_filtrados[produtos_filtrados['PDESC'].str.contains(search_term, case=False) | produtos_filtrados['PREF'].str.contains(search_term, case=False)].copy()
                produtos_filtrados_cliente = produtos_clientes_alta[produtos_clientes_alta['PDESC'].str.contains(search_term, case=False) | produtos_clientes_alta['PREF'].str.contains(search_term, case=False)].copy()

            # Exibir as métricas
            if search_term == "":
                quantidade_amais = f'{soma_quantidade_amais:.2f}'
                quantidade_menos = f'{soma_quantidade_menos:.2f}'
                valor_venda_amais = f'R${soma_valor_venda_amais:,.2f}'
                valor_venda_menos = f'R${soma_valor_venda_menos:,.2f}'
                custo= f'R${soma_custo:,.2f}'
                margem = f'R${soma_margem:,.2f}'
                valor_venda = f'R${soma_valor_venda:,.2f}'
                lucro_final_i = f'R${lucro_final:,.2f}'
            else:
                quantidade_amais = produtos_filtrados['QP_AMAIS'].sum()
                quantidade_menos = produtos_filtrados['QP_AMENOS'].sum()
                valor_venda_amais = produtos_filtrados['V_AMAIS'].sum()
                valor_venda_menos = produtos_filtrados['V_AMENOS'].sum()
                custo = produtos_filtrados['MVALOR3'].sum()
                margem = produtos_filtrados['MARGEM'].sum()
                valor_venda = produtos_filtrados['VLVENDA'].sum()

                lucro_final_i = valor_venda - custo

                quantidade_amais = f'{quantidade_amais:.2f}'
                quantidade_menos = f'{quantidade_menos:.2f}'
                valor_venda_amais = f'R${valor_venda_amais:,.2f}'
                valor_venda_menos = f'R${valor_venda_menos:,.2f}'
                custo= f'R${custo:,.2f}'
                margem = f'R${margem:,.2f}'
                valor_venda = f'R${valor_venda:,.2f}'
                lucro_final_i = f'R${lucro_final_i:,.2f}'

        except KeyError:  # Tratar KeyError caso a coluna não exista no DataFrame
            st.write("Erro: Coluna não encontrada. Verifique se os dados estão corretos.")
        except ValueError:  # Tratar ValueError caso a conversão de tipo falhe
            st.write("Erro: Valor inválido. Verifique se os dados estão corretos.")
        except Exception as e:  # Tratar outras exceções genéricas
            st.write(f"Ocorreu um erro: {e}")


        produtos_filtrados = produtos_filtrados.sort_values(by=['QP_AMAIS','V_AMAIS'],ascending=False)
        # Configurando AgGrid para filtrar as colunas de data e texto
        gb = GridOptionsBuilder.from_dataframe(produtos_filtrados)
        gb.configure_column('PDESC', filter='agTextColumnFilter')
        gb.configure_column('PUNIDADE', filter='agTextColumnFilter')
        gb.configure_column('PREF', filter='agTextColumnFilter')
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        grid_options = gb.build()

        # Capturar dados filtrados pelo AgGrid
        grid_response = AgGrid(produtos_filtrados, gridOptions=grid_options, update_mode=GridUpdateMode.FILTERING_CHANGED, use_container_width=True)

        # Dados filtrados
        filtered_data_aggrid = pd.DataFrame(grid_response['data'])

        # Atualizar métricas com base nos dados filtrados
        quantidade_amais_aggrid = filtered_data_aggrid['QP_AMAIS'].sum()
        quantidade_amenos_aggrid = filtered_data_aggrid['QP_AMENOS'].sum()
        soma_venda_amais_aggrid = filtered_data_aggrid['V_AMAIS'].replace({'R\$ ': '', ',': ''}, regex=True).astype(float).sum()
        soma_venda_amenos_aggrid = filtered_data_aggrid['V_AMENOS'].replace({'- R\$ ': '', ',': ''}, regex=True).astype(float).sum()

        cols = st.columns(2)
        with cols[0]:
            st.metric("QUANTIDADES VENDIDA A MAIS",f'{quantidade_amais_aggrid:.0f}')
            st.metric("VALOR VENDIDO A MAIS", f'R$ {millify(soma_venda_amais_aggrid,precision=2)}')
        with cols[1]:
            st.metric("QUANTIDADES VENDIDAS A MENOS",f'{quantidade_amenos_aggrid:.0f}')
            st.metric("VALOR VENDIDO A MENOS",f'R$ {millify(soma_venda_amenos_aggrid,precision=2)}')

        cols_o = st.columns(2)
        with cols_o[0]:
            st.metric("LUCRO EM REAIS", lucro_final_i)
        style_metric_cards(border_radius_px=12, border_left_color='#AA00DD')
        st.title('RELACAO DE COMPRA DO(S) PRODUTO(S) PELOS CLIENTES EM CADASTRO ATIVO')

        # Dividindo os dados em duas tabelas: uma para valores "a mais" e outra para valores "a menos"
        produtos_amais = produtos_filtrados_cliente[['IDCLI','NOMECLI','CIDADE','PCOD','PDESC','QP_AMAIS','V_AMAIS','QTDVENDA','VLVENDA','PREF']]
        produtos_menos = produtos_filtrados_cliente[['IDCLI','NOMECLI','CIDADE','PCOD','PDESC','QP_AMENOS','V_AMENOS','QTDVENDA','VLVENDA','PREF']]

        # Formatação dos dados para as duas tabelas
        produtos_amais['V_AMAIS'] = produtos_amais['V_AMAIS'].map(lambda x: f'R$ {x:,.2f}')
        produtos_amais['VLVENDA'] = produtos_amais['VLVENDA'].map(lambda x: f'R$ {x:,.2f}')
        produtos_menos['V_AMENOS'] = produtos_menos['V_AMENOS'].map(lambda x: f'R$ {x:,.2f}')
        produtos_menos['VLVENDA'] = produtos_menos['VLVENDA'].map(lambda x: f'R$ {x:,.2f}')

        # Exibindo as duas tabelas
        st.subheader("Produtos Vendidos a Mais:")
        st.dataframe(produtos_amais, use_container_width=True)

        st.subheader("Produtos Vendidos a Menos:")
        st.dataframe(produtos_menos, use_container_width=True)
    def produtos_em_queda():
        st.title('CLIENTE RECOMPROU, MAS COMPROU MENOS QUE NO PERIODO ANTERIOR')
        produtos_queda = pd.merge(relacao_venda_produtos[['PCOD','QTDVENDA','MVALOR3','VLVENDA','TENDENCIA','QP_AMAIS','QP_AMENOS','V_AMAIS','V_AMENOS']],produtos[['PCOD','PDESC','PUNIDADE','PVLUVENDA','SALDO','PREF']],on='PCOD')
        produtos_clientes_queda = pd.merge(relacao_venda_cliente_vendedor_produto[['IDCLI','PCOD','QTDVENDA','VLVENDA','QP_AMAIS','QP_AMENOS','V_AMAIS','V_AMENOS']],produtos_queda[['PCOD','PDESC','PREF']],on='PCOD')
        produtos_clientes_queda = pd.merge(produtos_clientes_queda[['IDCLI','QP_AMAIS','QP_AMENOS','QTDVENDA','VLVENDA','PCOD','PDESC','PREF','V_AMAIS','V_AMENOS']],clientes[['IDCLI','NOMECLI','CIDADE']],on='IDCLI')
        produtos_clientes_queda = produtos_clientes_queda[['IDCLI','NOMECLI','CIDADE','PCOD','PDESC','QP_AMAIS','V_AMAIS','QP_AMENOS','V_AMENOS','QTDVENDA','VLVENDA','PREF']]
        
        filtro_tendencia_queda = produtos_queda['TENDENCIA'] == "1"
        produtos_filtrados_e = produtos_queda[filtro_tendencia_queda]
        
            # organizando as variaveis
        produtos_filtrados_e['MARGEM'] = produtos_filtrados_e['VLVENDA'] - produtos_filtrados_e['MVALOR3']
        produtos_filtrados_e['LUCRO'] = ((produtos_filtrados_e['MARGEM']) / (produtos_filtrados_e['VLVENDA'])) * 100
        # Construção das variaveis
        soma_quantidade_amais = produtos_filtrados_e['QP_AMAIS'].sum()
        soma_quantidade_menos = produtos_filtrados_e['QP_AMENOS'].sum()
        soma_valor_venda_amais = produtos_filtrados_e['V_AMAIS'].sum() # R$
        soma_valor_venda_menos = produtos_filtrados_e['V_AMENOS'].sum() # R$
        soma_custo = produtos_filtrados_e['MVALOR3'].sum()
        soma_margem = (produtos_filtrados_e['VLVENDA'].sum()) - soma_custo
        soma_valor_venda = produtos_filtrados_e['VLVENDA'].sum()
        lucro_final = soma_valor_venda - soma_custo
        produtos_filtrados_e = produtos_filtrados_e[['PCOD','PDESC','PUNIDADE','VLVENDA','QTDVENDA','QP_AMAIS','V_AMAIS','QP_AMENOS','V_AMENOS','TENDENCIA','PVLUVENDA','MVALOR3','SALDO','MARGEM','LUCRO','PREF']]

        # Pesquisa por código ou nome do produto
        search_term = st.text_input("Digite o nome, referencia ou código do produto:")
        try:
            # Verifica se o termo de pesquisa contém vírgulas para separar os códigos
            if ',' in search_term:
                # Divide os códigos de produto
                codigos = [int(codigo.strip()) for codigo in search_term.split(',') if codigo.strip().isdigit()]
                # Filtra os dados para incluir apenas os códigos de produto presentes na lista
                produtos_filtrados_cliente = produtos_clientes_queda[produtos_clientes_queda['PCOD'].isin(codigos)]
                produtos_filtrados_e = produtos_filtrados_e[produtos_filtrados_e['PCOD'].isin(codigos)]
            elif search_term.isdigit():
                # Pesquisa por um único código de produto
                produtos_filtrados_e = produtos_filtrados_e[produtos_filtrados_e['PCOD'] == int(search_term)]
                produtos_filtrados_cliente = produtos_clientes_queda[produtos_clientes_queda['PCOD'] == int(search_term)]
            else:
                # Pesquisa pelo nome do produto
                produtos_filtrados_e = produtos_filtrados_e[produtos_filtrados_e['PDESC'].str.contains(search_term, case=False) | produtos_filtrados_e['PREF'].str.contains(search_term, case=False)].copy()
                produtos_filtrados_cliente = produtos_clientes_queda[produtos_clientes_queda['PDESC'].str.contains(search_term, case=False) | produtos_clientes_queda['PREF'].str.contains(search_term, case=False)].copy()

            # Exibir as métricas
            if search_term == "":
                quantidade_amais = f'{soma_quantidade_amais:.0f}'
                quantidade_menos = f'{soma_quantidade_menos:.0f}'
                valor_venda_amais = f'R${soma_valor_venda_amais:,.0f}'
                valor_venda_menos = f'R${soma_valor_venda_menos:,.0f}'
                custo= f'R${soma_custo:,.0f}'
                margem = f'R${soma_margem:,.0f}'
                valor_venda = f'R${soma_valor_venda:,.0f}'
                lucro_final_i = f'R${lucro_final:,.0f}'
            else:
                quantidade_amais = produtos_filtrados_e['QP_AMAIS'].sum()
                quantidade_menos = produtos_filtrados_e['QP_AMENOS'].sum()
                valor_venda_amais = produtos_filtrados_e['V_AMAIS'].sum()
                valor_venda_menos = produtos_filtrados_e['V_AMENOS'].sum()
                custo = produtos_filtrados_e['MVALOR3'].sum()
                margem = produtos_filtrados_e['MARGEM'].sum()
                valor_venda = produtos_filtrados_e['VLVENDA'].sum()

                lucro_final_i = valor_venda - custo

                quantidade_amais = f'{quantidade_amais:.0f}'
                quantidade_menos = f'{quantidade_menos:.0f}'
                valor_venda_amais = f'R${valor_venda_amais:,.0f}'
                valor_venda_menos = f'R${valor_venda_menos:,.0f}'
                custo= f'R${custo:,.0f}'
                margem = f'R${margem:,.0f}'
                valor_venda = f'R${valor_venda:,.0f}'
                lucro_final_i = f'R${lucro_final_i:,.0f}'

        except KeyError:  # Tratar KeyError caso a coluna não exista no DataFrame
            st.write("Erro: Coluna não encontrada. Verifique se os dados estão corretos.")
        except ValueError:  # Tratar ValueError caso a conversão de tipo falhe
            st.write("Erro: Valor inválido. Verifique se os dados estão corretos.")
        except Exception as e:  # Tratar outras exceções genéricas
            st.write(f"Ocorreu um erro: {e}")

        # Formatação dos dados
        produtos_filtrados_e['PCOD'] = produtos_filtrados_e['PCOD'].map(str)
        produtos_filtrados_e['VLVENDA'] = produtos_filtrados_e['VLVENDA'].map(lambda x: f'R$ {x:,.2f}')
        produtos_filtrados_e['V_AMAIS'] = produtos_filtrados_e['V_AMAIS'].map(lambda x: f'R$ {x:,.2f}')
        produtos_filtrados_e['V_AMENOS'] = produtos_filtrados_e['V_AMENOS'].map(lambda x: f'R$ {x:,.2f}')
        produtos_filtrados_e['MVALOR3'] = produtos_filtrados_e['MVALOR3'].map(lambda x: f'R$ {x:,.2f}')
        produtos_filtrados_e['MARGEM'] = produtos_filtrados_e['MARGEM'].map(lambda x: f'R$ {x:,.2f}')
        produtos_filtrados_e['LUCRO'] = produtos_filtrados_e['LUCRO'].map(lambda x: f'{x:,.2f}%')

        produtos_filtrados_e = produtos_filtrados_e.sort_values(by=['QP_AMAIS','V_AMAIS'],ascending=False)
        # permitindo o filto pela coluna
        available_columns = produtos_filtrados_e.columns.tolist()
        default_columns = ['PCOD','PDESC','PUNIDADE','VLVENDA','QTDVENDA','QP_AMAIS','V_AMAIS','QP_AMENOS','V_AMENOS','TENDENCIA','PVLUVENDA','MVALOR3','SALDO','MARGEM','LUCRO','PREF']
        default_columns = [col for col in default_columns if col in available_columns]
        showData = st.multiselect('Filter: ', available_columns, default=default_columns)
        st.dataframe(produtos_filtrados_e[showData], use_container_width=True)
        
        cols = st.columns(2)
        with cols[0]:
            ui.metric_card(title="QUANTIDADES VENDIDA A MAIS", content=f'{quantidade_amais}', description="SOMA DAS QUANTIDADES VENDIDAS A MAIS QUE O BIMESTREA PASSADO", key="card1")
            ui.metric_card(title="VALOR VENDIDO A MAIS", content=f'{valor_venda_amais}', description="SOMA DO VALOR VENDIDO A MAIS QUE O BIMESTREA PASSADO", key="card2")
        with cols[1]:
            ui.metric_card(title="QUANTIDADES VENDIDAS A MENOS", content=f'{quantidade_menos}', description="SOMA DAS QUANTIDADES VENDIDAS A MENOS QUE O BIMESTRE PASSADO", key="card3")
            ui.metric_card(title="VALOR VENDIDO A MENOS", content=f'{valor_venda_menos}', description="SOMA DO VALOR VENDIDO A MAIS QUE O BIMESTREA PASSADO", key="card4")
        cols_o = st.columns(2)
        with cols_o[0]:
            ui.metric_card(title="LUCRO EM REAIS", content=f'{lucro_final_i}', description="SOMA DO VALOR DE COMPRA", key="card5")

        # CLIENTES --------------------------------
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.title('RELACAO DE COMPRA DO(S) PRODUTO(S) PELOS CLIENTES EM CADASTRO ATIVO')

        # Dividindo os dados em duas tabelas: uma para valores "a mais" e outra para valores "a menos"
        produtos_amais = produtos_filtrados_cliente[['IDCLI','NOMECLI','CIDADE','PCOD','PDESC','QP_AMAIS','V_AMAIS','QTDVENDA','VLVENDA','PREF']]
        produtos_menos = produtos_filtrados_cliente[['IDCLI','NOMECLI','CIDADE','PCOD','PDESC','QP_AMENOS','V_AMENOS','QTDVENDA','VLVENDA','PREF']]

        # Formatação dos dados para as duas tabelas
        produtos_amais['V_AMAIS'] = produtos_amais['V_AMAIS'].map(lambda x: f'R$ {x:,.2f}')
        produtos_amais['VLVENDA'] = produtos_amais['VLVENDA'].map(lambda x: f'R$ {x:,.2f}')
        produtos_menos['V_AMENOS'] = produtos_menos['V_AMENOS'].map(lambda x: f'R$ {x:,.2f}')
        produtos_menos['VLVENDA'] = produtos_menos['VLVENDA'].map(lambda x: f'R$ {x:,.2f}')

        # Exibindo as duas tabelas
        st.subheader("Produtos Vendidos a Mais:")
        st.dataframe(produtos_amais, use_container_width=True)

        st.subheader("Produtos Vendidos a Menos:")
        st.dataframe(produtos_menos, use_container_width=True)

    # SIDEBAR
    st.sidebar.header('ANÁLISES DAS VENDAS')
    option = st.sidebar.selectbox('Escolha uma opção', ['PRODUTOS VENDIDOS', 'TOP PRODUTOS VENDIDOS','PRODUTOS EM ALTA','PRODUTOS EM QUEDA'])
    st.title('')
    if option == 'PRODUTOS VENDIDOS':
        lista_produtos_vendidos()
    elif option == 'TOP PRODUTOS VENDIDOS':
        top_produtos_mais_vendidos()
    elif option == 'PRODUTOS EM ALTA':
        produtos_em_alta()
    elif option == 'PRODUTOS EM QUEDA':
        produtos_em_queda()
