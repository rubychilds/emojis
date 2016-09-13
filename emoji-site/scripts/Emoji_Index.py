from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import pandas as pd
import simplejson as json

es = Elasticsearch()
EMOJI_INDEX_ALIAS = 'emojis'
EMOJI_DOC = 'emoji'


def _delete_past_alias_references(self):
    if es.indices.exists_alias(name=EMOJI_INDEX_ALIAS):
        old_index_names = es.indices.get_alias(name=EMOJI_INDEX_ALIAS).keys()
        for index_name in old_index_names:
            try:
                es.indices.delete_alias(index=index_name,
                                        name=EMOJI_INDEX_ALIAS)
            except Exception as error:
                print(error)
    return


def _add_alias(index_name):
    try:
        es.indices.put_alias(index=index_name, name=EMOJI_INDEX_ALIAS)
    except Exception as error:
        print(error)


def main():
    data = pd.read_csv('data/emoji_lookup.csv').drop('Unnamed: 0', axis=1)
    data['name'] = data['name'].apply(lambda x: x.replace('\n', ' ').strip())

    data = json.loads(data.to_json(orient='index'))
    now = datetime.datetime.now()
    EMOJI_INDEX_NAME = EMOJI_INDEX_ALIAS + '-' + \
        now.strftime('%Y-%m-%d-%H:%M:%S')

    es.indices.create(index=EMOJI_INDEX_NAME, ignore=400,
                      body=json.loads(open('emoji_mapping.json').read()))
    data = [{"_index": EMOJI_INDEX_NAME,
             "_type": EMOJI_DOC,
             "_body": v} for v in data.values()]

    chunks = 1000
    for i in range(0, len(data), chunks):
        part_data = data[i:i+chunks]
        helpers.bulk(es, part_data)


def test_index():
    doc = {}
    res = es.index(index=EMOJI_INDEX_ALIAS,
                   doc_type=EMOJI_DOC, body=doc)
    res = es.get(index=EMOJI_INDEX_ALIAS, doc_type=EMOJI_DOC, id=1)
    es.indices.refresh(index=EMOJI_INDEX_ALIAS)
    res = es.search(index=EMOJI_INDEX_ALIAS, body={"query": {"match_all": {}}})
    print(res)
