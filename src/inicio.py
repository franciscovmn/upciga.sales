import streamlit as st
import myfunc   # from myfunc import load_table, mostra_progress_bar_venda_meta, mostra_grafico_barras_e_pizza

# st.set_option('deprecation.showPyplotGlobalUse', False)

# def app( df_totais_empresa, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf, clientes, setores, segmentos, vendedores ):
def app( self ):

    def tela_inicial():
        cTituloDaVendaGeral = f'Vendas de {st.session_state.sys_usuario} (Cod{st.session_state.idvendedor}) :bar_chart:' if st.session_state.grupo == 'vendedor' else 'Totais Gerais das Vendas :bar_chart:'
        if st.session_state.grupo == 'vendedor':
            # st.subheader(f'Vendas de {st.session_state.sys_usuario} (Cod{st.session_state.idvendedor}) :bar_chart:', divider='rainbow')
            venda_total = self.df_totais_por_vendedores['FVAL'].sum() 
            meta_total = self.df_totais_por_vendedores['V_META'].sum() 
        else:
            # st.subheader('Totais Gerais das Vendas :bar_chart:', divider='rainbow')
            venda_total = df_totais_empresa['FVAL'].sum() 
            meta_total = df_totais_empresa['V_META'].sum() 

        cFiltrosAplicados = myfunc.get_filtros_ativos()
        if cFiltrosAplicados != '':
            venda_total_com_filtros = self.df_totais_por_clientes['FVAL'].sum() 
            meta_total_com_filtros = self.df_totais_por_clientes['V_META'].sum() 
            col1, col2= st.columns([0.5,0.5])   # Divide a tela em duas colunas
            with col1:
                with st.container(border=True):
                    st.subheader( f"{cFiltrosAplicados}:" + ' :bar_chart:', divider='rainbow')
                    myfunc.mostra_progress_bar_venda_meta(venda_total_com_filtros, meta_total_com_filtros)
            with col2:
                with st.container(border=True):
                    st.subheader(cTituloDaVendaGeral, divider='rainbow')
                    myfunc.mostra_progress_bar_venda_meta(venda_total, meta_total)                
        else:
            st.subheader(cTituloDaVendaGeral, divider='rainbow')
            myfunc.mostra_progress_bar_venda_meta(venda_total, meta_total)


        if st.session_state.grupo != 'vendedor':
            vendedores_com_vendas = self.df_totais_por_vendedores[ self.df_totais_por_vendedores['FVAL'] > 0 ]
            myfunc.mostra_grafico_barras_e_pizza(vendedores_com_vendas, 'FVAL', 'NOME', "Vendedores", 0, "NOME OU CODIGO(s) DOS VENDEDORES:", "Ex: 12, 13 ou JOAO ou 15", "Informe UM codigo de vendedor, ou ALGUNS codigos, ou PARTE DO NOME de um vendedor", 'IDVENDEDOR', 'NOME', 'brw_df_totais_por_vendedores' )
            # my_bar.progress(95)

        myfunc.mostra_grafico_barras_e_pizza(self.df_totais_por_setores, 'FVAL', 'NOME', "Setores", 0, "NOME OU CODIGO(s) DO(s) SETOR(es):", "Ex: 2, 3 ou CARIRI ou 1", "Informe UM codigo de Setor, ou ALGUNS codigos, ou PARTE DO NOME de um setor", 'IDSETOR', 'NOME', 'brw_df_totais_por_setores' )
        # my_bar.progress(96)
        myfunc.mostra_grafico_barras_e_pizza(self.df_totais_por_segmento, 'FVAL', 'SEGMENTO', "Segmentos", 0, "NOME OU CODIGO(s) DO(s) SEGMENTO(s):", "Ex: 2, 3 ou FARMACIA ou 1", "Informe UM codigo de Segmento, ou ALGUNS codigos, ou PARTE DO NOME de um segmento", 'IDSEGMENTO', 'SEGMENTO', 'brw_df_totais_por_segmentos' )
        # my_bar.progress(97)
        myfunc.mostra_grafico_barras_e_pizza(self.df_totais_por_cidades, 'FVAL', 'CIDADE', "Cidades",10, "NOME OU CODIGO(s) DAS(s) CIDADE(es):", "Ex: 2, 3 ou CAMPINA ou 1", "Informe PARTE DO NOME de uma cidade", '', 'NOME', 'brw_df_totais_por_cidades' )

        myfunc.mostra_grafico_barras_e_pizza(self.df_totais_por_clientes, 'FVAL', 'NOMECLI', "Clientes",10, "NOME OU CODIGO(s) DO(s) CLIENTE(s):", "Ex: 2, 3 ou DROGARIA ou 1", "Informe UM codigo de Cliente, ou ALGUNS codigos, ou PARTE DO NOME da razao social", 'IDCLI', 'NOMECLI', 'brw_df_totais_por_clientes')

        # my_bar.progress(98)
        myfunc.mostra_grafico_barras_e_pizza(self.df_totais_por_uf, 'FVAL', 'UF', "UFs") 


        # my_bar.progress(100)
        # time.sleep(2)

        # my_bar.empty()
        # st.dataframe( df_totais_por_vendedores )

    def filtros_por_vendedores():

        cFiltrosAplicados, grid_response = myfunc.my_aggrid(self.df_totais_por_vendedores, "Vendedores", "NOME OU CODIGO(s) DOS VENDEDORES:", "Ex: 12, 13 ou JOAO ou 15", "Informe UM codigo de vendedor, ou ALGUNS codigos, ou PARTE DO NOME de um vendedor", 'IDVENDEDOR', 'NOME', 'brw_df_totais_por_vendedores' )
        if cFiltrosAplicados!="":
            st.subheader( f"Subtotais de {cFiltrosAplicados}:" + ' :bar_chart:', divider='rainbow')

        venda_total = grid_response['FVAL'].sum() 
        meta_total = grid_response['V_META'].sum() 
        myfunc.mostra_progress_bar_venda_meta(venda_total, meta_total)

    def filtros_por_clientes():

        cFiltrosAplicados, grid_response = myfunc.my_aggrid(self.df_totais_por_clientes, "Clientes", "NOME OU CODIGO(s) DO(s) CLIENTE(s):", "Ex: 2, 3 ou DROGARIA ou 1", "Informe UM codigo de Cliente, ou ALGUNS codigos, ou PARTE DO NOME da razao social", 'IDCLI', 'NOMECLI', 'brw_df_totais_por_clientes' )
        
        if cFiltrosAplicados!="":
            st.subheader( f"Subtotais de {cFiltrosAplicados}:" + ' :bar_chart:', divider='rainbow')

        venda_total = grid_response['FVAL'].sum() 
        meta_total = grid_response['V_META'].sum() 
        myfunc.mostra_progress_bar_venda_meta(venda_total, meta_total)

    # st.sidebar.header('RESUMO DAS VENDAS')

    # option = st.sidebar.selectbox('Escolha uma opção', ['INDICADORES', 'FILTROS POR VENDEDORES','FILTROS POR CLIENTES','FILTROS POR DATAS'])
    option = st.sidebar.selectbox('Escolha uma opção', ['INDICADORES', 'FILTROS POR VENDEDORES','FILTROS POR CLIENTES'])
    st.title('')

    if option == 'INDICADORES':
        tela_inicial()
    elif option == 'FILTROS POR VENDEDORES':
        filtros_por_vendedores()
    elif option == 'FILTROS POR CLIENTES':
        filtros_por_clientes()
    # elif option == 'TOTAIS DIA A DIA':
    #     filtros_por_datas()


