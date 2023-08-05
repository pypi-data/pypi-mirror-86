# encoding=utf-8
import jieba
import xlrd
import xlwt
import math
import re
import json
import datetime
import sys, getopt

from groupingsentences.ssdistance import get_similarity_val_by_sentences
from groupingsentences.ssdistance import get_funcname_by_func_type_id
from groupingsentences.fileload import load_cells_from_file

#1：词向量文本分类，这套程序的核心思路是：
#a: 两两比对词库里的关键词
#b: 比对时计算两者之间的余弦值
#c: 根据返回的余弦值选择是否归为一类（修改该关键词所处顺序）
#d: 输出排序后的结果放在文档里


def cells_to_groups(cells, type_of_func = 0 , threshold = 0.55):
    groups = {}
    sentences_processed = set()

    for sentence1 in cells:
        if sentence1 not in sentences_processed:
            sentence_related = set()
            groups[sentence1] = sentence_related
            sentences_processed.add(sentence1)
            for sentence2 in cells:
                #print(sentence1)
                if sentence2 not in sentences_processed:
                    dist1 = get_similarity_val_by_sentences(sentence1, sentence2, type_of_func)
                    if dist1 > threshold:
                        #related
                        sentence_related.add(sentence2)
                        sentences_processed.add(sentence2)
    return groups

def save_groups_to_xls(dest_file_name, groups):
    #纵向优先
    #写入xls文件
    # 打开文件
    style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold off',
        num_format_str='#,##0.00')
    stylered = xlwt.easyxf('font: name Times New Roman, color-index red, bold off',
        num_format_str='#,##0.00')

    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet0')
    max_j_start = 0
    max_j_height = 0
    sorted_word_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse = True)
    total_counts = 0
    for key, value in sorted_word_groups:
        total_counts = total_counts + len(value) + 1
    print('total counts', total_counts)
    max_height = (total_counts + len(sorted_word_groups) + 254)/255 # max height we need
    print('max_height', max_height)

    style_index = 0
    i = 0 #column
    j = 0 #row
    for key, value in sorted_word_groups: #sort by the len of set() 
        #print('## j,i row,column',j,i)
        style_index = style_index + 1
        style_item = style0
        if style_index%2 == 0:
            style_item = stylered
        ws.write(j, i, key , style_item)
        j = j + 1
        if j > max_height:
            j = 0
            i = i + 1
        for value2 in sorted(value):
            #print('j,i',j,i)
            ws.write(j, i, value2 , style_item)
            j = j + 1
            if j > max_height:
                j = 0
                i = i + 1
        j = j + 1 # add a space
        if j > max_height:
            j = 0
            i = i + 1
    wb.save(dest_file_name)

def gs_grouping_sentences_to_xls(inputfile, outputfile, max_items=10000, encoding='gb18030', type_of_func = 0, threshold = 0.55):
    cells = load_cells_from_file(inputfile, encoding , max_items)
    ts = datetime.datetime.now().timestamp() 
    groups = cells_to_groups(cells, type_of_func, threshold)
    print('groups items count', len(groups))
    ts2 = datetime.datetime.now().timestamp() 
    save_groups_to_xls(outputfile, groups)
    ts3 = datetime.datetime.now().timestamp() 
    print('type of compare function', type_of_func)
    print('total cells count', len(cells))
    print('compare sentences time passed (seconds):', ts2-ts)
    print('save to xls time passed (seconds):', ts3-ts2) 

def main(argv):
    inputfile = ''
    outputfile = ''
    type_of_func = 0
    threshold = 0.55
    encoding = 'gb18030'
    max_items = 1000

    try:
        opts, args = getopt.getopt(argv,"hi:o:c:e:f:t:",["ifile=","ofile=","encoding=","maxcount="])
    except getopt.GetoptError:
        print('first.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -f <typeofcomparefunction 0 default> -t <threshold 0.55 default>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('first.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -f <typeofcomparefunction 0 default> -t <threshold 0.55 default>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-f"):
            type_of_func = int(arg)
        elif opt in ("-t"):
            threshold = float(arg)
        elif opt in ("-e", "--encoding"):
            encoding = (arg)
        elif opt in ("-c", "--maxcount"):
            max_items = int(arg)
    if len(inputfile)==0 or len(outputfile)==0:
        print('first.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -f <typeofcomparefunction 0 default> -t <threshold 0.55 default>')
        sys.exit(2)

    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    gs_grouping_sentences_to_xls(inputfile, outputfile, max_items, encoding, type_of_func , threshold)
   

if __name__ == "__main__":
    main(sys.argv[1:])
