# -*- coding: utf-8 -*-
import datetime
import pytest
from radio_monitor import core


def test_metadata_parsing():
    fip_collector = core.FipCollector(1)
    current_metadata = fip_collector.get_current_metadata()

    assert isinstance(current_metadata.title, unicode)
    assert isinstance(current_metadata.artist, unicode)
    assert isinstance(current_metadata.broadcaster, str)
    assert isinstance(current_metadata.broadcast_time, datetime.datetime)

