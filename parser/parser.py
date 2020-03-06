import json
import re
import sys
from html.parser import HTMLParser

import psycopg2
import psycopg2.extras
from psycopg2 import pool

minConnection = 5
maxConnection = 20
# Keep calm, GitHub password crawlers. Localhost is here...
connectionPool = psycopg2.pool.ThreadedConnectionPool(minConnection, maxConnection, user="sreapp",
                                                      password="scheme54inverse63Frenzy",
                                                      host="127.0.0.1", port="15432", database="servicerepo")
if (connectionPool):
    print("Connection pool created successfully")


def insertData(service):
    endpoint = service['endpoint']
    servicename = service['name']

    queryVars = {}
    queryVarsArray = []
    if str(endpoint).find("{") > -1:
        queryVarsArray = re.findall('{(.+?)}', str(endpoint))

    queryVars["vars"] = queryVarsArray

    method = service['method']
    area = service['area']

    allTagsJson = {}
    tagsArray = []
    allTagsJson["tags"] = tagsArray

    incomingjson = service['incomingjson']
    if "" == str(incomingjson).strip():
        incomingjson = "{}"

    outgoingjson = service['outgoingjson']
    if "" == str(outgoingjson).strip():
        outgoingjson = "{}"

    dbConnection = connectionPool.getconn()
    try:
        dbCursor = dbConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        insert_query = "insert into service_repo (servicename, endpoint, queryvars, method, area, incomingjson,outgoingjson, tags) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        dbCursor.execute(insert_query, (
        servicename, endpoint, json.dumps(queryVars), method, area, incomingjson, outgoingjson,
        json.dumps(allTagsJson)))

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

    service = {}

    def handle_starttag(self, tag, attrs):
        if str(tag) == 'h3':
            self.waitForRequestUrlTag = True

        if str(tag) == 'h2':
            self.waitForServiceName = True
            self.sectionOpened = True
        else:
            self.waitForServiceName = False

        if str(tag) == 'code':
            if len(attrs) == 1 and attrs[0] == ('class', 'language-bash'):
                self.waitForRequest = True

        if str(tag) == 'code' and self.requestPassed:
            if len(attrs) == 1 and attrs[0] == ('class', 'language-json'):
                self.waitForResponse = True

        if str(tag) == 'code' and len(attrs) == 0 and self.waitForRequestUrlTag:
            self.waitForRequestUrlValue = True

    def handle_data(self, data):
        clearData = str(data).strip()
        if (self.waitForServiceName and len(clearData)) > 0:
            self.service['name'] = str(data).strip()

        if (self.waitForRequestUrlValue):
            methodAndUrl = clearData.split(" ")
            method = methodAndUrl[0]
            self.service['method'] = method
            self.service['endpoint'] = clearData
            if clearData.find("external") > 0:
                self.service['area'] = "external"
            else:
                self.service['area'] = "internal"

            print("-----------------------------")
            print(self.service)
            insertData(self.service)
            self.waitForRequestUrlTag = False
            self.waitForRequestUrlValue = False

        if (self.waitForRequest and len(clearData)) > 0:
            pattern = "(.*?)\'(.*?)\'(.*?)"
            req = re.search(pattern, data)
            if req != None:
                self.service['incomingjson'] = re.search(pattern, data).group(2)
            else:
                self.service['incomingjson'] = ''
            self.waitForRequest = False
            self.requestPassed = True

        if (self.waitForResponse and len(clearData)) > 0:
            self.service['outgoingjson'] = "".join(data.splitlines())
            self.waitForResponse = False
            self.requestPassed = False


parser = SourceHTMLParser()
data = ""
with open(sys.argv[1], 'r', encoding='utf-8') as srcFile:
    data = srcFile.read()

parser.feed(data)
