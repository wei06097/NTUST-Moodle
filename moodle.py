###  moodle.py  ###

TIMEOUT = 30
SEMESTER = "1112"

import requests, bs4
MOODLE_URL = "https://moodle2.ntust.edu.tw"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}

#################################################################################
class Moodle:
    def __init__(self, username="", password=""):
        self.rs = requests.session()
        self.rs.headers.update(HEADERS)
        self.good_state = True
        #--------------------
        self.__sesskey = ""  #got after login
        self.__messages = {
            "login": "message: login succeed",
            "logout": "message: logout succeed"
        }
        self.__error_messages = {
            "token": "error: get logintoken failed",
            "login": "error: login failed",
            "logout": "error: logout failed"
        }
        self.__url = {
            "login": str(MOODLE_URL) + "/login/index.php",
            "homepage": str(MOODLE_URL) + "/my/",
            "logout": str(MOODLE_URL) + "/login/logout.php"
        }
        self.__form_data = {
            "logintoken": str(self.__getToken()),
            "username": str(username),
            "password": str(password)
        }
    #----------------------------------------
    def __getToken(self):
        try: login_html = self.rs.get(self.__url["login"], timeout=TIMEOUT).text
        except Exception: login_html = ""
        root = bs4.BeautifulSoup(login_html, "html.parser")
        inputs = root.find_all("input")
        for input_ in inputs:
            if (input_.get("name") == "logintoken"): return input_.get("value")
        print(self.__error_messages["token"])
        self.good_state = False
        return ""
    #----------------------------------------
    def __history(self, result):  #test
        if result.history:
            print("requests was redirected:")
            for resp in result.history: print(resp.status_code, resp.url)
        else: print("requests was not redirected:")
        print("Final destination:")
        print(result.status_code, result.url)
    #----------------------------------------
    def login(self):  #return homepage_html
        if(not self.good_state):
            print(self.__error_messages["login"])
            return ""
        try:
            result = self.rs.post(self.__url["login"], data=self.__form_data, timeout=TIMEOUT)
            homepage_html = self.rs.get(self.__url["homepage"], timeout=TIMEOUT).text
        except Exception: homepage_html = ""
        #self.__history(result)
        root = bs4.BeautifulSoup(homepage_html, "html.parser")
        inputs = root.find_all("input")
        for input_ in inputs:
            if (input_.get("name") == "sesskey"): self.__sesskey = input_.get("value")
        if(self.__sesskey != ""):
            print(self.__messages["login"])
            return homepage_html
        else:
            print(self.__error_messages["login"])
            self.good_state = False
            return ""
    #----------------------------------------
    def logout(self):  #clear cookie
        if(not self.good_state):
            print(self.__error_messages["logout"])
            return
        try:
            result = self.rs.post(self.__url["logout"], params={"sesskey": self.__sesskey}, timeout=TIMEOUT)
            print(self.__messages["logout"])
        except Exception:
            print(self.__error_messages["logout"])
            self.good_state = False

#################################################################################
def getCourses(html):
    root = bs4.BeautifulSoup(html, "html.parser")
    names = root.find_all("span", class_="text")
    keys = root.find_all("li", class_="list-group-item-action")
    #print(names, keys)
    courses = []; ids = []; count = 0
    for name in names:
        if ("[TaiwanTech]" in name.string) & (name.string[-14:-10] == SEMESTER):
            courses += [name.text[13:-16]]
            count += 1
    for key in keys:
        try: 
            ids += [str(int(key.get("data-key")))]
            count -= 1
            if (count == 0): break
        except Exception: pass
    #print(courses, ids)
    return [courses, ids]

def getCourseData(rs, id):
    course_href = "https://moodle2.ntust.edu.tw/course/view.php?id=" + id 
    try: course_html = rs.get(course_href, timeout=TIMEOUT).text
    except Exception:
        print("error: get course data failed")
        return "error"
    #print(course_html)
    root = bs4.BeautifulSoup(course_html, "html.parser")
    instancenames = root.find_all("span", class_="instancename")
    accesshides = root.find_all("span", class_="accesshide")
    aalinks = root.find_all("a", class_="aalink")
    #print(instancenames, accesshides, aalinks)
    types=[]; serials=[]; names=[]; links=[]
    for i in range(len(aalinks)-6):
        names += [instancenames[i].text.replace(accesshides[i].text, "")]
        links += [aalinks[i].get("href")]
        [a, b] = links[i].replace("https://moodle2.ntust.edu.tw/mod/", "").replace("/view.php?id", "").split("=")
        types+=[a]; serials+=[b]
    #for i in range(len(aalinks)): print(types[i], serials[i], names[i], links[i])
    course_data_list = []
    for i in range(len(aalinks)-6):
        if(i != 0): course_data_list += [{"type": types[i], "id": serials[i], "name": names[i], "link": links[i]}]
    #print(course_data_list)
    return course_data_list