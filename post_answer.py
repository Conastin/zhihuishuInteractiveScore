import json
import random
import time
import os
import requests
import threading

cookie = ''
task = []


def read_cookie():
	global cookie
	with open('cookie.txt') as f:
		cookie = f.read()


def read_course(filename):
	with open('./course/' + filename + '.txt') as f:
		return json.loads(f.read())


def getLoginUserInfo() -> json:
	'''
	获取登录信息
	:return:
	'''
	getInfo_url = 'https://onlineservice.zhihuishu.com/login/getLoginUserInfo'
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',
		'Cookie': cookie,
		'Host': 'onlineservice.zhihuishu.com',
		'Origin': 'https://onlineh5.zhihuishu.com',
		'Referer': 'https://onlineh5.zhihuishu.com/onlineWeb.html'
	}
	r = json.loads(requests.get(getInfo_url, headers=headers).text)
	return r


def getCourseId(uuid) -> list:
	'''
	获取课程id
	:return:
	'''
	getCourseId_url = 'https://onlineservice.zhihuishu.com/student/course/share/queryShareCourseInfo'
	data = {
		'status': 0,
		'pageNo': 1,
		'pageSize': 50,
		'uuid': uuid,
	}
	r = json.loads(requests.post(getCourseId_url, data=data).text)
	return r['result']['courseOpenDtos']


def isHaveInteractive(course_id, course_recruitId) -> bool:
	'''
	判断是否有互动分
	:param course_id: 课程id
	:return: True or False
	'''
	check_url = 'https://stuonline.zhihuishu.com/stuonline/json/stuLearnReportNew/loadStuLearingTab/'
	data = {
		'courseId': course_id,
		'recruitId': course_recruitId,
		'type': 'l',
	}
	r = json.loads(requests.post(check_url, data=data).text)
	interactiveScore = r['scoreAssessRuleDto']['learnedInteractiveScoreShare']
	if interactiveScore == '0':
		return False
	return True


def getInteractiveScore(course_id, course_recruitId) -> int:
	'''
	获得互动成绩
	:param course_id: 课程id
	:param course_recruitId: 课程recruitId
	:return: 返回还差多少互动分
	'''
	getInteractiveScore_url = 'https://stuonline.zhihuishu.com/stuonline/json/stuLearnReportNew/loadCourseForum/'
	headers = {
		'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',
		'Host': 'stuonline.zhihuishu.com',
		'Origin': 'https://stuonline.zhihuishu.com',
		'Referer': 'https://stuonline.zhihuishu.com/stuonline/stuLearnReportNew/index?recruitId=' + str(
			course_recruitId) + '&recruitId=' + str(course_id),
		'Cookie': 'JSESSIONID=3E61714D8F18C66143C05EA18FE268E8; Z_LOCALE=1; exitRecod_dDQoqmlK=2; acw_tc=2f624a1b15913336014474538e47513802fdae9bd673ea0d7cacd79113d86d; privateCloudSchoolInfo_189362841=",1,#003333,https://image.zhihuishu.com/testzhs/myuni/home/201607/d99cafd14fd94370a8d991519ed445d1.png,https://image.zhihuishu.com/testzhs/myuni/home/201608/65046fface9e4795aa6c75eb484d7f4b.png,1511,//school.zhihuishu.com/sdmu,"; CASTGC=TGT-2340486-Q6QsZO5EJcwmfVm4qCIOz5EOlkxdccaekuHH2ysF1C9xFkglFa-passport.zhihuishu.com; CASLOGC=%7B%22realName%22%3A%22%E7%8E%8B%E5%AE%89%E7%90%AA%22%2C%22myuniRole%22%3A0%2C%22myinstRole%22%3A0%2C%22userId%22%3A189362841%2C%22headPic%22%3A%22https%3A%2F%2Fimage.zhihuishu.com%2Fzhs%2Fablecommons%2Fdemo%2F201804%2F586a2783a3054bd9a751dbbe5979b530_s3.jpg%22%2C%22uuid%22%3A%22dDQoqmlK%22%2C%22mycuRole%22%3A0%2C%22username%22%3A%22abc9ff5cf3c74fd88d9b227bd51448e5%22%7D; o_session_id=F3BAE46D8A54BDC865AA27C74CA2BA83; u_asec=099%23KAFEH7EKExSEhYTLEEEEEpEQz0yFD6fJSryoa6thSri7W6gTZcvMV6PHBYFETEEEbORuE7EFNIaHFXYTEHIEj%2FYEjrozRhj2iEAkWw7e0HzcmCXGkLFABFt05cToKi7bkfMWVDGt0HzqwHyu0HUAqmoRyUQAqHGtkfMWVDGNqCA0DLO4BwSG35t3yUQAqHGbBEFE13iSEqmrwTbUsYFET%2FyZTEwmLuGTE1LSt3llF4qRd%2FiS1JRP%2F3oGt37MlXZddqLStTLSsyaGC3iS1RRP%2F3w3AYFE4GEAb%2FZdCwUQrjDt929irOon6YA6b0dt6R7SwGCvasUBbyo6929irOon6YA6b0WVcOU81Ge8C18CcRfcaVOlrVXS6dbROKqVbOFVwGCYWipXh0%2Bu%2FrRFbyXWcMQRv98XhjYy9nsvSa7WcL%2Bc73%2F5rieWqgwqQodt6R7SwGCvasUBbyo692RRqOpneod3bq4B6weZa5MTEEySt9llsya5E7EFt37EFE%3D%3D; SERVERID=472b148b148a839eba1c5c1a8657e3a7|1591347313|1591347291'
	}
	data = {
		'courseId': course_id,
		'recruitId': course_recruitId,
		'type': 'l'
	}
	r = json.loads(requests.post(getInteractiveScore_url, data=data, headers=headers).text)
	learnedInteractiveScore = int(r['learnedInteractiveScore'])
	learnedInteractiveTotalScore = int(r['learnedInteractiveTotalScore'])
	return learnedInteractiveTotalScore - learnedInteractiveScore


