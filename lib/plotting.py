import plotly.express as px
import plotly.graph_objects as go


def plot_pie_chart(metrics: dict):
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=['Positive', 'Negative', 'Neutral'],
        values=[metrics['positive'], metrics['negative'], metrics['neutral']],
        hole=0.5
    ))
    return fig

def plot_bar_chart(metrics: dict):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Positive', 'Negative', 'Neutral'],
        y=[metrics['positive'], metrics['negative'], metrics['neutral']],
    ))
    return fig

def plot_line_chart(metrics: dict):
    fig = go.Figure()
    fig.add_trace(go.Line(
        x=['Positive', 'Negative', 'Neutral'],
        y=[metrics['positive'], metrics['negative'], metrics['neutral']],
    ))
    return fig

def plot_sentiment_analysis(metrics: dict):
    fig = go.Figure()
    pie_chart = plot_pie_chart(metrics)
    bar_chart = plot_bar_chart(metrics)
    line_chart = plot_line_chart(metrics)
    fig.add_trace(pie_chart.data[0])
    fig.add_trace(bar_chart.data[0])
    fig.add_trace(line_chart.data[0])
    return fig

