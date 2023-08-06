# 关于Pubsub
- `pubsub`的最初目的是通过`redis服务`转发单目摄像头数据，供`深度学习`和`ROS`两方同时订阅
- 实际使用过程中增加了转发`FairMOT`识别结果的用途，同时`pubsub`在主-从两台机器上进行部署
- 在0.1.4版本中，增加了对`主-从`和`多话题`的支持，修改了配置文件的配置方式
- 在0.1.5版本中，完善了`setup.py`，并发布到pypi
- 在0.1.6版本中，增加了`configs`模块，可通过此模块直接获得配置信息
- 在0.1.7版本中，修复了全局变量和单例引入的订阅”串台”问题

## 1. 问题
### 1.1. `redis.exceptions.ConnectionError: Connection closed by server.`
https://github.com/andymccurdy/redis-py/issues/1140

使用`try... except redis.exceptions.ConnectionError:`的方法规避了此问题

    FYI
    - 在本项目下，使用`py37`没有出现此问题
    - 在本项目下，使用`python`没有出现此问题
    - 在`FairMOT`下出现此问题，初步怀疑是`timeout`问题

**该问题通过安装hiredis的方式进行了修复，修复版本0.1.5，暂未出现此问题**

#### 1.1.1 原因2 `scheduled to be closed ASAP for overcoming of output buffer limits`
查看`/var/log/redis/redis-server.log`，可以发现
```
3105:M 23 Nov 18:06:12.428 # Client id=105 addr=<sub-ip>:33750 fd=7 name= age=2 idle=0 flags=N db=3 sub=1 psub=0 multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=38 omem=35102272 events=rw cmd=subscribe scheduled to be closed ASAP for overcoming of output buffer limits.
```
所有的`client`请求`redis`数据的时候，`redis`要返回给`client`的数据都会先被存储在`output-buffer`中，等所有信息都被传送完毕之后，再清除`output-buffer`中的数据。为了防止`output-buffer`过大，`redis`进行了限制。

在配置文件`/etc/redis/redis.conf`中进行修改
```
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
```

- 客户端种类，包括Normal，Slaves和Pub/Sub
- Normal: 普通的客户端。默认limit 是0，也就是不限制
- Pub/Sub: 发布与订阅的客户端的。默认hard limit 32M，soft limit 8M/60s
- Slaves: 从库的复制客户端。默认hard limit 256M，soft limit 64M/60s
- hard limit: 缓冲区大小的硬性限制
- soft limit: 缓冲去大小的软性限制
- soft seconds: 缓冲区大小达到了（超过）soft limit值的持续时间
- client buffer的大小达到了soft limit并持续了soft seconds时间，将立即断开和客户端的连接
- client buffer的大小达到了hard limit，server也会立即断开和客户端的连接

如果难以准确估计缓冲区需要的大小和持续时间，可以直接设为0，如下
```
client-output-buffer-limit pubsub 0 0 0
```

修改后重启`redis`服务。

### 1.2. 同一程序中有多个生产者/发送端发送多个`topic`，消费者/订阅端会“串台“

原因分析
- Subscriber中错误地将消息数据设置为全局变量
- 单例模式未能区分不同单例的name

状态：已修复，不影响调用方式

修复版本： 0.1.7

## 2. 依赖
本工具依赖redis服务请先安装redis-server
```
apt install redis-server
```

为Python安装依赖
```
pip3.7 install opencv-python numpy pyyaml hiredis redis
pip2.7 install opencv-python numpy pyyaml hiredis redis
```

- 补充说明

`setup.py` 文件本身指明了相关依赖，但是由于公司网络原因，可能会出现无法正常下载安装的情况，建议在安装之前手动完成依赖包的安装。

## 3. 作为程序部署
step1. 在`~`路径下新建路径`robot\configs`，注意：请勿使用其他路径

step2. 将项目目录下的配置文件`config\pubsub.yaml`拷贝到`~\robot\configs`路径下，注意：请勿修改文件名称

step3. 按实际情况修改`~\robot\configs\pubsub.yaml`文件
```
# camera data pub & sub config
mono:
  type: "pub"
  source: "0"
  host: "172.172.0.10"
  port: "6379"
  db: 3
  name: "robot_mono"
  topic: "robot_mono"

# bbox from FairMOT pub & sub config
track:
  type: "pub"
  source: "0"
  host: "172.172.0.11"
  port: "6379"
  db: 3
  name: "robot_track"
  topic: "robot_track"
```

参数说明：
```
mono: 指定为单目相机，该名称请勿修改
  type: 发布消息，请勿修改
  source: camera device id, 通过 ls /dev/video* 配合 v4l2-ctl -d  /dev/video0 --all查看
  host: 消息发布ip，对应部署了pubsub程序的服务器的IP地址
  port: 消息发布端口，对应部署了pubsub程序的服务器的Redis服务的端口
  db: 不需改动
  name: 消息发布服务的名称
  topic: 消息发布话题的名称

track: 指定为跟踪算法，该名称请勿修改
  type: 发布消息，请勿修改
  source: 请勿修改
  host: 消息发布ip，对应部署了tracking算法的服务器的IP地址
  port: 消息发布端口，对应部署了tracking算法的服务器的Redis服务的端口
  db: 不需改动
  name: 消息发布服务的名称
  topic: 消息发布话题的名称
```

