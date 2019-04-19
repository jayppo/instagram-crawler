from __future__ import unicode_literals

import multiprocessing
from builtins import open

from inscrawler import InsCrawler
import sys
import argparse
import json
from io import open
import urllib.request
import os
import tqdm
import numpy

username = 'i_icaruswalks'
post_count = 1
output_path = 'output'


def usage():
    return '''
        python crawler.py posts -u cal_foodie -n 100 -o ./output
        python crawler.py posts_full -u cal_foodie -n 100 -o ./output
        python crawler.py profile -u cal_foodie -o ./output
        python crawler.py hashtag -t taiwan -o ./output

        The default number for fetching posts via hashtag is 100.
    '''


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


def output(data, filepath):
    out = json.dumps(data, ensure_ascii=False)
    if filepath:
        with open(filepath, 'w', encoding='utf8') as f:
            f.write(out)
    else:
        print(out)


def get_posts_by_user(username, number, detail, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_user_posts(username, number, detail)


def crawl_image_one(x, out_path):
    fname = x['img_urls'].split('/')[-1].split('.jpg')[0] + '.jpg'
    urllib.request.urlretrieve(x['img_urls'], os.path.join(out_path, fname))


def crawl_and_save(username, out_path, num=100):
    # Create when directory does not exist
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    data_raw = get_posts_by_user(username, num, 'posts', False)
    output(data_raw, os.path.join(out_path, username + '.json'))
    cores = 4

    with multiprocessing.Pool(cores) as pool:
        tqdm.tqdm(pool.starmap(crawl_image_one, zip(data_raw, out_path)), total=len(data_raw))
        # df = pd.concat(r)
        pool.close()
        pool.join()


def json_to_address(json_path):
    with open(json_path, 'rt', encoding='UTF-8') as json_file:
        json_data = json.load(json_file)

        json_string = json_data['img_urls']
        return json_string


def json_to_dict(json_path):
    with open(json_path, 'rt', encoding='UTF-8') as json_file:
        json_data = json.load(json_file)  # json 데이터를 파싱

        # print(type(json_data))
        # print(json_data)
        return json_data


def my_func(username, json_path, out_path, num=4):
    # debug_str = json_to_address('output/i_icaruswalks.json')
    debug_str = json_to_dict(json_path)
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    # print(debug_str)
    # print(debug_str[0]['img_url'])

    print(len(debug_str))
    for dic in debug_str:
        filename = username + '-' + dic['img_url'].split('/')[-1].split('.jpg')[0] + '.jpg'
        print(filename)
        urllib.request.urlretrieve(dic['img_url'], os.path.join(out_path, filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Instagram Crawler',
                                     usage=usage())
    #
    # args = parser.parse_args()
    # output(
    #     get_posts_by_user(
    #             username,
    #             post_count,
    #             'posts',
    #             True
    #     ),
    #     output_path)
    # crawl_and_save(username, output_path, post_count)
    my_func(username, 'output/1.json', output_path, post_count)
