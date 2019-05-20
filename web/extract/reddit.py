import json, os, praw
from web import settings
from common import ioutil, file_cache, orm

def reddit_api(source):
    username, password = source.origin_path.split('<->')
    return praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        username=username,
        password=password,
        user_agent=settings.REDDIT_USER_AGENT
    )

def get_saves(source):
    username, password = source.origin_path.split('<->')
    #saves_cache_path = ioutil.path(settings.REDDIT_SAVES_DIR, f"{username}.json")

    #if ioutil.cached(saves_cache_path):
    #    return ioutil.read_json(saves_cache_path)

    reddit = reddit_api(source)
    saved = reddit.user.me().saved(limit=settings.REDDIT_SAVE_READ_LIMIT)
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
            'sort_index': save_index,
            'created': save.created
        }
        if hasattr(save, 'title'):
            result['title'] = save.title
        if hasattr(save, 'url'):
            result['internet_link'] = save.url
        if callable(save.permalink):
            result['reddit_link'] = save.permalink(fast=True)
        result['reddit_index'] = result['sort_index']
        results[post_id] = result

    #ioutil.write_json(saves_cache_path, results)

    return results

def get_media(source):
    extract_dir = orm.extract_dir('reddit', source.legacy_v1_id)
    file_name = source.origin_path.split('/')[-1]

    extract_path = os.path.join(extract_dir, file_name)

    if not ioutil.cached(extract_path):
        ioutil.get_file(source.origin_path, extract_path)

    return {
        'extract_path': extract_path,
        'content_hash': file_cache.content_hash(extract_path)
    }
