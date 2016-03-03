import collectors
import time
import threading


class Pinger(threading.Thread):

    def __init__(self, collector):
        super(Pinger, self).__init__()
        self.collector = collector
        self.current_meta = None
        self._stop = threading.Event()

    def run(self):
        while self.stopped() is False:
            meta = self.collector.get_current_metadata()

            try:
                if self.current_meta is None or (self.current_meta.title != meta.title
                                                 and self.current_meta.artist != meta.artist):
                    self.current_meta = meta
            except AttributeError:
                self.current_meta = None

            time.sleep(self.collector.crawl_frequency)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

def main():
    threads = {"FIP": Pinger(collectors.FipCollector()),
               "Nova": Pinger(collectors.NovaCollector()),
               "NRJ": Pinger(collectors.NrjCollector()),
               "Fun Radio": Pinger(collectors.FunRadioCollector()),
               "Skyrock": Pinger(collectors.SkyrockCollector())}

    for _, radio_thread in threads.iteritems():
        radio_thread.start()

    time.sleep(2)

    current_metas = {}

    for radio, pinger in threads.iteritems():
        current_metas[radio] = pinger.current_meta

    for radio, meta in current_metas.iteritems():
        print radio
        print meta

    on = True
    while on:
        try:
            time.sleep(1)
            for radio, meta in current_metas.iteritems():
                if meta != threads[radio].current_meta:
                    current_metas[radio] = threads[radio].current_meta
                    print current_metas[radio]
                    print "\n\n"
        except KeyboardInterrupt:
            on = False

    for _, thread in threads.iteritems():
        thread.stop()

    for _, thread in threads.iteritems():
        thread.join()

if __name__ == '__main__':
    main()