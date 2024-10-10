import streamlit as st
import altair as alt
import socket
from services import get_youtube_service, get_wordpress_service, get_comments_as_dataframe
from lib import get_stream_service, bulk_stream, bulk_consume, get_db_connection

# BOxw-XXkjao

st.set_page_config(
    page_title="FeedBeat",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

kafka_service = None
hostname = socket.gethostname()

with st.sidebar:
    app_type_list = [
        "Youtube",
        "Wordpress",
        # "Tiktok",
        # "Instagram",
        # "Facebook",
        # "Twitter",
        # "LinkedIn",
    ]
    
    selected_app = st.selectbox('Select a App', app_type_list, index=len(app_type_list)-1)
    if selected_app == "Youtube":
        text = "Enter the YouTube video ID:"
        st.title('Youtube Comment Scraper')
        service = get_youtube_service()
    elif selected_app == "Wordpress":
        text = "Enter the Wordpress post URL:"
        st.title('Wordpress Comment Scraper')
        service = get_wordpress_service(text)
    else:
        text = "Other apps are not supported yet"

    app_id = st.text_input(text)
    comments = None
    if st.button("Stream"):
        if app_id and selected_app == "Youtube":
            channel_id = service.get_channel_id(app_id)
            youtube_video_stats = {
                'channel_stats': service.get_channel_statistics(channel_id),
                'video_stats': service.get_video_statistics(app_id),
                'comments': service.get_video_comments(app_id)   
            }
            producer = get_stream_service("cs1v3m2mcflfffl9tk60.any.us-east-1.mpx.prd.cloud.redpanda.com:9092", "youtube-comments", type="producer")
            producer.send_message(youtube_video_stats)
        elif app_id and selected_app == "Wordpress":
            comments = service.get_comments(app_id)
        else:
            st.text(text)

    if st.button("Show Comments"):
        consumer = get_stream_service("cs1v3m2mcflfffl9tk60.any.us-east-1.mpx.prd.cloud.redpanda.com:9092", "youtube-comments", type="consumer")
        comments = bulk_consume(consumer)

col = st.columns(1)
with col[0]:
    st.write("Comments")
    st.write(comments)