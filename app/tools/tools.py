#!/usr/bin/env python
# -*- coding: utf-8 -*-

def can(perm):
    """
    根据role字段查询改用户的角色
    :param perm:
    :return:
    """
    if perm != 1:
        return False
    else:
        return True