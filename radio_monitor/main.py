import collectors
import time
from threading import Thread


class Pinger(Thread):

    def __init__(self, collector):
        Thread.__init__(self)
        self.collector = collector

    def run(self):
        while True:
            meta = self.collector.get_current_metadata()
            print self.collector.RADIO_NAME
            print meta
            print "--------"
            time.sleep(self.collector.crawl_frequency * 60)


def main():
    fip_thread = Pinger(collectors.FipCollector())
    nova_thread = Pinger(collectors.NovaCollector())

    fip_thread.start()
    nova_thread.start()

    fip_thread.join()
    nova_thread.join()

if __name__ == '__main__':
    main()