# -智慧树刷互动分
# 运行环境 #
> - **python3.X**
> - **requests模块**
# 介绍 #
1. 默认回答50个问题
2. 自动给自己的回答点赞
# 注意 #
速度过快会封请求,解封时间半天到一天不等，time.sleep里的时间不要改
# 使用教程 #
1. 浏览器打开[http://www.zhihuishu.com](http://www.zhihuishu.com "知到智慧树官网")
2. 登录你的账号
3. 访问随便一门课程的成绩分析(https://stuonline.zhihuishu.com/stuonline/stuLearnReportNew)前缀为这一网址，打开后再刷新一下
4. 访问随便一门课程的问答(https://creditqa-web.zhihuishu.com/shareCourse/qaAnswerIndexPage)前缀为这一网址，打开后再刷新一下
5. 返回智慧树个人首页(https://onlineh5.zhihuishu.com/onlineWeb.html#/studentIndex)
6. F12打开网络选项卡，刷新
7. CTRL+F搜索找到getLoginUserInfo这个名称，注意是xhr类型，复制该请求的cookie
8. 在postAnswer.py同目录下建立cookie.txt,打开cookie.txt，粘贴复制的cookie，保存
6. 运行postAnswer.py
