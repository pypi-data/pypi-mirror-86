# encoding=utf-8
import jieba
import xlrd
import math
import re
import xmind
import json
import datetime
from groupingsentences.ssdistance import get_similarity_val_by_sentences
from groupingsentences.ssdistance import get_funcname_by_func_type_id
from groupingsentences.fileload import load_cells_from_file
import sys, getopt
import os.path

#关键词根提取法，这套程序的核心思路是：

#a: 统计top词根N个
#b: 提取包含词根的对应关键词子集
#c: 利用xmind模块，在循环中插入对应节点
#21：top词根不一定是合适的 同时 已经被作为节点的词根不应该重复计算
#因此需要一个库，记录已经被作为节点的词根
#同时，类似”可是“这样的词不具有研究意义，不应该被作为节点，所以需要一个库，事先导入非法词根表
#22：几百万的关键词，当需要打印的层级较多时，提取各级词频对应词库的交集很耗时，而且分词操作在遍历的过程中可以预计是会重复执行的，因此还是一样要做分词预处理，只不过这个预处理会更复杂一点，需要建立几个词典库：
#库1：{id:[长尾词，对应词根集合]}
#如：记录id”1“，对应值是一个列表，里面有长尾词”QQ邮箱格式怎么写“，和这个长尾词对应的所有词根集合（set(["QQ","邮箱","格式","怎么","写"])）
#库2：{长尾词:id}
#如：记录”QQ邮箱格式怎么写“，它对应在库1的记录id是”1“
#库3：{词根:对应词频}
#如：记录”QQ“，它的词频是5，说明它出现在5个关键词里
#库4：{词根:对应ID集合}
#如：记录”QQ“，它的对应ID集合是set([1,2,3,4,5])，表示有包含它的关键词的对应ID是哪几个

def create_stores(cells, words_already, illeagle_words):
    value_id = 1
    store1 = {}
    store2 = {}
    store3 = {}
    store4 = {}

    for sentence1 in cells:
        seg_list = jieba.cut_for_search(sentence1)
        for seg in list(seg_list):
            if seg not in words_already:
                seg_count = store3.get(seg, 0)
                store3[seg] = seg_count+1
                if seg in store4:
                    store4[seg].add(value_id) 
                else:
                    store4[seg] = set([value_id])
        seg_list = jieba.cut_for_search(sentence1)
        #print(",".join(list(seg_list)))
        if value_id not in store1:
            store1[value_id]=[sentence1,set(list(seg_list))]
        if sentence1 not in store2:
            store2[sentence1]=value_id
        value_id = value_id+1
    return store1,store2,store3,store4

