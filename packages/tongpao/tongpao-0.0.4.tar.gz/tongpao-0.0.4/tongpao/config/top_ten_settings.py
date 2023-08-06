# -*- coding: utf-8 -*-
# author： work
# datetime： 2020/11/25 2:24 下午 
# software: PyCharm
# 文件接口说明： 
# -*- coding: utf-8 -*-

# 请求模块
request_step = [
    {
        "TongPaoProduct": {
            # 执行模式,往redis推入任务
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
    {
        "TongPaoOne": {
            # 执行模式requests/WebDriver
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
    {
        "TongPaoTwo": {
            # 执行模式requests/WebDriver
            "run_mode": "requests",
            # 是否需要auth或cookie
            "need_token": False,
        },
    },
]

# 存储途径
output = [
    {
        "print": {}
    },
    {
        "csv": {
            "file_name": "同袍.csv",
            "csv_header": {
                "分类": "category",
                "店铺名称": "shop_name",
                "全部商品数": "all_goods",
                "关注人数": "follow_num",
                "最热前十": "hot_list"
            }
        }
    },
]
