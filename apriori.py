#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@author: Jan Yang
@software: PyCharm Community Edition
@time: 2018/3/26 10:47
"""


def generate_freq_supports(data_set, item_set, min_support):
    """ 从候选项集中选出频繁集

    :param data_set:
    :param item_set:
    :param min_support:
    :return:
    """

    freq_set = set()  # 保存频繁项集元素
    item_count = {}  # 保存元素频次，用于计算支持度
    supports = {}  # 保存支持度

    # 如果项集中元素在数据集中则计数
    for record in data_set:
        for item in item_set:
            if item.issubset(record):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1

    data_len = float(len(data_set))

    # 计算项集支持度
    for item in item_count:
        if (item_count[item] / data_len) >= min_support:
            freq_set.add(item)
            supports[item] = item_count[item] / data_len

    return freq_set, supports


def generate_new_combinations(freq_set, k):
    """ 生成新的频繁项集组合

    :param freq_set:
    :param k:
    :return:
    """
    new_combinations = set()  # 保存新组合
    sets_len = len(freq_set)  # 集合含有元素个数，用于遍历求得组合
    freq_set_list = list(freq_set)  # 集合转为列表用于索引

    for i in range(sets_len):
        for j in range(i + 1, sets_len):
            l1 = list(freq_set_list[i])
            l2 = list(freq_set_list[j])
            l1.sort()
            l2.sort()

            # 项集若有相同的父集则合并项集
            if l1[0:k-2] == l2[0:k-2]:
                freq_item = freq_set_list[i] | freq_set_list[j]
                new_combinations.add(freq_item)

    return new_combinations


def apriori(data_set, min_support, max_len=None):
    """ Apriori algorithm

    :param data_set:
    :param min_support:
    :param max_len:
    :return:
    """
    max_items = 2  # 初始项集元素个数
    freq_sets = []  # 保存所有频繁项集
    supports = {}  # 保存所有支持度

    # 候选项1项集
    c1 = set()
    for items in data_set:
        for item in items:
            item_set = frozenset([item])
            c1.add(item_set)

    # 频繁项1项集及齐支持度
    l1, support1 = generate_freq_supports(data_set, c1, min_support)

    freq_sets.append(l1)
    supports.update(support1)

    if max_len is None:
        max_len = float('inf')

    while max_items and max_items <= max_len:
        ci = generate_new_combinations(freq_sets[-1], max_items)  # 生成候选集
        li, support = generate_freq_supports(data_set, ci, min_support)  # 生成频繁项集和支持度

        # 如果有频繁项集则进入下个循环
        if li:
            freq_sets.append(li)
            supports.update(support)
            max_items += 1
        else:
            max_items = 0

    return freq_sets, supports


def association_rules(freq_sets, supports, min_conf):
    """ 生成满足最小置信度的关联规则

    :param freq_sets:
    :param supports:
    :param min_conf:
    :return:
    """
    rules = []
    max_len = len(freq_sets)

    # 生成关联规则，筛选符合规则的频繁集计算置信度，满足最小置信度的关联规则添加到列表
    for k in range(max_len - 1):
        for freq_set in freq_sets[k]:
            for sub_set in freq_sets[k + 1]:
                # print(freq_set, sub_set)
                if freq_set.issubset(sub_set):
                    # print(freq_set, sub_set)
                    conf = supports[sub_set] / supports[freq_set]
                    rule = (freq_set, sub_set - freq_set, conf)
                    if conf >= min_conf:
                        # print(rule)
                        rules.append(rule)
    return rules


if __name__ == '__main__':
    data = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

    L, support_data = apriori(data, min_support=0.5)
    print('='*50)
    print('frequent \t\tsupport')
    print('='*50)
    for i in L:
        for j in i:
            print(set(j), '\t\t', support_data[j])

    print()
    print('='*50)
    print('antecedent consequent \t\tconf')
    print('='*50)
    association_rules = association_rules(L, support_data, min_conf=0.7)
    for _rule in association_rules:
        print('{}  =>  {}\t\t{}'.format(set(_rule[0]), set(_rule[1]), _rule[2]))
