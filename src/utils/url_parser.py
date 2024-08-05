import tldextract

def parse_url(url):
    extracted = tldextract.extract(url)
    domain = f"{extracted.domain}.{extracted.suffix}"
    full_url = url if url.startswith(('http://', 'https://')) else f"https://{url}"
    return domain, full_url