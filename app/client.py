import os

import httpx

BASE_URL = "https://api.youversion.com"

def _headers() -> dict[ str, str ]:
	app_key = os.getenv( "YOUVERSION_APP_KEY" )
	return { "x-yvp-app-key": app_key }

def get_passage_id( day : int ) -> str:
	response = httpx.get(f"{BASE_URL}/v1/verse_of_the_days/{day}", 
					  headers=_headers())
	response.raise_for_status()
	return response.json()[ "passage_id" ]