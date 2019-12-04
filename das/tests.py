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
from django.db.models import Count
# def fetch_provinces():
#     page = requests.get('http://college.gaokao.com/schpoint/')
#     soup = BeautifulSoup(page.content, 'html.parser')
#     provinces = soup.select('#wrapper > div.menufix > p:nth-child(1) > a')[1:]
#     for p in provinces:
#         Province.objects.get_or_create(
#             name=p.text
#         )

# def fetch_exam_divisions():
#     page = requests.get('http://college.gaokao.com/schpoint/')
#     soup = BeautifulSoup(page.content, 'html.parser')
#     subjects = soup.select('#wrapper > div.menufix > p:nth-child(3) > a')[1:]
#     for s in subjects:
#         print(s.text)
#         ExamDivision.objects.get_or_create(
#             subject=s.text
#         )

# def fetch_admission_batches():
#     page = requests.get('http://college.gaokao.com/schpoint/')
#     soup = BeautifulSoup(page.content, 'html.parser')
#     batches = soup.select('#wrapper > div.menufix > p:nth-child(4) > a')[1:]
#     for b in batches:
#         print(b.text)
#         AdmissionBatch.objects.get_or_create(
#             batch_name=b.text
#         )

# def fetch_admission_years():
#     page = requests.get('http://college.gaokao.com/schpoint/')
#     soup = BeautifulSoup(page.content, 'html.parser')
#     years = soup.select('#wrapper > div.menufix > p:nth-child(5) > a')[1:]
#     for y in years:
#         print(y.text)
#         AdmissionYear.objects.get_or_create(
#             year=y.text
#         )

# def fetch_schools():
#     for p in range(107):
#         url = "http://college.gaokao.com/schlist/p%s/" % (p+1)
#         page = requests.get(url)
#         soup = BeautifulSoup(page.content, 'html.parser')
#         schools = soup.select('#wrapper > div.cont_l.in > div.scores_List > dl')

#         for s in schools:
#             shool_name = s.select('dt > strong > a:nth-child(1)')[0].text
#             province_name = s.select('dd > ul > li:nth-child(1)')[0].text.split('：')[-1]
#             school_features = [span.text for span in s.select('dd > ul > li:nth-child(2) > span')]
#             type_name = s.select('dd > ul > li:nth-child(3)')[0].text.split('：')[-1]
#             belong_to = s.select('dd > ul > li:nth-child(4)')[0].text.split('：')[-1]
#             level = s.select('dd > ul > li:nth-child(5)')[0].text.split('：')[-1]
#             home_page = s.select('dd > ul > li:nth-child(6)')[0].text.split('：')[-1]

#             print(
#                 shool_name,
#                 province_name,
#                 school_features,
#                 type_name,
#                 belong_to,
#                 level,
#                 home_page
#             )

#             province, _ = Province.objects.get_or_create(name=province_name)

#             for feature in school_features:
#                 SchoolFeature.objects.get_or_create(feature=feature)
#             features = ",".join(school_features)
#             school_type, _ = SchoolType.objects.get_or_create(type_name=type_name)
#             affiliation, _ = Affiliation.objects.get_or_create(belong_to=belong_to)
#             school_level, _ = SchoolLevel.objects.get_or_create(level=level)
#             defalt_rank = Rank.objects.get(id=1)

#             school = School.objects.get_or_create(
#                 name=shool_name,
#                 province=province,
#                 home_page=home_page,
#                 features=features,
#                 level=school_level,
#                 affiliation=affiliation,
#                 school_type=school_type,
#                 rank=defalt_rank
#             )

def fetch_schools():
    params  = [
        ['http://www.gaosan.com/gaokao/222526.html', '#data222526 > table > tbody > tr'],
        ['http://www.gaosan.com/gaokao/223294.html', '#data223294 > table > tbody > tr'],
    ]

    for url, selector in params:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for line in soup.select(selector):
            school_code = line.select('td:nth-child(3)')[0].text
            school_name = line.select('td:nth-child(4)')[0].text
            # Univercity.objects.get_or_create(
            #     name=school_name,
            # )
            print(school_code, school_name)


