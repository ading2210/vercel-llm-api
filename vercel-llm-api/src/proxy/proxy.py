import requests, random, re

def fetch_proxy_list(protocol):
    response = requests.get(f'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/{protocol}.txt')
    response.raise_for_status()
    return [f'{protocol}://{line.strip()}' for line in response.text.split('\n')]

protocols = ['socks5', 'socks4', 'http']
proxies = []

for protocol in protocols:
    proxies.extend(fetch_proxy_list(protocol))


def get_proxied_session() -> requests.Session:
    proxy = random.choice(proxies)
    
    session = requests.Session()
    session.proxies = {'http': proxy}

    session.headers.update({
        "X-Forwarded-For": re.search(r'(\d+\.\d+\.\d+\.\d+)', proxy).group(1),
    })
    
    return session


def get_random_proxy() -> str:
    return random.choice(proxies)
