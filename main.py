import asyncio

import gbulb

from gi.repository import Gtk


class AdminWindow(Gtk.Window):

    def __init__(self):
        super().__init__(self, title="Manipulateuw")
        self.set_border_width(10)

        # setting up grid on which to position elements
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # setting up userlist
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)

        # setting up buttons
        self.buttons = {"ban": Gtk.Button("Banniw"),
                        "slowban": Gtk.Button("Slowbanniw"),
                        "trash": Gtk.Button("Cancèw"),
                        "shadowban": Gtk.Button("Fantomutèw")}
        self.grid.attach_next_to(self.buttons["ban"], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.buttons["slowban"], self.buttons["ban"], Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.buttons["trash"], self.buttons["slowban"], Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.buttons["shadowban"], self.buttons["trash"], Gtk.PositionType.RIGHT, 1, 1)
        handlers_mapping = {"ban": self.ban_handler,
                            "slowban": self.slowban_handler,
                            "trash": self.trash_handler,
                            "shadowban": self.shadowban_handler}
        for key, button in self.buttons.items():
            button.connect("clicked", handlers_mapping[key])

        self.show_all()

    def get_currently_selected(self):
        """Return the user_id of the user currently being selected"""
        pass

    def ban_handler(self, widget):
        """Called on ban button press"""
        pass

    def slowban_handler(self, widget):
        """Called on slowban button press"""
        pass

    def trash_handler(self, widget):
        """Called on trash button press"""
        pass

    def shadowban_handler(self, widget):
        """Called on shadowban button press"""
        pass



@asyncio.coroutine
def counter(label):
    i = 0
    while True:
        label.set_text(str(i))
        yield from asyncio.sleep(1)
        i += 1


@asyncio.coroutine
def text_watcher(label):
    while True:
        yield from gbulb.wait_signal(label, 'changed')
        print('label changed', label.get_text())


def main():
    gbulb.install(gtk=True)
    loop = gbulb.get_event_loop()

    display = Gtk.Entry()
    vbox = Gtk.VBox()

    vbox.pack_start(display, True, True, 0)

    win = Gtk.Window(title='Counter window')
    win.connect('delete-event', lambda *args: loop.stop())
    win.add(vbox)

    win.show_all()

    asyncio.ensure_future(text_watcher(display))
    asyncio.ensure_future(counter(display))
    loop.run_forever()

if __name__ == '__main__':
    main()
