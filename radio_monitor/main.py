import collectors
import threads


def main():
    pingers = {"FIP": threads.Pinger(collectors.FipCollector()),
               "FunRadio": threads.Pinger(collectors.FunRadioCollector()),
               "Nova": threads.Pinger(collectors.NovaCollector()),
               "NRJ": threads.Pinger(collectors.NrjCollector()),
               "Skyrock": threads.Pinger(collectors.SkyrockCollector())}

    telex = threads.Telex(pingers)
    telex.start()
    while True:
        try:
            pass
        except KeyboardInterrupt:
            telex.stop()

if __name__ == '__main__':
    main()