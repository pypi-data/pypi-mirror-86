import datetime
import json
import logging
import re
import traceback
import os

from rjTools.log_handler import DefaultLogHandler
from rjTools.utils import file2dict
from rjTools.utils_APScheduler import ApschedulerUtils

os.system("color 5f")
os.system("title Keepalive Task")

"""
#################################
任务管理工具类
#################################

配置文件参数：
------ 基础字段 ------ 
基础必须字段：
{
name 任务名称，唯一
exec_cmd 执行命令
exec_path 执行路径，‘/’结尾
job_type 任务类型，1 定时任务 2 循环间隔任务 3 保活任务

可选基础字段:
desc 未使用
enable 是否启用，默认启用
}
------ 类型特有字段 ------ 
1 定时任务
可选字段：
day_of_week 默认"0-6"
hour 默认0
minute 默认0
second 默认0

2 循环间隔任务
必须字段：
second

3 保活任务
必须字段：
task_name 任务管理器的程序名.后缀

可选字段：
second 默认5
"""

logHandler = DefaultLogHandler(filename='keep_alive.log', consolelevel=logging.DEBUG, filelevel=logging.ERROR)


def initLog(filename='keep_alive.log', consolelevel=logging.DEBUG, filelevel=logging.ERROR):
    """
    初始化日志
    :param filename: 日志文件名
    :param consolelevel:控制台日志级别
    :param filelevel:文件日志级别
    :return:
    """
    global logHandler
    logHandler = DefaultLogHandler(filename=filename, consolelevel=consolelevel, filelevel=filelevel)


def execCmd(cmd: str):
    """
    执行cmd命令
    :param cmd:
    :return:
    """
    try:
        file = os.popen(cmd, 'r')
        text = file.readlines()
        # 倒序删除
        for i in range(len(text))[::-1]:
            if text[i] == '\n':
                del text[i]
            else:
                text[i] = re.sub('[\n]+', '\n', text[i])
                text[i] = re.sub('[“ ”]+', ' ', text[i])
                text[i] = text[i].strip()
        file.close()
        return text
    except Exception as e:
        logHandler.error(e.args)
        return ''


def killTaskProcess(process_name: str):
    """
    停止进程
    :param process_name: 任务管理器中的程序名：python.exe tq.py
    :return:
    """
    if process_name.endswith('.py'):
        # 因为python执行程序比较特殊，任务管理器中执行的python脚本都是相同名称，只能根据执行的命令进行区分
        index = process_name.rfind('.')
        key = process_name[:index]
        process_detail = execCmd(
            f'wmic process where caption="python.exe" get commandline,processid|find "{key}"')
        if len(process_detail) != 0:
            for item in process_detail:
                index = item.rfind(' ')
                pid = int(item[index + 1:])
                try:
                    # -t(结束该进程) -f(强制结束该进程以及所有子进程)
                    os.system(f'taskkill /pid {pid} -f -t')
                    logHandler.info(f'杀死 {process_name} pid:{pid}')
                except Exception as e:
                    logHandler.error(e.args)
                    logHandler.error(traceback.print_exc())
        else:
            logHandler.error('找不到进程信息')
    elif process_name.endswith('.exe'):
        try:
            # -t(结束该进程) -f(强制结束该进程以及所有子进程)
            os.system(f'taskkill /im {process_name} -f -t')
            logHandler.info(f'杀死 {process_name}')
        except Exception as e:
            logHandler.error(e.args)
            logHandler.error(traceback.print_exc())

    else:
        logHandler.error('程序名不正确，需要带文件后缀，例如：clion.exe,TQ.py')
        return


def doKeepAliveJob(path: str, cmd: str, task_name: str):
    """
    间隔任务
    :param path: 文件路径
    :param cmd: 命令
    :param task_name: 程序在任务管理器中的名称
    :return:
    """
    if task_name.endswith('.py'):
        index = task_name.rfind('.')
        key = task_name[:index]
        process_detail = execCmd(
            f'wmic process where caption="python.exe" get commandline,processid|find "{key}"')
    elif task_name.endswith('.exe'):
        process_detail = execCmd(f'wmic process where caption="{task_name}" get commandline,processid')
    else:
        logHandler.error('程序名不正确，需要带文件后缀，例如：clion.exe,TQ.py')
        return

    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # logHandler.info(process_detail)
    if len(process_detail) != 0:
        logHandler.info(f'{cmd} 在运行 {now_time}')
        return

    if not os.path.exists(path):
        logHandler.error(f'目录:{path}不存在')
        return

    logHandler.info(f'执行命令，path：{path} cmd：{cmd} time：{now_time}')
    doCronJob(path, cmd)


