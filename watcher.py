from __future__ import print_function
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
#from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector


cnx = mysql.connector.connect(user='root', password='Kundjanasith@hpcnc801', database='gpu')
cursor = cnx.cursor()

g1_command = ("INSERT INTO gpu1_utilization (ts, gpu_util) VALUES (%s, %s)")
g2_command = ("INSERT INTO gpu2_utilization (ts, gpu_util) VALUES (%s, %s)")

class Watcher:
    DIRECTORY_TO_WATCH = "./"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            #print "Error"

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            #print "Received created event - %s." % event.src_path
            print("a")
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            #print "Received modified event - %s." % event.src_path
            line = subprocess.check_output(['tail', '-2', 'data.csv'])
            #print(line)
            #l = line.split('\n')[1]
            g1 = line.split('\n')[0]
            g2 = line.split('\n')[1]
            print(g1)
            current_t = g1.split(', ')[0]
            print(current_t)
            gpu1_util = g1.split(', ')[8].split(' %')[0]
            print(gpu1_util)
            ymd = current_t.split(' ')[0]
            y = ymd.split('/')[0]
            m = ymd.split('/')[1]
            d = ymd.split('/')[2]
            hms = current_t.split(' ')[1]
            h = hms.split(':')[0]
            m = hms.split(':')[1]
            s = hms.split(':')[2]
            datetime_object = datetime.strptime(current_t.split('.')[0], '%Y/%m/%d %H:%M:%S')
            #current_t = datetime.utcnow().date()
            #print(current_t)
            cursor.execute(g1_command, (datetime_object,float(gpu1_util)))
            cnx.commit()
            #print(gpu1_util)
       

if __name__ == '__main__':
    w = Watcher()
    w.run()
