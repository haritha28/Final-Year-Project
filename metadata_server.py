# !/usr/bin/env python

from os import path
from local_settings import *

import tornado.options
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import random
import json
import socket, struct, sys
from tornado import autoreload
from hashlib import sha512 as hash_func
import tornado.ioloop
import hello
import static.analysis.AHE_predict.wrapper_analyze_AHE_abp as AHP
import static.analysis.AHE_classify.wrapper_analyze_AHE_abp as AHC
import static.analysis.sleep_apnea_IHR_web_Integration.wrapper_analyze_sleep_apnea_IHR as SF
#import static.analysis.BP.wrapper_analyze_BP as BP


import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options


class LoginHandler(BaseHandler):
    username = ''

    # Authentication using device username and password
    @tornado.web.asynchronous
    def get(self):
        self.render("auth/login.html")

    @tornado.web.asynchronous
    def post(self):
        username = tornado.escape.xhtml_escape(self.get_argument("username"))
        # getpassword = tornado.escape.xhtml_escape(self.get_argument("password"))
        self.db.execute("select password from doctors where username=('%s')" % username,
                        callback=self.add_response)

    def add_response(self, cursor):
        getpassword = tornado.escape.xhtml_escape(self.get_argument("password"))
        getpassword = hash_func(getpassword).hexdigest();
        results = cursor.fetchall()
        passwordfromdb = ''
        if results:
            passwordfromdb = results[0]
        try:
            if str(passwordfromdb[0]) == str(getpassword):
                self.set_secure_cookie("user", self.get_argument("username"))
                self.set_secure_cookie("incorrect", "0")
                self.redirect("/")
            else:
                incorrect = self.get_secure_cookie("incorrect")
                if not incorrect:
                    incorrect = 0
                self.set_secure_cookie("incorrect", str(int(incorrect) + 1))
                # self.write('<center>Something Wrong With Your Data <a href="/">Go Home</a></center>')
                self.redirect("/login")
        except IndexError:
            incorrect = self.get_secure_cookie("incorrect")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [

            tornado.web.url(r'/', MainHandler, name='main'),
            tornado.web.url(r'/login', LoginHandler, name='login'),
            tornado.web.url(r'/getPatientList', DBHandler, name='db'),
            tornado.web.url(r'/getEMRList', emrHandler, name='emr'),
            tornado.web.url(r'/getSensorTypes/(.*)', NodeManageHandler),
            tornado.web.url(r'/getTimeStamps/(.*)', NodeHandler),
            tornado.web.url(r'/getFileLocation/(.*)', NodeLinkHandler),
            tornado.web.url(r'/analyzeECGData', analyzeECGData),
            tornado.web.url(r'/analyzeSPO2Data', analyzeSPO2Data),  # replaced SP02 analyzeSPO2Data
            tornado.web.url(r'/analyzeIHRData', analyzeIHRData),
            tornado.web.url(r'/analyzeAHEPData', analyzeAHEPData),  # adding AHEP
            tornado.web.url(r'/analyzeAHECData', analyzeAHECData),
            tornado.web.url(r'/analyzeBPData', analyzeBPData),
            tornado.web.url(r'/addPatient', addPatientHandler),
            tornado.web.url(r'/addFile', addFileHandler),
            tornado.web.url(r'/logout', LogoutHandler)

        ]
        settings = dict(
            template_path=path.join(path.dirname(__file__), 'templates'),
            static_path=path.join(path.dirname(__file__), 'static'),
            xsrf_cookies=False,
            cookie_secret='dsfretghj867544wgryjuyki9p9lou67543/Vo=',
            login_url='/login'
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = None


class NodeManageHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, mrd):
        if not self.current_user:
            self.redirect("/login")
        self.db.execute("SELECT DISTINCT (type) from emr_log WHERE mrd='%s'" % mrd, \
                        callback=self.add_response)

    def add_response(self, cursor):
        results = cursor.fetchall()

        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj

        self.write(json.dumps(results, default=date_handler))
        self.finish()


class NodeHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, mrd):
        if not self.current_user:
            self.redirect("/login")
        self.db.execute("SELECT type,start_time,end_time from emr_log WHERE mrd='%s'" % mrd, \
                        callback=self.add_response)

    def add_response(self, cursor):
        results = cursor.fetchall()

        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj

        self.write(json.dumps(results, default=date_handler))
        self.finish()


class addPatientHandler(BaseHandler):
    def write_error(self, status_code, **kwargs):
        self.render("newPatient/fail.html", results=self.current_user)

    @tornado.web.asynchronous
    def get(self, mrd):
        if not self.current_user:
            self.redirect("/login")

    @tornado.web.asynchronous
    def post(self):
        try:
            usr = self.current_user
            self.db.execute("SELECT id FROM doctors WHERE doctors.username = '%s'" % usr, callback=self.add_Id)

        except:
            self.set_status(500)

    def add_Id(self, cursor):
        results = cursor.fetchall()
        DoctorId = results[0][0]

        mrd = tornado.escape.xhtml_escape(self.get_argument("mrd"))
        name = tornado.escape.xhtml_escape(self.get_argument("name"))
        age = tornado.escape.xhtml_escape(self.get_argument("age"))
        gender = tornado.escape.xhtml_escape(self.get_argument("gender"))
        address = tornado.escape.xhtml_escape(self.get_argument("address"))
        phoneNumber = tornado.escape.xhtml_escape(self.get_argument("phoneNumber"))
        bloodGroup = tornado.escape.xhtml_escape(self.get_argument("bloodGroup"))
        dateOfReg = tornado.escape.xhtml_escape(self.get_argument("dateOfReg"))

        self.db.execute("INSERT INTO patients(mrd, name, age, gender, address, phone_number, blood_group,\
        registration_date, doctorid) values ('%s', '%s', '%s', '%s','%s','%s','%s','%s', '%s')" % (mrd, name, \
                                                                                                   age, gender, address,
                                                                                                   phoneNumber,
                                                                                                   bloodGroup,
                                                                                                   dateOfReg, DoctorId),
                        callback=self.add_response)

    def add_response(self, response):
        if response:
            self.render("newPatient/success.html", results=self.current_user)
            self.finish()


