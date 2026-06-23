import time
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
from PIL import Image
import pandas as pd

from menu import menu_with_redirect
from data_processing.stylized_table import StylizedCQ, styled_tests_need_to_do
from data_processing.filters import filters_archivation, user_period_query
from data_processing.plot_data import plot_indicadores
from data_processing.indicadores import (
    current_month_due,
    current_month_done,
    get_tests_need_to_do,
    check_materials,
    calculate_indicadores
)
from forms import FormMongoDB


st.set_page_config(page_title="Gerência de Controle de Qualidade", layout="wide")

img = Image.open('Logo_SFMR_Horizontal_Centralizado.png')
st.sidebar.image(img, use_column_width=True)

menu_with_redirect()

uri = f"mongodb+srv://medphys_user:{st.secrets['MONGODB_PASSWORD']}@cluster0.dl2yo1n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'), maxIdleTimeMS=60000 * 10)

try:
    client.admin.command('ping')
    print("Mongo conectado!")
except Exception as e:
    print(e)

db = client['cq_gestao']


indicadores, arquivamento, registrar_teste, remover_teste = st.tabs([
    'Indicadores',
    'Arquivamento',
    'Registrar teste',
    'Remover teste'
])

# =========================
# INDICADORES
# =========================
with indicadores:
    collection = db['testes']

    col1, col2 = st.columns(2)

    # -------- ANOS: busca por "Data de realização" (campo preenchido pelo usuário) --------
    with col1:
        try:
            pipeline = [
                {
                    "$project": {
                        "year": {
                            "$year": {
                                "$ifNull": ["$Data de realização", datetime.now()]
                            }
                        }
                    }
                },
                {"$group": {"_id": "$year"}}
            ]
            distinct_years = list(collection.aggregate(pipeline))
            years = sorted(
                [y["_id"] for y in distinct_years if y.get("_id") is not None]
            )
        except Exception as e:
            st.warning(f"Erro ao buscar anos: {e}")
            years = []

        current_year = datetime.now().year
        if not years:
            years = [current_year]
        if current_year not in years:
            years.append(current_year)
            years = sorted(years)

        default_index = years.index(current_year)
        year = st.selectbox("Selecione o ano", years, index=default_index)

    # -------- MESES --------
    with col2:
        months = {
            'Janeiro': 1, 'Fevereiro': 2, 'Março': 3,
            'Abril': 4, 'Maio': 5, 'Junho': 6,
            'Julho': 7, 'Agosto': 8, 'Setembro': 9,
            'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
        }
        current_month = datetime.now().month
        months_key = st.selectbox(
            "Selecione o mês",
            list(months.keys()),
            index=current_month - 1
        )
        month = months[months_key]

    # -------- PERÍODO --------
    # begin/end do mês selecionado
    begin_month = datetime(year, month, 1)
    end_month   = datetime(year, month, 1) + pd.DateOffset(months=1)

    # query_due: testes que VENCEM no mês selecionado
    # (usa "Data da próxima realização" — define o que precisa ser feito no mês)
    query_due = {
        "Data da próxima realização": {
            "$gte": begin_month,
            "$lt": end_month
        }
    }

    # query_done: testes que FORAM REALIZADOS no mês selecionado
    # (usa "Data de realização" — campo real preenchido pelo usuário)
    query_done = {
        "Data de realização": {
            "$gte": begin_month,
            "$lt": end_month
        }
    }

    try:
        df_tests_to_due = current_month_due(collection, query_due)
        df_tests_now = current_month_done(collection, query_done)
    except Exception as e:
        st.error(f"Erro MongoDB query: {e}")
        st.stop()

    df_tests_need_to_do = get_tests_need_to_do(df_tests_to_due, df_tests_now)
    df_tests_need_to_do = check_materials(df_tests_need_to_do)

    styled_tests_need_to_do(df_tests_need_to_do)

    indicador_realizacao, indicador_arquivamento, total_tests = calculate_indicadores(df_tests_need_to_do)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total de testes", total_tests)
    with c2:
        st.metric("Realização", f"{indicador_realizacao:.2f}%".replace('.', ','))
    with c3:
        st.metric("Arquivamento", f"{indicador_arquivamento:.2f}%".replace('.', ','))
    with c4:
        def refresh():
            current_month_due.clear()
            current_month_done.clear()
            get_tests_need_to_do.clear()

        st.button("Atualizar dados", on_click=refresh)

    done_df = df_tests_need_to_do.query(
        "not_done == False and `Sem material` == False"
    )[["Equipamento", "Nome", "Arquivado"]]

    due_df = df_tests_need_to_do.query(
        "`Sem material` == False"
    )[["Equipamento", "Nome", "Arquivado"]]

    tab_realizacao, tab_arquivamento = st.tabs([
        "Realização por equipamento",
        "Arquivamento por equipamento"
    ])

    with tab_realizacao:
        plot_indicadores(done_df, due_df, indicador='realizados', month=months_key, year=year)

    with tab_arquivamento:
        archived_df = done_df[done_df["Arquivado"] == True]
        plot_indicadores(archived_df, due_df, indicador='arquivados', month=months_key, year=year)


# =========================
# ARQUIVAMENTO
# =========================
if 'teste_archivation' not in st.session_state:
    st.session_state.teste_archivation = False


def change_archive_status():
    st.session_state.teste_archivation = True


with arquivamento:
    teste_col = db['testes']
    query = user_period_query()
    raw = list(teste_col.find(query, {'_id': 0, 'Data da próxima realização': 0}))

    if not raw:
        st.info("Nenhum teste encontrado para o período.")
    else:
        testes = pd.DataFrame(raw)
        filtered_tests = filters_archivation(testes)
        styler = StylizedCQ(filtered_tests)
        stylized_table = styler.stylized_testes()

        edited_df = st.data_editor(
            stylized_table,
            hide_index=True,
            use_container_width=True,
            on_change=change_archive_status,
            disabled=('Equipamento', 'Nome', 'Data de realização', 'Data da próxima realização')
        )

        st.markdown("""
            <span style='font-size: smaller;'>
            <b>Observação:</b> período de 1 mês. Clique na caixa para arquivar.
            </span>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("""
                <b>Legenda:</b> <br>
                <span style='color: #FFA07A;'>Relatório atrasado</span> <br>
                <span style='color: #FFD700;'>Dentro do período de desenvolvimento do relatório</span> <br>
                <span style='color: #90EE90;'>Relatório realizado</span>
            """, unsafe_allow_html=True)

        if st.session_state.teste_archivation:
            st.session_state.teste_archivation = False
            diff = filtered_tests.compare(edited_df)
            diff.columns = diff.columns.droplevel(0)
            diff_indices = diff[diff['self'].notna() | diff['other'].notna()].index
            diff_rows = filtered_tests.loc[diff_indices]
            query = diff_rows.drop(columns='Arquivado').to_dict('records')
            diff_value = diff['other']
            archived_status = {'Arquivado': diff_value.values[0]}
            update_status = teste_col.update_one(query[0], {'$set': archived_status})
            if update_status.matched_count > 0:
                st.success("Atualizado!")
                time.sleep(1)
                client.close()
                st.rerun()
            else:
                st.error("Erro ao atualizar!")

with registrar_teste:
    FormMongoDB(client).form_widget('registration')

with remover_teste:
    FormMongoDB(client).form_widget('removal')

client.close()
