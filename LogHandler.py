from datetime import datetime
import sys
import traceback

class LogHandler:
    def __init__(self, className):
        self.className = className
    
    def printMsg(self, message, tabStop=0):
        if not tabStop:
            print "\t" * tabStop + "* %s" % message
        elif tabStop == 1:
            print "\t" * tabStop + "# %s" % message
        elif tabStop == 2:
            print "\t" * tabStop + "- %s" % message
        elif tabStop == 3:
            print "\t" * tabStop + ". %s" % message

        sys.stdout.flush()

    # Hata ve uyarilarin loglanmasi
    def logger(self, function, message=""):
        #Dosyaya
        with open("logs/error.log", "a") as f:
            f.writelines("[%s]\n%s.%s %s\n" % (str(datetime.now())[:19], self.className, function, message))
            traceback.print_exc(file=f)
            f.writelines("\n")
        #Ekrana
        print "[%s]\n%s.%s %s\n" % (str(datetime.now())[:19], self.className, function, message),
        print traceback.format_exc()
        print "\n"
        sys.stdout.flush()

