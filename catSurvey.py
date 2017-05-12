import tornado.ioloop
import tornado.web


def resultHandler(likes, ip):
    with open("surveyResults.txt", "r") as surveyResultsFile:
        surveyResults = surveyResultsFile.read().strip().split("\n")
    with open("surveyResults.txt", "w") as surveyResultsFile:
        yes = int(surveyResults[0][4:].strip())
        no = int(surveyResults[1][3:].strip())
        if likes == "True":
            yes += 1
        if likes == "False":
            no += 1
        surveyResultsFile.write("Yes: " + str(yes) + "\n" + "No: " + str(no) + "\n")
        try:
            noPercent = no / ((no + yes) / 100.00)
        except ZeroDivisionError:
            noPercent = 0.00
            
        yesPercent = 100 - noPercent
        
        
    with open("voteLog.txt", "a") as voteLogFile:
        voteLogFile.write(ip + ": " + likes + "\n")
        
    return int(round(yesPercent)), int(round(noPercent))
    
    
class catSurveyHandler(tornado.web.RequestHandler):
    def get(self):
        self.add_header("Access-Control-Allow-Origin", "*")
        yesPercent, noPercent = resultHandler(self.get_argument("likesCats"), self.request.remote_ip)
        self.write(str(yesPercent) + "," + str(noPercent))
            


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", catSurveyHandler),
    ])
    app.listen(81)
    tornado.ioloop.IOLoop.current().start()

