# -*- coding: utf-8 -*-
import pytest
from radio_monitor import core


def test_answer():
    fip_collector = core.FipCollector(1)
    current_metadata = fip_collector.get_current_metadata()
    assert current_metadata is not None