import streamlit as st
import pandas as pd
# import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from millify import millify
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go
import myfunc   # from myfunc import load_table, mostra_progress_bar_venda_meta, mostra_grafico_barras_e_pizza

from agstyler import PINLEFT, PRECISION_TWO, draw_grid
from aggrid_com_pesquisa_generica import aggrid_com_pesquisa


st.set_option('deprecation.showPyplotGlobalUse', False)

def app( df_totais_empresa, clientes, setores, segmentos, vendedores, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf ):

    # def filtros_por_datas():
        vendas = myfunc.load_table('csv/venda.csv')
        vendas_dia = vendas.groupby('FDATAEMI')['FVAL'].sum().reset_index()  

        soma_vendas_total = vendas['FVAL'].sum()

        # Formatar as somas como moeda
        # soma_vendas_total_str = f'R$ {soma_vendas_total:,.2f}'

        st.metric('VENDA TOTAL', f'R${millify(soma_vendas_total,precision=2)}')
        # ui.metric_card(title="VENDA TOTAL", content=soma_vendas_total_str, key="card2")

        # Colocando em ordem
        vendas_dia = vendas_dia.sort_values(by='FDATAEMI',ascending=False)
        # Converter a coluna 'FDATAEMI' para o formato de data
        vendas_dia['FDATAEMI'] = pd.to_datetime(vendas_dia['FDATAEMI'], format='%m/%d/%Y')
        # Formatar a data como 'dia/mês/ano'
        vendas_dia['FDATAEMI'] = vendas_dia['FDATAEMI'].dt.strftime('%d/%m/%Y')

        # Criar uma nova coluna com a soma das vendas formatada como moeda real
        vendas_dia['Soma_Vendas_Formatada'] = vendas_dia['FVAL'].map(lambda x: f'R$ {x:,.2f}')

        # Plotar o gráfico de linhas horizontais
        fig = px.bar(vendas_dia, y='FDATAEMI', x='FVAL', text='Soma_Vendas_Formatada', color='FVAL',
                    labels={'FVAL': 'Soma das Vendas'}, orientation='h')

        # Adicionar título e rótulos dos eixos
        fig.update_layout(title='Soma das Vendas por Dia',xaxis_title='Soma das Vendas',yaxis_title='Data')

        # Exibir o gráfico
        st.plotly_chart(fig)
        # ----------------------

        vendas = vendas.reindex(columns=['FDATAEMI','FVAL','HORA','FLOJA'])
        # Date Range Picker
        dt1 = ui.date_picker(key="date_picker2", mode="range", label="Selecione um intervalo de datas")

        # Converter as datas para o formato esperado (mes/dia/ano)
        vendas['FDATAEMI'] = pd.to_datetime(vendas['FDATAEMI'], format='%m/%d/%Y')

        # Aplicar filtro de datas, se selecionado
        if dt1 is not None:
            start_date = dt1[0]
            end_date = dt1[1]
            
            # Filtrar o DataFrame com base no intervalo de datas selecionado
            soma_vendas_total_filtradas = vendas[(vendas['FDATAEMI'] >= start_date) & (vendas['FDATAEMI'] <= end_date)]

            soma_FVAL = soma_vendas_total_filtradas['FVAL'].sum()
            
            # Exibir os dados filtrados
            st.write("Dados filtrados:")
            
            # Criar uma nova coluna com a data formatada para exibição na tabela
            soma_vendas_total_filtradas['FDATAEMI_FORMATADA'] = soma_vendas_total_filtradas['FDATAEMI'].dt.strftime('%d/%m/%Y')

            soma_vendas_total_filtradas['FVAL'] = soma_vendas_total_filtradas['FVAL'].map(lambda x: f'R$ {x:,.2f}')



            ui.metric_card(title="Total Vendas", content=f"R$ {soma_FVAL:,.2f}", description="SOMA TOTAL ATÉ O DIA ATUAL")

            soma_vendas_total_filtradas = soma_vendas_total_filtradas.rename(columns={'FVAL': 'VALOR DA VENDA', 'FLOJA': 'LOJA','FDATAEMI_FORMATADA':'DATA DA VENDA'})


            st.write(soma_vendas_total_filtradas.drop(columns=['FDATAEMI']))  # Exclua a coluna original

        else:
            st.write("Nenhum intervalo de datas selecionado.")


    # option = st.sidebar.selectbox('Escolha uma opção', ['INDICADORES', 'FILTROS POR VENDEDORES','FILTROS POR CLIENTES','FILTROS POR DATAS'])
    # st.title('')

    # if option == 'INDICADORES':
    #     indicadores_gerais()
    # elif option == 'FILTROS POR VENDEDORES':
    #     filtros_por_vendedores()
    # elif option == 'FILTROS POR CLIENTES':
    #     filtros_por_clientes()
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



# def CreateProgressBar(pg_caption, pg_int_percentage, pg_colour, pg_bgcolour):
#     pg_int_percentage = str(pg_int_percentage).zfill(2)
#     pg_html = f"""<table style="width:50%; border-style: none;">
#                         <tr style='font-weight:bold;'>
#                             <td style='background-color:{pg_bgcolour};'>{pg_caption}: <span style='accent-color: {pg_colour}; bgcolor: transparent;'>
#                                 <progress value='{pg_int_percentage}' max='100'>{pg_int_percentage}%</progress> </span>{pg_int_percentage}% 
#                             </td>
#                         </tr>
#                     </table><br>"""
#     return pg_html

# st.markdown(CreateProgressBar("Positive", 62, "#A5D6A7", "#B2EBF2"), True)
# st.markdown(CreateProgressBar("Neutral", 40, "#FFD54F", "#B2EBF2"), True)
# st.markdown(CreateProgressBar("Negative", 65, "red", "#B2EBF2"), True)


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