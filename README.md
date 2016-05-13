

系统环境：
    Nginx 1.4.6
    uWSGI 2.0
    MySQL 5.6
    Python 3.5
    pip 8.0
Oracle Linux请使用包管理系统yum安装以上软件


PIP:
安装python工程依赖库
在工程根目录内执行：
pip install -r pip.txt
(如果系统同时存在python2和python3, 需要指定pip3)


ENV:
把工程根目录内的env文件改名为.env
并打开作以下修改
修改DATABASE_URL中数据库的账号，密码，地址,端口以及库名称
修改LOGIN_URL和UINFO_URL中前半部分的UAT地址
修改LOGIN_URL中最后url=中的回调域名
修改公众号接口ZUMBA_SECRET的Secret
创建STATIC_ROOT和MEDIA_ROOT文件夹
正式环境把DEBUG设置为False


NGINX:
按deploy文件夹内的nginx.conf配置nginx段
修改server_name中的域名
log位置按需修改，确保该文件夹存在并有权限即可
static和media的路径确保和.env内的相同
启动nginx


UWSGI:
编辑deploy文件夹内的uwsgi.ini文件
确保项目根目录名字为zumba
修改chdir使之与项目路径一致
删除home一行
其他配置按需修改


START:
    在deploy文件夹内执行start.sh
    sh start.sh

如果是首次启动
在根目录运行下列命令进行数据库初始化操作
python manage.py migrate
python manage.py collectstatic

确认域名+/voting/i/显示正常


LOG:
本项目使用syslog
默认路径为/var/log/syslog
