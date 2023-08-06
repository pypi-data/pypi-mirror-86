import requests
from typing import Union, List
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"


def get_shards(council: str, shards: Union[List[str], str], resolution_id: str = None) -> str:
    if type(shards) is str:
        shards = [shards]
    payloads = {"wa": council, "q": "+".join(shards)}
    if resolution_id is not None:
        payloads["id"] = resolution_id
    headers = {
        "User-Agent": userAgent}
    res = requests.get("https://www.nationstates.net/cgi-bin/api.cgi", params=payloads, headers=headers)
    return str(res.content)
