__all__ = [
    'PrecisionComponent',
    'ConfusionMatrixComponent',
    'LiftCurveComponent',
    'ClassificationComponent',
    'RocAucComponent',
    'PrAucComponent',
    'CumulativePrecisionComponent',
    'ClassifierModelSummaryComponent' 
]

import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from ..dashboard_methods import *


class PrecisionComponent(ExplainerComponent):
    def __init__(self, explainer, title="Precision Plot", name=None,
                    hide_title=False,
                    hide_cutoff=False, hide_binsize=False, hide_binmethod=False,
                    hide_multiclass=False, hide_selector=False, pos_label=None,
                    bin_size=0.1, quantiles=10, cutoff=0.5,
                    quantiles_or_binsize='bin_size', multiclass=False, **kwargs):
        """Shows a precision graph with toggles.

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Precision Plot".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            hide_title (bool, optional): hide title
            hide_cutoff (bool, optional): Hide cutoff slider. Defaults to False.
            hide_binsize (bool, optional): hide binsize/quantiles slider. Defaults to False.
            hide_selector(bool, optional): hide pos label selector. Defaults to False.
            hide_binmethod (bool, optional): Hide binsize/quantiles toggle. Defaults to False.
            hide_multiclass (bool, optional): Hide multiclass toggle. Defaults to False.
            hide_selector (bool, optional): Hide pos label selector. Default to True.
            pos_label ({int, str}, optional): initial pos label. Defaults to explainer.pos_label
            bin_size (float, optional): Size of bins in probability space. Defaults to 0.1.
            quantiles (int, optional): Number of quantiles to divide plot. Defaults to 10.
            cutoff (float, optional): Cutoff to display in graph. Defaults to 0.5.
            quantiles_or_binsize (str, {'quantiles', 'bin_size'}, optional): Default bin method. Defaults to 'bin_size'.
            multiclass (bool, optional): Display all classes. Defaults to False.
        """
        super().__init__(explainer, title, name)

        self.cutoff_name = 'precision-cutoff-' + self.name

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.description = f"""
        On this plot you can see the relation between the predicted probability
        that a {self.explainer.index_name} belongs to the positive class, and
        the percentage of observed {self.explainer.index_name} in the positive class.
        The observations get binned together in groups of roughly 
        equal predicted probabilities, and the percentage of positives is calculated
        for each bin. A perfectly calibrated model would show a straight line
        from the bottom left corner to the top right corner. A strong model would
        classify most observations correctly and close to 0% or 100% probability.
        """
        self.register_dependencies("preds", "pred_probas", "pred_percentiles")

    def layout(self):
        return html.Div([
            make_hideable(
                html.Div([
                    html.H3(self.title, id='precision-title-'+self.name),
                    dbc.Tooltip(self.description, target='precision-title-'+self.name),
                ]), hide=self.hide_title),
            dbc.Row([
                make_hideable(
                    dbc.Col([self.selector.layout()], width=3), hide=self.hide_selector)
            ], justify="end"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Graph(id='precision-graph-'+self.name,
                                                config=dict(modeBarButtons=[['toImage']], displaylogo=False)),
                    ], style={'margin': 0}),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    make_hideable(
                        html.Div([
                            html.Div([
                                dbc.Label('Bin size:', html_for='precision-binsize-'+self.name),
                                html.Div([
                                    dcc.Slider(id='precision-binsize-'+self.name, 
                                            min = 0.01, max = 0.5, step=0.01, value=self.bin_size,
                                            marks={0.01: '0.01', 0.05: '0.05', 0.10: '0.10',
                                                0.20: '0.20', 0.25: '0.25' , 0.33: '0.33', 
                                                0.5: '0.5'}, 
                                            included=False,
                                            tooltip = {'always_visible' : False})
                                ], style={'margin-bottom': 5}),
                            ], id='precision-bin-size-div-'+self.name, style=dict(margin=5)),
                            dbc.Tooltip("Size of the bins to divide prediction score by", 
                                    target='precision-bin-size-div-'+self.name,
                                    placement='bottom'),
                        ]), hide=self.hide_binsize),
                    make_hideable(
                        html.Div([
                        html.Div([
                            dbc.Label('Quantiles:', html_for='precision-quantiles-'+self.name),
                            html.Div([
                                dcc.Slider(id='precision-quantiles-'+self.name, 
                                            min = 1, max = 20, step=1, value=self.quantiles,
                                            marks={1: '1', 5: '5', 10: '10', 15: '15', 20:'20'}, 
                                            included=False,
                                            tooltip = {'always_visible' : False}),
                            ], style={'margin-bottom':5}),
                        ], id='precision-quantiles-div-'+self.name), 
                        dbc.Tooltip("Number of equally populated bins to divide prediction score by", 
                                    target='precision-quantiles-div-'+self.name,
                                    placement='bottom'),
                        ]), hide=self.hide_binsize),
                    make_hideable(
                        html.Div([
                        html.Div([
                            html.Label('Cutoff prediction probability:'),
                            dcc.Slider(id='precision-cutoff-'+self.name, 
                                        min = 0.01, max = 0.99, step=0.01, value=self.cutoff,
                                        marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                                0.75: '0.75', 0.99: '0.99'}, 
                                        included=False,
                                        tooltip = {'always_visible' : False}),
                        ], id='precision-cutoff-div-'+self.name),
                        dbc.Tooltip(f"Scores above this cutoff will be labeled positive",
                                        target='precision-cutoff-div-'+self.name,
                                        placement='bottom'),
                        ], style={'margin-bottom': 5}), hide=self.hide_cutoff),
                ]),
            ]),
            dbc.Row([
                make_hideable(
                    dbc.Col([
                        dbc.Label('Binning Method:', html_for='precision-binsize-or-quantiles-'+self.name),
                        dbc.RadioItems(
                            id='precision-binsize-or-quantiles-'+self.name,
                            options=[
                                {'label': 'Bin Size', 
                                'value': 'bin_size'},
                                {'label': 'Quantiles', 
                                'value': 'quantiles'}
                            ],
                            value=self.quantiles_or_binsize,
                            inline=True),
                        dbc.Tooltip("Divide the x-axis by equally sized ranges of prediction scores (bin size),"
                                    " or bins with the same number of observations (counts) in each bin: quantiles",
                                    target='precision-binsize-or-quantiles-'+self.name),     
                    ], width=3), hide=self.hide_binmethod),
                make_hideable(
                    dbc.Col([
                        dbc.FormGroup([
                                dbc.RadioButton(
                                    id="precision-multiclass-"+self.name, 
                                    className="form-check-input",
                                    checked=self.multiclass
                                ),
                                dbc.Label(
                                    "Display all classes",
                                    html_for="precision-multiclass-"+self.name,
                                    className="form-check-label",
                                ),
                                dbc.Tooltip("Display the percentage of all labels or only of the positive label",
                                    target="precision-multiclass-"+self.name),                              
                        ], check=True),
                    ], width=3), hide=self.hide_multiclass), 
            ])    
        ])

    def _register_callbacks(self, app):
        @app.callback(
            [Output('precision-bin-size-div-'+self.name, 'style'),
             Output('precision-quantiles-div-'+self.name, 'style')],
            [Input('precision-binsize-or-quantiles-'+self.name, 'value')],
        )
        def update_div_visibility(bins_or_quantiles):
            if self.hide_binsize:
                return dict(display='none'), dict(display='none')
            if bins_or_quantiles=='bin_size':
                return {}, dict(display='none')
            elif bins_or_quantiles=='quantiles':
                return dict(display='none'), {}
            raise PreventUpdate   

        @app.callback(
            Output('precision-graph-'+self.name, 'figure'),
            [Input('precision-binsize-'+self.name, 'value'),
             Input('precision-quantiles-'+self.name, 'value'),
             Input('precision-binsize-or-quantiles-'+self.name, 'value'),
             Input('precision-cutoff-'+self.name, 'value'),
             Input('precision-multiclass-'+self.name, 'checked'),
             Input('pos-label-'+self.name, 'value')],
            #[State('tabs', 'value')],
        )
        def update_precision_graph(bin_size, quantiles, bins, cutoff, multiclass, pos_label):
            if bins == 'bin_size':
                return self.explainer.plot_precision(
                    bin_size=bin_size, cutoff=cutoff, multiclass=multiclass, pos_label=pos_label)
            elif bins == 'quantiles':
                return self.explainer.plot_precision(
                    quantiles=quantiles, cutoff=cutoff, multiclass=multiclass, pos_label=pos_label)
            raise PreventUpdate


