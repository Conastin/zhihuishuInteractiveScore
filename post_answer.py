import json
import random
import requests

cookie = ''


def getLoginUserInfo():
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
    return r['result']


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


def getInteractiveScore(course_id, course_recruitId):
    '''
    获得互动成绩
    :param course_id:
    :param course_recruitId:
    :return:
    '''
    getInteractiveScore_url = 'https://stuonline.zhihuishu.com/stuonline/json/stuLearnReportNew/loadCourseForum/'
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77',
        'Host': 'stuonline.zhihuishu.com',
        'Origin': 'https://stuonline.zhihuishu.com',
        'Referer': 'https://stuonline.zhihuishu.com/stuonline/stuLearnReportNew/index?recruitId=' + str(course_id) + '&recruitId=' + str(course_recruitId),
        'Cookie': cookie
    }
    data = {
        'courseId': course_id,
        'recruitId': course_recruitId,
        'type': 'l'
    }
    r = json.loads(requests.post(getInteractiveScore_url, data=data, headers=headers).text)
    learnedInteractiveScore = int(r['learnedInteractiveScore'])
    learnedInteractiveTotalScore = int(r['learnedInteractiveTotalScore'])
    return learnedInteractiveTotalScore-learnedInteractiveScore


def getQaNum(course_id, course_recruitId) -> int:
    '''
    获得答题数量
    :return:
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


def getQuestionId(course_id, course_recruitId) -> list:
    '''
    获取问题id
    :return: Idlist
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
        'pageSize': 300,
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


def postAnswer(question_id, answer):
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


if __name__ == '__main__':
    userInfo = getLoginUserInfo()
    userName = userInfo['realName']
    uuid = userInfo['uuid']
    print(userName, uuid)
    course_list = getCourseId(uuid)
    for course in course_list:
        course_id = course['courseId']
        course_name = course['courseName']
        course_recruitId = course['recruitId']
        print(course_id, course_recruitId, course_name, end=' ')
        if isHaveInteractive(course_id, course_recruitId):
            score = getInteractiveScore(course_id, course_recruitId)
            print('还需要', score, '分')
            if score == 0:
                continue
            count = 0
            print('开始时作答数目： ', getQaNum(course_id, course_recruitId))
            question_list = getQuestionId(course_id, course_recruitId)
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
                    postAnswer(question_id, answer)
                    # time.sleep(5)
                    print(getQaNum(course_id, course_recruitId))
                except:
                    print('ERROR:  ', question)
            print('结束时作答数目： ', getQaNum(course_id, course_recruitId))
            print('共提交题目：', count)
