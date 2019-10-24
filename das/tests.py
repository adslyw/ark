# -*- coding: utf-8 -*-
import os
import sys
import django
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ark.settings")
django.setup()

from das.models import *

import requests
from bs4 import BeautifulSoup

def fetch_provinces():
    page = requests.get('http://college.gaokao.com/schpoint/')
    soup = BeautifulSoup(page.content, 'html.parser')
    provinces = soup.select('#wrapper > div.menufix > p:nth-child(1) > a')[1:]
    for p in provinces:
        Province.objects.get_or_create(
            name=p.text
        )

def fetch_exam_divisions():
    page = requests.get('http://college.gaokao.com/schpoint/')
    soup = BeautifulSoup(page.content, 'html.parser')
    subjects = soup.select('#wrapper > div.menufix > p:nth-child(3) > a')[1:]
    for s in subjects:
        print(s.text)
        ExamDivision.objects.get_or_create(
            subject=s.text
        )

def fetch_admission_batches():
    page = requests.get('http://college.gaokao.com/schpoint/')
    soup = BeautifulSoup(page.content, 'html.parser')
    batches = soup.select('#wrapper > div.menufix > p:nth-child(4) > a')[1:]
    for b in batches:
        print(b.text)
        AdmissionBatch.objects.get_or_create(
            batch_name=b.text
        )

def fetch_admission_years():
    page = requests.get('http://college.gaokao.com/schpoint/')
    soup = BeautifulSoup(page.content, 'html.parser')
    years = soup.select('#wrapper > div.menufix > p:nth-child(5) > a')[1:]
    for y in years:
        print(y.text)
        AdmissionYear.objects.get_or_create(
            year=y.text
        )

def fetch_schools():
    for p in range(107):
        url = "http://college.gaokao.com/schlist/p%s/" % (p+1)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        schools = soup.select('#wrapper > div.cont_l.in > div.scores_List > dl')

        for s in schools:
            shool_name = s.select('dt > strong > a:nth-child(1)')[0].text
            province_name = s.select('dd > ul > li:nth-child(1)')[0].text.split('：')[-1]
            school_features = [span.text for span in s.select('dd > ul > li:nth-child(2) > span')]
            type_name = s.select('dd > ul > li:nth-child(3)')[0].text.split('：')[-1]
            belong_to = s.select('dd > ul > li:nth-child(4)')[0].text.split('：')[-1]
            level = s.select('dd > ul > li:nth-child(5)')[0].text.split('：')[-1]
            home_page = s.select('dd > ul > li:nth-child(6)')[0].text.split('：')[-1]

            print(
                shool_name,
                province_name,
                school_features,
                type_name,
                belong_to,
                level,
                home_page
            )

            province, _ = Province.objects.get_or_create(name=province_name)

            for feature in school_features:
                SchoolFeature.objects.get_or_create(feature=feature)
            features = ",".join(school_features)
            school_type, _ = SchoolType.objects.get_or_create(type_name=type_name)
            affiliation, _ = Affiliation.objects.get_or_create(belong_to=belong_to)
            school_level, _ = SchoolLevel.objects.get_or_create(level=level)
            defalt_rank = Rank.objects.get(id=1)

            school = School.objects.get_or_create(
                name=shool_name,
                province=province,
                home_page=home_page,
                features=features,
                level=school_level,
                affiliation=affiliation,
                school_type=school_type,
                rank=defalt_rank
            )

if __name__ == '__main__':
    fetch_provinces()
    fetch_exam_divisions()
    fetch_admission_batches()
    fetch_admission_years()
    fetch_schools()


