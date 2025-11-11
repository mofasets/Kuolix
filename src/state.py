import httpx

class AppState:
    """
    """
    def __init__(self):
        self.api_client: httpx.AsyncClient | None = None # Cliente para hacer las llamadas a la API
        self.token: str | None = None
        self.user_profile = None
        self.current_user = None
        
        self.explore_items = []
        self.explore_last_image_b64 = None
        self.explore_img_description = {}
        
        self.search_query = ""
        self.search_results = []
        
        self.users_list = []

app_state = AppState()