# df = df.append(dict_, ignore_index=True)
# import pandas as pd
# # Create a sample DataFrame
# df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
# # Create a new row as a dictionary
# new_row = {'A': 5, 'B': 6}
# # Append the new row to the DataFrame using `loc[]`
# df.loc[len(df)] = new_row
# print(df)

# >>> import pandas as pd
# >>> from numpy.random import randint

# >>> df = pd.DataFrame(columns=['lib', 'qty1', 'qty2'])
# >>> for i in range(5):
# >>>     df.loc[i] = ['name' + str(i)] + list(randint(10, size=2))

# >>> df
#      lib qty1 qty2
# 0  name0    3    3
# 1  name1    2    4
# 2  name2    2    8
# 3  name3    2    1
# 4  name4    9    6



# import streamlit as st
# from st_aggrid import AgGrid, GridOptionsBuilder
# import plotly.graph_objects as go

# # Your data
# df = pd.DataFrame({'Category': [...], 'Items': [...], 'Price': [...]})

# # Configure Ag Grid
# gb = GridOptionsBuilder.from_dataframe(df)
# gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
# gb.configure_selection(selection_mode="multiple", use_checkbox=True)
# gb.configure_side_bar()
# gridoptions = gb.build()

# # Render Ag Grid
# response = AgGrid(df, gridOptions=gridoptions, ...)

# # Get selected rows
# selected_rows = response['selected_rows']
# # Process selected rows
# selected_data = []
# for row in selected_rows:
#     selected_data.append({
#         'Category': row['Category'],
#         'Items': row['Items'],
#         'Price': row['Price']
#     })

# # Visualize selected data
# fig = go.Figure(data=[go.Bar(x=[row['Items'] for row in selected_data], y=[row['Price'] for row in selected_data])])
# fig.update_layout(title='Selected Items and Prices')
# st.plotly_chart(fig)



