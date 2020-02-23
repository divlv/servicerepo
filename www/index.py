import json
import re
import uuid
import srutils

import psycopg2
import psycopg2.extras
from flask import Flask
from flask import render_template, request, redirect
from psycopg2 import pool

import captions

minConnection = 5
maxConnection = 20
# Keep calm, GitHub password crawlers. Go hack example.com!
connectionPool = psycopg2.pool.ThreadedConnectionPool(minConnection, maxConnection, user="sreapp", password="scheme54inverse63Frenzy",
                                                      host="postgres.example.com", port="5432", database="servicerepo")
if (connectionPool):
    print("Connection pool created successfully")

app = Flask(__name__)

PATH_TO_TEMPLATES = "./tpl/"
app = Flask(__name__, template_folder=PATH_TO_TEMPLATES)


"""
Main starter page
"""
@app.route('/')
def home_page():
    return render_template('layout.html',
                           captions=captions,
                           featured=0,
                           id=0,
                           edit=0,
                           itemid=0,
                           endpoint="",
                           getmethod="",
                           postmethod="checked",
                           internal="checked",
                           external="",
                           tags="",
                           incomingjson="",
                           outgoingjson="",
                           bodyhtml='main')

"""
Initial search window (without results yet)
"""
@app.route('/search')
def search_page():
    return render_template('layout.html',
                           captions=captions,
                           featured=0,
                           showslides=0,
                           andChecked="checked",
                           orChecked="",
                           outgoingChecked="",
                           incomingChecked="checked",
                           bodyhtml='search')


"""
Saving new endpoint
"""
@app.route('/save', methods=['POST'])
def map_page():
    endpoint = request.form['endpoint']

    # Prevent saving empty endpoint name.
    if str(endpoint).strip()=="":
        return redirect("/?c="+str(uuid.uuid4()), code=302)

    queryVars = {}
    queryVarsArray = []
    if str(endpoint).find("{")>-1:
        queryVarsArray = re.findall('{(.+?)}', str(endpoint))

    queryVars["vars"] = queryVarsArray

    tags = request.form['tags']
    method = request.form['method']
    area = request.form['area']

    allTags = tags.split(",")
    allTagsJson = {}
    tagsArray = []
    for t in allTags:
        tt = str(t).strip()
        if ""!=tt:
            tagsArray.append(tt)

    allTagsJson["tags"] = tagsArray


    incomingjson = request.form['incomingjson']
    if ""== str(incomingjson).strip():
        incomingjson = "{}"

    outgoingjson = request.form['outgoingjson']
    if ""== str(outgoingjson).strip():
        outgoingjson = "{}"

    dbConnection = connectionPool.getconn()
    try:
        dbCursor = dbConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        insert_query = "insert into service_repo (endpoint, queryvars, method, area, incomingjson,outgoingjson, tags) values (%s,%s,%s,%s,%s,%s,%s)"
        dbCursor.execute(insert_query, (endpoint, json.dumps(queryVars), method, area, incomingjson, outgoingjson, json.dumps(allTagsJson)))

        dbCursor.close()
        dbConnection.commit()
    finally:
        connectionPool.putconn(dbConnection)

    # your code
    # return a response
    return render_template('layout.html',
                           captions=captions,
                           rnd=str(uuid.uuid4()),
                           featured=0,
                           showslides=0,
                           bodyhtml='inserted')