def doCronJob(path, cmd):
    """
    定时任务
    :param path:
    :param cmd:
    :return:
    """
    try:
        current_dir = os.curdir
        if len(path) != 0:
            os.chdir(path)  # 在父进程中切换工作目录，否则子进程找不到文件，或者os.system('cd path-to-repo && svn ci')
        cmd = cmd.strip()
        if cmd.startswith('python') or cmd.endswith('.bat'):
            os.system(f'start {cmd}')
        elif cmd.lower().startswith('taskkill'):
            cmd_param = cmd.split(' ')
            if len(cmd_param) != 2:
                if len(path) != 0:
                    os.chdir(current_dir)
                logHandler.error(f'任务格式不对：{path}{cmd}，taskkill指令格式：taskkill <任务管理器的程序名.后缀>，例如：taskkill TQ.py')
                return
            killTaskProcess(cmd_param[1])
        else:
            os.system(f'{cmd}')
        if len(path) != 0:
            os.chdir(current_dir)
    except Exception as e:
        logHandler.error(e.args)
        logHandler.error(traceback.print_exc())


def doJobs(path: str):
    """
    调用任务
    :param path: 配置文件路径
    :return:
    """
    logHandler.info('**************************')
    sch = ApschedulerUtils()
    service_list = file2dict(path)

    if service_list is None or not service_list:
        logHandler.error('任务列表为空')
        return

    def checkNUll(ser, name):
        if ser.get(name) is None:
            logHandler.error(f'{name} 字段为空，请检查！！')
            return None
        return ser.get(name)

    logHandler.info('任务初始化...')

    for ser in service_list:
        if checkNUll(ser, 'exec_cmd') is None \
                or checkNUll(ser, 'name') is None \
                or checkNUll(ser, 'job_type') is None:
            continue
        cmd = ser.get('exec_cmd')
        path = ser.get('exec_path') if ser.get('exec_path') is not None else './'
        name = ser.get('name')
        jobtype = ser.get('job_type')
        enable = ser.get('enable') if ser.get('enable') is not None else 1
        if enable == 0:
            logHandler.info(f'任务：{name} 暂停')
            continue

        if jobtype == 1:
            week = ser.get('day_of_week') if ser.get('day_of_week') is not None else '0-6'
            hour = ser.get('hour') if ser.get('hour') is not None else 0
            minute = ser.get('minute') if ser.get('minute') is not None else 0
            second = ser.get('second') if ser.get('second') is not None else 0

            if len(path) == 0 or not os.path.exists(path):
                logHandler.error(f'目录:{path}不存在')
                continue

            sch.registCronJob(fun=doCronJob, args=[path, cmd]
                              , job_id=name
                              , day_of_week=week
                              , hour=hour
                              , minute=minute
                              , second=second)
        elif jobtype == 2:
            if ser.get('second') is None:
                logHandler.error(f'任务：{name} 的 second 字段为空，请检查！！')
                continue
            second = ser.get('second')
            sch.registIntervalJob(fun=doCronJob, args=[path, cmd], job_id=name, seconds=second)
        elif jobtype == 3:
            if ser.get('task_name') is None:
                logHandler.error(f'任务：{name} 的 task_name 字段为空，请检查！！')
                continue
            task_name = ser.get('task_name')
            second = ser.get('second') if ser.get('second') is not None else 5
            sch.registIntervalJob(fun=doKeepAliveJob, args=[path, cmd, task_name], job_id=name, seconds=second)
        else:
            logHandler.error(f'任务:{name} 中无效的类型：{jobtype}')
    logHandler.info('初始化完成！')
    logHandler.info('**************************')
    sch.start()


if __name__ == '__main__':
    killTaskProcess('webgate2.py')
    # doJobs(path='../conf/task.conf')
