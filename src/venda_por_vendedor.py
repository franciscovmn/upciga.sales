import streamlit as st
import pandas as pd
import plotly.graph_objects as go
# import numpy as np
from millify import millify
# from streamlit_extras.metric_cards import style_metric_cards
# from firebase_admin import firestor#e
import myfunc
# import os
import plotly.express as px
st.set_option('deprecation.showPyplotGlobalUse', False)

def app(df_totais_empresa, df_totais_por_clientes, df_totais_por_vendedores, df_totais_por_setores, df_totais_por_cidades, df_totais_por_segmento, df_totais_por_uf, clientes, setores, segmentos, vendedores):
    st.html("venda_por_vendedor.html")

    col1,col2 = st.columns(2)
    with col1:
        df_totais_por_vendedores = df_totais_por_vendedores[ df_totais_por_vendedores['FVAL'] > 0 ].sort_values(by='FVAL',ascending=False)
        cFiltroVendedor, df_totais_por_vendedores = myfunc.my_aggrid(df_totais_por_vendedores, "Vendedores", "NOME OU CODIGO(s) DOS VENDEDORES:", "Ex: 12, 13 ou JOAO ou 15", "Informe UM codigo de vendedor, ou ALGUNS codigos, ou PARTE DO NOME de um vendedor", 'IDVENDEDOR', 'NOME', 'brw_df_totais_por_vendedores' )
    with col2:
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['IDVENDEDOR'].isin( df_totais_por_vendedores['IDVENDEDOR']) ]
        df_totais_por_clientes = df_totais_por_clientes[ df_totais_por_clientes['FVAL'] > 0 ].sort_values(by='FVAL',ascending=False)
        cFiltroCliente, df_totais_por_clientes = myfunc.my_aggrid(df_totais_por_clientes, "Clientes", "NOME OU CODIGO(s) DO(s) CLIENTE(s):", "Ex: 2, 3 ou DROGARIA ou 1", "Informe UM codigo de Cliente, ou ALGUNS codigos, ou PARTE DO NOME da razao social", 'IDCLI', 'NOMECLI', 'brw_df_totais_por_clientes' )
    


    # if cFiltrosAplicados!="":
    #     st.subheader( f"Subtotais de {cFiltrosAplicados}:" + ' :bar_chart:', divider='rainbow')

    # venda_total = grid_response['FVAL'].sum() 
    # meta_total = grid_response['V_META'].sum() 
    # myfunc.mostra_progress_bar_venda_meta(venda_total, meta_total)

    vendas = myfunc.load_table('csv/venda.csv')

    # Outro formato da selecao seria:
    # vendedor_selecionado = st.selectbox('Selecione um vendedor:', vendedores['NOME'])
    # try:
    #     venda_por_vendedores = venda_por_vendedores[venda_por_vendedores['NOME'] == vendedor_selecionado].iloc[0]
    # except IndexError:
    #     st.error('Vendedor não possui métricas')
    #     return 
    venda_clientes_vendedores = pd.merge(vendas[['IDCLI', 'FDATAEMI', 'HORA', 'FVAL']], clientes, on='IDCLI', how='left')
    venda_clientes_vendedores = pd.merge(venda_clientes_vendedores, vendedores, on='IDVENDEDOR', how='left')
    venda_clientes_vendedores = venda_clientes_vendedores.groupby(['IDCLI'])['FVAL'].sum().reset_index()
    # venda_clientes_vendedores_setores = pd.merge(venda_clientes_vendedores, setores, on='IDSETOR')
    #st.write(venda_clientes_vendedores_setores)

    # IDVENDEDOR;QCLIPOSIT;QCLICAD;QCLIVISIT;QC_AMAIS;QC_AMENOS;QPRDCOMSLD;QPRDNAOVND;QTDPROD;QTDPRODCAD;QP_AMAIS;QP_AMENOS;VB1;VB2;V_AMAIS;V_AMENOS;V_META;V_PROJ;FVAL;FCREDDEVOL;QPEDIDOS;FVALPROD;FDESCONTO;TENDENCIA;A1A2;Q1;Q2;Q3;Q4;Q1A;Q2A;Q3A;Q4A;V1;V2;V3;V4;V1A;V2A;V3A;V4A

    total_clientes_cadastrados = df_totais_por_vendedores['QCLICAD'].sum()
    total_clientes_compraram = df_totais_por_vendedores['QCLIPOSIT'].sum()
    total_meta = df_totais_por_vendedores['V_META'].sum()
    total_projetado = df_totais_por_vendedores['V_PROJ'].sum()
    total_vendido = df_totais_por_vendedores['FVAL'].sum()
    cliente_visitados = df_totais_por_vendedores['QCLIVISIT'].sum()

    # col = st.columns(3)
    # with col[0]:
    #     st.metric('VENDA R$', f'{millify(venda_total,precision=0)}') # st.metric('VENDA TOTAL', f'R${venda_total:,.0f}')
    # with col[1]:
    #     st.metric('META R$', f'{millify(meta_total,precision=2)}')  # st.metric('Meta', f'R${millify( df_totais_empresa['V_META'].sum() ,precision=2)}')
    # with col[2]:
    #     st.metric('%Meta (%)', f'{millify(100*venda_total/meta_total,precision=1)} %') # st.metric('Projecao', f'R${millify( df_totais_empresa['V_PROJ'].sum() ,precision=2)}')



    domain = {'x': [0, 0.9], 'y': [0, 0.7]}

    # Criação dos indicadores
    fig = go.Figure(go.Indicator(
        domain=domain,
        value=total_clientes_compraram,
        mode="gauge+number+delta",
        title={'text': f"CLIENTES POSITIVADOS "},
        delta={'reference': total_clientes_cadastrados},
        gauge={'axis': {'range': [None, total_clientes_cadastrados]},
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': total_clientes_compraram}}
    ))

    fig_2 = go.Figure(go.Indicator(
        domain=domain,
        value=total_vendido,
        mode="gauge+number+delta",
        title={'text': f"PROJECAO DE VENDAS"},
        delta={'reference': total_meta},
        gauge={'axis': {'range': [None, total_meta]},
            'steps': [{'range': [total_projetado, total_meta], 'color': "gray"}],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': total_vendido}}
    ))

    # fig_2 = go.Figure(go.Indicator(
    #     domain=domain,
    #     value=cliente_visitados,
    #     mode="gauge+number+delta",
    #     title={'text': f"CLIENTES VISITADOS "},
    #     delta={'reference': total_clientes_cadastrados},
    #     gauge={'axis': {'range': [None, total_clientes_cadastrados]},
    #         'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': cliente_visitados}}
    # ))

    # col1,col2 = st.columns(2)

    # with col1:
    #     l, r = st.columns(2)
    #     with l:
    #         st.plotly_chart(fig, use_container_width=True)
    #         st.html('<span class="low_indicator"></span>')
    #         st.metric(f'{millify(total_clientes_cadastrados)} CADASTRADOS e {millify(total_clientes_compraram)} COMPRARAM',
    #                   millify(total_clientes_cadastrados),
    #                   millify(total_clientes_compraram - total_clientes_cadastrados))
    #     with r:
    #         st.plotly_chart(fig_2, use_container_width=True)
    #         st.html('<span class="high_indicator"></span>')
    #         st.metric(f'{millify(total_clientes_cadastrados)}/{millify(cliente_visitados)} FORAM VISITADOS',
    #                   millify(total_clientes_cadastrados),
    #                   millify(cliente_visitados - total_clientes_cadastrados))

    # with col2:
    #     vendas_por_cidades = venda_clientes_vendedores.groupby(['IDSETOR','CIDADE_x'])['FVAL'].sum().reset_index()

    #     # Plotly Horizontal Bar Chart
    #     fig = px.bar(
    #         vendas_por_cidades,
    #         y='CIDADE_x',
    #         x='FVAL',
    #         barmode="group",
    #         orientation='h',
    #         text_auto=".2s",
    #         title=f"Vendas por Cidade",
    #         height=400,
    #     )
    #     fig.update_traces(
    #         textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    #     )
    #     st.plotly_chart(fig, use_container_width=True)
    #     # Plotly Horizontal Bar Chart
    #     fig1 = px.bar(
    #         vendas_por_cidades,
    #         y='IDSETOR',
    #         x='FVAL',
    #         barmode="group",
    #         orientation="h",
    #         text_auto=".2s",
    #         title=f"Vendas por Setores",
    #         height=400,
    #     )
    #     fig.update_traces(
    #         textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    #     )
    #     st.plotly_chart(fig1, use_container_width=True)

