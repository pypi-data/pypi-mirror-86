# -*- coding: utf-8 -*-
from common.define import MODE
FILTER_STOCK_MARKET = ["sh"]        # 需要过滤市场
MAX_KEEP = 100                      # 最大持仓数量
# ----------------------回测配置----------------------
# PRINT_CNT =1000                      # 行情打印频度
# LOG_CNT =60                          # 净值计算打印频度 单位秒
# LOG_FUNDID2_LIST =[512880,515000,512000,512760]                         # 净值清单配置
STRATEGY_MODE = MODE.backtesting      # 回测
# MARKET_VALUE = 100000                 # 每只开仓市值。如果为0，则为1手
# ----------------------实盘配置----------------------
PRINT_CNT =1000                  # 行情打印频度
GROUP_AREA = 0                  # 分组的第一组索引.每1s1组。3秒循环一次
GROUP_NUM = 12                   # 分组数量
FIRST_LOG_TIME = 1230            # 日志首次打印时间
SEC_LOG_TIME = 1530              # 日志首次打印时间
IS_SET_DB = 1                    # 是否启用redis写库
# STRATEGY_MODE = MODE.public      # 实盘
MARKET_VALUE = 100000            # 每只开仓市值。如果为0，则为1手
IS_REWRITE = False