def fetch_school_city():
    url = 'http://www.gaosan.com/gaokao/248720.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for line in soup.select('#data248720 > table > tbody > tr'):
        if '（' in line.select('td:nth-child(1)')[0].text:
            continue
        school_name = line.select('td:nth-child(2)')[0].text
        city_name = line.select('td:nth-child(5)')[0].text.replace('市', '')
        comment = line.select('td:nth-child(7)')[0].text
        # print(school_name, city_name, comment)
        try:
            u = Univercity.objects.get(
                name=school_name,
            )
            c = City.objects.get(
                name=city_name
            )
        except Exception:
            continue

        print(school_name, city_name, comment)
        u.city = c
        if comment == '民办':
            u.is_private = True
        else:
            u.is_private = False

        u.save()


def fetch_school_rank():
    params = [
        ['https://www.dxsbb.com/news/5463.html', '#newsContent > table:nth-child(14) > tbody > tr'],
        ['https://www.dxsbb.com/news/5463_2.html', '#newsContent > table:nth-child(1) > tbody > tr']
    ]

    for url, selector in params:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for line in soup.select(selector):
            rank = line.select('td:nth-child(1)')[0].text
            school_name = line.select('td:nth-child(2)')[0].text
            try:
                u = Univercity.objects.get(
                    name=school_name,
                )
            except Exception:
                continue
            print(rank, school_name)
            if rank != '暂无':
                u.total_rank = int(rank)
                u.save()

def fetch_univercity_city_and_is_private():
    params  = [
        ['http://www.gaosan.com/gaokao/222526.html', '#data222526 > table > tbody > tr'],
        ['http://www.gaosan.com/gaokao/223294.html', '#data223294 > table > tbody > tr'],
    ]

    for url, selector in params:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for line in soup.select(selector):
            school_name = line.select('td:nth-child(4)')[0].text
            city = line.select('td:nth-child(3)')[5].text.replace('市', '')
            try:
                u = Univercity.objects.get(
                    name=school_name,
                )
            except Exception:
                continue
            print(school_code, school_name)
            UnivercityCode.objects.get_or_create(
                code=school_code,
                univercity=u,
            )

