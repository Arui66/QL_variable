from conn.fo.core import main_core
from conn.gheaders import LoggerClass
from conn.sql.JD_ql import select_data

logger = LoggerClass('debug')


def tx_compared(tx1):
    """
    用于对比数据，由TG获取的文本对比数据库中的数据
    :return: 返回数组的脚本名称[0]和变量[1],异常返回-1
    """
    try:
        # 切割字符串
        if tx1[0:6:1] == 'export' or tx1[0:9:1] == 'NOTexport':
            # 把export DPLHTY="b4be"的键和值分开
            tx = tx1.split('=')
            # 先查询这个值在不在jd_value1中
            value1 = select_data('jd_js', f'jd_value1="{tx[0]}"')
            # 再查询这个值在不在jd_value2中
            value2 = select_data('jd_js', f'jd_value2="{tx[0]}"')
            # 再查询这个值在不在jd_value3中
            value3 = select_data('jd_js', f'jd_value3="{tx[0]}"')
            if len(value1) > 0:
                main_core([value1[0][0], tx1])
            elif len(value2) > 0:
                main_core([value2[0][0], tx1])
            elif len(value3) > 0:
                main_core([value3[0][0], tx1])
            else:
                logger.write_log(f"在数据库中没有找到: {tx1}")
    except Exception as e:
        logger.write_log(f"tx_compared 异常对比脚本异常信息信息: {e}")