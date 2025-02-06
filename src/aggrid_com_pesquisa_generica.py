import streamlit as st
from agstyler import draw_grid
from aggrid_colunas_a_exibir import colunas_aggrid

def aggrid_com_pesquisa(df, cTitulo1, cTextoDoInputDePesquisa='', conteudo_do_placeholder='', CHelpText='', cColunaId='', cColunaNome='', cColunasAgGrid='', fg_permite_rerun=False):
    fgDeveExecutarRerun = False
    cNomeDaVariavelDeSessao = "psq" + cTitulo1
    cFiltroSalvoNaSessao = ''
    cFiltrosAplicados = ''
    if cNomeDaVariavelDeSessao in st.session_state and not getattr(st.session_state, cNomeDaVariavelDeSessao) is None:
        cFiltroSalvoNaSessao = getattr(st.session_state, cNomeDaVariavelDeSessao)
        conteudo_do_placeholder = cTitulo1+": "+cFiltroSalvoNaSessao          # st.session_state.psqUFs

    search_term = st.text_input(cTextoDoInputDePesquisa, placeholder=conteudo_do_placeholder, help=CHelpText, key='input_'+cNomeDaVariavelDeSessao)
    if search_term != "":           # search_term != "" eh o mesmo que: not search_term == "":
        try:
            if cColunaId!="" and ',' in search_term:
                codigos = [int(codigo.strip()) for codigo in search_term.split(',') if codigo.strip().isdigit()]
                df_filtrado = df[ df[cColunaId].isin(codigos) ]
                # codigos_selecionados = ', '.join( df_filtrado[cColunaId].values.astype(str) )
                # search_term = ', '.join( df_filtrado[cColunaId].values.astype(str) )
            elif cColunaId!="" and search_term.isdigit():
                df_filtrado = df[ df[cColunaId] == int(search_term) ]
            else:
                df_filtrado = df[ df[cColunaNome].str.contains(search_term, case=False)  ].copy()
        
            if len(df_filtrado.index) > 0:
                df = df_filtrado
                if fg_permite_rerun:
                    setattr(st.session_state, cNomeDaVariavelDeSessao, search_term)
                    setattr(st.session_state, 'df_'+cNomeDaVariavelDeSessao, df)
                    fgDeveExecutarRerun = True
                # st.info(f""" Search_term={search_term} """)
            else:
                st.info(f""" Filtro invalido={search_term} """)
                search_term = ""
                if fg_permite_rerun:
                    setattr(st.session_state, cNomeDaVariavelDeSessao, None)
                    setattr(st.session_state, 'df_'+cNomeDaVariavelDeSessao, None)

        except KeyError:  # Tratar KeyError caso a coluna não exista no DataFrame
            st.write("Erro: Coluna não encontrada. Verifique se os dados estão corretos.")
        except ValueError:  # Tratar ValueError caso a conversão de tipo falhe
            st.write("Erro: Valor inválido. Verifique se os dados estão corretos.")
        except Exception as e:  # Tratar outras exceções genéricas
            st.write(f"Ocorreu um erro: {e}")

    if cColunasAgGrid !="" :
        cDictComColunasAgGrid = colunas_aggrid(cColunasAgGrid)

    if cColunasAgGrid !="" and not cDictComColunasAgGrid is None:
        grid_response = draw_grid(
            df,  # df_totais_por_vendedores.head(row_number)
            formatter=cDictComColunasAgGrid,
            fit_columns=True,
            selection='multiple',  # or 'single', or None
            use_checkbox='True',  # or False by default
            max_height=300
        )
        # st.dataframe(df)

        # comentei o trecho abaixo que permitiria processar as linhas selecionadas no aggrid porque o componente esta apresentando problemas de formatacao
        
        # df_selected = grid_response['selected_rows']
        # if not df_selected is None:
        #     search_term = ', '.join( df_selected[cColunaId].values.astype(str) ) # precisa testar se o tipo da coluna eh string
        #     codigos = [int(codigo.strip()) for codigo in search_term.split(',') if codigo.strip().isdigit()]
        #     # df_filtrado = df[ df[cColunaId].isin(codigos) ]
        #     # df = df_filtrado
        #     df = df[ df[cColunaId].isin(codigos) ]
        #     setattr(st.session_state, cNomeDaVariavelDeSessao, search_term)
        #     setattr(st.session_state, 'df_'+cNomeDaVariavelDeSessao, df)
            
        #     fgDeveExecutarRerun = True

    else:
        st.dataframe(df)

    # # st.info(f""" grid_response[data] ={ grid_response['data'] } \n\n grid_response[selected_rows] ={ grid_response['selected_rows'] } """)
    # # st.write(df_selected)
    if not fg_permite_rerun:
        if cFiltroSalvoNaSessao!="":
            cFiltrosAplicados = "Filtros: "+ cTitulo1+": "+cFiltroSalvoNaSessao
        if search_term!="":
            cFiltrosAplicados += "  SubFiltro: "+ search_term
        # cFiltrosAplicados = "Filtro "+cTitulo1+": "+search_term if cFiltroSalvoNaSessao=="" else ("SubFiltro "+cTitulo1+": "+search_term+" " if search_term!="" else "")+"Filtros: "+ cTitulo1+": "+cFiltroSalvoNaSessao + () if cFiltroSalvoNaSessao!=""  
        return cFiltrosAplicados, df
    elif fg_permite_rerun and fgDeveExecutarRerun:
        st.rerun()

        # st.info(f""" AgGrid Search_term={search_term} cNomeDaVariavelDeSessao={cNomeDaVariavelDeSessao} \n\n st.session_state.psqVendedores= {st.session_state.psqVendedores} """)

    # st.rerun()