"""
Flickr download tool

- Get API key: https://www.flickr.com/services/apps/by/me
- Install pip package: pip install flickr_api
"""
import os
import flickr_api

API_KEY = "enter api key here"
API_SECRET = "enter api secret here"

# Eg: https://www.flickr.com/people/13623257@N03/
FLICKR_PEOPLE_URL = "enter flickr people url here"

flickr_api.set_keys(api_key=API_KEY, api_secret=API_SECRET)
os.makedirs(os.path.join(os.getcwd(), "photos"), exist_ok=True)

user = flickr_api.Person.findByUrl('')
pages_nb = user.getPublicPhotos().info.pages
total = user.getPublicPhotos().info.total
current = 0

for page_nb in range(1, pages_nb+1):
    for index, photo in enumerate(user.getPublicPhotos(page=page_nb)):
        sizes = photo.getSizes()
        biggest_size = list(sizes.keys())[-1]
        filename = photo.title.replace("/", "-") + "_" + photo.id

        current += 1
        try:
            print(f"{current}/{total}", filename)
            photo.save(os.path.join(os.getcwd(), "photos", filename), size_label = biggest_size)
        except Exception as e:
            print(e)
