import urlparse

def extract_hostname(o):
  hostname = urlparse.urlparse(o.url).hostname
  if hostname.startswith('www.'):
    return hostname[4:]
  return hostname

def extract_base_hostname(o):
  hostname = extract_hostname(o)
  return '.'.join(hostname.split('.')[-2:])
