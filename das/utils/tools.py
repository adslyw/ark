# -*- coding: utf-8 -*-
from das.models import *

def fetch_score_difference_value(score, batch_name, subject_type_name, year):
    difference_value = None

    if batch_name != '本科二批':
        batch_name = '本科一批'

    score_line = ScoreLine.objects.get(
        admission_batch__batch_name=batch_name,
        subject_type__type_name=subject_type_name,
        admission_year__year=year,
    )

    difference_value = score - score_line.score

    return difference_value


def fetch_rank_difference_value(rank, batch_name, subject_type_name, year):
    difference_value = None

    diff_map = {
        '2017_理工_本科二批': 52052,
        '2017_文史_本科二批': 9722,
        '2018_理工_本科二批': 53596,
        '2018_文史_本科二批': 10971,
        '2019_理工_本科二批': 63559,
        '2019_文史_本科二批': 14592,
        '2017_理工_本科一批': 0,
        '2017_文史_本科一批': 0,
        '2018_理工_本科一批': 0,
        '2018_文史_本科一批': 0,
        '2019_理工_本科一批': 0,
        '2019_文史_本科一批': 0,
    }

    if batch_name != '本科二批':
        batch_name = '本科一批'

    score_line = ScoreLine.objects.get(
        admission_batch__batch_name=batch_name,
        subject_type__type_name=subject_type_name,
        admission_year__year=year,
    )

    key = "{}_{}_{}".format(
        year,
        subject_type_name,
        batch_name,
    )
    difference_value = rank - diff_map.get(key)

    return difference_value

def fetch_recommend_univercity(score_difference_value, batch_name, subject_type_name, year):
    result = {}

    if score_difference_value < 0:
        return result

    ps = PlanStatistic.objects.filter(
        admission_batch__batch_name=batch_name,
        subject_type__type_name=subject_type_name,
        admission_year__year=year,
    )

    t1 = list(ps.filter(
        d1__lte=score_difference_value,
        d2__gt=score_difference_value,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'd1',
        'd2',
        'd3',
        'd4',
        'd5',
        'd6',
        'd7',
    ).order_by('-d1'))
    result['t1'] = t1

    t2 = list(ps.filter(
        d2__lte=score_difference_value,
        d3__gt=score_difference_value,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'd1',
        'd2',
        'd3',
        'd4',
        'd5',
        'd6',
        'd7',
    ).order_by('-d2'))
    result['t2'] = t2

    t3 = list(ps.filter(
        d3__lte=score_difference_value,
        d4__gt=score_difference_value,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'd1',
        'd2',
        'd3',
        'd4',
        'd5',
        'd6',
        'd7',
    ).order_by('-d3'))
    result['t3'] = t3

    t4 = list(ps.filter(
        d4__lte=score_difference_value,
        d5__gt=score_difference_value,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'd1',
        'd2',
        'd3',
        'd4',
        'd5',
        'd6',
        'd7',
    ).order_by('-d4'))
    result['t4'] = t4

    t5 = list(ps.filter(
        d5__lte=score_difference_value,
        d6__gt=score_difference_value,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'd1',
        'd2',
        'd3',
        'd4',
        'd5',
        'd6',
        'd7',
    ).order_by('-d5'))
    result['t5'] = t5

    t6 = list(ps.filter(
        d6__lte=score_difference_value,
        d7__gt=score_difference_value,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'd1',
        'd2',
        'd3',
        'd4',
        'd5',
        'd6',
        'd7',
    ).order_by('-d6'))
    result['t6'] = t6

    return result

def fetch_recommend_univercity_by_rank(rank, batch_name, subject_type_name, year):
    result = {}
    print(rank, batch_name, subject_type_name, year)
    # if rank < 0:
    #     return result

    ps = PlanStatistic.objects.filter(
        admission_batch__batch_name=batch_name,
        subject_type__type_name=subject_type_name,
        admission_year__year=year,
    )

    t6 = list(ps.filter(
        r2__gt=rank,
        r1__lte=rank,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'r1',
        'r2',
        'r3',
        'r4',
        'r5',
        'r6',
        'r7',
    ).order_by('r1'))

    t5 = list(ps.filter(
        r3__gt=rank,
        r2__lte=rank,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'r1',
        'r2',
        'r3',
        'r4',
        'r5',
        'r6',
        'r7',
    ).order_by('r2'))

    t4 = list(ps.filter(
        r4__gt=rank,
        r3__lte=rank,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'r1',
        'r2',
        'r3',
        'r4',
        'r5',
        'r6',
        'r7',
    ).order_by('r3'))

    t3 = list(ps.filter(
        r5__gt=rank,
        r4__lte=rank,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'r1',
        'r2',
        'r3',
        'r4',
        'r5',
        'r6',
        'r7',
    ).order_by('r4'))

    t2 = list(ps.filter(
        r6__gt=rank,
        r5__lte=rank,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'r1',
        'r2',
        'r3',
        'r4',
        'r5',
        'r6',
        'r7',
    ).order_by('r5'))

    t1 = list(ps.filter(
        r7__gte=rank,
        r6__lte=rank,
    ).values_list(
        'univercity_code__code',
        'univercity_code__univercity__name',
        'r1',
        'r2',
        'r3',
        'r4',
        'r5',
        'r6',
        'r7',
    ).order_by('r6'))
    result['t1'] = t1
    result['t2'] = t2
    result['t3'] = t3
    result['t4'] = t4
    result['t5'] = t5
    result['t6'] = t6

    return result

# def main():
#     score = 567
#     batch_name = '本科一批'
#     subject_type_name = '理工'
#     year = '2019'

#     score_difference_value = fetch_score_difference_value(
#         score,
#         batch_name,
#         subject_type_name,
#         year
#     )

#     print('score_difference_value: ', score_difference_value)

# if __name__ == '__main__':
#     main()
