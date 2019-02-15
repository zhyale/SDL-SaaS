# coding=utf-8
from django.core.cache import cache
from models import *

# cache time by minutes * seconds
CACHE_TIMEOUT = 1 * 10


def get_hans_replace_set():
    cache_key='HANS_REPLACE'
    replace_set=cache.get(cache_key)
    if not replace_set:
        if HansReplaceItem.objects.count()==0:
            HansReplaceItem.objects.bulk_create([
                HansReplaceItem(chn_word=u'星',replaced_by='*'),
                HansReplaceItem(chn_word=u'点',replaced_by='.'),
                HansReplaceItem(chn_word=u'不',replaced_by='!'),
                HansReplaceItem(chn_word=u'半',replaced_by='1/2'),
                HansReplaceItem(chn_word=u'两',replaced_by='2'),
                HansReplaceItem(chn_word=u'似',replaced_by='4'),
                HansReplaceItem(chn_word=u'寺',replaced_by='4'),
                HansReplaceItem(chn_word=u'午',replaced_by='5'),
                HansReplaceItem(chn_word=u'武',replaced_by='5'),
                HansReplaceItem(chn_word=u'舞',replaced_by='5'),
                HansReplaceItem(chn_word=u'戚',replaced_by='7'),
                HansReplaceItem(chn_word=u'酒',replaced_by='9'),
                HansReplaceItem(chn_word=u'正月',replaced_by='Jan.'),
                HansReplaceItem(chn_word=u'二月',replaced_by='Feb.'),
                HansReplaceItem(chn_word=u'三月',replaced_by='Mar.'),
                HansReplaceItem(chn_word=u'四月',replaced_by='Apr.'),
                HansReplaceItem(chn_word=u'五月',replaced_by='May.'),
                HansReplaceItem(chn_word=u'六月',replaced_by='Jun.'),
                HansReplaceItem(chn_word=u'七月',replaced_by='Jul.'),
                HansReplaceItem(chn_word=u'八月',replaced_by='Aug.'),
                HansReplaceItem(chn_word=u'九月',replaced_by='Sep.'),
                HansReplaceItem(chn_word=u'十月',replaced_by='Oct.'),
                HansReplaceItem(chn_word=u'冬月',replaced_by='Nov.'),
                HansReplaceItem(chn_word=u'腊月',replaced_by='Dec.'),
                HansReplaceItem(chn_word=u'谁',replaced_by='Who'),
                HansReplaceItem(chn_word=u'何处',replaced_by='Where'),
                HansReplaceItem(chn_word=u'何时',replaced_by='When'),
                HansReplaceItem(chn_word=u'几时',replaced_by='When'),
                HansReplaceItem(chn_word=u'何事',replaced_by='What'),
                HansReplaceItem(chn_word=u'明月光',replaced_by='moonlight'),
                HansReplaceItem(chn_word=u'月光',replaced_by='moonlight'),
                HansReplaceItem(chn_word=u'明月',replaced_by='moon'),
                HansReplaceItem(chn_word=u'到如今',replaced_by='Now'),
                HansReplaceItem(chn_word=u'如今',replaced_by='Now'),
                HansReplaceItem(chn_word=u'东风',replaced_by='Eastwind'),
                HansReplaceItem(chn_word=u'人间',replaced_by='World'),
            ])
        replace_set=HansReplaceItem.objects.all()
        cache.set(cache_key, replace_set, CACHE_TIMEOUT)
    return replace_set


def get_ascii_replace_set():
    cache_key='ASCII_REPLACE'
    replace_set=cache.get(cache_key)
    if not replace_set:
        if AsciiReplaceItem.objects.count()==0:
            AsciiReplaceItem.objects.bulk_create([
                AsciiReplaceItem(asc_char='a', replaced_by='@'),
                # AsciiReplaceItem(asc_char='o', replaced_by='0'),
            ])
        replace_set=AsciiReplaceItem.objects.all()
        cache.set(cache_key, replace_set, CACHE_TIMEOUT)
    return replace_set
