import pickle

#获取两个语料库的词汇表
def get_vocab(corpus1, corpus2):
    word_vocab = set()      #空集合word_vocab，用于存储词汇
    #遍历两个语料库中的每个元素，将其中的词汇添加到word_vocab中
    for corpus in [corpus1, corpus2]:
        for i in range(len(corpus)):
            word_vocab.update(corpus[i][1][0])
            word_vocab.update(corpus[i][1][1])
            word_vocab.update(corpus[i][2][0])
            word_vocab.update(corpus[i][3])
    print(len(word_vocab))
    return word_vocab

#用于从文件中加载pickle数据
def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)  #从文件中加载数据
    return data

#用于处理词汇表。
def vocab_processing(filepath1, filepath2, save_path):
    with open(filepath1, 'r') as f:
        total_data1 = set(eval(f.read()))
    with open(filepath2, 'r') as f:
        total_data2 = eval(f.read())
    #调用get_vocab()函数获取词汇表
    word_set = get_vocab(total_data2, total_data2)
    #计算两个词汇表的交集，并将交集中的词汇从词汇表中移除
    excluded_words = total_data1.intersection(word_set)
    word_set = word_set - excluded_words

    print(len(total_data1))
    print(len(word_set))

    with open(save_path, 'w') as f:
        f.write(str(word_set))

#四个变量python_hnn、python_staqc、python_word_dict和sql_word_dict
# 分别表示Python语言的HNN数据、STAQC数据和词汇表文件名
#四个变量，sql_hnn、sql_staqc、new_sql_staqc和large_word_dict_sql
# 分别表示SQL语言的HNN数据、STAQC数据、未标注的STAQC数据和词汇表文件名
if __name__ == "__main__":
    python_hnn = './data/python_hnn_data_teacher.txt'
    python_staqc = './data/staqc/python_staqc_data.txt'
    python_word_dict = './data/word_dict/python_word_vocab_dict.txt'

    sql_hnn = './data/sql_hnn_data_teacher.txt'
    sql_staqc = './data/staqc/sql_staqc_data.txt'
    sql_word_dict = './data/word_dict/sql_word_vocab_dict.txt'

    new_sql_staqc = './ulabel_data/staqc/sql_staqc_unlabled_data.txt'
    new_sql_large = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.txt'
    large_word_dict_sql = './ulabel_data/sql_word_dict.txt'
    #处理两个语料库的词汇表
    final_vocab_processing(sql_word_dict, new_sql_large, large_word_dict_sql)
