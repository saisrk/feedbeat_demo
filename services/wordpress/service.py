import requests

class WordpressService:
    def __init__(self, uri):
        self.base_url = f"{uri}/wp-json/wp/v2".format(uri)

    def get_comments(self, post_id):
        url = f"{self.base_url}/comments"
        response = requests.get(url)
        return response.json()
    
    def get_posts(self):
        url = f"{self.base_url}/posts"
        response = requests.get(url)
        return response.json()
    
def get_wordpress_service(uri):
    return WordpressService(uri)