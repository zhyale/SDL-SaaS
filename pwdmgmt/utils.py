# coding=utf-8
import re
import pypinyin
from pypinyin import pinyin
from models import *
from cache import get_hans_replace_set, get_ascii_replace_set
import random


def get_digit_num_from_chn_digit(chn):
    digit_dict = {u'零':0,u'〇':0,
                  u'一':1,u'二':2,u'三':3,u'四':4,u'五':5,u'六':6,u'七':7,u'八':8,u'九':9,
                  u'壹':1,u'贰':2,u'叁':3,u'肆':4,u'伍':5,u'陆':6,u'柒':7,u'捌':8,u'玖':9,
                  u'十':10,u'百':100,u'千':1000,u'万':10000,
                  u'拾':10,u'佰':100,u'仟':1000,u'萬':10000}
    chn_list=list(chn)
    sum=0
    last_digit=1   # 允许数据直接以单位开头，如万、千
    chn_list_len=len(chn_list)
    for i in range(chn_list_len):
        digit=digit_dict.get(chn_list[i])
        # print(str(i) + " " + str(digit))
        if digit>9:      # 单位:万、千、百、十
            unit=digit
            sum+=last_digit*unit
            last_digit=0   # 使用过后清零
        else:           # 个位数
            if i==0:             # 首位
                last_digit=digit # 记录下来备用
            else:               # 非首位
                if last_digit !=0:   # 连续数字，三九天
                    last_digit=last_digit*10+digit
                elif i == chn_list_len-1:   #非连续数字最后一位
                    sum+=digit
                else:
                    last_digit=digit
    if last_digit:
        sum+=last_digit
    return str(sum)


def replace_chn_digital_number(sentence):
    # Replace Chinese to digital number
    chn_digit_list=re.findall(ur'[〇零一二三四五六七八九十百千万壹贰叁肆伍陆柒捌玖拾佰仟萬]+',sentence,re.U)
    result=sentence
    for chn_digit in chn_digit_list:
        digit=get_digit_num_from_chn_digit(chn_digit)
        result=result.replace(chn_digit,digit)
    return result


def replace_by_pinyin(sentence):
    return pypinyin.slug(sentence, style=pypinyin.FIRST_LETTER,separator='')


def replace_chn_by_symbol(sentence):
    hans_replace_set=get_hans_replace_set()
    result = sentence
    for item in hans_replace_set:
        result=result.replace(item.chn_word, item.replaced_by)
    return result


def replace_ascii_by_symbol(sentence):
    ascii_replace_set=get_ascii_replace_set()
    result=sentence
    for item in ascii_replace_set:
        result=result.replace(item.asc_char, item.replaced_by)
    return result


def get_password_by_sentence(sentence):
    result=''
    if sentence:
        short_sentence_list = re.split(ur',|，|；|。|？|！',sentence, re.U)
        for short_sentence in short_sentence_list:
            short_result=replace_chn_by_symbol(short_sentence)
            short_result=replace_chn_digital_number(short_result)
            short_result=replace_by_pinyin(short_result)
            short_result=replace_ascii_by_symbol(short_result)
            if len(short_result)>1:
                short_result=short_result[0].upper()+short_result[1:]
            result+=short_result
    return result


def init_dice_dict():
    f=open("words.txt",'r')
    serial_num=0
    dice_list=[]
    for line in f:
        if line and len(line)<10:
            line=line[0].upper()+line[1:]
            line=line.replace('a','@').replace('o','0')
            serial_num+=1
            dice_list.append(DiceCode(sn=serial_num, word=line))
    f.close()
    DiceCode.objects.bulk_create(dice_list)
    return serial_num

def get_dice_password():
    count=DiceCode.objects.count()
    if count==0:
        count=init_dice_dict()
    result=''
    for i in range(3):
        rand_int=random.randint(1,count)
        try:
            dice=DiceCode.objects.get(sn=rand_int)
            result+=dice.word
        except:
            result+='*'
    return result
