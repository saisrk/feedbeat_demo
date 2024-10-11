import pandas as pd
from lib.sentiment import analyze_comments
from lib.plotting import plot_pie_chart, plot_bar_chart, plot_line_chart


def extract_comment_only(comments):
    return [comment for comment in comments if 'comment' in comment]

def get_yt_comments_as_dataframe(comments):
    # if you find anything other than comments in dataframe then remove it
    comments = extract_comment_only(comments)
    df = pd.DataFrame(comments)
    return df


def get_yt_comments_stats(comments):
    comments = extract_comment_only(comments)
    return analyze_comments(comments)


def get_yt_stats_pie_plot(metrics):
    return plot_pie_chart(metrics)


def get_yt_stats_bar_plot(metrics):
    return plot_bar_chart(metrics)


def get_yt_stats_line_plot(metrics):
    return plot_line_chart(metrics)