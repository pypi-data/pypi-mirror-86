#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : io_utils
# @Time         : 2020/11/19 3:04 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


def to_hdf(df2name_list):
    with timer("to_hdf"):
        for df, name in df2name_list:
            df.to_hdf(name, 'w', complib='blosc', complevel=8)


def to_excel(df2name_list, to_excel_kwargs=None):
    if to_excel_kwargs is None:
        to_excel_kwargs = {}

    with timer("to_excel"):
        with pd.ExcelWriter('filename.xlsx') as writer:
            for df, sheet_name in df2name_list:
                df.to_excel(writer, sheet_name, **to_excel_kwargs)
