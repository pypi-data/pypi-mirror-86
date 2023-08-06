from requests import get

def getPaginatedResults(request_url):
    r = get(request_url)
    results = r.json()["results"]
    while r.json()["next"]:
        r = get(r.json()["next"])
        results.extend(r.json()["results"])
    return results

class Url:
    def __init__(self):
        self.url = 'https://educationdata.urban.org/api/v1/{topic}'

    def topic(self, t):
        self.url = self.url.format(topic=t)
        return self

    def source(self, s):
        self.url += '/{source}'.format(source=s)
        return self

    def endpoint(self, e):
        self.url += '/{endpoint}'.format(endpoint=e)
        return self

    def year(self, y):
        self.url += '/{year}'.format(year=y)
        return self

    def grade(self, g):
        self.url += '/grade-' + str(g)
        return self

    def disaggregations(self, ds):
        for d in ds:
            self.url += '/{disaggregation}'.format(disaggregation=d)
        return self
        
    def filters(self, fs):
        self.url += '?'
        for k, v in fs.items():
            self.url += k + '=' + str(v) + '&'
        return self.url