def getQaNum(course_id, course_recruitId) -> int:
	'''
	获得答题数量
	:param course_id: 课程id
	:param course_recruitId: 课程recruitId
	:return: 返回当前课程下目前的答题数量
	'''
	getQaNum_url = 'https://creditqa-web.zhihuishu.com/shareCourse/myParticipateQaNum'
	data = {
		'sourceType': 2,
		'courseId': course_id,
		'recruitId': course_recruitId,
	}
	headers = {
		'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',
		'Host': 'creditqa-web.zhihuishu.com',
		'Origin': 'https://creditqa-web.zhihuishu.com',
		'Referer': 'https://creditqa-web.zhihuishu.com/shareCourse/qaAnswerIndexPage?sourceType=2&courseId=' + str(
			course_id) + '&recruitId=' + str(course_recruitId),
		'Cookie': cookie
	}
	r = json.loads(requests.post(getQaNum_url, data=data, headers=headers).text)
	return r['result']['answerNum']


def getQuestionId(course_id, course_recruitId, num=500) -> list:
	'''
	获取问题id
	:param course_id: 课程id
	:param course_recruitId: 课程recruitId
	:param num: 获取问题数量 默认500
	:return: 返回包含问题id的集合
	'''
	getQuestionId_url = 'https://creditqa-web.zhihuishu.com/shareCourse/getHotQuestionList'
	headers = {
		'Referer': 'https://creditqa-web.zhihuishu.com/shareCourse/qaAnswerIndexPage?sourceType=2&courseId=' + str(
			course_id) + '&recruitId=' + str(course_recruitId),
		'Host': 'creditqa-web.zhihuishu.com',
		'Origin': 'https://creditqa-web.zhihuishu.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',
		'Cookie': cookie
	}
	data = {
		'recruitId': course_recruitId,
		'courseId': course_id,
		'pageSize': num,
		'pageIndex': 0,
	}
	r = json.loads(requests.post(getQuestionId_url, data=data, headers=headers).text)
	# print(r)
	question_list = r['result']['questionInfoList']
	# for question in question_list:
	#     # 获取到问题id, 获取别人的回答
	#     print(question['questionId'], question['content'])
	return question_list


