# -*- coding: utf-8 -*-
import datetime
from radio_monitor import collectors, threads
import time


def test_metadata_fip():
    fip_collector = collectors.FipCollector()
    current_metadata = fip_collector.get_current_metadata()

    assert isinstance(current_metadata.title, unicode)
    assert isinstance(current_metadata.artist, unicode)
    assert isinstance(current_metadata.album, unicode)
    assert isinstance(current_metadata.label, unicode)
    assert isinstance(current_metadata.year, int)
    assert isinstance(current_metadata.broadcaster, str)
    assert isinstance(current_metadata.broadcast_time, datetime.datetime)


def test_metadata_nova():
    nova_collector = collectors.NovaCollector()
    current_metadata = nova_collector.get_current_metadata()
    if current_metadata is not None:
        assert isinstance(current_metadata.title, unicode)
        assert isinstance(current_metadata.artist, unicode)
        assert current_metadata.album is None
        assert current_metadata.label is None
        assert current_metadata.year is None
        assert isinstance(current_metadata.broadcaster, str)
        assert isinstance(current_metadata.broadcast_time, datetime.datetime)


def test_metadata_fun():
    fun_collector = collectors.FunRadioCollector()
    current_metadata = fun_collector.get_current_metadata()

    assert isinstance(current_metadata.title, unicode)
    assert isinstance(current_metadata.artist, unicode)
    assert current_metadata.album is None
    assert current_metadata.label is None
    assert current_metadata.year is None
    assert isinstance(current_metadata.broadcaster, str)
    assert isinstance(current_metadata.broadcast_time, datetime.datetime)


def test_metadata_nrj():
    nrj_collector = collectors.NrjCollector()
    current_metadata = nrj_collector.get_current_metadata()

    if current_metadata is not None:
        assert isinstance(current_metadata.title, unicode)
        assert isinstance(current_metadata.artist, unicode)
        assert current_metadata.album is None
        assert current_metadata.label is None
        assert current_metadata.year is None
        assert isinstance(current_metadata.broadcaster, str)
        assert isinstance(current_metadata.broadcast_time, datetime.datetime)


def test_metadata_skyrock():
    skyrock_collector = collectors.SkyrockCollector()
    current_metadata = skyrock_collector.get_current_metadata()

    if current_metadata is not None:
        assert isinstance(current_metadata.title, unicode)
        assert isinstance(current_metadata.artist, unicode)
        assert current_metadata.album is None
        assert current_metadata.label is None
        assert current_metadata.year is None
        assert isinstance(current_metadata.broadcaster, str)
        assert isinstance(current_metadata.broadcast_time, datetime.datetime)


def test_pinger():
    fip_collector = collectors.FipCollector()
    fip_pinger = threads.Pinger(fip_collector)
    fip_pinger.start()
    assert fip_pinger.stopped() is False
    time.sleep(5)
    assert fip_pinger.current_meta is not None
    fip_pinger.stop()
    time.sleep(5)
    assert fip_pinger.stopped() is True
    fip_pinger.join()


def test_telex():
    pingers = {"FIP": collectors.FipCollector(),
               "Fun Radio": collectors.FunRadioCollector(),
               "Nova": collectors.NovaCollector(),
               "NRJ": collectors.NrjCollector(),
               "Skyrock": collectors.SkyrockCollector()}

    telex = threads.Telex(pingers)

    telex.start()
    assert telex.stopped() is False
    time.sleep(5)
    telex.stop()
    assert telex.stopped() is True
    telex.join()
