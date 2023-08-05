import gc 
import re 
import sys  
import warnings 
import os 
import time  
from datetime import datetime 
import warnings   
import pandas as pd
import numpy as np
import hashlib
from collections import defaultdict,Counter

from common_utils.sequence_functions import list_diff_outer_join, lcs, filter_lcs
from common_utils.os_functions import *
from common_utils.df_functions import *
from common_utils.config_table import ConfigReader 
from common_utils.excel_functions import write_format_columns
from common_utils.regex_functions import replace_re_special, replace_punctuations
from common_utils.decorator_functions import *
from common_utils.data_handle_func import * 

class CsvSheetClass(object):
    def __init__(self, table_path):
        self.name = '{}'.format(table_path)
        self.visibility = 0

class Handler(object):

    def __init__(self, require_file_path, data_file_path,table_dict):
        #获取以下两个即可读取所有的原始数据和规则表
        #original data files 
        self.data_file_path = data_file_path
        #config table dict 
        self.table_dict = table_dict
        self.require_file_path = require_file_path


    @catch_and_print
    def get_original2cn_dict(self, header_table_df, file_tag):
        """
        将所有原始mapping成中文表头,按国家区分字典
        """
        original2cn_dict_list = []
        original2cn_dict = defaultdict(str)
        fillna_dict = {}
        dtype_dict = {}

        if file_tag.lower() not in [ x.lower() for x in header_table_df.columns.get_level_values(0) ] :
            file_tag = 'Without file tag'

        header_column_index = header_table_df.columns.get_level_values(
            0) == file_tag.lower()

        header_table_df_c = header_table_df.iloc[:, header_column_index]

        header_table_first_three_c = header_table_df.loc[:, header_table_df.columns.get_level_values(0)[
            0]]

        # 同时获取填充的
        for row, last_three in zip(header_table_df_c.iterrows(), header_table_first_three_c.iterrows()):
            # 表头统一小写，换行符,空格全部去掉
            row_list = row[1].values
            last_three_list = last_three[1].values
            a_list = list(row_list)
            b_list = list(last_three_list)
            a_list = [str(x).lower().strip().replace('\n', '').replace('\xa0', '').replace(' ', '').replace('\t', '')
                      for x in a_list if x.strip() != '无' and x.strip().lower() != 'none' and x.strip() != '/' and x.strip() != '']

            if a_list:
                for x in a_list:
                    original2cn_dict[x] = b_list[2]

            # 构建需要合并前填充的字典
            c_list = [x for x in a_list if x.split(':')[0].lower().strip() == 'fillbeforeconcat' or x.split(':')[0].strip() == '合并前填充']

            if c_list:
                for x in c_list:
                    fillna_dict[b_list[2]] = x.split(':')[1]

            if (b_list[1] != '默认' and b_list[1].lower() != 'default' and b_list[1] != '') and b_list[2] != '':
                dtype_dict.update({b_list[2]: b_list[1]})

        return original2cn_dict, fillna_dict, dtype_dict

    #合并读取的数据表格, 该函数需要输入table_dict因为需要读取到, complete_header_df, 和target_cn_columns
    @get_run_time
    def concat_data(self, table_dict):
        # 此函数读取放入的数据表，必须要运行
        for keys in table_dict.keys():
            if 'mapping' in keys.lower():
                mapping_key = keys
        try:
            header_table_df = table_dict[mapping_key]
        except KeyError:
            enter_exit('Cannot find mapping configuration sheet!')

        complete_header_df = table_dict['complete_header_df']
        target_cn_columns = table_dict['target_cn_columns']

        header_table_df = df_fillna_str(header_table_df)
        info_path_list = get_walk_abs_files(self.data_file_path)

        # 检查是否有读取到各国的原始数据
        info_path_list = [x for x in info_path_list if '~$' not in x and (
            x[-5:].lower() == '.xlsx' or x[-4:].lower() in ['.xls', '.csv'])]

        if len(info_path_list) == 0:
            enter_exit('Cannot find any data file in folder data_files !\n')

        success_sheet_df_list = []

        for table_path in info_path_list:
            table_p = Path(table_path)
            table_stem = table_p.stem
            table_suffix = table_p.suffix

            # 读取文件名的信息
            file_tag = table_stem.split('-')[0]

            # 获取这个文档的映射字典  将原始mapping成中文表头
            original2cn_dict, fillna_dict, dtype_dict = self.get_original2cn_dict(header_table_df, file_tag)

            if not original2cn_dict:
                enter_exit('"Data_processing_configuration" required mapping field "{}" not found !'.format(file_tag))

            # 如果是CSV文档
            is_csv = False
            is_xls_special = False
            if table_suffix == '.csv':
                is_csv = True
                csv_sheet_class = CsvSheetClass(table_stem)
                sheets_property_list = [csv_sheet_class]
            else:
                try:
                    df_workbook = pd.ExcelFile(table_path)
                    sheets_property_list = df_workbook.book.sheets()
                except : #如果读取失败，尝试读取其他国家xls文档的格式
                    is_xls_special == True 
                    xls_sheet_class = CsvSheetClass(table_stem)
                    sheets_property_list = [xls_sheet_class]

            # 过滤掉模板数据
            for sheets_property in sheets_property_list:
                sheet = sheets_property.name
                sheet_visibility = sheets_property.visibility

                if sheet_visibility == 0:  # 只读取可见的Sheet

                    if is_csv:
                        df_worksheet = read_csv_data(table_path)
                        if df_worksheet.empty:
                            continue
                    elif is_xls_special:
                        df_worksheet = read_xls_special(table_path)
                        if df_worksheet.empty:
                            continue
                    else:
                        df_worksheet = df_workbook.parse(sheet, na_values='')

                    # 表头做小写等替换并且，通过字典rename,全部调整成去掉中间空格、去掉一切无意义符号的字段
                    df_worksheet.columns = [str(x).lower().strip().replace('\n', '').replace('\xa0', '')
                                            .replace(' ', '').replace('\t', '')if x == x else x for x in df_worksheet.columns]

                    df_worksheet = dropping_not_mapping(df_worksheet, original2cn_dict, target_cn_columns)

                    #mapping填入了 + 号
                    df_worksheet = combine_multi_plus(df_worksheet, original2cn_dict)

                    #mapping前检查是否有重复的字段，如果原表已经有别的字段映射成"机型"，那原表里面的"机型"字段属于要抛弃的字段
                    df_work_sheet = drop_duplicated_columns_before_rename(df_worksheet, original2cn_dict)

                    df_worksheet = df_worksheet.rename(original2cn_dict, axis=1)

                    # 还必须要确认映射的字段没有重复，否则会影响到后面的数据列, 返回一个没有重复的字段列
                    target_cn_columns = check_mapping_duplicates(df_worksheet, target_cn_columns, table_stem=table_stem)

                    # 重命名之后，合并前需要填充默认值
                    df_worksheet = fillna_with_dict(df_worksheet, fillna_dict)

                    # 检查完重复映射之后 需要再定位一次需要的字段, 注意处理顺序
                    df_worksheet = func_loc(df_worksheet, target_cn_columns)

                    if not df_worksheet.empty:
                        check_mapping_complete(df_worksheet, complete_header_df, original2cn_dict,file_tag=file_tag)

                        complete_header_df = dtype_handle(complete_header_df, dtype_dict)
                        # 记录成功表格
                        success_sheet_df_list.append([table_stem, sheet, df_worksheet.shape[0]])
                        complete_header_df = pd.concat([complete_header_df, df_worksheet], axis=0, sort=False, ignore_index=True)

                        print(f'Getting from: "{table_stem}" Number or rows: {df_worksheet.shape[0]}')

            success_sheet_df = pd.DataFrame(success_sheet_df_list, columns=['File Name', 'Source Sheet', 'Success reading records'])

        print(f'Data rows:{complete_header_df.shape[0]}')
        return complete_header_df, success_sheet_df


     # 1.字段标准化 : 是否考虑先做关联匹配以加速运行? -- 不可行，关联的国家字段需要先标准化才能用来统一关联匹配
    @get_run_time
    def standardize_columns(self, complete_header_df, standardize_config_df):
        # 将字段处理为标准表里的字段（模糊匹配）
        table_values = standardize_config_df.values
        not_standardize_df_list = []
        complete_header_df_sub_list = []
        partial_match_not_match_df_list = []

        row_counter = 0
        for row in table_values:
            row_counter += 1
            source_column = row[1]
            standard_table_name = row[2]
            standard_column = row[3]
            target_column = row[4]
            target_column_edit = row[5]
            order_columns = row[6]
            try:
                replace_dict = [x.strip()for x in row[7].split('\n') if x.strip() != '']
                replace_dict = dict([[y.strip() for y in x.replace('：', ':').split(':')] for x in replace_dict])
            except:
                replace_dict = {}
            special_syn = [x.lower() for x in row[8].split('\n')]  # 两边需要同时存在的字符
            filter_condition = row[9]
            # 标准化模式：简单模糊匹配 -- simple_lcs  严格模糊匹配 -- filter_lcs, 内存配置匹配--number_similarity
            standardize_mode = row[10]
                
            #决定最后的结果字段名称
            temp_column = ''
            if target_column_edit == source_column:
                temp_column = source_column
            else:
                temp_column = target_column_edit

            # 先把空值的数据剔除再做模糊匹配
            complete_header_df_notna = complete_header_df.loc[complete_header_df[source_column].isna() == False, :]
            complete_header_df_nan = complete_header_df.loc[complete_header_df[source_column].isna(), :]
            #过滤后全都是空值的话 直接继续下一行
            if complete_header_df_notna.empty:
                continue

            if standard_table_name != '' and standard_column.strip() != '':

                mode = get_standard_mode(standardize_mode)
                
                print(f'{row_counter}.Processing standardization for "{source_column}"')
                print(f'-- Referencing from table "{standard_table_name}" column "{target_column}",Mode:{standardize_mode}')
                standard_table_path = get_require_files(self.require_file_path, [standard_table_name])[standard_table_name]
                # 统一将原始关联表转成str格式
                standard_table_df = pd.read_excel(standard_table_path, dtype=str)
                ##读取出来的表 统一做删除重复字段处理
                standard_table_df = remove_duplicate_columns(standard_table_df)

                # 标准对照表排序,排序完之后删除重复项，似的做了排序后的结果取的是第一行上市日期最近的机型（后面循环的时候做duplicates删除）
                if order_columns != '':
                    standard_table_df = process_sort_order(standard_table_df, [standard_column], order_columns)

                # 需要对标准表做重复删除，类似字段匹配, 但不相同
                # 标准化前的第一层简单过滤
                filter_condition_2_columns_tag, filter_left_column, filter_right_column = False, '', ''

                if filter_condition != '':
                    filter_condition_2_columns_tag, filter_left_column, filter_right_column = \
                        get_filter_condition_standardize_tag(filter_condition)

                if filter_condition != '' and filter_condition_2_columns_tag == False:
                    try:
                        standard_table_df = standard_table_df.query(filter_condition)
                    except:
                        enter_exit(f'Standardization: Failed to compile condition: {filter_condition}')

                #转成半角符号
                standard_table_df[standard_column] = standard_table_df[standard_column].apply(
                                                            lambda x : strQ2B(x) if type(x) == str else x ) 
                complete_header_df_notna[source_column] = complete_header_df_notna[source_column].apply(
                                                            lambda x : strQ2B(x) if type(x) == str else x)
                # 标准化前的第二层检查过滤(过滤条件涉及两张表的字段相等(不同国家的机型匹配))
                # 如果存在另外一种过滤方式--左右表的字段相等, 需要循环条件 进行模糊匹配
                if filter_condition_2_columns_tag:
                    # 模糊关联匹配之前，必须做去重，防止笛卡尔积现象（模糊匹配防止获取的不是排序第一的数据）
                    try:
                        # 需要保留一个模糊匹配需要获取的 target_column
                        standard_table_df_x = standard_table_df.loc[:, [standard_column, target_column, filter_left_column]]\
                            .drop_duplicates(subset=[standard_column, filter_left_column], keep='first')
                    except KeyError:
                        lack_column_list = find_lack_columns(
                            standard_table_df, [standard_column, target_column, filter_left_column])


                    # 循环获取模糊匹配结果
                    if filter_right_column not in complete_header_df_notna.columns:
                        enter_exit(f'Standardization Error: Cannot find column:"{filter_right_column}"')
                    #记录每个的情况
                    complete_header_df_sub_list = []
                    for u in complete_header_df_notna[filter_right_column].unique()  :

                        temp_standard_df = standard_table_df_x\
                                .loc[standard_table_df_x[filter_left_column] == u, [standard_column, target_column]]
                        standard_dict = temp_standard_df.to_dict()

                        print(f'Standardizing: "{u}"--"{source_column}"')

                        standard_dict = {x: y for x, y in zip(
                            standard_dict[standard_column].values(), standard_dict[target_column].values())}

                        complete_header_df_sub = complete_header_df_notna.loc[
                            complete_header_df_notna[filter_right_column] == u, :]

                        complete_header_df_sub[temp_column] = complete_header_df_sub[source_column].fillna(value='').astype(str)

                        complete_header_df_sub[temp_column] = complete_header_df_sub[temp_column].apply(
                                lambda x: standardize_column_func(
                                x, standard_dict, special_syn, replace_dict, ignore_punctuation=True, mode=mode))

                        complete_header_df_sub_list.append(complete_header_df_sub)

                    if len(complete_header_df_sub_list) == 1:
                        complete_header_df_notna = complete_header_df_sub_list[0]
                    elif len(complete_header_df_sub_list) >= 2 :
                        complete_header_df_notna = pd.concat(complete_header_df_sub_list, axis=0, ignore_index=True)
                    else: #complete_header_df_sub都没有,生成一列空白的结果
                        complete_header_df_notna[temp_column] = ''

                # 如果是普通的df quiry过滤方式
                else:
                    # 提取出标准列表
                    try:
                        standard_dict = standard_table_df.loc[:, [standard_column, target_column]].to_dict()
                        standard_dict = {x: y for x, y in zip(standard_dict[standard_column].values(), 
                                                                standard_dict[target_column].values())}
                    except KeyError:
                        lack_column_list = find_lack_columns(standard_table_df, [standard_column, target_column])
                        error_msg = ','.join(lack_column_list)
                        enter_exit(f'Standardization reference table error: Column {error_msg} is not found!')

                    complete_header_df_notna[temp_column] = complete_header_df_notna[source_column]\
                            .apply(lambda x: standardize_column_func(x, standard_dict, special_syn, replace_dict,
                                                    ignore_punctuation=True, mode=mode) if type(x) == str else x)

                # 空的和处理过的非空数据记得合并
                complete_header_df = pd.concat([complete_header_df_notna, complete_header_df_nan], axis=0, ignore_index=True)

                # 需要记录这两个字段分别有哪些记录匹配不上
                partial_match_not_match_df = get_partial_not_match(complete_header_df_notna,row_counter,source_column,
                                                                    standard_table_name, standard_column,
                                                                    filter_condition, target_column_edit )

                partial_match_not_match_df_list.append(partial_match_not_match_df)

        if partial_match_not_match_df_list:
            partial_match_not_match_df = pd.concat(partial_match_not_match_df_list, axis=0, ignore_index=True)

        # 模糊匹配的因为涉及"获取结果的字段名称"可能会修改成原始字段名称，判断复杂, 故不做记录

        print(f'Data rows:{complete_header_df.shape[0]}')
        return complete_header_df, partial_match_not_match_df

    # 2.字段拆分
    @get_run_time
    def split_columns(self, complete_header_df, split_table_df):

        split_words_dict = get_split_config_dict(self.require_file_path, split_table_df)
        complete_header_df = split_column_by_words(
            complete_header_df, split_words_dict)

        print(f'Data rows:{complete_header_df.shape[0]}')
        return complete_header_df

    # 3.字段匹配
    @get_run_time
    def match_columns(self, complete_header_df, match_table_df):
        table_values = df_fillna_str(match_table_df).values

        not_match_df_list = []
        for row in table_values:
            source_columns = row[1].replace('：', ':').split(':')  # 目的表字段
            join_table_name = row[2]  # 关联表
            join_columns = row[3].replace('：', ':').split(':')  # 关联字段
            target_column = row[4]  # 想获取的目标字段
            target_column_edit = row[5]  # 结果字段名称
            filter_condition = row[6]  # 关联表过滤条件
            sort_order = row[7]  # 匹配前的去重排序
            match_mode = row[8]  # 匹配模式：1.case insensitive 2.case sensitive
            # For columns with spaces in their name, you can use backtick quoting.

            if join_columns != '':
                # 检查合并表 有没有这两个字段
                for s in source_columns:
                    if s not in complete_header_df.columns:
                        enter_exit(
                            f'Matching error: Target table cannot find column:"{s}"')

                if len(source_columns) != len(join_columns):
                    min_num = min([len(source_columns), len(join_column)])
                    source_columns = source_columns[:min_num+1]
                    join_columns = join_columns[:min_num+1]

                join_table_path = get_require_files(
                    self.require_file_path, [join_table_name])[join_table_name]
                join_table_df = pd.read_excel(join_table_path, dtype=str)
                ##读取出来的表 统一做删除重复字段处理
                join_table_df = remove_duplicate_columns(join_table_df)
                
                # 防止只匹配表只有一列，并且只想获取该列结果
                only_one_match_column = False
                if len(join_columns) == 1 and join_columns[0] == target_column:
                    only_one_match_column = True
                    join_table_df['additional_temp'] = join_table_df[target_column]
                    join_columns = join_columns + ['additional_temp']
                else:
                    join_columns = join_columns + [target_column]

                order_columns_new = []
                reverse_ordere_new = []

                if sort_order != '':
                    join_table_df = process_sort_order(
                        join_table_df, join_columns, sort_order)

                # 获取过滤条件后的关联表
                join_table_df = get_filter_condition_match(
                    join_table_df, filter_condition, join_columns)

                # 将剩下的所有关联列转成string格式
                try:
                    join_table_df = join_table_df.loc[:, join_columns].apply(
                        lambda x: x.fillna('').astype(str))
                except KeyError:
                    lack_column_list = find_lack_columns(
                        join_table_df, join_columns)
                    error_msg = ','.join(lack_column_list)
                    enter_exit(
                        f'Error:Matching table "{join_table_name}" have no column named "{error_msg}" or this column name is duplicated')

                for s in source_columns:
                    complete_header_df[s] = complete_header_df[s].fillna(
                        '').astype(str)

                rename_dict = {}
                for i in range(len(source_columns)):
                    rename_dict.update({join_columns[i]: source_columns[i]})

                join_table_df = join_table_df.rename(rename_dict, axis=1)

                # 关联之前必须做去重，避免笛卡尔积现象
                join_table_df = join_table_df.drop_duplicates(
                    subset=source_columns)

                # 忽略大小写
                if match_mode == '' or match_mode.lower().replace('-', '') == 'case sensitive':
                    complete_header_df = pd.merge(
                        complete_header_df, join_table_df, 'left', on=source_columns)
                else:
                    complete_header_df = merge_case_insensitive(
                        complete_header_df, join_table_df, 'left', on=source_columns)

                if target_column_edit != target_column:
                    if target_column_edit == '' or target_column_edit in complete_header_df.columns:
                        complete_header_df = complete_header_df.drop(
                            target_column_edit, axis=1)
                        complete_header_df = complete_header_df.rename(
                            {target_column: target_column_edit}, axis=1)
                    else:
                        complete_header_df = complete_header_df.rename(
                            {target_column: target_column_edit}, axis=1)

                if only_one_match_column:
                    complete_header_df = complete_header_df.rename(
                        {'additional_temp': target_column_edit}, axis=1)

                # 记录匹配不到的数据
                not_match_df = complete_header_df.loc[complete_header_df[target_column_edit].isna(
                ), source_columns]
                not_match_df['Matching field'] = '+'.join(
                    source_columns) + ' Match ' + '+'.join(join_columns[:-1])
                shift_order_list = list(not_match_df.columns)

                not_match_df = not_match_df.loc[:, [
                    shift_order_list[-1]] + shift_order_list[:-1]]

                not_match_df_list.append(not_match_df)

        not_match_df = pd.concat(not_match_df_list, axis=0, ignore_index=True)

        not_match_df = not_match_df.drop_duplicates()

        print(f'Data rows:{complete_header_df.shape[0]}')
        return complete_header_df, not_match_df

    # 4. 字段去重, 顺便生成MD5
    @get_run_time
    def drop_duplicate_data(self, complete_header_df, drop_duplicates_table_df):
        table_values = drop_duplicates_table_df.values
        drop_subset_list = []
        md5_unique_column_list = []
        for row in table_values:
            column = row[0]
            if_drop_duplicate = row[1]
            if_gen_md5 = row[2]

            if column.strip() != '' and column in complete_header_df.columns:
                if if_drop_duplicate.lower().strip() in ['是', 'yes', 'y']:
                    drop_subset_list.append(column)
                if if_gen_md5.lower().strip() in ['是', 'yes', 'y']:
                    md5_unique_column_list.append(column)
            else:
                enter_exit(
                    f'Deduplicate reference table error: Column "{column}" not found! ')

        if drop_subset_list:
            complete_header_df = complete_header_df.drop_duplicates(
                subset=drop_subset_list)

        if md5_unique_column_list:
            complete_header_df = column_gen_md5(
                complete_header_df, md5_unique_column_list, 'MD5')

        print(f'Data rows:{complete_header_df.shape[0]}')
        return complete_header_df

    # 5.填充排序
    @get_run_time
    def fill_and_order_columns(self, complete_header_df, fill_and_order_table):

        table_values = fill_and_order_table.values
        complete_header_df_new = pd.DataFrame(data=[])

        seen_columns = set()
        sort_column_list = []
        sort_column_order_list = []

        for row in table_values:
            input_column = row[0]
            output_column = row[1]
            # 输出的类型 日期类型--不包含时分秒 normalize().date 时间类型-包含时分秒-to_datetime, 和其他pandas支持的数据类型
            output_dtype = row[2]
            # 先做内容替换，再做空值填充
            replace_value_str = row[3]
            sort_value_str = row[4]
            fillna_value_str = row[5]

            dtype_dict = {}
            if input_column != '' and output_column != '':
                if input_column not in complete_header_df.columns:
                    if_skip = input(
                        f'"{input_column}" not found in result table, thus not able to be mapped to the output result, continue?(Enter to continue)')
                    if if_skip == '' or if_skip.lower() == 'yes' or if_skip.lower() == 'y':
                        continue
                    else:
                        enter_exit('')
                #先将旧数据赋值到新数据 , 如果是重复填入的则保持用complete_header_df_new的数据处理即可
                if input_column not in seen_columns:
                    complete_header_df_new[output_column] = complete_header_df[input_column].fillna(value='')
                    seen_columns.add(input_column)
                if input_column != '':
                    if replace_value_str != '':
                        complete_header_df_new = replace_value_func(complete_header_df_new, replace_value_str, input_column, output_column)

                    # 过滤： 以下全部沿用上面获得的complete_header_df_new和他的所有output_column
                    if fillna_value_str != '':
                        for fillna_value_str_x in fillna_value_str.split(':'):
                            complete_header_df_new = fillna_value_func(
                                complete_header_df, complete_header_df_new, fillna_value_str_x, output_column)
                    # 排序：统一加到列表，统一排序
                    if sort_value_str == 'desc':
                        sort_column_list.append(output_column)
                        sort_column_order_list.append(True)
                    elif sort_value_str != '':
                        sort_column_list.append(output_column)
                        sort_column_order_list.append(True)
                    # 输出类型：
                    if output_dtype != '':
                        dtype_dict.update({output_column: output_dtype})

            complete_header_df_new = dtype_handle(
                complete_header_df_new, dtype_dict, output=True)

        if sort_column_list:
            complete_header_df_new = sort_value_func(
                complete_header_df_new, sort_column_list, sort_column_order_list)

        print(f'Data rows:{complete_header_df_new.shape[0]}')
        return complete_header_df_new

    # 6.条件过滤
    @get_run_time
    def filter_columns(self, complete_header_df, filter_condition_table):

        table_values = filter_condition_table.values
        for row in table_values:
            condition = row[0].strip()
            complete_header_df = df_query(complete_header_df, condition)

        print(f'Data rows:{complete_header_df.shape[0]}')
        return complete_header_df