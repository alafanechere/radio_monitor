import collectors


def main():
    fip_collector = collectors.FipCollector(1)
    meta = fip_collector.get_current_metadata()
    print meta

    print "------------"
    nova_collector = collectors.NovaCollector(1)
    meta = nova_collector.get_current_metadata()
    print meta

    print "------------"
    fun_radio_collector = collectors.FunRadioCollector()
    meta = fun_radio_collector.get_current_metadata()
    print meta

    print "------------"
    nrj_collector = collectors.NrjCollector()
    meta = nrj_collector.get_current_metadata()
    print meta

    print "------------"
    skyrock_collector = collectors.SkyrockCollector()
    meta = skyrock_collector.get_current_metadata()
    print meta

if __name__ == '__main__':
    main()