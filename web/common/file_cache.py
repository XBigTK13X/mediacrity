from common import ioutil

import hashlib
import os

from web import settings

def hash(slug):
	hasher = hashlib.sha1()
	hasher.update(slug.encode('utf-8'))
	return hasher.hexdigest()


def get_path(cache_id):
	path = ioutil.path(settings.CACHE_DIR, cache_id[0], cache_id[1])
	ioutil.mkdir(path)
	return ioutil.path(path, cache_id)


def set(cache_id):
	path = get_path(cache_id)
	with open(path, 'w') as file_data:
		file_data.write('')


def get(cache_id):
	path = get_path(cache_id)
	with open(path, 'r') as file_data:
		return file_data.read()


def exists(cache_id):
	path = get_path(cache_id)
	return os.path.isfile(path)