"""
Edit endpoint method
"""
@app.route('/update', methods=['POST'])
def update_page():
    id = request.form['itemid']

    tags = request.form['tags']
    method = request.form['method']
    area = request.form['area']

    allTags = tags.split(",")
    allTagsJson = {}
    tagsArray = []
    for t in allTags:
        tt = str(t).strip()
        if ""!=tt:
            tagsArray.append(tt)

    allTagsJson["tags"] = tagsArray


    incomingjson = request.form['incomingjson']
    if ""== str(incomingjson).strip():
        incomingjson = "{}"

    outgoingjson = request.form['outgoingjson']
    if ""== str(outgoingjson).strip():
        outgoingjson = "{}"

    dbConnection = connectionPool.getconn()
    try:
        dbCursor = dbConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        update_query = "UPDATE service_repo SET method=%s, area=%s, incomingjson=%s, outgoingjson=%s, tags=%s WHERE id=%s"
        dbCursor.execute(update_query, (method, area, incomingjson, outgoingjson, json.dumps(allTagsJson), id))

        dbCursor.close()
        dbConnection.commit()
    finally:
        connectionPool.putconn(dbConnection)

    return render_template('layout.html',
                           captions=captions,
                           rnd=str(uuid.uuid4()),
                           featured=0,
                           showslides=0,
                           bodyhtml='inserted')


"""
On-the-fly endpoint unique name check. Called from javascript onBlur
"""
@app.route('/checkendpoint', methods=['POST'])
def check_endpoints_count():
    endpoint = request.form['endpoint']

    dbConnection = connectionPool.getconn()
    result = {}
    try:
        dbCursor = dbConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dbCursor.execute(
            'SELECT count(id) AS cnt '
            'FROM service_repo WHERE endpoint=%s',
            (endpoint,))
        rows = dbCursor.fetchall()
        result["count"] = rows[0]['cnt'];
        dbCursor.close()
    finally:
        connectionPool.putconn(dbConnection)
    return result

"""
Delete endpoint routine
"""
@app.route('/deleteitem/<itemid>')
def delete_endpoint(itemid):
    dbConnection = connectionPool.getconn()
    try:
        dbCursor = dbConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dbCursor.execute(
            'DELETE FROM service_repo WHERE id=%s',
            (itemid,))
        dbConnection.commit()
        dbCursor.close()
    finally:
        connectionPool.putconn(dbConnection)
    return redirect("/search", code=302)

"""
Open edit endpoint form
"""
@app.route('/edit/<itemid>')
def edit_endpoint(itemid):
    dbConnection = connectionPool.getconn()
    try:
        dbCursor = dbConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dbCursor.execute(
            'SELECT * FROM service_repo WHERE id=%s',
            (itemid,))
        rows = dbCursor.fetchall()
        dbCursor.close()
    finally:
        connectionPool.putconn(dbConnection)

    dbtags = rows[0]['tags']
    tagsForEdit = ''
    divider = ''
    for t in dbtags['tags']:
        tagsForEdit = tagsForEdit + divider + t
        divider = ', '

    return render_template('layout.html',
                           captions=captions,
                           featured=0,
                           edit=1,
                           itemid=itemid,
                           endpoint=rows[0]['endpoint'],
                           getmethod="checked" if rows[0]['method'] == "GET" else "",
                           postmethod="checked" if rows[0]['method'] == "POST" else "",
                           internal="checked" if rows[0]['area'] == "internal" else "",
                           external="checked" if rows[0]['area'] == "external" else "",
                           tags=tagsForEdit,
                           incomingjson=json.dumps(rows[0]['incomingjson'], indent=4, sort_keys=True),
                           outgoingjson=json.dumps(rows[0]['outgoingjson'], indent=4, sort_keys=True),
                           bodyhtml='main')

