import os
import hashlib
import json

from web import settings

def mkdir(path, clean=False):
	if clean:
		try:
			shutil.rmtree(path)
		except:
			swallow = True

	try:
		os.makedirs(path)
	except:
		swallow = True


def path(*targets):
	result = os.path.join(targets[0], targets[1])
	for ii in range(2, len(targets)):
		result = os.path.join(result, targets[ii])
	return result


def path_compact(*targets):
	targets = list(targets)
	if len(targets) == 1:
		targets = targets[0].split('/')
	# Given a path to a cache_id directory, split the path into a/b/abcdef..xyz format
	last = targets[-1]
	targets[-1] = f"{last[0]}"
	targets.append(f"{last[1]}")
	targets.append(f"{last[2]}")
	targets.append(f"{last[3]}")
	targets.append(last)
	targets[0] = '/'+targets[0]
	return path(*targets)

def cached(path):
	return os.path.isfile(path) and settings.FILE_CACHE_ENABLED

def write_json(path, dict_content):
    if not os.path.isfile(path):
        mkdir(os.path.dirname(path))
    with open(path, 'w') as data_file:
        content_json = json.dumps(dict_content, indent=4)
        data_file.write(content_json)

def read_json(path):
    with open(path, 'r') as file_data:
        return json.load(file_data)
