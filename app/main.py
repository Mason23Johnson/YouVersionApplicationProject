from fastapi import FastAPI

from app import service

app = FastAPI()

@app.get("/verse_of_the_day/{day}/{versionid}")
async def verse_of_the_day(day: int, versionid: int):
	passage = service.get_verse_of_the_day(day, versionid)
	return passage
