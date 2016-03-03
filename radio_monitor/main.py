import collectors
import time
import threading


class Pinger(threading.Thread):

    def __init__(self, collector):
        super(Pinger, self).__init__()
        self.collector = collector
        self._stop = threading.Event()

    def run(self):
        current_meta = None
        while self.stopped() is False:
            meta = self.collector.get_current_metadata()

            try:
                if current_meta is None or (current_meta.title != meta.title and current_meta.artist != meta.artist):
                    current_meta = meta
                    print self.collector.RADIO_NAME
                    print meta
                    print "--------"
            except AttributeError:
                current_meta = None

            time.sleep(self.collector.crawl_frequency)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


def main():
    threads = [Pinger(collectors.FipCollector()),
               Pinger(collectors.NovaCollector()),
               Pinger(collectors.NrjCollector()),
               Pinger(collectors.FunRadioCollector()),
               Pinger(collectors.SkyrockCollector())]

    for radio_thread in threads:
        radio_thread.start()

    on = True
    while on:
        try:
            pass
        except KeyboardInterrupt:
            on = False

    for radio_thread in threads:
        radio_thread.stop()

    for radio_thread in threads:
        radio_thread.join()

if __name__ == '__main__':
    main()