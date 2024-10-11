import pandas as pd
import streamlit as st

def add_yt_video_id(conn, video_id):
    conn.insert("public.youtube_video_ids", video_id)

def view_yt_video(selected_row, yt_video_ids):
    st.write(f"Viewing video {yt_video_ids.loc[selected_row]['video_id']}")

def get_yt_video_ids(conn):
    all_yt_ids = conn.get_all_ids("public.youtube_video_ids")
    yt_df = pd.DataFrame(all_yt_ids, columns=["id", "video_id", "channel_id"])
    return yt_df