"""
Main search routine
"""
@app.route('/dosearch', methods=['GET'])
def do_search():
    searchString = srutils.getQueryStringParam(request, 'searchString')
    searchStringTag = srutils.getQueryStringParam(request, 'searchStringTag')
    jsontype = srutils.getQueryStringParam(request, 'jsontype')
    outgoingChecked="checked"
    incomingChecked=""
    if "outgoingjson" != jsontype:
        jsontype = "incomingjson"
        outgoingChecked=""
        incomingChecked="checked"

    criteria = srutils.getQueryStringParam(request, 'criteria')
    andChecked=""
    orChecked="checked"
    if "or" != criteria:
        criteria = "and"
        andChecked="checked"
        orChecked=""

    # JSON keys...
    wordsArray = []
    if len(searchString.strip())>0:
        searchString = searchString.replace('\'', '')

    allKeyWords = re.findall(r"[\w']+", searchString.strip())
    for keyWord in allKeyWords:
        w = str(keyWord).strip()
        if ""!=w:
            wordsArray.append(w)

    wordsTuple = tuple(wordsArray)

    # Query vars, tags is any...
    tagsArray = []
    if len(searchStringTag.strip())>0:
        searchStringTag = searchStringTag.replace('\'', '')

    allTagsWords = re.findall(r"[\w']+", searchStringTag.strip())
    for keyTag in allTagsWords:
        w = str(keyTag).strip()
        if ""!=w:
            tagsArray.append(w)

    tagsAndWarsTuple = tuple(tagsArray)



    if "or"==criteria or len(wordsTuple)==0:
        sqlQuery = "select * from service_repo where 1=2"
        for t in wordsTuple:
            sqlQuery = sqlQuery + " or jsonb_path_exists(%s, '$.**.%s')" % (jsontype, t)

        if len(tagsAndWarsTuple)>0:
            sqlQuery = sqlQuery + " or tags->'tags' ?| ARRAY['nosuchtag'"
            for t in tagsAndWarsTuple:
                sqlQuery = sqlQuery + ",'%s'" % t
            sqlQuery = sqlQuery + "]"

        if len(tagsAndWarsTuple)>0:
            sqlQuery = sqlQuery + " or queryvars->'vars' ?| ARRAY['nosuchvar'"
            for t in tagsAndWarsTuple:
                sqlQuery = sqlQuery + ",'%s'" % t
            sqlQuery = sqlQuery + "]"

        if  len(wordsTuple)==0:
            sqlQuery = sqlQuery + " or 1=1"
    else:
        # AND criteria
        sqlQuery = "select * from service_repo where "
        subDivider=""
        for w in wordsTuple:
            sqlQuery = sqlQuery + subDivider + "jsonb_path_exists(%s, '$.**.%s') " % (jsontype, w)
            subDivider=" and "

        if len(tagsAndWarsTuple)>0:
            sqlQuery = sqlQuery + subDivider + "((tags->'tags' ?& ARRAY["
            div = ""
            for t in tagsAndWarsTuple:
                sqlQuery = sqlQuery + div+ "'%s'" % t
                div=","
            sqlQuery = sqlQuery + "]) or ("

            sqlQuery = sqlQuery + "queryvars->'vars' ?& ARRAY["
            div = ""
            for t in tagsAndWarsTuple:
                sqlQuery = sqlQuery + div+ "'%s'" % t
                div=","
            sqlQuery = sqlQuery + "]))"




    sqlQuery = sqlQuery + " ORDER BY id DESC"

    dbConnection = connectionPool.getconn()
    try:
        dbCursor = dbConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        dbCursor.execute(
            sqlQuery)
            #wordsTuple)
        rows = dbCursor.fetchall()

        for row in rows:
            row['incomingjson'] = json.dumps(row['incomingjson'], indent=4, sort_keys=True)
            row['outgoingjson'] = json.dumps(row['outgoingjson'], indent=4, sort_keys=True)

        resultsCount = len(rows)
    finally:
        connectionPool.putconn(dbConnection)

    return render_template('layout.html',
                           captions=captions,
                           searchString=searchString,
                           searchStringTag=searchStringTag,
                           rows=rows,
                           resultsCount =resultsCount,
                           featured=0,
                           showslides=0,
                           andChecked=andChecked,
                           orChecked=orChecked,
                           outgoingChecked=outgoingChecked,
                           incomingChecked=incomingChecked,
                           bodyhtml='searchresult')



# <Error pages>
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', captions=captions), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', captions=captions), 500
# </Error pages>


# Uncomment this line, if running in Development environment
# i.e. NOT with something like Gunicorn
# Will be automatically commented by Docker build script
app.run(host='0.0.0.0', port='80', threaded=True)
