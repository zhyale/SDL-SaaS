# SDL SaaS

特别说明：此项目已停止维护更新，不再提供支持，请谨慎选用并测试。

## 环境约定

* Python 2.7
* MySQL
* VirtualEnv
* Memcached

### virtualenv安装参考
```
pip install virtualenv
$virtualenv --python=/usr/local/bin/python2.7 pmpenv  （指定使用python2.7）
$cd pmpenv  
$source ./bin/activate
(pmpenv) $pip install uwsgi 
```
国内如遇网络故障请使用`pip install -i http://pypi.douban.com/simple uwsgi` 语句代替

```
(pmpenv) $pip install django
(pmpenv) $pip install pillow
(pmpenv) $pip install Mysql-python  （如果失败可尝试：easy_install MySQL-python）
```
依赖：
python-devel
mysql-devel 
如果出现图片上传失败，安装相关依赖后：
pip install --no-cache-dir -I pillow


### 服务器基本环境

操作系统：CentOS6.4 + 
Web服务器：Nginx 1.6.2
CGI: uwsgi （在系统环境和virtualenv环境都安装）
应用环境：Python 2.7.10 + django 1.7
数据库：Mysql-server
参考步骤：
```
#yum install mysql-server
#chkconfig --add mysqld
#chkconfig mysqld on
```

特别注意：pip –V所显示的版本信息中，所使用的python必须为Python2.7 。

退出root权限，选定一个目录放置Python虚拟环境
$ virtualenv --python=/usr/local/bin/python2.7 pmpenv  （指定使用python2.7）
$cd pmpenv
$source ./bin/activate
此时即进入虚拟环境，此后需要的组件均安装在虚拟环境内（退出虚拟环境指令为 deactivate）。
(pmpenv)$pip install uwsgi
(pmpenv)$pip install django
(pmpenv)$pip install Mysql-python
假设代码目录结构为/data/pmpenv/pmp/pmp ,第一个pmp是django站点的主目录，第二个pmp放置主要配置文件。

### 服务器参数配置

性能参数：
在/etc/sysctl.conf中添加如下一行：
net.core.somaxconn = 2048
然后在终端中执行
sysctl –p
uwsgi.ini中的listen参数已经设为1024 （不能超过net.core.somaxconn变量值）。
此项如果没有修改，则uwsgi服务起不来。

### UWSGI配置

检查/data/pmpenv/pmp/uwsgi.ini 的相关配置（和manage.py 在同一级目录下），内容为（如有变化，以实际发布的文件为准）：  
```
[uwsgi]
chdir=/data/pmpenv/pmp
home=/data/pmpenv
socket=/var/pmp.sock
uid = nobody
gid = nobody
chmod-socket=666
chown-socket=nobody
module=pmp.wsgi
master=True
pidfile=pmp.pid
vacuum=True
listen=1024
workers=8
daemonize=pmp.log
```
其中listen不能超过net.core.somaxconn变量值。
开机启动，在/etc/rc.d/rc.local文件中添加：
```
/usr/local/bin/uwsgi –ini /data/pmpenv/pmp/uwsgi.ini
```

其中uwsgi的路径请确认（whereis uwsgi）后再配置，特别是系统中存在两个uwsgi时，请使用全路径（对应pip2.7安装的uwsgi）。

### NGINX安装配置

如果是编译安装则默认路径为`/usr/local/nginx/conf/nginx.conf`

```
user nobody;
conf.d/default.conf配置：
server {
        listen 9080 default_server;
        server_name  xxxxxx;#domain name
        error_log /usr/local/nginx/logs/djerror.log;

        location /static/ { 
            alias /data/pmpenv/pmp/static/;
            expires 30d;
        }
       
        location / {
            include uwsgi_params;
            uwsgi_pass unix:///var/pmp.sock; 
            uwsgi_read_timeout 1800;
            uwsgi_send_timeout 300;
            proxy_read_timeout 300;
        }
}
```

备注：pmp.sock需要确保nginx worker process（一般为nobody）和uwsgi进程可正常读写。

### MySQL配置

配置文件/etc/my.cnf
统一设置编码，需要在/etc/my.cnf的[mysqld]下加上
```
character_set_server=utf8
character_set_client=utf8
```
加入系统服务
```
chkconfig --add mysqld
chkconfig mysqld on
service mysqld start
```
命令行修改密码：mysqladmin –uroot password xxxxxx 
连接mysql之后创建数据库并设置用户及权限：
```
create database pmp;
grant all privileges on pmp.* to 'pmp'@'localhost' identified by 'xxxxxxxx';
flush privileges;
```
应用中使用pmp用户连接mysql。

### 应用实施

将服务器代码复制到服务器，目录为：/data/pmpenv/pmp 。
修改/data/pmpenv/pmp/pmp/settings.py中的：
数据库账号和密码，不使用root账号，以及：
```
DEBUG = False
TEMPLATE_DEBUG=False
ALLOWED_HOSTS = ['*']
```
进入/data/pmpenv/，执行
```
source ./bin/activate
```
执行`python manage.py syncdb` 在过程中设置django后台管理账号。
检查确认/etc/rc.d/rc.local文件中已添加：
```
/usr/local/bin/uwsgi –ini /data/pmpenv/pmp/uwsgi.ini
```
重启服务器测试各项服务是否正常启动。
首次部署，请访问http://xxx.xxx.xxx.xxx/initsystem 初始化。


### 服务监控

/etc/crontab中添加：
```
* * * * * root /sbin/service mysqld status || service mysqld restart
00 19 * * * root /data/backup/backupdb.sh
```

### 备份参考

#cat /data/backup/backupdb.sh
```
mysqldump -ubackup –p****** --single-transaction pmp|gzip>/data/backup/mysql/pmp_`date +%Y-%m-%d`.sql.gz
cd /data/backup/mysql
rm -rf `find . -name '*.sql.gz' -mtime 7`
```
恢复：
```
mysql –uroot –p pmp<***.sql
```

### RSA配置

python manage.py shell环境
```
import rsa
```
密钥生成：
```
(pubkey, privkey) = rsa.newkeys(1024)
```
N,E值获取：pubkey.n  pubkey.e
以文件形式存储：
```
pkcs1 = pubkey.save_pkcs1()
pubfile = open('pubkey_1024.pem','w+')
pubfile.write(pkcs1)
pubfile.close()
```
从文件读取：
```
with open('privkey_1024.pem') as privatefile:
    pkcs1 = privatefile.read()
privkey = rsa.PrivateKey.load_pkcs1(pkcs1)
```

### 如果忘记密码

如果你忘记了后台管理员（默认为admin，本例采用root）的密码，要用Django shell：
进入/data/pmpenv/，执行
source ./bin/activate  进入虚拟环境
cd pmp
python manage.py shell
然后获取你的用户名，并且重设密码：
```
from django.contrib.auth.models import User 
user = User.objects.get(username='admin') 
user.set_password('new_password') 
user.save()
```

### 小版本升级参考

如果需要升级服务器，请根据升级指导进行，如保留数据升级，参考如下：
进入/data/pmpenv/，执行
source ./bin/activate  进入虚拟环境
cd pmp
执行
python manage.py makemigrations
python manage.py migrate
更新数据库结构。
重启uwsgi服务（安装包stop_uwsgi.sh和start_uwsgi.sh）。


### 常见问题与诊断

网络连通性，可使用curl测试。