def getAnswer(course_recruitId, course_id, question_id):
	'''
	获取别人的回答
	:param course_id: 课程id
	:param course_recruitId: 课程recruitId
	:param question_id:
	:return:
	'''
	getAnser_url = 'https://creditqa-web.zhihuishu.com/answer/getAnswerInInfoOrderByTime'
	headers = {
		'Cookie': cookie,
		'Host': 'creditqa-web.zhihuishu.com',
		'Origin': 'https://creditqa-web.zhihuishu.com',
		'Referer': 'https://creditqa-web.zhihuishu.com/shareCourse/qaAnswerIndexPage?sourceType=2&courseId=' + str(
			course_id) + '&recruitId=' + str(course_recruitId),
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
	}
	data = {
		'pageSize': 100,
		'pageIndex': 0,
		'questionId': question_id,
		'sourceType': 2,
		'recruitId': course_recruitId,
		'courseId': course_id
	}
	r = json.loads(requests.post(getAnser_url, data=data, headers=headers).text)
	answer_list = r['result']['answerInfos']
	return answer_list


def postAnswer(question_id, answer, course_id, course_recruitId):
	postAnswer_url = 'https://creditqa-web.zhihuishu.com/answer/saveAnswer'
	headers = {
		'Cookie': cookie,
		'Host': 'creditqa-web.zhihuishu.com',
		'Origin': 'https://creditqa-web.zhihuishu.com',
		'Referer': 'https://creditqa-web.zhihuishu.com/shareCourse/qaAnswerIndexPage?sourceType=2&courseId=' + str(
			course_id) + '&recruitId=' + str(course_recruitId),
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
	}
	data = {
		'qid': question_id,
		'aContent': answer,
		'source': 2,
	}
	requests.post(postAnswer_url, data=data, headers=headers)


def getMyAnswerList(course_id, course_recruitId):
	url = 'https://creditqa-web.zhihuishu.com/shareCourse/myParticipateQaNum'
	headers = {
		'Host': 'creditqa-web.zhihuishu.com',
		'Origin': 'https://creditqa-web.zhihuishu.com',
		'Referer': 'https://creditqa-web.zhihuishu.com/shareCourse/qaAnswerIndexPage?sourceType=2&courseId=' + str(
			course_id) + '&recruitId=' + str(course_recruitId),
		'cookie': cookie,
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
	}
	data = {
		'sourceType': 2,
		'courseId': course_id,
		'recruitId': course_recruitId,
	}
	r = json.loads(requests.post(url, headers=headers, data=data).text)
	if r['code'] == 200:
		num = r['result']['answerNum']
		print(num)
	else:
		return 'error'
	url = 'https://creditqa-web.zhihuishu.com/answer/myAnswerList'
	headers = {
		'Host': 'creditqa-web.zhihuishu.com',
		'Origin': 'https://creditqa-web.zhihuishu.com',
		'Referer': 'https://creditqa-web.zhihuishu.com/shareCourse/myParticipatePage?sourceType=2&type=1&courseId=' + str(
			course_id) + '&recruitId=' + str(course_recruitId),
		'cookie': cookie,
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
	}
	answer = []
	i = 0
	while num > 0:
		num -= 200
		data = {
			'courseId': course_id,
			'recruitId': course_recruitId,
			'pageSize': 200,
			'pageIndex': i
		}
		r = json.loads(requests.post(url, headers=headers, data=data).text)
		if r['code'] == 200:
			answer += r['result']['myAnswers']
		i += 1
	return answer


def postLike(answer_id, course_id, course_recruitId):
	url = 'https://creditqa-web.zhihuishu.com/answer/updateOperationToLike'
	headers = {
		'Host': 'creditqa-web.zhihuishu.com',
		'Origin': 'https://creditqa-web.zhihuishu.com',
		'Referer': 'https://creditqa-web.zhihuishu.com/shareCourse/myParticipatePage?sourceType=2&type=1&courseId=' + str(
			course_id) + '&recruitId=' + str(course_recruitId),
		'cookie': cookie
	}
	data = {
		'answerId': answer_id,
		'islike': 0,
		'sourceType': 2
	}
	r = json.loads(requests.post(url, headers=headers, data=data).text)
	if r['code'] == 200:
		print(' answer_id:', answer_id, ' 点赞成功')
	else:
		print(' answer_id:', answer_id, ' 点赞失败:', r)


