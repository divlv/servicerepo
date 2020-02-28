import json
from html.parser import HTMLParser
import re
import psycopg2
import psycopg2.extras
from psycopg2 import pool

#services=[]

minConnection = 5
maxConnection = 20
# Keep calm, GitHub password crawlers. Go hack example.com!
connectionPool = psycopg2.pool.ThreadedConnectionPool(minConnection, maxConnection, user="sreapp", password="scheme54inverse63Frenzy",
                                                      host="postgres.example.com", port="5432", database="servicerepo")
if (connectionPool):
    print("Connection pool created successfully")



def insertData(service):
    endpoint = service['endpoint']
    servicename = service['name']

    queryVars = {}
    queryVarsArray = []
    if str(endpoint).find("{")>-1:
        queryVarsArray = re.findall('{(.+?)}', str(endpoint))

    queryVars["vars"] = queryVarsArray

    tags = ""
    method = service['method']
    area = service['area']

    # allTags = tags.split(",")
    allTagsJson = {}
    tagsArray = []
    # for t in allTags:
    #     tt = str(t).strip()
    #     if ""!=tt:
    #         tagsArray.append(tt)
    #
    allTagsJson["tags"] = tagsArray


    incomingjson = service['incomingjson']
    if ""== str(incomingjson).strip():
        incomingjson = "{}"

    outgoingjson = service['outgoingjson']
    if ""== str(outgoingjson).strip():
        outgoingjson = "{}"

    dbConnection = connectionPool.getconn()
    try:
        dbCursor = dbConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        insert_query = "insert into service_repo (servicename, endpoint, queryvars, method, area, incomingjson,outgoingjson, tags) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        dbCursor.execute(insert_query, (servicename, endpoint, json.dumps(queryVars), method, area, incomingjson, outgoingjson, json.dumps(allTagsJson)))

        dbCursor.close()
        dbConnection.commit()
    finally:
        connectionPool.putconn(dbConnection)



class SourceHTMLParser(HTMLParser):
    waitForServiceName = False
    waitForRequestUrlTag = False
    waitForRequestUrlValue = False
    waitForRequest = False
    requestPassed = False
    waitForResponse = False

    service={}

    def handle_starttag(self, tag, attrs):
        if str(tag)=='h3':
            self.waitForRequestUrlTag = True

        if str(tag)=='h2':
            self.waitForServiceName = True
            self.sectionOpened = True
        else:
            self.waitForServiceName = False

        if str(tag)=='code':
            if len(attrs)==1 and attrs[0]==('class', 'language-bash'):
                self.waitForRequest = True

        if str(tag)=='code' and self.requestPassed:
            if len(attrs)==1 and attrs[0]==('class', 'language-json'):
                self.waitForResponse = True

        if str(tag)=='code' and len(attrs)==0 and self.waitForRequestUrlTag:
            self.waitForRequestUrlValue = True

    #def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        clearData = str(data).strip()
        if (self.waitForServiceName and len(clearData))>0:
            #print("SERVICE NAME:::::::", data, "\n")
            self.service['name'] = str(data).strip()

        if (self.waitForRequestUrlValue):
            print("-----------------------------------------------")
            methodAndUrl = clearData.split(" ")
            method = methodAndUrl[0]
            #print("REQUEST METHOD:::::::" + method, "\n")
            self.service['method'] = method
            #print("REQUEST URL:::::::" + methodAndUrl[1], "\n")
            #print("REQUEST URL:::::::" + clearData, "\n")
            self.service['endpoint'] = clearData
            if clearData.find("external")>0:
                self.service['area'] = "external"
            else:
                self.service['area'] = "internal"


            print (self.service)
            insertData(self.service)
            self.waitForRequestUrlTag = False
            self.waitForRequestUrlValue = False


        if (self.waitForRequest and len(clearData))>0:
            pattern = "(.*?)\'(.*?)\'(.*?)"
            req = re.search(pattern, data)
            if req!=None:
               #print("REQUEST::::::::::::", re.search(pattern, data).group(2))
               self.service['incomingjson'] = re.search(pattern, data).group(2)
            else:
               #print("REQUEST::::::::::::", "No body")
               self.service['incomingjson'] = ''
            self.waitForRequest = False
            self.requestPassed = True

        if (self.waitForResponse and len(clearData))>0:
            #print("RESPONSE::::::::::::", "".join(data.splitlines()))
            self.service['outgoingjson'] = "".join(data.splitlines())
            self.waitForResponse = False
            self.requestPassed = False





parser = SourceHTMLParser()
data = ""
with open('g:/Projects/servicerepo-doc/docs/index.html', 'r', encoding='utf-8') as myfile:
  data = myfile.read()


parser.feed(data)