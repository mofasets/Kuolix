class AppState:
    """
    """
    def __init__(self):
        self.user_profile = None

        self.explore_items = []
        self.explore_last_image_b64 = None
        self.explore_img_description = ''
        
        self.search_query = ""
        self.search_results = []

app_state = AppState()