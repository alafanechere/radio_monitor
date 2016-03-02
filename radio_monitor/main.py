import core


def main():
    fip_collector = core.FipCollector(1)
    meta = fip_collector.get_current_metadata()
    print meta

    print "------------"
    nova_collector = core.NovaCollector(1)
    meta = nova_collector.get_current_metadata()
    print meta

    print "------------"
    fun_radio_collector = core.FunRadioCollector()
    meta = fun_radio_collector.get_current_metadata()
    print meta

    print "------------"
    nrj_collector = core.NrjCollector()
    meta = nrj_collector.get_current_metadata()
    print meta

    print "------------"
    skyrock_collector = core.SkyrockCollector()
    meta = skyrock_collector.get_current_metadata()
    print meta

if __name__ == '__main__':
    main()