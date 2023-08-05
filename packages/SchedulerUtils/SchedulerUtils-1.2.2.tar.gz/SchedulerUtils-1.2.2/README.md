**StrategiesManager**

# 这是一个任务管理工具类

## 格式

### 配置文件参数：
### 基础必须字段： 
- name 任务名称，唯一
- exec_cmd 执行命令
- exec_path 执行路径，‘/’结尾
- job_type 任务类型，1 定时任务 2 循环间隔任务 3 保活任务

可选基础字段
- desc 未使用
- enable 是否启用，默认启用 1,不启用 0

1）1 定时任务

可选字段：
- day_of_week 默认"0-6"
- hour 默认0
- minute 默认0
- second 默认0

2）2 循环间隔任务

必须字段：
- second

3）3 保活任务

保活任务只支持python跟exe等单窗口或单进程文件，就是一个文件一个操作。文件里面另开运行窗口就会被监控忽略。

必须字段：
- task_name 任务管理器的程序名.后缀

可选字段：
- second 默认5

### **注意事项**
1）保活任务只支持python跟exe文件，bat文件因为无法得知执行的是什么内容所以无法保活里面执行的内容

2）taskkill+文件.后缀 自定义命令

杀死进程的原理前提是要知道进程的id，可以使用wmic命令根据任务名称或者执行的命令信息找到对应的id。检测进程是否存在也是这个原理。
```
"exec_cmd": "taskkill xxxx.py"
"exec_cmd": "taskkill xxxx.exe"
```
3）执行路径要使用斜杠
```
"exec_path": "C:/Users/Administrator/Desktop/klDataService"
```
4）任务配置文件使用utf-8编码，不支持中文字符

5）除了执行python命令跟bat文件是启动单独窗口之外其它的命令都在父窗口执行，如果要单独窗口可以在命令前添加‘start’指令
```
[{
    "exec_cmd": "start xx.exe",
...
}]
```

6）任务执行的命令
 - 查找任务进程id
    - wmic process where caption="python.exe" get commandline,processid|find "{key}"
 - 杀死进程
    - 根据id杀死进程：taskkill /pid {pid} -f -t
    - 根据任务名杀死进程：taskkill /im {process_name} -f -t
 
### 例子
配置文件：task.conf
```
[
	{
        "name": "KILL_TQ_H_KL_WEB",
        "exec_cmd": "taskkill tq_server.py",
        "exec_path": "./",
        "job_type": 1,
        "day_of_week": "0-6",
        "hour": 5,
        "minute": 10,
        "second": 0,
        "desc": "kill TQ history",
		"enable": 1
    },
	{
        "name": "TQ_H_KL_WEB",
        "exec_cmd": "python tq_server.py -p 10022",
        "exec_path": "C:/Users/Administrator/Desktop/xxxx",
        "job_type": 3,
        "task_name": "tq_server.py",
        "desc": "TQ history service",
		"enable": 1
    },
	{
        "name": "FT_KL_PUSH",
        "exec_cmd": "start xx.exe",
        "exec_path": "C:/Users/Administrator/Desktop/xxxx",
        "job_type": 3,
        "task_name": "xx.exe",
        "desc": "FT kl push",
		"enable": 1
    }
]
```
例子：
```python
import logging
from rjTools.scheduler_task import doJobs, initLog

initLog(filename='dojob.log', consolelevel=logging.DEBUG, filelevel=logging.ERROR)
doJobs(path='../conf/task.conf')
```

### 新增可视化配置界面
```
from rjTools.scheduler_ui import ShowConfigureUI
ShowConfigureUI('../conf/task.conf')
```
界面提供编辑task.conf文件功能。
菜单的“开机服务”功能依赖winsw服务，跟执行界面py文件放同一级目录，可以设置定时任务加入到开机服务。


### 更新日志
- 2020.11.19
    1) 修改检测任务逻辑
    2) 支持uvicorn启动的python任务
    
- 2020.10.20
    1) 修改包名

- 2020.10.19
    1) 修复小bug,杀死进程exe类型的错误
    
- 2020.10.16
    1) 修复小bug
    
- 2020.09.18
    1) 完成基本定时任务启动框架
