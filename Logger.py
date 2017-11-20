
#from Worker import Worker

class Logger(object):
    
    log = open("/home/lex/devel/i3statusbar/status1.log", 'w')  
#    worker = Worker()

    @staticmethod
    def logMessage(message):
        Logger._writeMessage(message)
        #Logger.worker.addJob(Logger._writeMessage, message)

    @staticmethod
    def _writeMessage(message):
        Logger.log.write(message + "\n")
        Logger.log.flush()

