import json, os, praw

from django.conf import settings

#from common import ioutil

def reddit_api(source):
    username, password = source.path.split('<->')
    return praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID
        client_secret=settings.REDDIT_CLIENT_SECRET,
        username=username,
        password=password,
        user_agent=settings.REDDIT_USER_AGENT
    )

def get_saves(source):
    saves_cache_path = ioutil.path(config['source_dirs_reddit'], config['reddit_username']+'.json')

    if not ioutil.should_download(config, saves_cache_path) and config['enable_reddit_save_cache']:
        with open(saves_cache_path, 'r') as file_data:
            return json.load(file_data)

    reddit = reddit_api(source)
    saved = reddit.user.me().saved(limit=config['reddit_read_limit'])
    results = {}
    save_index = -1
    for save in saved:
        post_id = save.id
        save_index = save_index + 1
        if post_id in results and not 'refresh' in results[post_id]:
            continue

        result = {
            'reddit_link': save.permalink,
            'reddit_post_id': post_id,
            'sort_index': save_index
        }

        if hasattr(save, 'url'):
            result['internet_link'] = save.url
        if callable(save.permalink):
            result['reddit_link'] = save.permalink(fast=True)
        # Use timestamps instead of result set order
        result['reddit_index'] = result['sort_index']
        results[post_id] = result
    with open(saves_cache_path, 'w') as data_file:
        results_json = json.dumps(results, indent=4)
        data_file.write(results_json)
    return results
