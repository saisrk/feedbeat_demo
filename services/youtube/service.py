import googleapiclient.discovery

class YoutubeService:
    def __init__(self):
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey='AIzaSyCETNXLNfEQ3sylHHjLTZtg9VhHkuKNVjE')

    def get_video_comments(self, video_id):
        """
        Get comments from a YouTube video using the YouTube Data API.

        Args:
            video_id (str): The ID of the YouTube video.
        """
        comments = []
        next_page_token = None

        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "order": "relevance",
            "textFormat": "plainText"
        }

        while True:
            # Update params with page token if it exists
            if next_page_token:
                params["pageToken"] = next_page_token

            # Make the API request
            response = self.youtube.commentThreads().list(**params).execute()

            # Extract comments and authors from the response
            for item in response.get("items", []):
                comments.append({
                    "comment": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                    "author": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                    "likes": item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                    "published_date": item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                    "updated_date": item["snippet"]["topLevelComment"]["snippet"]["updatedAt"],
                    "replies": item["snippet"]["totalReplyCount"]
                })

            # Check if there are more pages
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return comments
    
    def get_channel_id(self, video_id):
        """
        Get the channel ID from a YouTube video using the YouTube Data API.

        Args:
            video_id (str): The ID of the YouTube video.
        """
        response = self.youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        return response['items'][0]['snippet']['channelId'] if response['items'] else None

    def get_video_statistics(self, video_id):
        """
        Get stats from a YouTube video using the YouTube Data API.

        Args:
            video_id (str): The ID of the YouTube video.
        """
        response = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        ).execute()

        return response['items'][0]['statistics']

    def get_channel_statistics(self, channel_id):
        """
        Get stats from a YouTube channel using the YouTube Data API.

        Args:
            channel_id (str): The ID of the YouTube channel.
        """
        channel_stats = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id
        ).execute()

        channel_title = channel_stats['items'][0]['snippet']['title']
        video_count = channel_stats['items'][0]['statistics']['videoCount']
        channel_logo_url = channel_stats['items'][0]['snippet']['thumbnails']['high']['url']
        channel_created_date = channel_stats['items'][0]['snippet']['publishedAt']
        subscriber_count = channel_stats['items'][0]['statistics']['subscriberCount']
        channel_description = channel_stats['items'][0]['snippet']['description']
        

        channel_info = {
            'channel_title': channel_title,
            'video_count': video_count,
            'channel_logo_url': channel_logo_url,
            'channel_created_date': channel_created_date,
            'subscriber_count': subscriber_count,
            'channel_description': channel_description
        }

        return channel_info
    
def get_youtube_service():
    return YoutubeService()