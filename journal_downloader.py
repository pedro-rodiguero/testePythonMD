NOME_DO_CANDIDATO = 'Pedro Menezes Rodiguero'
EMAIL_DO_CANDIDATO = 'pedro.m.rodiguero@gmail.com'

from ctypes import sizeof
from errno import ERANGE
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from stat import FILE_ATTRIBUTE_DEVICE
from time import sleep
from typing import Dict, List, Tuple

import requests
import datetime

MAIN_FOLDER = Path(__file__).parent.parent

x = xrange(0, sizeof['diaries'])

def request_journals(start_date, end_date):
    url = 'https://engine.procedebahia.com.br/publish/api/diaries'

    r = requests.post(url, data={"cod_entity": '50', "start_date": start_date,
                                 "end_date": end_date})
    if r.status_code == 200:
        return r.json()
    elif r.status_code == 400:
        sleep(10)
        return request_journals(start_date, end_date)
    return {}

editions = request_journals()

def download_jornal(edition, path):
    url = 'http://procedebahia.com.br/irece/publicacoes/Diario%20Oficial' \
          '%20-%20PREFEITURA%20MUNICIPAL%20DE%20IRECE%20-%20Ed%20{:04d}.pdf'.format(int(edition))
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        with open(path, 'wb') as writer:
            writer.write(r.content)
        return edition, path
    return edition, ''


def download_mutiple_jornals(editions, paths):
    threads = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for edition, path in zip(editions, paths):
            threads.append(executor.submit(download_jornal, edition, path))

        results = []
        for task in as_completed(threads):
            results.append(task.result())

    results = [[r for r in results if r[0] == e][0] for e in editions]
    return [r[1] for r in results]


class JournalDownloader:
    def __init__(self):
        self.pdfs_folder = MAIN_FOLDER / 'pdfs'
        self.jsons_folder = MAIN_FOLDER / 'out'

        self.pdfs_folder.mkdir(exist_ok=True)
        self.jsons_folder.mkdir(exist_ok=True)

    def get_day_journals(self, year: int, month: int, day: int) -> List[str]:
        # TODO: get all journals of a day, returns a list of JSON paths
        date = datetime.date_format(year, month, day)

        while(x):
            list.append(self.dump_json)

            edition_day_journal = editions['diaries'][x]['edition']
            file = edition_day_journal['file_name']
            
            list.append(self.dump_json())
            download_jornal(editions['diaries'][x]['edition'], file)
        pass

    def get_month_journals(self, year: int, month: int) -> List[str]:
        # TODO: get all journals of a month, returns a list of JSON paths
        
        date_start = datetime.date_format(year, month)
        date_finish = datetime.date_format(year, month)
        
        edition_month_journal = request_journals(date_start, date_finish)
        
        while(x):
            edition = editions['diaries'][x]['edition']
            file = edition['file_name']
            
            list.append(self.dump_json())
            download_jornal(edition_month_journal['diaries'][x]['edition'], file)
        pass

    def get_year_journals(self, year: int) -> List[str]:
        # TODO: get all journals of a year, returns a list of JSON paths
        
        date_start = datetime.date_format(year)
        date_finish = datetime.date_format(year)
        
        edition_year_journal = request_journals(date_start, date_finish)
        
        while(x):
            edition = editions['diaries'][x]['edition']
            file = edition['file_name']
            
            list.append(self.dump_json())
            download_jornal(edition_year_journal['diaries'][x]['edition'], file)
        pass

    @staticmethod
    def parse(response: Dict) -> List[Tuple[str, str]]:
        # TODO: parses the response and returns a tuple list of the date and edition
        pass

    def download_all(self, editions: List[str]) -> List[str]:
        # TODO: download journals and return a list of PDF paths. download in `self.pdfs_folder` folder
        #  OBS: make the file names ordered. Example: '0.pdf', '1.pdf', ...
        
        while():
            index = 0
            download_jornal(index, self.pdfs_folder)
            ++index
            print(list())
        pass

    def dump_json(self, pdf_path: str, edition: str, date: str) -> str:
        if pdf_path == '':
            return ''
        output_path = self.jsons_folder / f"{edition}.json"
        data = {
            'path': str(pdf_path),
            'name': str(edition),
            'date': date,
            'origin': 'Irece-BA/DOM'
        }
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data,
                                  indent=4, ensure_ascii=False))
        return str(output_path)

def main():
    JournalDownloader().get_day_journals(2022, 2, 22)
    
    JournalDownloader().get_month_journals(2022, 1, 2022, 2)
    
    JournalDownloader().get_year_journals(2022)
    
if __name__ == '__main__':
    main()