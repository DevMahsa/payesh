from venv import logger

import sys
from django.core.management.base import BaseCommand
import pandas as pd
import requests
import json


def read_from_csv():
    where_file()


def where_file():
    file = '/home/mahsa/Desktop/phd_std_file.csv'
    file = '/home/mahsa/Downloads/new_phd_file.csv'
    xl = pd.read_csv(file)
    read_csv_action(file)


def read_csv_action(file):
    try:
        print('scopus-result:name:surname:stdid:auid:subject-area:doc-count:h-index:citation')

        for i in range(1, list(pd.read_csv(file)._values).__len__()):
            det = pd.read_csv(file)._values[i]
            name_fa = det[1]
            surname_fa = det[2]
            std_id = det[0]
            section = det[8]
            major = det[7]
            pardis = det[5]
            faculty = det[6]
            std_given_name = det[3]
            std_surname = det[4]
            try:
                resp = requests.get(
                    'https://api.elsevier.com/content/search/author?query=authlast(' + std_surname + ')%20and%20authfirst(' + std_given_name + ')%20and%20affil(university of tehran)&apiKey=6959e275f42d45ece5b478b84b1fbec7')
            except TypeError:
                continue
            res = json.loads(resp.content.decode('utf-8'))
            try:
                if res['search-results']:
                    pass
            except KeyError:
                print('quota exceeded')
                sys.exit()
            if res['search-results']['opensearch:totalResults'] == '0':
                # print(res['search-results']['entry'][0]['error']+':'+ std_given_name+':'+std_surname+':'+name_fa+':'+surname_fa+':'+std_id+':'+major+':'+faculty+':'+section+':'+pardis)
                print(str(res['search-results']['entry'][0][
                          'error']) + ':' + str(std_given_name) + ':' + str(std_surname) + ':' + str(std_id))

                continue
            else:
                try:
                    auid = res['search-results']['entry'][0]['dc:identifier'].split('AUTHOR_ID:')[1]
                    newresp = requests.get('http://api.elsevier.com/content/author?author_id='+auid+'&view=metrics&apiKey=6959e275f42d45ece5b478b84b1fbec7')
                    h_index= newresp.text.split('h-index>')[1].split('</')[0]
                    citation = newresp.text.split('citation-count>')[1].split('</')[0]
                    doc_count = res['search-results']['entry'][0]['document-count']
                    subject_areas = subject_area(res)
                    # print('True :'+std_given_name+':'+std_surname+':'+auid+':'+str(subject_areas) + ':'+str(doc_count)+':'+name_fa+':'+surname_fa+':'+std_id+':'+major+':'+faculty+':'+section+':'+pardis)
                    print('True :' + str(std_given_name) + ':' + str(std_surname) + ':' + str(std_id) + ':' +str(auid) + ':' + str(subject_areas) + ':' + str(
                        doc_count)+':'+str(h_index)+':'+str(citation))
                except Exception as e:
                    print(e)
                    continue
    except IndexError:
        pass


def subject_area(res):
    subject_area_len = res['search-results']['entry'][0]['subject-area'].__len__()
    for i in range(subject_area_len):
        sub_area = []
        try:
            sub_area.append(res['search-results']['entry'][0]['subject-area'][i]['$'])
        except KeyError:
            pass
    return sub_area


class Command(BaseCommand):
    def handle(self, **options):
        read_from_csv()
