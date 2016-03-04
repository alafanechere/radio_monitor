import log
import logging
import time
import threading


class Pinger(threading.Thread):

    def __init__(self, collector):
        super(Pinger, self).__init__()
        self.collector = collector
        self.current_meta = None
        self.new_meta = False
        self.daemon = True
        self.stop = False

    def run(self):
        while self.stop is False:
            meta = self.collector.get_current_metadata()

            try:
                if self.current_meta is None or (self.current_meta.title != meta.title
                                                 and self.current_meta.artist != meta.artist):
                    self.current_meta = meta
                    if self.current_meta is not None:
                        self.new_meta = True
                    else:
                        self.new_meta = False

            except AttributeError:
                self.current_meta = None
                self.new_meta = False

            time.sleep(self.collector.crawl_frequency)


class Telex(threading.Thread):

    telex_logger = log.setup_telex_logger('telex')
    logger = logging.getLogger('telex')

    def __init__(self, pingers_to_monitor):
        super(Telex, self).__init__()
        self.pingers = pingers_to_monitor
        self.daemon = True
        self.stop = False

    def run(self):

        for pinger in self.pingers:
            pinger.start()

        time.sleep(2)

        self.check_new_track()

        while self.stop is False:
            time.sleep(1)
            self.check_new_track()

        for pinger in self.pingers:
            pinger.stop = True

    def check_new_track(self):
        for pinger in self.pingers:
            if pinger.new_meta:
                self.logger.info(unicode(pinger.current_meta))
                pinger.new_meta = False
