from common import ioutil
import hashlib
import os
import sys
from web import settings

BUF_SIZE = 65536  # 64kb

def hash(slug):
	hasher = hashlib.sha1()
	hasher.update(slug.encode('utf-8'))
	return hasher.hexdigest()

def content_hash(path):
	hasher = hashlib.sha1()
	with open(path, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			hasher.update(data)
	return hasher.hexdigest()

def exists(cache_id):
	path = get_path(cache_id)
	return os.path.isfile(path)
