import json
from pathlib import Path

from lanz_mining.params import URL_PREFIX, URL_EXPORT_PATH

link_filter_fn = lambda url: URL_PREFIX in url.get("href")
link_href_fn = lambda url: url.get("href")


def export_url_paths(url_paths: list[str], export_path: str = URL_EXPORT_PATH) -> Path:
    out_path = Path(export_path)
    json.dump({"url_paths": url_paths}, out_path.open("w", encoding="utf-8"), indent=4)
    return out_path
