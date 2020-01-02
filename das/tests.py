# -*- coding: utf-8 -*-
import os
import sys
import django
sys.path.append('../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ark.settings")
django.setup()

from das.models import *
from django.db.models import Q
import requests
from bs4 import BeautifulSoup
from django.db.models import Count
from das.utils.tools import *
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

def test_fetch_score_difference_value():
    score = 567
    batch_name = '本科一批'
    subject_type = 1
    year = '2019'

    score_difference_value = fetch_score_difference_value(
        score,
        batch_name,
        subject_type,
        year
    )

    print('score_difference_value: ', score_difference_value)


def compute_plan_sctatics(year):
    # admission_year = AdmissionYear.objects.get(year=year)
    # for admission_batch in AdmissionBatch.objects.all():
    #     for plan in plans.objects.:
    #         pass

    target_years = [
        year,
        str(int(year) -1),
        str(int(year) -2),
    ]
    print(target_years)
    plans = Plan.objects.filter(
        admission_year__year=year,
        admission_batch__batch_name='本科二批',
    )

    for plan in plans:
        target_plans = Plan.objects.filter(
            admission_year__year__in=target_years,
            subject_type=plan.subject_type,
            admission_batch=plan.admission_batch,
            univercity_code=plan.univercity_code,
        )

        # if plan.admission_batch.batch_name != '本科二批':
        #     print(plan.id)
        #     continue

        plan_statistic, _ = PlanStatistic.objects.get_or_create(
            univercity_code=plan.univercity_code,
            admission_year=plan.admission_year,
            subject_type=plan.subject_type,
            admission_batch=plan.admission_batch,
        )

        # if not _:
        #     print(plan_statistic.id, _)
        #     continue

        lowest_score_diffs = list(sorted([
            x.lowest_score_diff
            for x in target_plans.exclude(lowest_score=0)
        ]))

        lowest_rank_diffs = list(sorted([
            fetch_rank_difference_value(
                x.lowest_rank,
                x.admission_batch.batch_name,
                x.subject_type.type_name,
                x.admission_year.year
            )
            for x in target_plans.exclude(lowest_rank=0)
        ]))

        # if len(lowest_score_diffs) == 3:
        #     [l1, l2, l3] = lowest_score_diffs
        # elif len(lowest_score_diffs) == 2:
        #     [l1, l2] = lowest_score_diffs
        #     l3 = l2
        # else:
        #     [l1] = lowest_score_diffs
        #     l2 = l1
        #     l3 = l1

        highest_score_diffs = list(sorted([
            x.highest_score_diff
            for x in target_plans.exclude(highest_score=0)
        ]))

        highest_rank_diffs = list(sorted([
            fetch_rank_difference_value(
                x.highest_rank,
                x.admission_batch.batch_name,
                x.subject_type.type_name,
                x.admission_year.year
            )
            for x in target_plans.exclude(highest_rank=0)
        ]))

        # if len(highest_score_diffs) == 3:
        #     [h1, h2, h3] = highest_score_diffs
        # elif len(highest_score_diffs) == 2:
        #     [h1, h2] = highest_score_diffs
        #     h3 = h2
        # else:
        #     [h1] = highest_score_diffs
        #     h2 = h1
        #     h3 = h1

        average_score_diffs = list(sorted([
            x.average_score_diff
            for x in target_plans.exclude(average_score=0)
        ]))

        average_rank_diffs = list(sorted([
            fetch_rank_difference_value(
                x.average_rank,
                x.admission_batch.batch_name,
                x.subject_type.type_name,
                x.admission_year.year
            )
            for x in target_plans.exclude(average_rank=0)
        ]))

        # if len(average_score_diffs) == 3:
        #     [a1, a2, a3] = average_score_diffs
        # elif len(average_score_diffs) == 2:
        #     [a1, a2] = average_score_diffs
        #     a3 = a2
        # else:
        #     [a1] = average_score_diffs
        #     a2 = a1
        #     a3 = a1
        d_list = list(sorted(average_score_diffs + highest_score_diffs + lowest_score_diffs))
        r_list = list(sorted(average_rank_diffs + highest_rank_diffs + lowest_rank_diffs))
        if len(d_list) < 6 or len(r_list) < 6:
            print('---', plan.univercity_code)
            continue

        # print(d_list)

        d1 = d_list[-6]
        d2 = d_list[-5]
        d3 = d_list[-4]
        d4 = d_list[-3]
        d5 = d_list[-2]
        d6 = d_list[-1]
        d7 = d_list[-1] + 10
        r7 = r_list[5]
        r6 = r_list[4]
        r5 = r_list[3]
        r4 = r_list[2]
        r3 = r_list[1]
        r2 = r_list[0]
        r1 = int(r_list[0] * 0.9)
        print(plan.univercity_code, [d1, d2, d3, d4, d5, d6, d7, r1, r2, r3, r4, r5, r6, r7])

        plan_statistic.d1 = d1
        plan_statistic.d2 = d2
        plan_statistic.d3 = d3
        plan_statistic.d4 = d4
        plan_statistic.d5 = d5
        plan_statistic.d6 = d6
        plan_statistic.d7 = d7
        plan_statistic.r1 = r1
        plan_statistic.r2 = r2
        plan_statistic.r3 = r3
        plan_statistic.r4 = r4
        plan_statistic.r5 = r5
        plan_statistic.r6 = r6
        plan_statistic.r7 = r7
        plan_statistic.save()

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


    # years = ['2018', '2018']
    # subject_type_names = ['理工', '文史']
    # params = zip(years, subject_type_names)
    # for year, subject_type_name in params:
    #     score_rank_map = dict(ScoreStatistic.objects.filter(
    #         admission_year__year=year,
    #         subject_type__type_name=subject_type_name,
    #     ).values_list(
    #         'score',
    #         'cumulative_number',
    #     ))

    #     plans = Plan.objects.filter(
    #         admission_year__year=year,
    #         subject_type__type_name=subject_type_name,
    #     )

    #     for plan in plans:
    #         print(
    #             year,
    #             subject_type_name,
    #             plan.admission_batch.batch_name,
    #             plan.univercity_code.univercity.name,
    #             plan.highest_rank,
    #             score_rank_map.get(plan.highest_score),
    #             plan.lowest_rank,
    #             score_rank_map.get(plan.lowest_score),
    #             plan.average_score,
    #             score_rank_map.get(plan.average_score)
    #         )

    #         plan.highest_rank = score_rank_map.get(plan.highest_score)
    #         plan.lowest_rank = score_rank_map.get(plan.lowest_score)
    #         plan.average_rank = score_rank_map.get(plan.average_score)
    #         plan.save()

    # # 提前批
    # batch_names = list(AdmissionBatch.objects.values_list(
    #     'batch_name',
    #     flat=True,
    # ))

    # type_names = list(SubjectType.objects.values_list(
    #     'type_name',
    #     flat=True,
    # ))

    # year = '2017'
    # for batch_name in batch_names:
    #     # if batch_name  not in ['提前批']:
    #     #     continue
    #     for subject_type_name in type_names:
    #         plans = Plan.objects.filter(
    #             # admission_batch__batch_name=batch_name,
    #             subject_type__type_name=subject_type_name,
    #             admission_year__year='2017',
    #         )

    #         low_score_map = dict(plans.values_list(
    #             'lowest_score',
    #             'lowest_rank'
    #         ).distinct())

    #         high_score_map = dict(plans.values_list(
    #             'highest_score',
    #             'highest_rank'
    #         ).distinct())

    #         # average_score_map = dict(Plan.objects.filter(
    #         #     admission_batch__batch_name='本科一批',
    #         #     subject_type__type_name='理工',
    #         #     admission_year__year='2017'
    #         # ).values_list(
    #         #     'average_score',
    #         #     'average_rank'
    #         # ).distinct())

    #         score_map = {
    #             **high_score_map,
    #             **low_score_map,
    #             # **average_score_map,
    #         }

    #         # score_map = dict([

    #         #    for x in  sorted(score_map.items())
    #         # ])
    #         result = []
    #         pre = None
    #         for x in sorted(score_map.items()):
    #             current = x
    #             if pre:
    #                 if pre[0] + 1 == current[0]:
    #                     continue

    #                 result.append([pre[0], pre[1]])
    #                 dx = current[0] - pre[0]
    #                 dy = int((pre[1] - current[1]) / dx)
    #                 for i in range(1, dx):
    #                     result.append([pre[0] + i, pre[1] - i*dy])
    #             pre = x

    #         score_map = dict(result)
    #         # plans1 = Plan.objects.filter(
    #         #     admission_batch__batch_name=batch_name,
    #         #     subject_type__type_name=subject_type_name,
    #         #     admission_year__year='2017',
    #         # )

    #         for plan in plans.filter(admission_batch__batch_name=batch_name).filter(Q(highest_rank=0) | Q(lowest_rank=0) | Q(average_rank=0)):
    #             print(
    #                 year,
    #                 subject_type_name,
    #                 plan.admission_batch.batch_name,
    #                 plan.univercity_code.univercity.name,
    #                 plan.highest_score,
    #                 score_map.get(plan.highest_score),
    #                 plan.lowest_score,
    #                 score_map.get(plan.lowest_score),
    #                 plan.average_score,
    #                 score_map.get(plan.average_score),
    #             )

    #             plan.highest_rank = score_map.get(plan.highest_score)
    #             plan.lowest_rank = score_map.get(plan.lowest_score)
    #             plan.average_rank = score_map.get(plan.average_score)
    #             plan.save()


    # test_fetch_score_difference_value()
    compute_plan_sctatics('2019')

