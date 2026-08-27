from app import cache, client


def get_verse_of_the_day(day: int, version_id: int) -> dict:
    cached = cache.get(day, version_id)
    if cached is not None:
        return cached

    passage_id = client.get_passage_id(day)
    passage = client.get_passage_text(version_id, passage_id)
    result = passage  # change day, reference, text, version_id

    cache.set(day, version_id, result)
    return result