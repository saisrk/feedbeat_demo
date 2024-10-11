import streamlit as st
import altair as alt
from services import (
    get_youtube_service, get_wordpress_service, get_yt_comments_as_dataframe,
    get_yt_comments_stats, get_yt_stats_pie_plot, get_yt_stats_bar_plot, get_yt_stats_line_plot, 
    bulk_yt_stream, bulk_yt_consume, get_yt_video_ids, view_yt_video, add_yt_video_id
)
from lib import (
    get_stream_service, get_db_connection, get_overall_sentiment
)

st.set_page_config(
    page_title="FeedBeat",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")   

kafka_service = None
selected_row = -1
db = get_db_connection('postgresql://postgres:postgres@localhost:5432/postgres')
db.connect()

# Initialize your session state variables
if 'app_id' not in st.session_state:
    st.session_state.app_id = ''

def clear_app_id():
    st.session_state.app_id = ''

with st.sidebar:
    st.write("FEEDBEAT")
    app_type_list = [
        "Youtube",
        # "Wordpress",
        # "Tiktok",
        # "Instagram",
        # "Facebook",
        # "Twitter",
        # "LinkedIn",
    ]
    
    selected_app = st.selectbox('Select a App', app_type_list, index=len(app_type_list)-1)
    if selected_app == "Youtube":
        text = "Enter the YouTube video ID:"
        st.title('Youtube Feed Beat')
        service = get_youtube_service()
    elif selected_app == "Wordpress":
        text = "Enter the Wordpress post URL:"
        st.title('Wordpress Comment Scraper')
        service = get_wordpress_service(text)
    else:
        text = "Other apps are not supported yet"

    app_id = st.text_input(text, value=st.session_state.app_id, label_visibility="collapsed")
    comments = None
    metrics = None

    if st.button("Add To FeedBeat"):
        # Save the app_id to database
        add_yt_video_id(db, app_id)
        channel_id = service.get_channel_id(app_id)
        youtube_video_stats = {
            'channel_stats': service.get_channel_statistics(channel_id),
            'video_stats': service.get_video_statistics(app_id),
            'comments': service.get_video_comment_stats(app_id)   
        }
        producer = get_stream_service("cs1v3m2mcflfffl9tk60.any.us-east-1.mpx.prd.cloud.redpanda.com:9092", "youtube-comments", type="producer")
        producer.send_message({"video_stats": youtube_video_stats['video_stats'], "video_id": app_id})
        producer.send_message({"channel_stats": youtube_video_stats['channel_stats'], "video_id": app_id})
        bulk_yt_stream(producer, youtube_video_stats['comments'])
        producer.flush()

if selected_app == "Youtube":
    yt_video_ids = get_yt_video_ids(db)
    st.write('List of videos' if not yt_video_ids.empty else 'No videos added yet')
    row = st.dataframe(yt_video_ids, on_select='rerun', selection_mode="single-row")
    selected_row = row.selection['rows'][0] if len(row.selection['rows']) > 0 else None
    if selected_row is not None and selected_row > -1:
        st.write(f"Viewing video {yt_video_ids.iloc[selected_row]['video_id']}")
        consumer = get_stream_service("cs1v3m2mcflfffl9tk60.any.us-east-1.mpx.prd.cloud.redpanda.com:9092", "youtube-comments", type="consumer")
        comments = bulk_yt_consume(consumer)
        metrics = get_yt_comments_stats(comments)

    st.write("SENTIMENT ANALYSIS") if metrics else ''

    col = st.columns(3)
    with col[0]:
        if comments:
            plots = get_yt_stats_pie_plot(metrics)
            st.write(plots)
    with col[1]:
        if comments:    
            st.write(get_yt_stats_bar_plot(metrics))

    with col[2]:
        if comments:    
            st.write(get_yt_stats_line_plot(metrics))
            
    if comments:   
        overall_sentiment = get_overall_sentiment(metrics)
        st.write(overall_sentiment) 
        st.write("COMMENTS")
        st.write(get_yt_comments_as_dataframe(comments))