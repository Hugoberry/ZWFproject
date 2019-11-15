# coding=utf-8

import os
from utils.readconfig import ReadConfig

# 读取配置文件
config_file_path = os.path.split(os.path.realpath(__file__))[0]
read_config = ReadConfig(os.path.join(config_file_path, 'config.ini'))
# 项目参数设置
prj_path = read_config.getValue('projectConfig', 'project_path')
# 测试用例路径
if not os.path.exists(prj_path + '/case'):
    os.makedirs(prj_path + '/case')
case_path = os.path.join(prj_path, 'case')
# 日志路径
if not os.path.exists(prj_path + '/log'):
    os.makedirs(prj_path + '/log')
log_path = os.path.join(prj_path, 'log')
# 截图文件路径
if not os.path.exists(prj_path + '/image'):
    os.makedirs(prj_path + '/image')
img_path = os.path.join(prj_path, 'image')
# 测试报告路径
if not os.path.exists(prj_path + '/report'):
    os.makedirs(prj_path + '/report')
report_path = os.path.join(prj_path, 'report')
# 默认浏览器
browser = 'Chrome'
# 测试数据路径
if not os.path.exists(prj_path + '/data'):
    os.makedirs(prj_path + '/data')
data_path = os.path.join(prj_path, 'data')
# 驱动路径
# driver_path = os.path.join(prj_path, 'driver')
