
def get_token_body(username, password) -> str:
    return "grant_type=password&username=" + username + "&password=" + password 

def get_headers(api_key) -> dict:
    return {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-us",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Flexit%20GO/2.0.6 CFNetwork/1128.0.1 Darwin/19.6.0",
        "Ocp-Apim-Subscription-Key": api_key
    }

def get_headers_with_token(api_key, token) -> dict:
    headers = get_headers(api_key)
    headers['Authorization'] = "Bearer " + token
    return headers