import collectors
import threads


def main():
    pingers = [threads.Pinger(collectors.FipCollector()),
               threads.Pinger(collectors.FunRadioCollector()),
               threads.Pinger(collectors.NovaCollector()),
               threads.Pinger(collectors.NrjCollector()),
               threads.Pinger(collectors.SkyrockCollector())]

    telex = threads.Telex(pingers)
    telex.start()

    while True:
        try:
            pass
        except KeyboardInterrupt:
            telex.stop()
            break

if __name__ == '__main__':
    main()