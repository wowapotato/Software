# softwareEngineering
20211060024 郭硕

## 目录

- [一、项目框架](#一项目框架)
- [二、文件说明](#二文件说明)
  - [2.1 getSru2Vec.py文件](#getStru2Vecpy文件)
  - [2.2 embeddings_process.py文件](#embeddings_processpy文件)
  - [2.3 process_single_corpus.py文件](#process_single_corpuspy文件)
  - [2.4 python_structured.py文件](#python_structuredpy文件)
  - [2.5 sqlang_structured.py文件](#sqlang_structuredpy文件)
  - [2.6 word_dict.py文件](#word_dictpy文件)

## 一、项目框架
```
|── gs_processing  
│     └── embeddings_process.py  
│     └── getStru2Vec.py
│     └── process_single_corpus.py
│     └── python_structured.py
│     └── sqlang_structured.py
│     └── word_dirt.py
```
此仓库通过修改代码注释，在不改变代码原始功能的前提下提高代码的可读性。

## 二、文件说明

### embeddings_process.py 

#### 1. 概述
处理词向量，构建词典和词向量矩阵，并提供函数对语料数据进行序列化，以便后续的模型训练和评估。

#### 2. 具体功能
- `trans_bin`：用于将文本格式的词向量文件转换为二进制格式。
过程：
(1)使用gensim.models.KeyedVectors的load_word2vec_format方法加载文本格式的词向量文件；
(2)使用init_sims方法初始化词向量模型；
(3)使用save方法将词向量模型保存为二进制文件。
- `get_new_dict`：用于构建新的词典和词向量矩阵。
过程：
(1)使用KeyedVectors.load方法加载原始词向量模型；
(2)读取原始词典文件中的所有单词；
(3)创建一个包含特殊标记（PAD、SOS、EOS、UNK）的词典列表，并为每个单词分配一个唯一的索引。对于每个单词，尝试从词向量模型中获取其对应的词向量，如果成功则将其添加到词向量矩阵中，否则将其添加到失败列表中；(4)将词典和词向量矩阵保存为二进制文件。
- `get_index`：根据文本内容和词典，获取文本中每个词在词典中的索引。
过程：
(1)根据文本类型（"code"或"text"）和词典，获取每个词的索引。
(2)如果文本是代码类型，则在索引列表的开始添加特殊标记；如果文本长度超过特定阈值，则截断或填充索引列表，以适应预定义的长度。
- `Serialization`：将训练、测试和验证语料进行序列化处理。
过程：
(1)加载词典和语料库文件；
(2)读取原始语料文件。对于每个语料样本，提取查询、上下文和代码等信息，并将它们转换为词在词典中的位置列表。最后将这些信息组合成一个列表，并将其添加到总数据列表中；
(3)将总数据列表保存到指定的文件中。
- `__main__`：设置了一系列路径，用于指定输入和输出文件的位置。调用一系列函数，包括将词向量文件转换为二进制格式、构建新的词典和词向量矩阵、获取词在词典中的位置以及将语料序列化为二进制文件。
---
### getStru2Vec.py文件

#### 1. 概述
对给定的Python和SQL语料数据进行处理，包括解析上下文(context)、查询(query)和代码(code)，将其解析成结构化的形式，并将处理后的数据保存为pickle文件。

#### 2. 具体功能
- `multipro_python_query`：多进程函数。并行处理Python查询数据，对每条数据进行解析和分词处理。
- `multipro_python_code`：多进程函数。并行处理Python代码数据，对每条数据进行解析和分词处理。
- `multipro_python_context`：多进程函数。并行处理Python上下文数据，对每条数据进行解析和分词处理。
- `multipro_sqlang_query`：多进程函数。并行处理SQL查询数据，对每条数据进行解析和分词处理。
- `multipro_sqlang_code`：多进程函数。并行处理SQL代码数据，对每条数据进行解析和分词处理。
- `multipro_sqlang_context`：多进程函数。并行处理SQL上下文数据，对每条数据进行解析和分词处理。
- `parse`：用于将数据列表分割成小块，并使用多进程分别解析上下文、查询和代码数据。
过程：
(1)接受一个数据列表、一个分割数、三个函数作为参数；
(2)使用multiprocessing.Pool()创建一个进程池，将数据集分割成多个子列表，并使用进程池对每个子集应用相应的处理函数；
(3)合并所有解析结果并返回。
- `main`：接受语言类型、分割数、源文件路径、保存路径和三个处理函数作为参数。
过程：
(1)从源文件加载语料数据;
(2)调用parse函数解析数据,将处理后的数据按照指定的格式组合成一个列表，并将该列表保存到指定的文件中。
- `__main__`：定义了保存Python和SQL语料数据的路径，并调用main函数对不同类型的数据集进行处理，并将处理后的数据保存到相应的文件中。
---
### process_single_corpus.py文件

#### 1. 概述
处理已经解析的Python和SQL语料数据，并对数据进行处理和分割，最终保存到不同的文件中。

#### 2. 具体功能
- `load_pickle`：加载pickle格式的文件并返回其中的数据。
过程：
(1)使用open函数以二进制读取模式打开文件；
(2)使用pickle.load方法加载文件数据，然后返回加载的数据。
- `split_data`：将语料库数据分为单一元素和多个元素两个列表。
过程：
(1)遍历语料库数据，提取每个样本的qid。使用Counter计算每个qid的频率；
(2)根据qid的频率，将数据分为单一元素和多个元素两类。
- `data_staqc_processing`：处理STAQC数据集，并将结果保存到指定的文件中。
过程：
(1)使用load_pickle函数加载STAQC数据集；
(2)提取qid并调用split_data()函数进行分割，然后将值保存到不同的文件中。
- `data_large_processing`：处理大规模语料数据，并将结果保存到指定的文件中。
过程：
(1)使用load_pickle函数加载大语料库数据；
(2)提取qid并调用split_data()函数进行分割，然后将值保存到不同的文件中。
- `single_unlabeled_to_labeled`：将单一未标记数据转换为带有标签的数据。
过程：
(1)使用load_pickle函数加载单条未标注数据；
(2)将每个样本的label设置为1(表示标注)。
- `__main__`：对Python和SQL数据分别调用data_staqc_processing()和data_large_processing()处理数据，并保存到单一元素和多个元素文件中。然后调用single_unlabeled_to_labeled()函数将单一未标记的数据转换为带有标签的有序数据，并将结果保存到文件中。
---

### python_structured.py文件

#### 1. 概述
用于处理和分析自然语言文本和Python代码，包括预处理、分词、词性标注、词性还原和词干提取等步骤。

#### 2. 具体功能
- `repair_program_io`：修复Python代码中的输入输出格式错误.它识别并修复了两种常见的情况。
情况1：
pattern_case1_in: 匹配输入格式In [行号]:
pattern_case1_out: 匹配输出格式Out [行号]:
pattern_case1_cont: 匹配连续的.号
情况2：
pattern_case2_in: 匹配>>>
pattern_case2_cont: 匹配.号连续
过程：
(1)将代码按行分割成多行，并为每一行分配一个标志lines_flags，表示该行匹配的模式；
(2)根据匹配的模式，修复代码。如果代码中没有模式匹配，说明不需要修复，直接返回原始代码；如果代码中存在pattern_case1_in和pattern_case1_out的模式，或者pattern_case2_in和pattern_case2_cont的模式，函数会修复代码。修复过程包括识别连续的.号，并将它们替换为适当的换行符。
(3)修复后的代码可能会被分割成多个代码块，这些代码块被存储在code_list列表中。返回修复后的代码和代码块列表。
- `get_vars`：遍历抽象语法树（AST）的节点，找到所有不是Load上下文的变量名，并将它们排序后返回。
- `get_vars_heuristics`：从给定的代码中提取变量名。
过程：
(1)将代码按行分割，然后尝试对每一行进行解析，获取其中的变量名。如果解析失败，则减少行数重新尝试；
(2)对于剩余的行，使用正则表达式匹配变量赋值和循环语句中的变量名，并将其添加到结果集中。最终返回所有变量名的集合。
- `PythonParser`：对给定的代码进行解析和分词。
过程：
(1)尝试使用ast.parse()函数解析代码，并获取其中的变量名。如果解析失败，会尝试修复代码并重新解析。如果仍然失败，会使用get_vars_heuristics()函数获取变量名；
(2)使用tokenize.generate_tokens()函数对代码进行分词。对于每个分词结果，会根据分词类型进行处理。如果分词类型是数字、字符串或换行符，会将分词结果添加到tokenized_code列表中。如果分词类型不是注释或结束标记，并且分词内容不为空，它会检查分词内容是否在变量名列表中。如果不在，它会将分词内容添加到tokenized_code列表中；否则，它会添加"VAR"；
(3)返回tokenized_code列表以及两个布尔值，分别表示变量解析是否失败和分词是否失败。
- `revert_abbrev`：将缩写还原为完整的单词。例如，将"it's"还原为"it is"，将"I'm"还原为"I am"等。
过程：
(1)使用正则表达式模式匹配各种缩写形式；
(2)使用re.sub()方法将匹配到的缩写替换为完整的单词;
(3)返回处理后的字符串。
- `get_wordpos`：接受一个参数tag。根据tag的前缀，函数返回对应的词性。
具体来说：
(1)如果tag以'J'开头，返回wordnet.ADJ（形容词）；
(2)如果tag以'V'开头，返回wordnet.VERB（动词）；
(3)如果tag以'N'开头，返回wordnet.NOUN（名词）；
(4)如果tag以'R'开头，返回wordnet.ADV（副词）；
(5)其他情况下，返回None。
- `process_nl_line`：对输入的字符串进行预处理。
过程：
(1)将缩写还原为完整形式，合并多余的制表符、换行符和空格；
(2)将骆驼命名法转换为下划线命名法；
(3)使用正则表达式匹配括号内的内容，并将其从句子中移除；
(4)去除字符串开始和末尾的空格；
(5)返回经过预处理后的句子。
- `process_sent_word`：处理自然语言句子，并进行分词、词性标注、词性还原和词干提取。
过程：
(1)分词。使用正则表达式找到句子中的单词和特殊字符，将找到的单词和特殊字符合并成一个字符串，并用空格分隔；
(2)替换特殊字符。使用正则表达式替换句子中的小数、字符串、十六进制数、数字和特殊字符。这些替换将特殊字符标记为TAGINT、TAGSTR、TAGINT、TAGINT和TAGOER；
(3)小写化。将分词后的单词转换为小写形式；
(4)词性标注。使用pos_tag函数对单词进行词性标注，将标注结果存储在tags_dict字典中；
(5)词性还原。对于具有特定词性的单词（如形容词、动词、名词和副词），使用wnler.lemmatize函数进行词性还原；
(6)词干提取。使用wordnet.morphy函数尝试提取单词的词干，如果提取失败，保留原始单词。
- `filter_all_invachar`：去除字符串中的非常用符号，以防止解析有误。
过程：
(1)使用正则表达式替换掉所有非数字、字母、横杠、下划线、单引号和双引号的字符；
(2)将连续的中横线替换为单个中横线；
(3)将连续的下划线替换为单个下划线；
(4)去除横杠和竖杠;
(5)最后，函数返回处理后的字符串。
- `filter_part_invachar`：去除字符串中的非常用符号，以防止解析有误。
过程：
(1)使用正则表达式替换掉所有非数字、字母、横杠、下划线、单引号和双引号的字符；
(2)将连续的中横线替换为单个中横线；
(3)将连续的下划线替换为单个下划线；
(4)去除横杠和竖杠;
(5)最后，函数返回处理后的字符串。
- `python_code_parse`：接受一个字符串参数line，然后对其进行一系列的处理，最后返回一个包含处理后的单词的列表。
过程：
(1)使用filter_part_invachar函数过滤掉所有非英文字母数字和换行符的字符；使用正则表达式替换连续的点号、制表符、换行符，以减少字符串中的空格；使用正则表达式替换连续的空格，以减少字符串中的空格；使用strip()方法去除字符串的开始和末尾的换行符；
(2)使用re.findall方法找到句子中的单词和特殊字符，将找到的单词和特殊字符合并成一个字符串，并用空格分隔；
(3)尝试使用PythonParser解析字符串，如果解析失败，返回'-1000'。将解析后的代码转换为下划线命名法；
(4)将所有单词转换为小写，去除空字符串和只包含空格的字符串。
- `python_query_parse`：接受一个字符串参数line，然后对其进行一系列的处理，最后返回一个包含处理后的单词的列表。
过程：
(1)使用filter_all_invachar函数过滤掉所有非英文字母数字和换行符的字符；
(2)使用process_nl_line函数对查询进行预处理，包括重写缩略词、替换连续的制表符和换行符、替换连续的空格、骆驼命名法转下划线等；
(3)使用process_sent_word函数对预处理后的查询进行分词和词性标注；
(4)遍历分词后的单词列表，如果单词包含括号，则将其替换为空字符串，使用列表推导式过滤掉单词列表中的空字符串和单个空格。
- `python_context_parse`：接受一个字符串参数line，然后对其进行一系列的处理，最后返回一个包含处理后的单词的列表。
过程：
(1)使用filter_all_invachar函数过滤掉所有非英文字母数字和换行符的字符；
(2)使用process_nl_line函数对上下文进行预处理，包括重写缩略词、替换连续的制表符和换行符、替换连续的空格、骆驼命名法转下划线等；
(3)使用process_sent_word函数对预处理后的上下文进行分词和词性标注；
(4)使用列表推导式过滤掉单词列表中的空字符串和单个空格。
- `__main__`：对输入的字符串进行处理，返回一个包含处理后的单词的列表。
---

### sqlang_structured.py文件

#### 1. 概述
完成一个SQL语言解析器的功能，用于对SQL代码进行解析和处理。

#### 2. 具体功能
- `tokenizeRegex`：使用正则表达式模式将字符串进行分词，返回分词后的结果。
- `sanitizeSql`：对输入的SQL语句进行清理和规范化。
过程：
(1)使用strip()方法去除字符串两端的空白字符，并使用lower()方法将字符串转换为小写；
(2)检查字符串的最后一个字符是否为分号，如果不是，则在字符串末尾添加一个分号；
(3)使用正则表达式替换括号，定义一个包含单词的列表，如'index'、'table'、'day'、'year'、'user'和'text'。对于列表中的每个单词，使用正则表达式替换字符串中以该单词结尾的部分，将其替换为该单词后跟数字1。同时，如果该单词位于其他单词之间，也会进行相应的替换；
(4)使用replace()方法删除字符串中的所有#号。
- `parseStrings`：用于处理SQL语句中的字符串。
过程：
(1)如果tok是一个sqlparse.sql.TokenList对象，即一个包含多个子token的列表，则递归地调用parseStrings方法来处理每个子token；
(2)如果tok的类型是STRING，即它是一个字符串字面量，则根据self.regex的值来决定如何处理该字符串。如果self.regex为True，表示启用了正则表达式分词，则使用tokenizeRegex函数将字符串分词成单词，并将这些单词用空格连接成一个字符串。如果self.regex为False，表示没有启用正则表达式分词，则将字符串标记为代码字符串（CODSTR），以便于后续处理；
(3)将处理后的字符串值赋给tok.value，这样原始的字符串字面量就被修改了，其值被替换为处理后的字符串。
- `renameIdentifiers`：重命名SQL语句中的标识符（列名和表名）。
过程：
(1)如果tok是一个sqlparse.sql.TokenList对象，即一个包含多个子token的列表，则递归地调用renameIdentifiers方法来处理每个子token；
(2)如果tok的类型是COLUMN，即它是一个列名，则检查该列名是否已经在idMap["COLUMN"]字典中。如果列名不在字典中，则分配一个新的名称，格式为col加上一个递增的数字。将新的列名存储在idMap["COLUMN"]字典中，并将原始列名作为键存储在idMapInv字典中。更新idCount["COLUMN"]以反映新的列名分配。将新的列名赋值给tok.value；
(3)如果tok的类型是TABLE，即它是一个表名，则处理方式与列名类似，只是使用tab作为前缀；
(4)对于其他类型的token（如FLOAT、INTEGER、HEX），直接将它们的值替换为特定的代码字符串（CODFLO、CODINT、CODHEX）。
- `__hash__`：用于计算对象的哈希值。
- `__init__`：用于解析和分析SQL语句，提取关键信息。
- `getTokens`：将parse中的字符串表达式展平，并将其拆分为单词列表。
过程：
(1)创建一个空列表flatParse，然后遍历parse中的每个表达式。对于每个表达式，它会调用flatten()方法将其展平，并遍历展平后的每个token；
(2)如果token的类型是字符串（即token.ttype == STRING），则将该字符串拆分为单词列表，并将其添加到flatParse中。否则，直接将token转换为字符串并添加到flatParse中；
(3)返回flatParse列表。移除tok中的空白字符。
- `removeWhitespaces`：从解析后的SQL语句中移除所有空白字符。
过程：
(1)如果tok是一个sqlparse.sql.TokenList对象，即一个包含多个子token的列表，则递归地调用removeWhitespaces方法来处理每个子token；
(2)对于tok中的每个子tokenc，检查它是否是空白字符。如果c不是空白字符，将其添加到临时列表tmpChildren中。更新tok.tokens属性，将其替换为tmpChildren列表，这样tok中只包含非空白字符的token；
(3)对于tok中的每个非空白字符的token，再次调用removeWhitespaces方法，以递归地移除它们的子token中的空白字符。
- `identifySubQueries`：用于识别SQL语句中的子查询。
过程：
(1)设置一个标志isSubQuery为False；
(2)遍历tokenList，这是使用sqlparse解析后的SQL语句的解析树；
(3)对于每个tokentok，执行以下操作：如果tok是一个sqlparse.sql.TokenList对象，即一个包含多个子token的列表，则递归地调用identifySubQueries方法来处理每个子token。如果递归处理返回True，并且tok是一个sqlparse.sql.Parenthesis对象，则将tok.ttype设置为SUBQUERY，表示这是一个子查询。如果tok是"select"关键字，则将isSubQuery设置为True；
(4)遍历结束后，返回isSubQuery的值。如果过程中遇到子查询，isSubQuery将被设置为True；否则保持False。
- `identifyLiterals`：用于识别SQL语句中的文字字面量。
过程：
(1)遍历解析树中的每个token，并根据其类型分配一个类型标签；
(2)对于数字、字符串和通配符，将它们的类型标记为INTEGER、STRING和WILDCARD。对于其他类型的token，根据其内容（如关键字、列名等）将其类型标记为KEYWORD、COLUMN。
- `identifyFunctions`：用于识别SQL语句中的函数。
过程：
(1)遍历解析树中的每个token，并根据其类型和内容标记函数；
(2)如果token是一个函数对象，则将其类型标记为FUNCTION。如果token是sqlparse.sql.Parenthesis对象，则表示它可能包含一个子查询，此时将函数标记重置为False。如果token是一个sqlparse.sql.TokenList对象，即一个包含多个子token的列表，则递归地调用identifyFunctions方法来处理每个子token。
- `identifyTables`：用于识别SQL语句中的表。
过程：
(1)遍历解析树中的每个token，并根据其类型和内容标记表；
(2)对于列名和表名，根据它们的位置和关系将其类型标记为TABLE；
(3)如果token的类型是SUBQUERY，则将表标记栈添加一个元素。如果token的类型是COLUMN，并且当前表标记栈的顶部元素为True，则将列名标记为TABLE。如果token的类型是SUBQUERY，则将表标记栈弹出一个元素。
- `__str__`：用于定义类的字符串表示。
- `parseSql`：用于返回解析后的SQL语句的token列表的字符串表示。
- `revert_abbrev`：将缩写还原为完整的单词。例如，将"it's"还原为"it is"，将"I'm"还原为"I am"等。
过程：
(1)使用正则表达式模块re定义了一系列模式，用于匹配和替换缩写；
(2)使用sub()方法将这些缩写替换为完整的单词；
(3)返回处理后的字符串。
- `get_wordpos`：根据输入的词性标签（tag）返回对应的词性。根据输入的词性标签（tag），通过判断其开头字母来确定具体的词性。
(1)如果标签以'J'开头，则返回wordnet.ADJ表示形容词；
(2)如果以'V'开头，则返回wordnet.VERB表示动词；如果以'N'开头，则返回wordnet.NOUN表示名词；
(3)如果以'R'开头，则返回wordnet.ADV表示副词。
(4)如果无法匹配到任何已知的词性，则返回None。
- `process_nl_line`：对输入的字符串进行预处理。
过程：
(1)使用revert_abbrev函数将句子中的缩写词重写为完整的单词；
(2)去除空白字符；
(3)将句子中的骆驼命名法的单词转换为下划线形式；
(4)使用正则表达式匹配括号内的内容，并将其从句子中移除；
(5)使用strip()方法去除句子的末尾的点号和空格。
- `process_sent_word`：对句子进行分词、词性标注、词性还原和词干提取。
过程：
(1)使用正则表达式找到句子中的单词和特殊字符，将找到的单词和特殊字符合并成一个字符串，并用空格分隔；
(2)使用正则表达式替换句子中的小数、字符串、十六进制数、数字和特殊字符，这些替换将特殊字符标记为TAGINT、TAGSTR、TAGINT、TAGINT和TAGOER；
(3)将分词后的单词转换为小写形式；
(4)使用pos_tag函数对单词进行词性标注，将标注结果存储在tags_dict字典中；
(5)对于具有特定词性的单词（如形容词、动词、名词和副词）进行词性还原，提取单词的词干。
- `filter_all_invachar`：过滤掉输入字符串中的所有非常用字符，只保留英文字母、数字、中横线、下划线、单引号、双引号和换行符。
- `filter_part_invachar`：过滤掉输入字符串中的部分非常用字符，只保留英文字母、数字、中横线、下划线、斜杠（/）、单引号（'）、花括号（{、}）和换行符（\n）等。
- `sqlang_code_parse`：解析SQL代码，移除多余的空白字符、换行符和制表符，还替换了小数点为单词"number"。尝试使用SqlangParser解析SQL语句，并将结果转换为小写，使用下划线分隔的格式。
- `sqlang_query_parse`：首先移除所有非文字字符，然后对句子进行分词处理，并最终移除括号。
- `sqlang_context_parse`：处理上下文信息，移除部分非文字字符，并对句子进行分词处理。
- `__main__`：调用函数，用于解析SQL语句。
---

### word_dict.py文件

#### 1. 概述
加载两个语料库，获取它们的词汇表，并保存排除重复词汇后的词汇表。

#### 2. 具体功能
- `get_vocab`：获取两个语料库的词汇表。
过程：
(1)初始化一个空集合word_vocab，用于存储词汇;
(2)遍历两个语料库中的每个元素，将其中的词汇添加到word_vocab中。
- `load_pickle`：用于从文件中加载pickle数据。使用pickle.load()方法从文件中加载数据，并返回加载的数据。
- `vocab_processing`：用于处理词汇表。
过程：
(1)从两个文件中读取数据，然后调用get_vocab()函数获取词汇表；
(2)计算两个词汇表的交集，并将交集中的词汇从词汇表中移除;
(3)将处理后的词汇表保存到指定的文件中。
- `__main__`：定义两个语料库的文件路径、词汇表的文件路径和词汇表保存路径，接着调用vocab_processing函数处理两个语料库的词汇表。
