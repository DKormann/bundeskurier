import requests


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


if __name__ == "__main__":
    import sys
    print(BT.get_newest(int(sys.argv[1]) if len(sys.argv) > 1 else 0))