def fetch_school_plan():
    params  = [
        # [2017, '本科一批', 'http://www.sneac.com/2017YBZS--LG.html', 'table > tbody > tr'],
        # [2017, '本科一批', 'http://www.sneac.com/2017YBZS--WS.html', 'table > tbody > tr'],
        # [2017, '本科二批', 'http://www.sneac.com/EBZS-LG.html', 'table > tbody > tr'],
        # [2017, '本科二批', 'http://www.sneac.com/EBZS-WS.html', 'table > tbody > tr'],
        # [2018, '本科一批', 'http://www.sneac.com/2018YBZS-LG.html', 'table > tbody > tr'],
        # [2018, '本科一批', 'http://www.sneac.com/2018YBZS-WS.html', 'table > tbody > tr'],
        # [2018, '本科二批', 'http://www.sneac.com/2018EBZS-LG.html', 'table > tbody > tr'],
        # [2018, '本科二批', 'http://www.sneac.com/2018EBZS-WS.html', 'table > tbody > tr'],
        # [2019, '本科一批', 'http://www.sneac.com/fujin/2019YB-ZS-LG.html', 'table > tr'],
        # [2019, '本科一批', 'http://www.sneac.com/fujin/2019YB-ZS-WS.html', 'table > tr'],
        # [2019, '本科二批', 'http://www.sneac.com/fujin/2019-EB-ZS-LG.html', 'table > tr'],
        # [2019, '本科二批', 'http://www.sneac.com/fujin/2019-EB-ZS-WS.html', 'table > tr'],
        # [2017, '单设本科批次A段(国家专项计划)', 'http://www.sneac.com/2017DS-A-LG.html', 'table > tbody > tr'],
        # [2017, '单设本科批次A段(国家专项计划)', 'http://www.sneac.com/2017DS-A-WS.html', 'table > tbody > tr'],
        # [2017, '单设本科批次B段(地方专项计划)', 'http://www.sneac.com/info/1009/1549.htm', 'table > tbody > tr'],
        # [2018, '单设本科批次A段(国家专项计划)', 'http://www.sneac.com/2018n3A-LG.html', 'table > tbody > tr'],
        # [2018, '单设本科批次A段(国家专项计划)', 'http://www.sneac.com/2018n3A-WS.html', 'table > tbody > tr'],
        ##[2018, '单设本科批次B段(地方专项计划)', 'http://www.sneac.com/info/1009/1473.htm', 'table > tbody > tr'],
        # [2019, '单设本科批次A段(国家专项计划)', 'http://www.sneac.com/fujin/2019DSBK-A-WS.html', 'table > tr'],
        # [2019, '单设本科批次A段(国家专项计划)', 'http://www.sneac.com/fujin/2019DSBK-A-LG.html', 'table > tr'],
        # [2019, '单设本科批次B段(地方专项计划)', 'http://www.sneac.com/fujin/2019DSBK-B-WS.html', 'table > tr'],
        # [2019, '单设本科批次B段(地方专项计划)', 'http://www.sneac.com/fujin/2019DSBK-B-LG.html', 'table > tr'],
    ]

    for year, batch, url, selector in params:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.select('table > tr'))
        for line in soup.select(selector):
            school_code = line.select('td:nth-child(3)')[0].text.replace(' ', '').strip()
            if school_code == '院校代号':
                continue
            sublect_type = line.select('td:nth-child(2)')[0].text.replace(' ', '').strip()
            school_name = line.select('td:nth-child(4)')[0].text.replace(' ', '').replace("\r\n", '').replace("\n", '').strip()
            plan_amount = line.select('td:nth-child(5)')[0].text.replace(' ', '').strip().replace('-', '0')
            actual_amount = line.select('td:nth-child(6)')[0].text.replace(' ', '').strip().replace('-', '0')
            # highest_score = line.select('td:nth-child(4)')[0].text.replace(' ', '').strip()
            lowest_score = line.select('td:nth-child(7)')[0].text.replace(' ', '').strip().replace('-', '0')
            # average_score = line.select('td:nth-child(4)')[0].text.replace(' ', '').strip()
            lowest_rank = line.select('td:nth-child(8)')[0].text.replace(' ', '').strip().replace('-', '0')

            a_y = AdmissionYear.objects.get(year=year)
            a_b = AdmissionBatch.objects.get(batch_name=batch)
            u = Univercity.objects.filter(
                name=school_name,
            ).first()
            s_t = SubjectType.objects.get(type_name=sublect_type)
            u_c, _ = UnivercityCode.objects.get_or_create(
                code=school_code,
            )
            u_c.univercity_name_alias=school_name
            u_c.save()

            if u:
                u_c.univercity = u
                u_c.save()

            plan, _ = Plan.objects.get_or_create(
                univercity_code=u_c,
                subject_type=s_t,
                admission_batch=a_b,
                admission_year=a_y,
            )
            plan.plan_amount = int(plan_amount)
            plan.actual_amount = int(actual_amount)
            plan.lowest_score = int(lowest_score)
            # plan.highest_score =
            # plan.average_score =
            # plan.highest_rank =
            plan.lowest_rank = int(lowest_rank)
            plan.save()

            print(
                year,
                batch,
                sublect_type,
                school_code,
                school_name,
                plan_amount,
                actual_amount,
                lowest_score,
                lowest_rank,
            )
            # # UnivercityCode.objects.get_or_create(
            # #     code=school_code,
            # #     univercity=u,
            # # )

