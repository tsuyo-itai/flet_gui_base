import sys
import os
import configparser


# -----------------------------------
# ファイルのパス取得(exe実行&通常実行にも対応)
# -----------------------------------
def get_resource_path(relative_path):

    if getattr(sys, 'frozen', False):
        #exeから実行している場合のPATH
        program_directory = os.path.dirname(os.path.abspath(sys.executable))
    else:
        #ファイルから起動している場合のPATH
        program_directory = os.path.dirname(os.path.abspath(__file__))

    resource_path = os.path.join(program_directory, relative_path)

    return resource_path


#-----------------------------------
# Configセット
#-----------------------------------
def set_config(filename):
    config_ini_path = get_resource_path(filename)
    if not os.path.exists(config_ini_path):
        print("【Err.05】{} が見つかりません".format(config_ini_path))
        return None
    Config = configparser.ConfigParser()
    Config.read(config_ini_path, encoding='shift-jis')

    return Config