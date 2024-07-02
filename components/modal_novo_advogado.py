import dash
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from app import app

# ========= Layout ========= #
layout = dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Adicione um Advogado")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("OAB"),
                        dbc.Input(id="adv_oab", placeholder="Apenas números, referente a OAB...", type="number")
                    ], sm=12, md=6),
                    dbc.Col([
                        dbc.Label("CPF"),
                        dbc.Input(id="adv_cpf", placeholder="Apenas números, CPF...", type="number")
                    ], sm=12, md=6),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Nome"),
                        dbc.Input(id="adv_nome", placeholder="Nome completo do advogado...", type="text")
                    ]),
                ]),
                html.H5(id='div_erro2')
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="cancel_button_novo_advogado", color="danger", className="btn btn-outline-danger"),
                dbc.Button("Salvar", id="save_button_novo_advogado", color="success", className="btn btn-outline-success")
            ])
        ], id="modal_new_lawyer", size="lg", is_open=False)


# ======= Callbacks ======== #
# Callback para adicionar novos advogados
