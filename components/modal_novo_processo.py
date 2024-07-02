from logging import exception
import dash
import plotly.express as px
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from datetime import timedelta, date

import json
import pandas as pd

from app import app
from sql_beta import df_proc, df_adv

col_centered_style={'display': 'flex', 'justify-content': 'center'}

# ========= Layout ========= #
layout = dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Adicione Um Processo")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        # Empresa
                        dbc.Label('Empresa', html_for='empresa_matriz'),
                        dcc.Dropdown(id='empresa_matriz', clearable=False, className='dbc',
                            options=['Escritório Matriz', 'Filial Porto Alegre', 'Filial Curitiba', 'Filial Canoas']),
                        # Tipo de Processo
                        dbc.Label('Tipo de Processo', html_for='tipo_processo'),
                        dcc.Dropdown(id='tipo_processo', clearable=False, className='dbc',
                            options=['Civil', 'Criminal', 'Previdenciário', 'Trabalhista', 'Vara de Família']),
                        # Tipo de Processo
                        dbc.Label('Ação', html_for='acao'),
                        dcc.Dropdown(id='acao', clearable=False, className='dbc',
                            options=['Alimentos', 'Busca e Apreensão', 'Cautelar Inominada', 'Consignação', 'Habeas Corpus', 'Mandado de Segurança', 'Reclamação']),
                    ], sm=12, md=4),
                    dbc.Col([
                        dbc.Label("Descrição", html_for='input_desc'),
                        dbc.Textarea(id="input_desc", placeholder="Escreva aqui observações sobre o processo...", style={'height': '80%'}),
                    ], sm=12, md=8)
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Vara", html_for='vara'),
                        dbc.RadioItems(id='vara',
                            options=[{'label': 'Civil', 'value': 'Civil'},
                            {'label': 'Conciliação e Julgamento', 'value': 'Conciliação e Julgamento'},
                            {'label': 'Trabalhista', 'value': 'Trabalhista'},
                            {'label': 'Vara de Família', 'value': 'Vara de Família'}])
                    ], sm=12, md=4),
                    dbc.Col([
                        dbc.Label("Fase", html_for='fase'),
                        dbc.RadioItems(id='fase', inline=True,
                            options=[{'label': 'Elaboração', 'value': 'Elaboração'},
                            {'label': 'Execução', 'value': 'Execução'},
                            {'label': 'Impugnação', 'value': 'Impugnação'},
                            {'label': 'Instrução', 'value': 'Instrução'},
                            {'label': 'Recurso', 'value': 'Recurso'},
                            {'label': 'Suspenso', 'value': 'Suspenso'}])
                    ], sm=12, md=5),
                    dbc.Col([
                        dbc.Label("Instância", html_for='instancia'),
                        dbc.RadioItems(id='instancia',
                            options=[{'label': '1A Instância', 'value': 1},
                            {'label': '2A Instância', 'value': 2},])
                    ], sm=12, md=3)
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Data Inicial - Data Final")
                            ], style=col_centered_style),
                            dbc.Col([
                                dcc.DatePickerSingle(
                                    id='data_inicial',
                                    className='dbc',
                                    min_date_allowed=date(1999, 12, 31),
                                    max_date_allowed=date(2030, 12, 31),
                                    initial_visible_month=date.today(),
                                    date=date.today()
                                ),
                                dcc.DatePickerSingle(
                                    id='data_final',
                                    className='dbc',
                                    min_date_allowed=date(1999, 12, 31),
                                    max_date_allowed=date(2030, 12, 31),
                                    initial_visible_month=date.today(),
                                    date=None
                                ),
                            ], style=col_centered_style)
                        ]),
                        html.Br(),
                        dbc.Switch(id='processo_concluido', label="Processo Concluído", value=False),
                        dbc.Switch(id='processo_vencido', label="Processo Vencido", value=False),
                        html.P("O filtro de data final só será computado se o checklist estiver marcado.", className='dbc', style={'font-size': '80%'}),
                    ], sm=12, md=5),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Selecione o advogado responsável: "),
                                dcc.Dropdown(
                                    id='advogados_envolvidos',
                                    options=[{'label': i, 'value': i} for i in df_adv['Advogado']],
                                    className='dbc'
                                )
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(id="input_cliente", placeholder="Nome completo do cliente...", type="text")
                            ])
                        ], style={'margin-top': '15px', 'padding': '15px'}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Input(id="input_cliente_cpf", placeholder="CPF do cliente (apenas números)...", type="number")
                            ])
                        ], style={'padding': '15px'}),
                    ], sm=12, md=7)
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(id='input_local_arquivo', clearable=False, className="btn btn-outline-success", placeholder="Local de Arquivo/Local Físico",
                            options=['Armário Principal', 'Armário 17 gaveta 2', 'Armário 5 gaveta 1', 'Arquivo 01', 'Arquivo 02']),
                    ], sm=12, md=5, style={'padding': '15px'}),
                    dbc.Col([
                        dbc.Input(id="input_no_processo", placeholder="Insira o número do Processo", type="number", disabled=False)
                    ], sm=12, md=7, style={'padding': '15px'})
                ], style={'margin-top': '15px'}),
                html.H5(id='div_erro')
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancel_button_novo_processo", color="danger", className="btn btn-outline-danger"),
                dbc.Button("Salvar", id="save_button_novo_processo", color="success", className="btn btn-outline-success"),
            ]),
        ], id="modal_processo", size="lg", is_open=True)



# ======= Callbacks ======== #
# Callback para abrir o modal


# Callback para CRUD de processos


# Callback pra atualizar o dropdown de advogados
@app.callback(
    Output('advogados_envolvidos', 'options'),
    Input('store_adv', 'data')
)
def atu(data):
    df = pd.DataFrame(data)
    return [{'label': i, 'value': i} for i in df['Advogado']]