def func_getAllCourse():
	userInfo = getLoginUserInfo()
	course_save = []
	if userInfo['code'] == 403:
		print('未登录')
	else:
		# print(userInfo)
		userName = userInfo['result']['realName']
		uuid = userInfo['result']['uuid']
		print(userName, uuid)
		course_list = getCourseId(uuid)
		for course in course_list:
			course_id = course['courseId']
			course_name = course['courseName']
			course_recruitId = course['recruitId']
			print(course_id, course_recruitId, course_name, end=' ')
			# if course_recruitId == 21383 and course_id == 2066435:
			# 	continue
			if isHaveInteractive(course_id, course_recruitId):
				course_save.append(
					{
						'course_id': course_id,
						'course_recruitId': course_recruitId,
					}
				)
		with open('./course/course_' + uuid + '_' + userName + '.txt', 'w') as f:
			f.write(json.dumps(course_save))
		return 'course_' + uuid + '_' + userName


def func_postAnswer(filename, number=50):
	courses = read_course(filename)
	for course in courses:
		course_id = course['course_id']
		course_recruitId = course['course_recruitId']
		print(course_id, course_recruitId)
		# score = getInteractiveScore(course_id, course_recruitId)
		# print('还需要', score, '分')
		count = 0
		print('开始时作答数目： ', getQaNum(course_id, course_recruitId))
		question_list = getQuestionId(course_id, course_recruitId, num=number)
		for question in question_list:
			question_id = question['questionId']
			questionInfo = question['content']
			answer_list = getAnswer(course_id, course_recruitId, question_id)
			try:
				if len(answer_list) == 0:
					continue
				answer = answer_list[random.randint(0, len(answer_list) - 1)]['answerContent']
				count += 1
				print(count, '. ', question_id, ' -> ', questionInfo, ' :　', answer, end=' ')
				postAnswer(question_id, answer, course_id, course_recruitId)
				time.sleep(3)
				QaNum = getQaNum(course_id, course_recruitId)
				print(QaNum)
				if QaNum == number:
					break
			except:
				print('ERROR:  ', question)
		print('结束时作答数目： ', getQaNum(course_id, course_recruitId))
		print('共提交题目：', count)


def func_getAllAnswer(filename):
	courses = read_course(filename)
	for course in courses:
		course_id = course['course_id']
		course_recruitId = course['course_recruitId']
		answerList = {
			'course_id': course_id,
			'course_recruitId': course_recruitId,
			'aid': []
		}
		MyAnswerList = getMyAnswerList(course_id, course_recruitId)
		for answer in MyAnswerList:
			answerList['aid'].append(answer['aid'])
		print(answerList)
		with open('./answer/answer_' + str(course_id) + '_' + str(answerList['aid'][0]) + '.txt', 'w') as f:
			f.write(json.dumps(answerList))


def func_like():
	files = os.listdir('./answer')
	for file in files:
		with open('./answer/' + file) as f:
			answerList = json.loads(f.read())
			course_id = answerList['course_id']
			course_recruitId = answerList['course_recruitId']
			print(course_id, course_recruitId)
			# for answer_id in answerList['aid']:
			# 	print(i, ' : ', answer_id)
			task.append(
				threading.Thread(target=thread_postLike, args=(answerList['aid'], course_id, course_recruitId,)))
	for thread in task:
		thread.start()
	for thread in task:
		thread.join()


def thread_postLike(answerList, course_id, course_recruitId):
	for answer_id in answerList:
		postLike(answer_id, course_id, course_recruitId)


if __name__ == '__main__':
	read_cookie()
	filename = func_getAllCourse()
	func_postAnswer(filename)
	func_getAllAnswer(filename)
	func_like()
