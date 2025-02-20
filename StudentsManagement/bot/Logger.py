from jdatetime import datetime


class Logger:
    def __init__(self, fname):
        self.fname = fname
        open(fname, "w").close()

    def __call__(self, *args, **kwargs):
        log = f"[{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}] : {args[0]}\n"
        with open(self.fname, "a", encoding="utf-8") as file_object:
            print(log, end='')
            file_object.write(log)


