class Metadata():

    def __init__(self, title, artist, broadcaster, broadcast_time, album=None, year=None, label=None):
        self.title = title.strip().lower()
        self.artist = artist.strip().lower()

        if album is not None:
            self.album = album.strip().lower()
        else:
            self.album = album

        if label is not None:
            self.label = label.strip().lower()
        else:
            self.label = label

        self.year = year
        self.broadcaster = broadcaster
        self.broadcast_time = broadcast_time

    def __unicode__(self):
            return "{} - {} \n" \
                   "Title: {}\n" \
                   "Artist: {}\n" \
                   "Album: {}\n" \
                   "Label: {}\n" \
                   "Year: {}\n".format(self.broadcaster,
                                       self.broadcast_time,
                                       self.title,
                                       self.artist,
                                       self.album,
                                       self.label,
                                       self.year)