def fetch_score_count():
    params = [
        # [1, 2, 'http://www.sneac.com/fujin/2019lgltjbiao.htm', 'table > tr'],
        # [1, 1, 'http://www.sneac.com/fujin/2019wsltjbiao.htm', 'table > tr'],
        [2, 2, 'http://www.sneac.com/info/1088/5956.htm', 'table > tbody > tr']
        # [2, 1, 'http://www.sneac.com/info/1009/1482.htm', 'table > tbody > tr']
    ]

    for admission_year, subject_type, url, selector in params:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for line in soup.select(selector):
            score = line.select('td:nth-child(1)')[0].text
            number = line.select('td:nth-child(2)')[0].text
            cumulative_number = line.select('td:nth-child(3)')[0].text

            if score == '分数' or score == '':
                continue

            if score.endswith('以上'):
                score = score.replace('以上', '').replace('分', '')
                number = cumulative_number

            print(
                score,
                number,
                cumulative_number,
            )

            ScoreStatistic.objects.create(
                admission_year_id=admission_year,
                subject_type_id=subject_type,
                score=int(score),
                number=int(number),
                cumulative_number=int(cumulative_number),
            )

if __name__ == '__main__':
    # fetch_provinces()
    # fetch_exam_divisions()
    # fetch_admission_batches()
    # fetch_admission_years()
    # fetch_schools()
    # fetch_school_city()
    # for school in Univercity.objects.filter(total_rank=999):
    #     print(school.name)
    # fetch_school_rank()
    # fetch_school_code()
    # fetch_school_plan()
    # for uc in UnivercityCode.objects.filter(code__startswith='9').exclude(univercity_name_alias__contains='中外合作办学'):
    #     new_alias = uc.univercity_name_alias + '(中外合作办学)'
    #     print(uc.code, uc.univercity_name_alias, new_alias)
    #     uc.univercity_name_alias = new_alias
    #     u, _ = Univercity.objects.get_or_create(
    #         name=new_alias,
    #     )
    #     u.city = uc.univercity.city
    #     u.total_rank = uc.univercity.total_rank
    #     u.project_tags = uc.univercity.project_tags
    #     u.is_private = uc.univercity.is_private
    #     u.save()
    #     uc.univercity = u
    #     uc.save()

    #     u, _ = Univercity.objects.get_or_create(
    #         name=uc.univercity_name_alias
    #     )
    #     uc.univercity = u
    #     uc.save()


    # a = Plan.objects.exclude(
    #     admission_batch__batch_name__in=['本科一批', '本科二批']
    # ).filter(
    #     admission_year__year='2019'
    # ).values_list(
    #     'univercity_code__univercity__name'
    # ).distinct()

    # b = Plan.objects.filter(
    #     admission_batch__batch_name='本科二批'
    # ).filter(
    #     admission_year__year='2019'
    # ).values_list(
    #     'univercity_code__univercity__name'
    # ).distinct()

    # for x in (set(a) & set(b)):
    #     uc = UnivercityCode.objects.get(univercity__name=x[0])
    #     print(uc.code, uc.univercity.name)
    # fetch_score_count()

    years = ['2018', '2017']
    subject_type_names = ['理工', '文史']
    params = zip(years, subject_type_names)
    for year, subject_type_name in params:
        score_rank_map = dict(ScoreStatistic.objects.filter(
            admission_year__year=year,
            subject_type__type_name=subject_type_name,
        ).values_list(
            'score',
            'cumulative_number',
        ))

        plans = Plan.objects.filter(
            admission_year__year=year,
            subject_type__type_name=subject_type_name,
        )

        for plan in plans:
            print(year, subject_type_name, plan.univercity_code.univercity.name, plan.average_score, score_rank_map.get(plan.average_score))

            plan.average_rank = score_rank_map.get(plan.average_score)
            plan.save()

    # ScoreStatistic.objects.filter(
    #     admission_year__year='2018',
    #     subject_type__type_name='理工',
    # ).delete()
