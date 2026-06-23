import pandas as pd
from tests_periodicity import TestsPeriodicity
import pymongo
from pymongo.collection import Collection
from datetime import timedelta
import streamlit as st


@st.cache_data(ttl=timedelta(hours=1), show_spinner='Obtendo os dados...')
def current_month_due(_collection: Collection, query: dict) -> pd.DataFrame:
    tests_to_due = _collection.find(
        query,
        {'_id': 0,
         'Equipamento': 1,
         'Nome': 1,
         'Data da próxima realização': 1}
    ).sort('Data da próxima realização', pymongo.DESCENDING)

    df_tests_to_due = pd.DataFrame(list(tests_to_due))

    if df_tests_to_due.empty:
        return pd.DataFrame(
            columns=['Equipamento', 'Nome', 'Data da próxima realização']
        )

    df_tests_to_due.drop_duplicates(
        subset=['Equipamento', 'Nome'],
        keep='first',
        inplace=True
    )

    return df_tests_to_due


@st.cache_data(ttl=timedelta(hours=1), show_spinner='Obtendo os dados...')
def current_month_done(_collection: Collection, query: dict) -> pd.DataFrame:
    tests_now = _collection.find(
        query,
        {'_id': 0, 'Data da próxima realização': 0}
    ).sort('Data de realização', pymongo.DESCENDING)

    df_tests_now = pd.DataFrame(list(tests_now))

    if df_tests_now.empty:
        return pd.DataFrame(
            columns=[
                'Equipamento',
                'Nome',
                'Data de realização',
                'Arquivado'
            ]
        )

    df_tests_now.drop_duplicates(
        subset=['Equipamento', 'Nome'],
        keep='first',
        inplace=True
    )

    return df_tests_now


@st.cache_data(ttl=timedelta(hours=1), show_spinner='Processando os dados...')
def get_tests_need_to_do(
    df_tests_to_due: pd.DataFrame,
    df_tests_now: pd.DataFrame
) -> pd.DataFrame:

    # garante as colunas mínimas
    if 'Data de realização' not in df_tests_now.columns:
        df_tests_now['Data de realização'] = pd.NaT

    if 'Arquivado' not in df_tests_now.columns:
        df_tests_now['Arquivado'] = False

    if df_tests_to_due.empty:
        return pd.DataFrame(columns=[
            'Equipamento',
            'Nome',
            'Data da próxima realização',
            'Data de realização',
            'Arquivado',
            'not_done'
        ])

    # LEFT JOIN para manter todos os testes previstos
    df_last_to_due_and_done = pd.merge(
        df_tests_to_due,
        df_tests_now,
        how='left',
        on=['Equipamento', 'Nome']
    )

    # garante existência das colunas
    if 'Data de realização' not in df_last_to_due_and_done.columns:
        df_last_to_due_and_done['Data de realização'] = pd.NaT

    if 'Arquivado' not in df_last_to_due_and_done.columns:
        df_last_to_due_and_done['Arquivado'] = False

    tests_periodicity = TestsPeriodicity().full_list()

    df_last_to_due_and_done['not_done'] = True

    def get_keys_by_value(dict_obj, value):
        return [k for k, v in dict_obj.items() if v == value]

    monthly_tests = get_keys_by_value(tests_periodicity, 'Mensal')
    trimestral_tests = get_keys_by_value(tests_periodicity, 'Trimestral')
    semestral_tests = get_keys_by_value(tests_periodicity, 'Semestral')
    anual_tests = get_keys_by_value(tests_periodicity, 'Anual')

    periodicidades = [
        (monthly_tests, 29),
        (trimestral_tests, 91),
        (semestral_tests, 182),
        (anual_tests, 366)
    ]

    resultado = []

    for testes, dias in periodicidades:
        df_temp = df_last_to_due_and_done[
            df_last_to_due_and_done['Nome'].isin(testes)
        ].copy()

        if not df_temp.empty:
            # Se o teste tem "Data de realização" preenchida, foi realizado.
            # A query já filtra pelo mês correto, não precisamos comparar dias.
            df_temp['not_done'] = df_temp['Data de realização'].isna()

        resultado.append(df_temp)

    if resultado:
        return pd.concat(resultado, ignore_index=True)

    return pd.DataFrame(columns=[
        'Equipamento',
        'Nome',
        'Data da próxima realização',
        'Data de realização',
        'Arquivado',
        'not_done'
    ])


def check_materials(df_tests_need_to_do: pd.DataFrame) -> pd.DataFrame:

    if df_tests_need_to_do.empty:
        df_tests_need_to_do['Sem material'] = False
        return df_tests_need_to_do

    df_tests_need_to_do['Sem material'] = False

    with st.sidebar:
        st.markdown('Materiais ausentes para realização dos testes:')

        materials = {}
        materials['Ga-67'] = st.toggle('Ga-67', value=True)
        materials['Tl-201'] = st.toggle('Tl-201', value=True)
        materials['I-131'] = st.toggle('I-131', value=False)

    materiais_ausentes = []

    if materials['Ga-67']:
        materiais_ausentes.append('Ga-67')

    if materials['Tl-201']:
        materiais_ausentes.append('Tl-201')

    if materials['I-131']:
        materiais_ausentes.append('I-131')

    if materiais_ausentes:
        df_tests_need_to_do['Sem material'] = (
            df_tests_need_to_do['Nome']
            .apply(lambda x: any(m in x for m in materiais_ausentes))
        )

    return df_tests_need_to_do


def calculate_indicadores(df_tests_need_to_do: pd.DataFrame) -> tuple:

    total = df_tests_need_to_do.query(
        '`Sem material` == False'
    ).shape[0]

    if total == 0:
        return (0.0, 0.0, 0)

    total_done = df_tests_need_to_do.query(
        'not_done == False and `Sem material` == False'
    ).shape[0]

    indicador_realizacao = total_done / total * 100

    total_done_and_archived = df_tests_need_to_do.query(
        'not_done == False and `Sem material` == False and Arquivado == True'
    ).shape[0]

    indicador_arquivado = total_done_and_archived / total * 100

    return (
        indicador_realizacao,
        indicador_arquivado,
        total
    )
