image access wikipedia ddos
https://medium.com/@rrojowiec/tutorial-a-simple-crawler-for-wikipedia-d7b6f6f55d5

For this tutorial (and because Wikipedia has a quite sensitive DDoS pro-tection) the web crawler will be crawling with only one thread (no paralle-lism). Additionally, only links will be queued which haven’t been seen before and point to another page on Wikipedia. To check if the links found are valid for further crawling, the original host is compared to a fixed list of hosts (in this case only https://en.wikipedia.org).



Avoid to many parallel requests as this might activate DDoS protection

# requests being blocked by 403
we have to assign a header https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy

Python
In Python, you can use the Requests library to set a header:
```
import requests

url = 'https://example/...'
headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}

response = requests.get(url, headers=headers)
```

# process
image was minified so I get the article, then the title via tag class - mw-page-title-main

and I get the metadata of this info via this API=https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles=


note that no political view was applied here since I acquired the images via random article access on wiki API.