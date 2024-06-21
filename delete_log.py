import os
import sys

def get_lines(filename):
    assert os.path.exists(filename), f'No such file {filename}.'
    with open(filename, 'r') as f:
        lines = f.readlines()
        return len(lines)

# 获取脚本名称
script_name = sys.argv[0]
print("Script name:", script_name)

log_dir = './'
pattern = 'log.'
line_thr = 1000

# 获取其他命令行参数
if len(sys.argv) > 1:
    args = sys.argv[1:]  # 取脚本名之后的所有参数
    print("Arguments:", args)
    log_dir = args[0]
    pattern = args[1]
    line_thr = args[2]
else:
    print("No additional arguments provided.")

for filename in os.listdir(log_dir):
    filepath = os.path.join(log_dir, filename)
    if not filename.startswith(pattern):
        continue
    lines = get_lines(filepath)
    if lines < line_thr:
        os.remove(filepath)
        print(f'Remove log file {filepath}.')
