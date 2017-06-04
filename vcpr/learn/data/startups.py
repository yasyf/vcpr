from ... import constants
import requests, urllib

URL = 'https://api.crunchbase.com/v/3/organizations'
LIMIT = 20 ** 4

def url(city, page):
  args = {
    'user_key': constants.CB_API_KEY,
    'sort_order': 'created_at DESC',
    'organization_types': 'company',
    'page': page,
  }
  if city:
    args['locations'] = city
  return URL + '?' + urllib.urlencode(args)

def urls(page):
  return [url('San Francisco', page), url('Boston', page), url('New York City', page), url('', page)]

def download():
  with open(constants.STARTUPS, 'w') as f:
    page = 1
    seen = set()
    while len(seen) < LIMIT:
      print('Page: {}'.format(page))
      for url in urls(page):
        response = requests.get(url).json()
        if 'data' not in response:
          continue
        for item in response['data']['items']:
          if not item['properties'] or not item['properties']['domain']:
            continue
          domain = item['properties']['domain'].lower()
          if domain not in seen:
            f.write(domain + '\n')
            seen.add(domain)
      page += 1

if __name__ == '__main__':
  download()
