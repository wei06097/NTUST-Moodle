###  main.py  ####

import moodle, line, file
USERNAME = ""
PASSWORD = ""

def checkMoodle():
    user = moodle.Moodle(USERNAME, PASSWORD)
    homepage_html = user.login()
    if (not user.good_state):
        line.sendMessage("\n\nerror: login failed")
        return
    [courses, ids] = moodle.getCourses(homepage_html)
    #print(courses, ids)

    all_course_data_list = []
    for id in ids:
        course_data_list = moodle.getCourseData(user.rs, id)
        if (course_data_list == "error"):
            user.logout()
            line.sendMessage("\n\nerror: get course data failed")
            return
        else: all_course_data_list += [course_data_list]
    data_json = dict(zip(ids, all_course_data_list))
    #print(data_json)

    user.logout()
    if (not user.good_state): line.sendMessage("\n\nerror: logout failed")
    [message_added, message_deleted] = file.compareData(data_json)
    for i in range(len(message_added)):
        if (message_added[i] == ""): continue
        message_added[i] = ("追加\n\n"+courses[i]+"\n"+message_added[i])
        line.sendMessage(message_added[i])
    for i in range(len(message_deleted)):
        if (message_deleted[i] == ""): continue
        message_deleted[i] = ("削除\n\n"+courses[i]+"\n"+message_deleted[i])
        line.sendMessage(message_deleted[i])

if __name__ == '__main__':
    checkMoodle()
    # line.testMessage()