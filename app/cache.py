_cache: dict[tuple[int, int], dict] = {}


def get(day: int, version_id: int) -> dict | None:
    return _cache.get((day, version_id))


def set(day: int, version_id: int, value: dict) -> None:
    _cache[(day, version_id)] = value