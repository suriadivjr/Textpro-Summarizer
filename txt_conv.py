import json
from w3lib.html import remove_tags, remove_tags_with_content

def converter(fname):
    with open(('./txtpro_webcrawler/txtpro_webcrawler/' + fname + '.json'), 'r') as jsonfile:
        data = jsonfile.read()

    obj = json.loads(data)

    txtfile = open('raw_results.txt', 'a+', encoding="utf-8")
    
    for o in obj:
        txtfile.write(o["title"])
        txtfile.write('\n')

        for content in o["contents"]:
            txtfile.write(content.rstrip())

        txtfile.write('\n')

    txtfile.close()

converter('news_cnnindo')
converter('news_detik')
converter('news_kompas')
converter('news_kumparan')
converter('news_liputan6')