#TOP 获取lw句子列表里对应的首N个词根列表
def get_top(lw, top_count, store1, store2, store3, words_already):
    #lw is a sentence list
    top_words = []
    segs = {}
    for value in lw:
        seg_list = store1[store2[value]][1] #库1：{id:[长尾词，对应词根集合]}
        for seg in list(seg_list):
            if seg not in words_already:
                segs[seg]=store3[seg] #库3：{词根:对应词频}
    sorted_segs = sorted(segs.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    for item in sorted_segs[:top_count]:
        top_words.append(item[0])
    return top_words

def get_first_topwords(top_words_count, words_already, store3):
    top_words_list=[]

    #print(sorted(store3.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)) 
    sorted_ku3 = sorted(store3.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    # TOP 8
    k = 0
    for item in sorted_ku3[:top_words_count*3]:
        if item[0] not in words_already:
            top_words_list.append(item[0])
            words_already.add(item[0])
        k = k+1
        if k>top_words_count:
            break;
    print('top_words_list items count', len(top_words_list))
    return top_words_list

def gen_my_xmind_file(top_words_list, dest_file_name, store1, store2, store3, store4, words_already, top_words_count=8):  
    # 1、如果指定的XMind文件存在，则加载，否则创建一个新的
    workbook = xmind.load("./my.xmind")
    # 新建一个画布
    #sheet = workbook.createSheet()
    primary_sheet = workbook.getPrimarySheet()
    root_topic = primary_sheet.getRootTopic()
    # 给中心主题添加一个星星图标
    #root_topic.addMarker(MarkerId.starRed)
    #design_sheet1(primary_sheet)
    primary_sheet.setTitle("ROOT") #.decode('utf-8')
    # 新建一个主题
    root_topic = primary_sheet.getRootTopic()
    root_topic.setTitle("ROOT") #.decode('utf-8')
    for word1 in top_words_list:
        word1_count = (store3[word1].__str__())
        sub_root_topic = root_topic.addSubTopic()
        sub_root_topic.setTitle(word1 + ' ('+ word1_count +')') #.decode('utf-8')
        # 获取词根所有id
        idsets = store4[word1] #库4：{词根:对应句子ID集合}
        # 提取词根所有长尾词
        lw = [store1[ids][0] for ids in idsets]  #{id:[长尾词，对应词根集合]}  lw = 长尾词 list
        # 统计子top词根列表
        top_count = top_words_count
        sub_top_words_list = get_top(lw, top_count, store1, store2, store3, words_already)#,set_top=set_top)
        #print("len(子top词根列表)")
        #print(len(sub_top_words_list))
        for sub_words in sub_top_words_list:
            words_already.add(sub_words)
            sub_idsets = store4[sub_words]
            # 插入子主题
            sub_topic = sub_root_topic.addSubTopic()
            subwords_count = (store3[sub_words].__str__())
            sub_topic.setTitle(sub_words + ' ('+ subwords_count+')')#.decode('utf-8'))
            #print(sub_words)
            #print("$$$$$$$$$$$$\n")
            longtail_words_ids = idsets & sub_idsets
            longtail_words_list = []
            # 打印主题对应的长尾词
            for id in longtail_words_ids:
                longtail_words_list.append(store1[id][0])
            sub_topic_s_kw = sub_topic.addSubTopic()
            sub_topic_s_kw.setTitle(','.join(longtail_words_list[:50]))#.decode('utf-8'))
    #print(workbook.to_prettify_json())
    #xmind.save(workbook)
    # 第2种：只保存思维导图内容content.xml核心文件，适用于没有添加评论、自定义样式和附件的情况
    xmind.save(workbook=workbook, path=dest_file_name)

def cells_to_xmind(cells, outputfile, top_words_count):
    ts = datetime.datetime.now().timestamp() 
    words_already = set() #用来保存已经加入xmind列表的无需再重复加入
    illeagle_words = set() #用来排除一些不适合参与排序词根，下一步可以从文件读取次列表
    illeagle_words_file_path = './dataset/illeagle_words.txt'
    if os.path.isfile(illeagle_words_file_path):
        ws = load_cells_from_file(illeagle_words_file_path, 'utf-8')
        for item in ws:
            illeagle_words.add(item)
            print(item)

    for word in list(illeagle_words):
        words_already.add(word)

    store1,store2,store3,store4 = create_stores(cells, words_already, illeagle_words)
    print('store1 count', len(store1))
    print('store2 count', len(store2))
    print('store3 count', len(store3))
    print('store4 count', len(store4))

    #获取首N个词根
    top_words_list = get_first_topwords(top_words_count, words_already, store3)

    ts2 = datetime.datetime.now().timestamp() 
    gen_my_xmind_file(top_words_list, outputfile, store1, store2, store3, store4, words_already, top_words_count)
    ts3 = datetime.datetime.now().timestamp() 
    print('time passed ', ts2-ts)
    print('create 4 stores time passed (seconds):', ts2-ts)
    print('save to xmind time passed (seconds):', ts3-ts2)

def gs_grouping_sentences_to_xmind(inputfile, outputfile, max_items=10000, encoding='gb18030', topwordscount = 8):
    cells = load_cells_from_file(inputfile, encoding , max_items)
    cells_to_xmind(cells, outputfile, topwordscount)   

def main(argv):
    inputfile = ''
    outputfile = ''
    top_words_count = 8
    encoding = 'gb18030'
    max_items = 1000

    try:
        opts, args = getopt.getopt(argv,"hi:o:c:e:t:",["ifile=","ofile=","encoding=","maxcount="])
    except getopt.GetoptError:
        print('second.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -t <topwordscount 8 default>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('second.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -t <topwordscount 8 default>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t"):
            top_words_count = int(arg)
        elif opt in ("-e", "--encoding"):
            encoding = (arg)
        elif opt in ("-c", "--maxcount"):
            max_items = int(arg)
    if len(inputfile)==0 or len(outputfile)==0:
        print('second.py -i <inputfile> -o <outputfile> -c <maxcount 1000 default> -e <encoding gb18030 default> -t <topwordscount 8 default>')
        sys.exit(2)

    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    gs_grouping_sentences_to_xmind(inputfile, outputfile, max_items=10000, encoding='gb18030', topwordscount = 8)


if __name__ == "__main__":
    main(sys.argv[1:])
