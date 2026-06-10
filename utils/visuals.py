import plotly.express as px
import streamlit as st

def plot_donut_chart(df, names_col, values_col, title, hole=0.4, colors=None):
    if colors is None:
        colors = px.colors.qualitative.Pastel
        
    fig = px.pie(df, names=names_col, values=values_col, title=title, hole=hole, color_discrete_sequence=colors)
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10))
    return fig

def plot_bar_chart(df, x_col, y_col, title, color_col=None, colorscale='Blues', horizontal=False):
    orientation = 'h' if horizontal else 'v'
    
    fig = px.bar(df, x=x_col, y=y_col, title=title, text_auto='.2s', color=color_col if color_col else y_col, color_continuous_scale=colorscale, orientation=orientation)

    if horizontal:
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        
    return fig

def plot_3d_scatter(df, x_col, y_col, z_col, color_col, title, height=800):
    fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col, color=color_col, size_max=10, opacity=0.7, title=title, color_discrete_sequence=px.colors.qualitative.Set1)
                        
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)", 
        scene=dict(bgcolor="rgba(0,0,0,0)")
    )
    return fig

def plot_boxplot(df, x_col, y_col, color_col, title, log_y=False, category_orders=None, color_map=None, y_tickformat=None):
    fig = px.box(df, x=x_col, y=y_col, color=color_col, title=title, points='outliers', log_y=log_y, category_orders=category_orders, color_discrete_map=color_map) 
    
    if y_tickformat:
        fig.update_layout(yaxis_tickformat=y_tickformat)
        
    return fig

def plot_heatmap(df, x_col, y_col, title, z_col=None, histfunc=None, colorscale='Plasma'):
    fig = px.density_heatmap(df, x=x_col, y=y_col, z=z_col, histfunc=histfunc, title=title, color_continuous_scale=colorscale)
    return fig

def plot_scatter(df, x_col, y_col, color_col, title, size_col=None, opacity=0.7, color_map=None, colors=None):
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col, title=title, opacity=opacity, color_discrete_map=color_map, color_discrete_sequence=colors, size_max=30 if size_col else None)
    return fig

def plot_violin(df, x_col, y_col, color_col, title, box=True, points=False):
    fig = px.violin(df, x=x_col, y=y_col, color=color_col, box=box, points=points, title=title)
    return fig