# Verse of the Day API

Wraps YouVersion's two-step verse of the day lookup into one endpoint. You give it a day and a version, it gives you back the reference and text.

GET /votd?day=195&version=206

```json
{
  "day": 195,
  "reference": "Revelation 3:20",
  "text": "Behold, I stand at the door and knock...",
  "version_id": 206
}
```

## Setup

Needs Python 3.11+.

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and put your app key in it. `.env` is gitignored so it never gets committed.

## Running

```bash
uvicorn app.main:app --reload
```

## Testing

```bash
python -m pytest
```

Tests mock the YouVersion calls so nothing hits the real API.

## Examples

```bash
curl "http://127.0.0.1:8000/votd"
curl "http://127.0.0.1:8000/votd?day=195&version=206"
curl "http://127.0.0.1:8000/votd?day=0"
```

That last one is invalid and returns a 400:
```json
{ "error": { "code": "INVALID_DAY", "message": "day must be an integer between 1 and 366" } }
```

## Decisions & assumptions

If day is left off I default to today in UTC, since there's no good way to know the caller's timezone. If version is left off I default to 206 (World English Bible) since it's public domain and works with the given key. The cache is just a plain dict in memory keyed by day and version, no TTL, since the calendar doesn't change, so it doesn't need one. Any upstream failure (timeout, bad status, whatever) just becomes a 502, didn't see a need to split those out further. Day gets parsed manually instead of relying on FastAPI to coerce it to int, otherwise something like "abc" would return FastAPI's default error instead of the 400 shape the spec wants.

## If I had more time

Probably a TTL on the cache, some logging around upstream failures, the optional /versions endpoint, and a couple more edge case tests.
