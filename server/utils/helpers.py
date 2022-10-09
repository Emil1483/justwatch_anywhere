def simplify_url(url):
    split = url.split('/')
    for part in split:
        if '.' in part:
            return part
    raise ValueError(f'{url} could not be simplified')
