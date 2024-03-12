import requests
import random


class BT:
    api_key = "rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF"

    @classmethod
    def get_newest_item(cls, skip=0):
        url = f'https://search.dip.bundestag.de/api/v1/plenarprotokoll-text/?apikey={cls.api_key}'
        response = requests.get(url)
        json = response.json()
        for item in json['documents']:
            if 'text' in item:
                skip -= 1
                if skip <= 0:
                    return item

    @classmethod
    def get_newest(cls, skip=0):
        item = cls.get_newest_item(skip)
        result = '\n'.join([
            f'# {item["dokumentart"]} {item["datum"]}\n',
            f'Vorgangsbezug:',
            *[f'- {x["titel"]} ({x["vorgangstyp"]})' for x in item["vorgangsbezug"]],
            f'\n## {item["titel"]}\n',
            f'{item["text"]}',
        ])
        return result
    
    @classmethod
    def get_newest_short(cls, skip=0):
        item = cls.get_newest_item(skip)
        # get random 5 sentences
        text = ' '.join(x.strip() for x in item['text'].split('\n') if x.strip() != '')
        sentences = ['']
        # join sentences that are less than 5 chars
        short_text = ''
        while '. '*3 not in short_text and len(short_text) < 100:
            for sentence in text.split('. ')[::-1]:
                if len(sentence) < 5 or sentence[-1] in '0123456789' or sentence[-2:] in ['Dr', 'Nr', 'zB']:
                    sentences[-1] += '. ' + sentence
                else: sentences.append(sentence)
            sentences = sentences[::-1]
            start = random.randint(10, len(sentences) - 20)
            short_text = '. '.join(sentences[start:start+10]) + '.'
        result = '\n'.join([
            f'# {item["dokumentart"]} {item["datum"]}\n',
            f'Vorgangsbezug:',
            *[f'- {x["titel"]} ({x["vorgangstyp"]})' for x in item["vorgangsbezug"]],
            f'\n## Zufälliger Auszug aus: {item["titel"]}\n',
            f'{short_text}',
        ])
        return result
        


if __name__ == "__main__":
    import sys
    print(BT.get_newest_short(int(sys.argv[1]) if len(sys.argv) > 1 else 0))
