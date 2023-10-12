
def plt_pie_save(passed_count, skipped_count, failed_count):
    import matplotlib.pyplot as plt
    import numpy as np

    passed = "passed   : "+str(passed_count)
    skipped = "skipped  : "+str(skipped_count)
    failed = "failed   : "+str(failed_count)
    print("passed  : %05d" % passed_count)
    print("skipped : %05d" % skipped_count)
    print("failed  : %05d" % failed_count)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']       # 指定字体为雅黑，解决文字乱码问题
    plt.pie(np.array([passed_count, skipped_count, failed_count]))
    plt.legend([passed, skipped, failed])
    plt.title("Test Logs Analysis")
    plt.savefig("total.png")
    # plt.show()


def save_log_to_file(save_path, str_input, target_str):
    import re
    import os
    import csv
    input_result = []

    file_name_index = str_input.find("::")
    filepath = save_path+"/"+str_input[:file_name_index].replace('.py', '.csv')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if " <- " in str_input:
        write_str_index = str_input.find(" <- ")
        write_str = str_input[:write_str_index]+" "+target_str
    else:
        write_str_index = str_input.find(target_str)+len(target_str)
        write_str = str_input[:write_str_index]
    input_result.append(re.split('/|::|[|]| ',
                        write_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '')))

    s_input_result = list(filter(lambda x: x is not None, filter(lambda x: x != "", input_result)))
    # 创建并打开文件，如果文件已存在则覆盖原文件内容
    with open(filepath, 'a', newline="") as file:
        writer = csv.writer(file)    
        writer.writerows(s_input_result)
    file.close()


def remove_dir_test(str_path):
    import shutil
    shutil.rmtree(str_path, ignore_errors=True)


def progress_output(current, total, last_count):
    percent = ((current + 1) * 20) / total
    count = int(percent)
    str_analysis = "["
    for index in range(0, count):
#        str_analysis += "▂"
        str_analysis += "▃"
    for index in range(count, 20):
        str_analysis += " "
    str_analysis += " ]"

    if count != last_count:
        print("Analysing : " + str_analysis)
    return count
    

def data_analysis(file_path):
    # 打开文件 按行拆分
    txt = open(file_path, "r", encoding='utf-16').read()
    txt_lines = txt.splitlines()
    save_path = "./pytorch_test"

    # 抽取有测试结果的日志
    # 并统计 passed skipped failed 各自的数量
    passed_excel = []
    skipped_excel = []
    failed_excel = []
    passed_count = 0
    skipped_count = 0
    failed_count = 0
    remove_dir_test(save_path)
    line_total_num = len(txt_lines)
    last_count = 0

    for index in range(line_total_num):
        target_str = ""
        if "RuntimeError:" not in txt_lines[index]:
            if "PASSED" in txt_lines[index]:
                passed_excel.append(txt_lines[index])
                passed_count += 1
                target_str = "PASSED"
            elif "SKIPPED" in txt_lines[index]:
                if "* SKIPPED:" not in txt_lines[index]:
                    skipped_excel.append(txt_lines[index])
                    skipped_count += 1
                    target_str = "SKIPPED"
            elif "FAILED" in txt_lines[index]:
                failed_excel.append(txt_lines[index])
                failed_count += 1
                target_str = "FAILED"
            if target_str:
                if ".py" in txt_lines[index]:
                    if txt_lines[index].find(target_str) > 4:
#                        print(" Line : "+str(index))
                        save_log_to_file(save_path, txt_lines[index], target_str)
        last_count = progress_output(index, line_total_num, last_count)

    # 使用统计的数量生成图片
    plt_pie_save(passed_count, skipped_count, failed_count)

def new_func(line_total_num, index):
    progress_output(index, line_total_num)


def del_files(dir_path):
    import os
    if os.path.isfile(dir_path):
        try:
            os.remove(dir_path) # 这个可以删除单个文件，不能删除文件夹
        except BaseException as e:
            print(e)
    elif os.path.isdir(dir_path):
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            subfile = os.path.join(dir_path, file_name)
            del_files(subfile)


def check_file_path(file_path):
    import os
    bret = False
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            bret = True
        else:
            print("the log file does not exist")
    else:
        print("the log file could not be a directory")
    return bret


if __name__ == "__main__":
    import argparse

    print("Analysis Start")
    parser = argparse.ArgumentParser(description='pytorch test log analysis')
    parser.add_argument('--file', '-f', type=str, default="./pytorch_test.log", required=False, help="the file path of pytorch test logs")

    args = parser.parse_args()
#    print(args.file)
    file_exist = check_file_path(args.file)
    if file_exist:
        print("open " + args.file)
        data_analysis(args.file)
    else:
        print("the log file does not exist")
    print("Analysis End")