import os


class addFileHandler(BaseHandler):
    def write_error(self, status_code, **kwargs):
        self.render("addLog/fail.html", results=self.current_user)

    @tornado.web.asynchronous
    def post(self):
        try:
            mrd = tornado.escape.xhtml_escape(self.get_argument("mrd"))
            type = tornado.escape.xhtml_escape(self.get_argument("type"))
            start_date = tornado.escape.xhtml_escape(self.get_argument("start_date"))
            start_time = tornado.escape.xhtml_escape(self.get_argument("start_time"))
            startTimestamp = start_date + " " + start_time
            end_date = tornado.escape.xhtml_escape(self.get_argument("end_date"))
            end_time = tornado.escape.xhtml_escape(self.get_argument("end_time"))
            endTimestamp = end_date + " " + end_time
            file1 = self.request.files['filearg'][0]
            original_fname = file1['filename']
            # extension = os.path.splitext(original_fname)[1]
            final_filename = original_fname
            output_file = open("static/patient_EMR_logs/" + final_filename, 'w')
            output_file.write(file1['body'])

            self.db.execute("INSERT INTO emr_log(mrd, type, filename, start_time, end_time, server_location)\
            values ('%s', '%s', '%s', '%s','%s','%s')" % (
                mrd, type, final_filename, startTimestamp, \
                endTimestamp, 'static/patient_EMR_logs/'), callback=self.add_response)
        except:
            print
            'exit'

    def add_response(self, response):
        if response:
            self.render("addLog/success.html", results=self.current_user)


class NodeLinkHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self, mrd):
        if not self.current_user:
            self.redirect("/login")
        self.db.execute("SELECT type,start_time,end_time,filename,server_location from emr_log WHERE mrd='%s'" % mrd, \
                        callback=self.add_response)

    def add_response(self, cursor):
        results = cursor.fetchall()

        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj

        self.write(json.dumps(results, default=date_handler))
        self.finish()


class DBHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        usr = self.current_user
        if not self.current_user:
            self.redirect("/login")
        self.db.execute(
            "SELECT * FROM patients WHERE patients.doctorid = (SELECT id FROM doctors WHERE doctors.username = '%s')" % (
                usr), callback=self.add_response)

    def add_response(self, cursor):
        results = cursor.fetchall()

        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj

        self.write(json.dumps(results, default=date_handler))
        self.finish()


class emrHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        if not self.current_user:
            self.redirect("/login")
        self.db.execute("SELECT * FROM emr_log",
                        callback=self.add_response)

    def add_response(self, cursor):
        results = cursor.fetchall()

        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj

        self.write(json.dumps(results, default=date_handler))
        self.finish()

#Handler for ECG
class analyzeECGData(BaseHandler):
    def post(self):
        dataRecieved = tornado.escape.xhtml_escape(self.request.body)
        outputReturned = hello.test(dataRecieved)
        self.write(json.dumps(outputReturned))


#Handler for SPO2
class analyzeSPO2Data(BaseHandler):
    def post(self):
        dataRecieved = tornado.escape.xhtml_escape(self.request.body)
        outputReturned = hello.test(dataRecieved)
        self.write(json.dumps(outputReturned))

#Handler for IHR
class analyzeIHRData(BaseHandler):
    def post(self):
        dataRecieved = tornado.escape.xhtml_escape(self.request.body)
        file_path = self.request.body
        AHIValue = SF.sendFile(file_path)
        self.write(json.dumps(AHIValue))

#Handler for BP
class analyzeBPData(BaseHandler):
    def post(self):
        dataRecieved = tornado.escape.xhtml_escape(self.request.body)
        outputReturned = hello.test(dataRecieved)
        self.write(json.dumps(outputReturned))



#Handler for Predict
class analyzeAHEPData(BaseHandler):
   def post(self):
       dataRecieved = tornado.escape.xhtml_escape(self.request.body)
       file_path = self.request.body
       AHEPvalue = AHP.wrapper_analyze_AHE_abp(file_path)
       self.write(json.dumps(AHEPvalue))

#Handler for classify
class analyzeAHECData(BaseHandler):
    def post(self):
        dataRecieved = tornado.escape.xhtml_escape(self.request.body)
        file_path = self.request.body
        AHECvalue = AHC.wrapper_analyze_AHE_abp(file_path)
        if AHECvalue == 'null':
            AHECvalue = 0
        else:
            AHECvalue = 1
        self.write(json.dumps(AHECvalue))


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", self.reverse_url("main")))





class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.db.execute("SELECT  mrd from patients;", callback=self.add_response)

    def add_response(self, cursor):
        results = cursor.fetchall()
        self.render("base.html", results=self.current_user)


def main():
    global memcache
    global loop
    sys.backtracelimit = 1000
    try:
        tornado.options.parse_command_line()
        http_server = HTTPServer(Application())
        http_server.bind(8888)
        http_server.start(0)  # Forks multiple sub-processes
        loop = IOLoop.instance()
        loop.run_sync(instantiate)
        loop.start()
        # autoreload.start(10)

    except KeyboardInterrupt:
        print
        'Exit'


if __name__ == '__main__':
    main()
metadata_server.py
