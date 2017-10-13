import sqlite3 as sqlite
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Headers", "Content-Type,origin,accept,authorization,")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write({"Data": "Hello World CORS"})


class TestSQLite(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite.connect('testDB.db')
        c = conn.cursor()
        try:
            c.execute('SELECT * FROM User')
            result = c.fetchall()
            returnresult = dict(Result=result)
        except Exception as e:
            print e

        conn.close()
        return self.write(json.dumps(returnresult))

class UserHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.connection = sqlite.connect('testDB.db')
        self.cursor = self.connection.cursor()


    def get(self, *args, **kwargs):
        self.cursor.execute('SELECT * FROM User')
        rows = self.cursor.fetchall()
        result = dict(Result=rows)
        #return self.write(json.dumps(result))
        return self.write(result)

    def post(self, *args, **kwargs):
        self.cursor.execute("INSERT INTO User(Name,Email,Description) "
                            "VALUES ('Tom','user44@gg.com','Hello Jerry');")
        lid = self.cursor.lastrowid
        print "The last Id of the inserted row is %d" % lid
        self.connection.commit()
        self.cursor.execute('SELECT * FROM User')
        rows = self.cursor.fetchall()
        self.connection.close()
        result = dict(Result=rows)
        return self.write(json.dumps(result))
        #return True

    def delete(self, *args, **kwargs):
        user_id = kwargs['Id']

        if user_id is not None:
            self.cursor.execute("DELETE FROM User "
                                "WHERE Id = {idf}".format(idf=user_id))
            self.connection.commit()
            self.cursor.execute('SELECT * FROM User')
            rows = self.cursor.fetchall()
            self.connection.close()
            result = dict(Result=rows)
            return self.write(json.dumps(result))

    def put(self, *args, **kwargs):
        try:
            self.cursor.execute("UPDATE User SET Description='GOGOGO' WHERE Id=4")
            self.connection.commit()
            self.cursor.execute('SELECT * FROM User')
            rows = self.cursor.fetchall()

        except Exception, e:
            return self.write(str(e))

        self.connection.close()
        result = dict(Result=rows)
        return self.write(json.dumps(result))


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/test", TestSQLite),
        (r"/user", UserHandler),
        (r"/user/(?P<Id>[[0-9]+)", UserHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    print "Start Tornado server at Port:"+str(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
    