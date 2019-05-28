import os
import json
from imgurpython import ImgurClient
from common import file_cache, orm, ioutil
from web import settings

def download(source):
    cache_path = ioutil.path(settings.TEMP_DIR, 'imgur', f"{source.legacy_v1_id}-images.json")
    images = {}

    if not ioutil.cached(cache_path):
        images = {'images': get_data(source.origin_path)}
        with open(cache_path, 'w') as data_file:
            results_json = json.dumps(images, indent=4)
            data_file.write(results_json)
    else:
        with open(cache_path) as data_file:
            images = json.load(data_file)

    extract_dir = orm.extract_dir('imgur', source.legacy_v1_id)

    downloaded = []
    imgur_index = 0
    for image in images['images']:
        imgur_index += 1

        web_path = image['link']
        extension = image['extension']
        if 'gifv' in image:
            web_path = image['gifv']
            extension = 'gifv'
        if 'mp4' in image:
            web_path = image['mp4']
            extension = 'mp4'
        image_path = ioutil.path(extract_dir, '{}.{}'.format(image['id'], extension))
        if not ioutil.cached(image_path):
            ioutil.get_file(web_path, image_path)
        entry = {
            'extract_path': image_path,
            'origin_path': web_path,
            'sort_index': imgur_index,
            'content_hash': file_cache.content_hash(image_path)
        }

        downloaded.append(entry)
    return downloaded


def get_data(link):
    client = ImgurClient(settings.IMGUR_CLIENT_ID, settings.IMGUR_CLIENT_SECRET)
    images = []
    if '/a/' in link:
        album_id = link.split('/a/')[1]
        images = client.get_album_images(album_id)
    else:
        parts = link.split('/')
        image_id = parts[-1]
        image_id = image_id.split(".")[0]
        images = [client.get_image(image_id)]
    results = []
    for image in images:
        result = {
            'id': image.id,
            'link': image.link,
            'extension': image.type.split('/')[1]
        }
        if hasattr(image, 'gifv'):
            result['gifv'] = image.gifv
        if hasattr(image, 'mp4'):
            result['mp4'] = image.mp4
        results.append(result)
    return results