class ConfusionMatrixComponent(ExplainerComponent):
    def __init__(self, explainer, title="Confusion Matrix", name=None,
                    hide_title=False,
                    hide_cutoff=False, hide_percentage=False, hide_binary=False,
                    hide_selector=False, pos_label=None,
                    cutoff=0.5, percentage=True, binary=True, **kwargs):
        """Display confusion matrix component

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Confusion Matrix".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            hide_title (bool, optional): hide title.
            hide_cutoff (bool, optional): Hide cutoff slider. Defaults to False.
            hide_percentage (bool, optional): Hide percentage toggle. Defaults to False.
            hide_binary (bool, optional): Hide binary toggle. Defaults to False.
            hide_selector(bool, optional): hide pos label selector. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. Defaults to explainer.pos_label
            cutoff (float, optional): Default cutoff. Defaults to 0.5.
            percentage (bool, optional): Display percentages instead of counts. Defaults to True.
            binary (bool, optional): Show binary instead of multiclass confusion matrix. Defaults to True.
        """
        super().__init__(explainer, title, name)

        self.cutoff_name = 'confusionmatrix-cutoff-' + self.name

        if len(self.explainer.labels) <= 2:
            self.hide_binary = True

        self.description = """
        The confusion matrix shows the number of true negatives (predicted negative, observed negative), 
        true positives (predicted positive, observed positive), 
        false negatives (predicted negative, but observed positive) and
        false positives (predicted positive, but observed negative). The amount
        of false negatives and false positives determine the costs of deploying
        and imperfect model. For different cutoffs you will get a different number
        of false positives and false negatives. This plot can help you select
        the optimal cutoff.
        """

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.register_dependencies("preds", "pred_probas", "pred_percentiles")

    def layout(self):
        return html.Div([
            make_hideable(
                html.Div([
                    html.H3(self.title, id='confusionmatrix-title-'+self.name),
                    dbc.Tooltip(self.description, target='confusionmatrix-title-'+self.name),
                ]), hide=self.hide_title),
            dbc.Row([
                make_hideable(
                    dbc.Col([self.selector.layout()], width=3), hide=self.hide_selector)
            ], justify="end"),
            dcc.Graph(id='confusionmatrix-graph-'+self.name,
                                            config=dict(modeBarButtons=[['toImage']], displaylogo=False)),
            make_hideable(
                html.Div([
                html.Div([
                    html.Label('Cutoff prediction probability:'),
                    dcc.Slider(id='confusionmatrix-cutoff-'+self.name, 
                                min = 0.01, max = 0.99, step=0.01, value=self.cutoff,
                                marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                        0.75: '0.75', 0.99: '0.99'}, 
                                included=False,
                                tooltip = {'always_visible' : False},
                                updatemode='drag'),
                ], id='confusionmatrix-cutoff-div-'+self.name),
                dbc.Tooltip(f"Scores above this cutoff will be labeled positive",
                                target='confusionmatrix-cutoff-div-'+self.name,
                                placement='bottom'),
                ], style={'margin-bottom': 25}), hide=self.hide_cutoff),
            make_hideable(
                html.Div([
                    dbc.FormGroup([
                            dbc.RadioButton(
                                id='confusionmatrix-percentage-'+self.name, 
                                className="form-check-input", 
                                checked=self.percentage
                            ),
                            dbc.Label(
                                "Display percentages",
                                html_for="confusionmatrix-percentage-"+self.name,
                                className="form-check-label",
                            ),
                            dbc.Tooltip("Highlight the percentage in each cell instead of the absolute numbers",
                                    target='confusionmatrix-percentage-'+self.name),  
                    ], check=True),
                ]), hide=self.hide_percentage),
            make_hideable(
                html.Div([
                    dbc.FormGroup([
                            dbc.RadioButton(
                                id="confusionmatrix-binary-"+self.name, 
                                className="form-check-input", 
                                checked=self.binary
                            ),
                            dbc.Label(
                                "Binary",
                                html_for="confusionmatrix-binary-"+self.name,
                                className="form-check-label",
                            ),
                            dbc.Tooltip("display a binary confusion matrix of positive "
                                        "class vs all other classes instead of a multi"
                                        " class confusion matrix.",
                                    target="confusionmatrix-binary-"+self.name)
                    ], check=True),
                ]), hide=self.hide_binary),
        ])

    def _register_callbacks(self, app):
        @app.callback(
             Output('confusionmatrix-graph-'+self.name, 'figure'),
            [Input('confusionmatrix-cutoff-'+self.name, 'value'),
             Input('confusionmatrix-percentage-'+self.name, 'checked'),
             Input('confusionmatrix-binary-'+self.name, 'checked'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_confusionmatrix_graph(cutoff, normalized, binary, pos_label):
            return self.explainer.plot_confusion_matrix(
                        cutoff=cutoff, normalized=normalized, binary=binary, pos_label=pos_label)


class LiftCurveComponent(ExplainerComponent):
    def __init__(self, explainer, title="Lift Curve", name=None,
                    hide_title=False,
                    hide_cutoff=False, hide_percentage=False, hide_selector=False,
                    pos_label=None, cutoff=0.5, percentage=True, **kwargs):
        """Show liftcurve component

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Lift Curve".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            hide_title (bool, optional): hide title.
            hide_cutoff (bool, optional): Hide cutoff slider. Defaults to False.
            hide_percentage (bool, optional): Hide percentage toggle. Defaults to False.
            hide_selector(bool, optional): hide pos label selector. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. Defaults to explainer.pos_label
            cutoff (float, optional): Cutoff for lift curve. Defaults to 0.5.
            percentage (bool, optional): Display percentages instead of counts. Defaults to True.
        """
        super().__init__(explainer, title, name)

        self.cutoff_name = 'liftcurve-cutoff-' + self.name

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.description = """
        The lift curve shows you the percentage of positive classes when you only
        select observations with a score above cutoff vs selecting observations
        randomly. This shows you how much better the model is than random (the lift).
        """
        self.register_dependencies("preds", "pred_probas", "pred_percentiles")

    def layout(self):
        return html.Div([
            make_hideable(
                html.Div([
                    html.H3(self.title, id='liftcurve-title-'+self.name),
                    dbc.Tooltip(self.description, target='liftcurve-title-'+self.name),
                ]), hide=self.hide_title),
            dbc.Row([
                make_hideable(
                    dbc.Col([self.selector.layout()], width=3), hide=self.hide_selector)
            ], justify="end"),
            html.Div([
                dcc.Graph(id='liftcurve-graph-'+self.name,
                            config=dict(modeBarButtons=[['toImage']], displaylogo=False)),
            ], style={'margin': 0}),
            make_hideable(
                html.Div([
                html.Div([
                    html.Label('Cutoff prediction probability:'),
                    dcc.Slider(id='liftcurve-cutoff-'+self.name, 
                                min = 0.01, max = 0.99, step=0.01, value=self.cutoff,
                                marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                        0.75: '0.75', 0.99: '0.99'}, 
                                included=False,
                                tooltip = {'always_visible' : False},
                                updatemode='drag'),
                    
                ], id='liftcurve-cutoff-div-'+self.name),
                dbc.Tooltip(f"Scores above this cutoff will be labeled positive",
                                target='liftcurve-cutoff-div-'+self.name,
                                placement='bottom'),
                ], style={'margin-bottom': 25}), hide=self.hide_cutoff),
            make_hideable(
                html.Div([
                    dbc.FormGroup([
                        dbc.RadioButton(
                            id="liftcurve-percentage-"+self.name, 
                            className="form-check-input", 
                            checked=True
                        ),
                        dbc.Label(
                            "Display percentages",
                            html_for="liftcurve-percentage-"+self.name,
                            className="form-check-label",
                        ),
                        dbc.Tooltip("Display percentages positive and sampled"
                                " instead of absolute numbers",
                                target="liftcurve-percentage-"+self.name)
                    ], check=True), 
                ]), hide=self.hide_percentage),         
        ])

    def _register_callbacks(self, app):
        @app.callback(
            Output('liftcurve-graph-'+self.name, 'figure'),
            [Input('liftcurve-cutoff-'+self.name, 'value'),
             Input('liftcurve-percentage-'+self.name, 'checked'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_precision_graph(cutoff, percentage, pos_label):
            return self.explainer.plot_lift_curve(cutoff=cutoff, percentage=percentage, pos_label=pos_label)


class CumulativePrecisionComponent(ExplainerComponent):
    def __init__(self, explainer, title="Cumulative Precision", name=None,
                    hide_title=False,
                    hide_selector=False, pos_label=None,
                    hide_cutoff=False, cutoff=None,
                    hide_percentile=False, percentile=None, **kwargs):
        """Show cumulative precision component

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Cumulative Precision".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            hide_title (bool, optional): hide the title.
            hide_selector(bool, optional): hide pos label selector. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. Defaults to explainer.pos_label
        """
        super().__init__(explainer, title, name)

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.cutoff_name = 'cumulative-precision-cutoff-'+self.name

        self.description = """
        This plot shows the percentage of each label that you can expect when you
        only sample the top x% highest scores. 
        """
        self.register_dependencies("preds", "pred_probas", "pred_percentiles")

    def layout(self):
        return html.Div([
            make_hideable(
                html.Div([
                    html.H3(self.title, id='cumulative-precision-title-'+self.name),
                    dbc.Tooltip(self.description, target='cumulative-precision-title-'+self.name),
                ]), hide=self.hide_title),
            html.Div([
                dcc.Graph(id='cumulative-precision-graph-'+self.name,
                            config=dict(modeBarButtons=[['toImage']], displaylogo=False)),
            ], style={'margin': 0}),
             dbc.Row([
                dbc.Col([
                    dbc.Row([
                            make_hideable(
                            dbc.Col([
                                html.Div([
                                    html.Label('Sample top fraction:'),
                                    dcc.Slider(id='cumulative-precision-percentile-'+self.name,
                                                min = 0.01, max = 0.99, step=0.01, value=self.percentile,
                                                marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                                        0.75: '0.75', 0.99: '0.99'},
                                                included=False,
                                                tooltip = {'always_visible' : False},
                                                updatemode='drag')
                                ], style={'margin-bottom': 15}, id='cumulative-precision-percentile-div-'+self.name),
                                dbc.Tooltip("Draw the line where you only sample the top x% fraction of all samples",
                                        target='cumulative-precision-percentile-div-'+self.name)
                            ]), hide=self.hide_percentile),
                    ]),
                    dbc.Row([
                        make_hideable(
                            dbc.Col([
                                html.Div([
                                    html.Label('Cutoff prediction probability:'),
                                    dcc.Slider(id='cumulative-precision-cutoff-'+self.name,
                                                min = 0.01, max = 0.99, step=0.01, value=self.cutoff,
                                                marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                                        0.75: '0.75', 0.99: '0.99'},
                                                included=False,
                                                tooltip = {'always_visible' : False}),
                                    
                                ], style={'margin-bottom': 15}, id='cumulative-precision-cutoff-div-'+self.name),
                                dbc.Tooltip(f"Scores above this cutoff will be labeled positive",
                                                target='cumulative-precision-cutoff-div-'+self.name,
                                                placement='bottom'),
                            ]), hide=self.hide_cutoff),
                    ]),    
                ]),
                make_hideable(
                    dbc.Col([
                        self.selector.layout()
                    ], width=2), hide=self.hide_selector),
            ])
                 
        ])

    def _register_callbacks(self, app):
        @app.callback(
            Output('cumulative-precision-graph-'+self.name, 'figure'),
            [Input('cumulative-precision-percentile-'+self.name, 'value'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_cumulative_precision_graph(percentile, pos_label):
            return self.explainer.plot_cumulative_precision(percentile=percentile, pos_label=pos_label)
        
        @app.callback(
            Output('cumulative-precision-percentile-'+self.name, 'value'),
            [Input('cumulative-precision-cutoff-'+self.name, 'value'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_cumulative_precision_percentile(cutoff, pos_label):
            return self.explainer.percentile_from_cutoff(cutoff, pos_label)


class ClassificationComponent(ExplainerComponent):
    def __init__(self, explainer, title="Classification Plot", name=None,
                    hide_title=False,
                    hide_cutoff=False, hide_percentage=False, hide_selector=False,
                    pos_label=None, cutoff=0.5, percentage=True, **kwargs):
        """Shows a barchart of the number of classes above the cutoff and below
        the cutoff.

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Classification Plot".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            hide_title (bool, optional): hide the title.
            hide_cutoff (bool, optional): Hide cutoff slider. Defaults to False.
            hide_percentage (bool, optional): Hide percentage toggle. Defaults to False.
            hide_selector(bool, optional): hide pos label selector. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. Defaults to explainer.pos_label
            cutoff (float, optional): Cutoff for prediction. Defaults to 0.5.
            percentage (bool, optional): Show percentage instead of counts. Defaults to True.
        """
        super().__init__(explainer, title, name)

        self.cutoff_name = 'classification-cutoff-' + self.name

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.description = """
        Plot showing the fraction of each class above and below the cutoff.
        """
        self.register_dependencies("preds", "pred_probas", "pred_percentiles")

    def layout(self):
        return html.Div([
            make_hideable(
                html.Div([
                    html.H3(self.title, id='classification-title-'+self.name),
                    dbc.Tooltip(self.description, target='classification-title-'+self.name),
                ]), hide=self.hide_title),
            dbc.Row([
                make_hideable(
                    dbc.Col([self.selector.layout()], width=3), hide=self.hide_selector)
            ], justify="end"),
            html.Div([
                dcc.Graph(id='classification-graph-'+self.name,
                            config=dict(modeBarButtons=[['toImage']], displaylogo=False)),
            ], style={'margin': 0}),
            make_hideable(
                html.Div([
                html.Div([
                    html.Label('Cutoff prediction probability:'),
                    dcc.Slider(id='classification-cutoff-'+self.name, 
                                min = 0.01, max = 0.99, step=0.01, value=self.cutoff,
                                marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                        0.75: '0.75', 0.99: '0.99'}, 
                                included=False,
                                tooltip = {'always_visible' : False},
                                updatemode='drag'),
                    
                ], id='classification-cutoff-div-'+self.name),
                dbc.Tooltip(f"Scores above this cutoff will be labeled positive",
                                target='classification-cutoff-div-'+self.name,
                                placement='bottom'),
                ], style={'margin-bottom': 25}), hide=self.hide_cutoff),
            make_hideable(
                html.Div([
                    dbc.FormGroup([
                        dbc.RadioButton(
                            id="classification-percentage-"+self.name, 
                            className="form-check-input", 
                            checked=True
                        ),
                        dbc.Label(
                            "Display percentages",
                            html_for="classification-percentage-"+self.name,
                            className="form-check-label",
                        ),
                        dbc.Tooltip("Do not resize the bar chart by absolute number of observations",
                            target="classification-percentage-"+self.name,)
                    ], check=True),
                ]), hide=self.hide_percentage),
        ])

    def _register_callbacks(self, app):
        @app.callback(
            Output('classification-graph-'+self.name, 'figure'),
            [Input('classification-cutoff-'+self.name, 'value'),
             Input('classification-percentage-'+self.name, 'checked'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_precision_graph(cutoff, percentage, pos_label):
            return self.explainer.plot_classification(
                    cutoff=cutoff, percentage=percentage, pos_label=pos_label)


class RocAucComponent(ExplainerComponent):
    def __init__(self, explainer, title="ROC AUC Plot", name=None, 
                    hide_title=False,
                    hide_cutoff=False, hide_selector=False,
                    pos_label=None, cutoff=0.5, **kwargs):
        """Show ROC AUC curve component

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "ROC AUC Plot".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            hide_title (bool, optional): hide title.
            hide_cutoff (bool, optional): Hide cutoff slider. Defaults to False.
            hide_selector(bool, optional): hide pos label selector. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. Defaults to explainer.pos_label
            cutoff (float, optional): default cutoff. Defaults to 0.5.
        """
        super().__init__(explainer, title, name)

        self.cutoff_name = 'rocauc-cutoff-' + self.name
        
        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.description = """
        """
        self.register_dependencies("preds", "pred_probas", "pred_percentiles")

    def layout(self):
        return html.Div([
            make_hideable(
                html.Div([
                    html.H3(self.title, id='rocauc-title-'+self.name),
                    dbc.Tooltip(self.description, target='rocauc-title-'+self.name),
                ]), hide=self.hide_title),
            dbc.Row([
                make_hideable(
                    dbc.Col([self.selector.layout()], width=3), hide=self.hide_selector)
            ], justify="end"),
            dcc.Graph(id='rocauc-graph-'+self.name,
                        config=dict(modeBarButtons=[['toImage']], displaylogo=False)),
            make_hideable(
                html.Div([
                html.Div([
                    html.Label('Cutoff prediction probability:'),
                    dcc.Slider(id='rocauc-cutoff-'+self.name, 
                                min = 0.01, max = 0.99, step=0.01, value=self.cutoff,
                                marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                        0.75: '0.75', 0.99: '0.99'}, 
                                included=False,
                                tooltip = {'always_visible' : False},
                                updatemode='drag' ),
                ] ,id='rocauc-cutoff-div-'+self.name),
                dbc.Tooltip(f"Scores above this cutoff will be labeled positive",
                                target='rocauc-cutoff-div-'+self.name,
                                placement='bottom'),
                ], style={'margin-bottom': 25}), hide=self.hide_cutoff),
        ])

    def _register_callbacks(self, app):
        @app.callback(
            Output('rocauc-graph-'+self.name, 'figure'),
            [Input('rocauc-cutoff-'+self.name, 'value'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_precision_graph(cutoff, pos_label):
            return self.explainer.plot_roc_auc(cutoff=cutoff, pos_label=pos_label)


class PrAucComponent(ExplainerComponent):
    def __init__(self, explainer, title="PR AUC Plot", name=None,
                    hide_title=False,
                    hide_cutoff=False, hide_selector=False,
                    pos_label=None, cutoff=0.5, **kwargs):
        """Display PR AUC plot component

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer() or RegressionExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "PR AUC Plot".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            hide_title (bool, optional): hide title.
            hide_cutoff (bool, optional): hide cutoff slider. Defaults to False.
            hide_selector(bool, optional): hide pos label selector. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. Defaults to explainer.pos_label
            cutoff (float, optional): default cutoff. Defaults to 0.5.
        """
        super().__init__(explainer, title, name)

        self.cutoff_name = 'prauc-cutoff-' + self.name

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.description = """
        """
        self.register_dependencies("preds", "pred_probas", "pred_percentiles")

    def layout(self):
        return html.Div([
            make_hideable(
                html.Div([
                    html.H3(self.title, id='prauc-title-'+self.name),
                    dbc.Tooltip(self.description, target='prauc-title-'+self.name),
                ]), hide=self.hide_title),
            dbc.Row([
                make_hideable(
                    dbc.Col([self.selector.layout()], width=3), hide=self.hide_selector)
            ], justify="end"),
            dcc.Graph(id='prauc-graph-'+self.name,
                        config=dict(modeBarButtons=[['toImage']], displaylogo=False)),
            make_hideable(
                html.Div([
                    html.Div([
                    html.Label('Cutoff prediction probability:'),
                    dcc.Slider(id='prauc-cutoff-'+self.name, 
                                min = 0.01, max = 0.99, step=0.01, value=self.cutoff,
                                marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                        0.75: '0.75', 0.99: '0.99'}, 
                                included=False,
                                tooltip = {'always_visible' : False},
                                updatemode='drag'),
                    
                    ], id='prauc-cutoff-div-'+self.name),
                    dbc.Tooltip(f"Scores above this cutoff will be labeled positive",
                                target='prauc-cutoff-div-'+self.name,
                                placement='bottom'),
                ], style={'margin-bottom': 25}), hide=self.hide_cutoff),
        ])

    def _register_callbacks(self, app):
        @app.callback(
            Output('prauc-graph-'+self.name, 'figure'),
            [Input('prauc-cutoff-'+self.name, 'value'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_precision_graph(cutoff, pos_label):
            return self.explainer.plot_pr_auc(cutoff=cutoff, pos_label=pos_label)

class ClassifierModelSummaryComponent(ExplainerComponent):
    def __init__(self, explainer, title="Model performance metrics", name=None,
                    hide_title=False,
                    hide_cutoff=False, hide_selector=False,
                    pos_label=None, cutoff=0.5, round=3, **kwargs):
        """Show model summary statistics (accuracy, precision, recall,  
            f1, roc_auc, pr_auc, log_loss) component.

        Args:
            explainer (Explainer): explainer object constructed with either
                        ClassifierExplainer()
            title (str, optional): Title of tab or page. Defaults to 
                        "Model performance metrics".
            name (str, optional): unique name to add to Component elements. 
                        If None then random uuid is generated to make sure 
                        it's unique. Defaults to None.
            hide_title (bool, optional): hide title.
            hide_cutoff (bool, optional): hide cutoff slider. Defaults to False.
            hide_selector(bool, optional): hide pos label selector. Defaults to False.
            pos_label ({int, str}, optional): initial pos label. Defaults to explainer.pos_label
            cutoff (float, optional): default cutoff. Defaults to 0.5.
            round (int): round floats. Defaults to 3.
        """
        super().__init__(explainer, title, name)
        
        self.cutoff_name = 'clas-model-summary-cutoff-' + self.name

        self.selector = PosLabelSelector(explainer, name=self.name, pos_label=pos_label)
        self.description = """
        Shows a list of various performance metrics.
        """

        self.register_dependencies(['preds', 'pred_probas'])

    def layout(self):
        return html.Div([
            make_hideable(
                html.Div([
                    html.H3(self.title, id='clas-model-summary-title-'+self.name),
                    dbc.Tooltip(self.description, target='clas-model-summary-title-'+self.name),
                ]), hide=self.hide_title),
            dbc.Row([

                make_hideable(
                    dbc.Col([self.selector.layout()], width=3), hide=self.hide_selector)
            ], justify="end"),
            html.Div(id='clas-model-summary-div-'+self.name),
            make_hideable(
                html.Div([
                html.Div([
                    html.Label('Cutoff prediction probability:'),
                    dcc.Slider(id='clas-model-summary-cutoff-'+self.name, 
                                min = 0.01, max = 0.99, step=0.01, value=self.cutoff,
                                marks={0.01: '0.01', 0.25: '0.25', 0.50: '0.50',
                                        0.75: '0.75', 0.99: '0.99'}, 
                                included=False,
                                tooltip = {'always_visible' : False},
                                updatemode='drag'),
                ], id='clas-model-summary-cutoff-div-'+self.name),
                dbc.Tooltip(f"Scores above this cutoff will be labeled positive",
                                target='clas-model-summary-cutoff-div-'+self.name,
                                placement='bottom'),
                ], style={'margin-bottom': 25}), hide=self.hide_cutoff),     
        ])
    
    def _register_callbacks(self, app):
        @app.callback(
            Output('clas-model-summary-div-'+self.name, 'children'),
            [Input('clas-model-summary-cutoff-'+self.name, 'value'),
             Input('pos-label-'+self.name, 'value')],
        )
        def update_classifier_summary(cutoff, pos_label):
            metrics_dict = self.explainer.metrics_descriptions(cutoff, pos_label)
            metrics_df = (pd.DataFrame(
                                self.explainer.metrics(cutoff=cutoff, pos_label=pos_label), 
                                index=["Score"])
                              .T.rename_axis(index="metric").reset_index()
                              .round(self.round))
            metrics_table = dbc.Table.from_dataframe(metrics_df, striped=False, bordered=False, hover=False)        
            metrics_table, tooltips = get_dbc_tooltips(metrics_table, 
                                                   metrics_dict, 
                                                   "clas-model-summary-div-hover", 
                                                   self.name)

            return html.Div([
                metrics_table,
                *tooltips
            ])
        