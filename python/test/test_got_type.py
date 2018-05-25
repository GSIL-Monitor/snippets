# -*- coding: utf-8 -*-
def judge_got_type(data, user_id):
    """
    判断got_type
    认领类型：0可捡漏(未领取)、1可捡漏已领取(当前用户领取)
    2不可捡漏已领(徒弟/徒孙自己领取)、3不可捡漏
    :param data:
    :param user_id:
    :return:
    """
    got_type = 3
    # 先判断可捡漏
    if data['is_reclaimable'] == 1 and data['got'] == 0:
        if data['owner_user_id'] == 0:
            got_type = 0
        if data['owner_user_id'] == user_id:
            got_type = 1
    # 判断不可捡漏
    elif data['is_reclaimable'] == 0:
        if data['owner_user_id'] == 0:
            got_type = 3
        else:
            got_type = 2

    return got_type


# 可捡(未捡)
def test_1():
    data = {
        'is_reclaimable': 1,
        'owner_user_id': 0,
        'got': 0,
    }
    current_user_id = 1
    result = judge_got_type(data, current_user_id)
    assert 0 == result


# 可捡(已捡)
def test_2():
    data = {
        'is_reclaimable': 1,
        'owner_user_id': 1,
        'got': 0,
    }
    current_user_id = 1
    result = judge_got_type(data, current_user_id)
    assert 1 == result


# 不可捡(已兑)
def test_3():
    data = {
        'is_reclaimable': 0,
        'owner_user_id': 0,
        'got': 1,
    }
    current_user_id = 1
    result = judge_got_type(data, current_user_id)
    assert 2 == result


# 不可捡(未兑)
def test_4():
    data = {
        'is_reclaimable': 0,
        'owner_user_id': 0,
        'got': 0,
    }
    current_user_id = 1
    result = judge_got_type(data, current_user_id)
    assert 3 == result


# 不可捡(已捡)，被别人捡走
def test_5():
    data = {
        'is_reclaimable': 0,
        'owner_user_id': 2,
        'got': 0,
    }
    current_user_id = 1
    result = judge_got_type(data, current_user_id)
    assert 3 == result
