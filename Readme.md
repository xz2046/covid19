## 疫情实时动态平台阅读文档
### 一、概述
##### 制作人：风船野 
##### 联系方式：2635078557@qq.com
##### 中国疫情实时：  
##### 全球疫情实时：
### 二、功能
* 对中国疫情和全球疫情进行实时的数据跟踪
* 对疫情数据进行数据处理存储
* 对疫情数据进行数据分析
* 对疫情数据进行可视化展示
### 三、技术依赖
* mysql数据库 
* python3.8  
  > requests模块 进行数据爬取存储，数据来源腾讯、丁香园
  > SQLAlchemy 对数据库进行连接  
  > pandas 对数据进行处理  
  > pyechart 数据可视化制图  
  > tornado 服务器框架搭建  
### 四、操作说明
* 安装mysql数据库  
    > 1.创建一个数据库  
* data文件夹，数据爬取和存储
    > 2.更改连接数据库配置文件：  
        &ensp;&ensp;./data/link.py,  
        &ensp;&ensp;./data/数据库建模/link.py,  
        &ensp;&ensp;./data/updatasql.py,  
        &ensp;&ensp;./app/settings.py。  
        (user：数据库用户名，password：数据库登录密码，dbname：数据库名)  
    > 3.创建数据表，运行数据库建模中所有文件  
    > 4.运行get_china_url.py和get_world_url.py获取丁香园数据接口  
    > 5.运行get_china_data.py和get_world_data.py获取疫情历史数据（过程可能较慢，需一个小时左右）  
    > 6.运行全get_today_data获取当天数据  
    > 7.运行updatesql.py更新数据表（第一次运行后注释掉36行sums()切记！！！）  
    > 8.每天定时运行get_today_data.py即可获取最新数据  
    > 9.每天23:55运行updatessql.py更新数据表（将今天最终数据加入到总体数据中）  
* app文件夹，服务器搭建可视化展示
    > 10.运行manager.py启动服务器，浏览器输入127.0.0.1:8800/yiqing访问页面。
  

