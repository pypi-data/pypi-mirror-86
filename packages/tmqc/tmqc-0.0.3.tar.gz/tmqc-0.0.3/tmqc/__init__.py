
import sys,os

#__file__获取执行文件相对路径，整行为取上一级的上一级目录
BASE_DIR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tmqc")

# 添加路径
sys.path.append(BASE_DIR)

# 修改当前工作目录
os.chdir(BASE_DIR)

# 获取当前工作目录
# abcdir = os.getcwd()
# print(abcdir)