step5. 在`~/.bashrc`中声明`configs`地址
- 执行下面的命令，将configs的路径加入到系统环境
```
echo export ROBOT_CONFIGS=$(dirname ~/.)'/robot/configs' >> ~/.bashrc && source ~/.bashrc
```
- 请务必注意将配置文件放在上述指定文件夹下

setp6. 如果存在主-从部署，请在从机上重复上述过程

请注意：
- 模块和程序使用同样的配置文件！！！

### 3.1. 开机自启动[未测试]
在`/etc/rc.local`脚本中增加了开机自启动代码，代码如下
```
export PUBLISHERPATH=$(dirname ~/.)'/robot/pubsub'
source $(dirname $(which conda))/activate pubsub
cd $PUBLISHERPATH
python app.py
```
第一段申明了MONOPUB的路径

第二段进入到该路径

第三段在后台启动脚本`publish.sh` 并输出日志到`pub.log`

第三段回到`home`

可使用`ps -ef | grep python`查看

## 4. 作为模块使用

分别在python2.7和python3.7版本下进行测试。

### 4.1. 安装

```
pip install aa-pubsub
```

### 4.2. 配置

- 如果主-从部署在同一`IP`下，可以不必另外配置
- 如果主-从部署在不同`IP`下，从机需要依照主机的配置方法自行配置

请注意：
- 模块和程序使用同样的配置文件！！！

## 5. 性能

### 5.1. 本地`Docker`间传输
目前`Publisher`端读取摄像头数据到`Subscriber`端得到数据拥有约`100ms`的延时，其中有20秒是`docker`造成的延时。

![1](images/1.jpg)
![2](images/2.jpg)

### 5.2. 同网段局域网间传输
目前`Publisher`端读取摄像头数据到`Subscriber`端得到数据拥有约`100ms`的延时，同网段指办公网段（10.1.x.x）

![1](images/1.png)
![2](images/2.png)
![3](images/3.png)

### 5.3. 不同网段局域网间传输
目前`Publisher`端读取摄像头数据到`Subscriber`端得到数据拥有约`100ms-200ms`的延时，不同网段指办公网段与GPU服务器（10.1.x.x与10.0.40.x）

![3](images/3.jpg)
![4](images/4.jpg)

## 6. 开发/贡献代码
### 6.1. 测试用例

测试用例的统一运行入口是`test.py`文件

```
python test.py
```

- 各测试用例请统一在`testcases`路径下实现，以`test_{name}.py`的形式命名
- `py`文件中，测试类以`{name}Test`的形式命名
- 更多请参考`unittest`

### 6.2. 提交pip

- 安装提交需要的工具
```
pip install twine
```
- 更新`version.py`的版本号
- 提交
```
python setup.py sdist
twine upload dist/*
```

## 7. 当前通过pubsub支持的消息

```
# 单目相机
mono:
    type: "pub"
    source: "0"
    host: "127.0.0.1"
    port: "6379"
    db: 3
    name: "robot_mono"
    topic: "robot_mono"

# FairMOT得到的bbox
track:
    type: "pub"
    source: "0"
    host: "127.0.0.1"
    port: "6379"
    db: 3
    name: "robot_track"
    topic: "robot_track"

# 跟随目标识别开/关量
switch_send:
    type: "pub"
    source: "0"
    host: "10.1.101.179"
    port: "6379"
    db: 3
    name: "robot_switch_send"
    topic: "robot_switch_send"

# 跟随目标识别开/关执行反馈量
switch_feedback:
    type: "pub"
    source: "0"
    host: "10.1.101.179"
    port: "6379"
    db: 3
    name: "robot_switch_feedback"
    topic: "robot_switch_feedback"

# 跟随目标切换信号量
control_singal_load_track_feature:
    type: "pub"
    source: "0"
    host: "10.1.101.179"
    port: "6379"
    db: 3
    name: "control_singal_load_track_feature"
    topic: "control_singal_load_track_feature"

# 匹配到的跟随目标的图片地址
target_matched:
  type: "pub"
  source: "0"
  host: "10.1.101.141"
  port: "6380"
  db: 3
  name: "target_matched"
  topic: "target_matched"

# 跌倒开关
fall_down_switch:
  type: "pub"
  source: "0"
  host: "10.1.157.165"
  port: "6379"
  db: 3
  name: "fall_down_switch"
  topic: "fall_down_switch"

# 跌倒开关的反馈
fall_down_switch_result:
  type: "sub"
  source: "0"
  host: "10.1.157.165"
  port: "6379"
  db: 3
  name: "fall_down_switch_result"
  topic: "fall_down_switch_result"

# 目标人员跌倒信息
target_status:
  type: "sub"
  source: "0"
  host: "10.1.157.165"
  port: "6379"
  db: 3
  name: "target_status"
  topic: "target_status"
```
