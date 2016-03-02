import core


def main():
    fip_collector = core.FipCollector(1)
    meta = fip_collector.get_current_metadata()
    print meta

if __name__ == '__main__':
    main()