# import streamlit as st
# from st_aggrid import AgGrid
# import pandas as pd

# # Load sample data frame
# df = pd.read_csv('airline-safety.csv')

# # Initialize Ag Grid
# grid_options = {'editable': True, 'columns': ['column1', 'column2']}
# grid = AgGrid(df, grid_options=grid_options)

# # Create button to trigger data update
# update_button = st.button('Update Data')

# # Define callback function for button
# def update_data():
#     # Update data frame based on user edits
#     updated_df = df.apply(lambda x: x + 1)  # simple example
#     return updated_df

# # Integrate button with Ag Grid
# if update_button:
#     updated_df = update_data()
#     grid.update_data(updated_df)

# df1 = df.nlargest(nFaixasToShow) #.sort_values(by=cColunaXComValor,ascending=True)  # top_3 = df.nlargest(3, 'values')
# st.write( df.sort_values(by=['FVAL']).head(nFaixasToShow) )
# selected_data = []
# for row in df:
#     selected_data.append({
#         'Category': row['Category'],
#         'Items': row['Items'],
#         'Price': row['Price']
#     })


# def foo(arg=None):
#     if arg is None:
#         arg = "default value"
#         # other stuff
#     # ...

# def get_user_data():
#     return 'Anna', 23, 'anna123'

# name, age, id = get_user_data()
# print(name)  # Anna
# print(age)   # 23
# print(id)    # anna123

        # time.sleep(1)
        # time.sleep(1)
        # df.nlargest(10, 'qtd_ordens')[['nome_cliente','qtd_ordens']] pega os 10 maiores valores... equivale a: df.sort_values(by='qtd_vendas', ascending=False).head(10) ... ou seja: o mesmo resultado pode ser obtido combinando as funções .sort_values(), que ordena o data frame, e .head(), que seleciona as primeiras linhas:

# Aspas simples, duplas ou triplas em Python?
# Aspas simples e duplas sao a mesma coisa. Ex: var1="he's your brother"   ou var2='Aqui temos "Joao"'
# ja aspas triplas permitem usar dentro do string ' ou " ou comecar o string em uma linha e terminar em outra linha

        # my_bar = st.progress(0) # st.progress(0, text="Carregando ...")
        # df_totais_empresa = myfunc.load_table('csv/totvenda_empresa.csv')  # DTINI;DTFIM;QCLIPOSIT;QCLICAD;QCLIVISIT;QC_AMAIS;QC_AMENOS;QPRDCOMSLD;QPRDNAOVND;QTDPROD;QTDPRODCAD;QP_AMAIS;QP_AMENOS;VB1;VB2;V_AMAIS;V_AMENOS;V_META;V_PROJ;FVAL;FCREDDEVOL;QPEDIDOS;FVALPROD;FDESCONTO;TENDENCIA;A1A2;Q1;Q2;Q3;Q4;Q1A;Q2A;Q3A;Q4A;V1;V2;V3;V4;V1A;V2A;V3A;V4A

        # st.header(f"Vendas de {df_totais_empresa['DTINI'].iloc[0]} a {df_totais_empresa['DTFIM'].iloc[0]} :bar_chart:", divider='rainbow')
        # st.info(f"""Periodo de {df_totais_empresa['DTINI'].iloc[0]} a {df_totais_empresa['DTFIM'].iloc[0]}  \n ultima atualizacao em {df_data_hora_ultima_atualizacao['DATAHORA'].iloc[0]} """)
        # col1, col2, col3= st.columns([0.4,0.4,0.2])   # Divide a tela em duas colunas, com proporções 1.5, 1
        # with col1:
        #     st.info(f""" Periodo de {df_totais_empresa['DTINI'].iloc[0]} a {df_totais_empresa['DTFIM'].iloc[0]}""")
        # with col2:
        #     st.info(f""" Atualizado em {df_data_hora_ultima_atualizacao['DATAHORA'].iloc[0]} """)
        # with col3:
        #     st.info(f"""Atualizar""")


        # my_bar.progress(10)
        # clientes, setores, segmentos, vendedores, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf = myfunc.load_table('load_totalizacoes_por_clientes')

        # my_bar.progress(20)
        # my_bar.progress(30)
        # time.sleep(1)

        # # informacoes das vendas por cliente do vendedor
        # vendedores_clientes = pd.merge(vendedores,vendas[['FVENDEDOR','FDATAEMI','FVAL','IDCLI']],left_on='IDVENDEDOR',right_on='FVENDEDOR')
        # vendedores_clientes = vendedores_clientes.drop(columns='FVENDEDOR')
