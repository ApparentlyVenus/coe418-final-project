import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os

class IGDBService:
    """
    Service for interacting with IGDB (Internet Game Database) API.
    
    To use IGDB API:
    1. Register at https://dev.twitch.tv/console/apps
    2. Create an application
    3. Get Client ID and Client Secret
    4. Set environment variables: IGDB_CLIENT_ID and IGDB_CLIENT_SECRET
    """
    
    BASE_URL = "https://api.igdb.com/v4"
    AUTH_URL = "https://id.twitch.tv/oauth2/token"
    
    def __init__(self):
        self.client_id = self._read_api_credentials(os.getenv("IGDB_CLIENT_ID_FILE"))
        self.client_secret = self._read_api_credentials(os.getenv("IGDB_CLIENT_SECRET_FILE"))

        if not self.client_id or not self.client_secret:
            raise EnvironmentError("IGDB_CLIENT_ID or IGDB_CLIENT_SECRET missing") 

        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
    
    def _read_api_credentials(self, file_path: Optional[str]) -> Optional[str]:
        if not file_path or not os.path.exists(file_path):
            return None
        try:
            with open(file_path, 'r') as f:
                return f.read().strip()
        except IOError as e:
            print(f"Warning: COuld not read file {file_path}. Error: {e}")
            return None
    

    async def _get_access_token(self) -> str:
        # Check if we have a valid token
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # Get new token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.AUTH_URL,
                params={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials"
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to get IGDB access token: {response.text}")
            
            data = response.json()
            self.access_token = data["access_token"]
            # Set expiration with some buffer (expires_in is in seconds)
            expires_in = data.get("expires_in", 3600)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
            
            return self.access_token
    
    async def _make_request(self, endpoint: str, query: str) -> List[Dict[str, Any]]:
        token = await self._get_access_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/{endpoint}",
                headers={
                    "Client-ID": self.client_id,
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json"
                },
                data=query
            )
            
            if response.status_code != 200:
                raise Exception(f"IGDB API error: {response.text}")
            
            return response.json()
    
    async def search_games(self, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        query = f'''
            search "{search_term}";
            fields name, cover.url, first_release_date, involved_companies.company.name, 
                   genres.name, platforms.name, summary;
            limit {limit};
        '''
        
        return await self._make_request("games", query)
    
    async def get_game_by_id(self, igdb_id: int) -> Optional[Dict[str, Any]]:
        query = f'''
            fields name, cover.url, first_release_date, involved_companies.company.name,
                   genres.name, platforms.name, summary, storyline, rating, rating_count;
            where id = {igdb_id};
        '''
        
        results = await self._make_request("games", query)
        return results[0] if results else None
    
    async def get_popular_games(self, limit: int = 20) -> List[Dict[str, Any]]:
        query = f'''
            fields name, cover.url, first_release_date, involved_companies.company.name,
                   genres.name, platforms.name, rating, rating_count;
            where rating_count > 100;
            sort rating desc;
            limit {limit};
        '''
        
        return await self._make_request("games", query)
    
    def format_game_data(self, igdb_data: Dict[str, Any]) -> Dict[str, Any]:
        # Extract developer (first company involved)
        developer = None
        if "involved_companies" in igdb_data and igdb_data["involved_companies"]:
            companies = igdb_data["involved_companies"]
            if isinstance(companies, list) and len(companies) > 0:
                if "company" in companies[0]:
                    developer = companies[0]["company"].get("name")
        
        # Extract genres
        genres = []
        if "genres" in igdb_data:
            genres = [g.get("name") for g in igdb_data["genres"] if "name" in g]
        
        # Extract platforms
        platforms = []
        if "platforms" in igdb_data:
            platforms = [p.get("name") for p in igdb_data["platforms"] if "name" in p]
        
        # Extract cover image URL
        cover_url = None
        if "cover" in igdb_data and "url" in igdb_data["cover"]:
            # IGDB returns thumbnails, convert to full size
            cover_url = igdb_data["cover"]["url"].replace("t_thumb", "t_cover_big")
            if not cover_url.startswith("https:"):
                cover_url = f"https:{cover_url}"
        
        # Convert release date (Unix timestamp to date string)
        release_date = None
        if "first_release_date" in igdb_data:
            timestamp = igdb_data["first_release_date"]
            release_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        
        return {
            "external_api_id": str(igdb_data.get("id")),
            "title": igdb_data.get("name"),
            "developer": developer,
            "release_date": release_date,
            "cover_image_url": cover_url,
            "genres": genres,
            "platforms": platforms,
            "summary": igdb_data.get("summary"),
            "rating": igdb_data.get("rating")
        }


# Singleton instance
igdb_service = IGDBService()
