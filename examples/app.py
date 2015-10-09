import time

from paxos.app.store import Store


class MyApp(object):
    def __init__(self):
        self.store = Store()
        self.store.items = []
        self.store.item_count = 0
        self.store.name_map = {}

def main():
    app = MyApp()

    for a in ["Mickey Mouse", "Donald Duck", "Shrek Donkey"]:
        app.store.items.append(a)
        app.store.item_count += 1
        app.store.name_map[a.split()[0]] = a.split()[1]

    for i in app.store.name_map:
        print(i)
    app.store.items.remove("Donald Duck")
    app.store.item_count -= 1

    print("ITEM COUNT {0}".format(app.store.item_count))
    print("ITEMS[0] = {0}".format(app.store.items[0]))


if __name__ == "__main__":
    main()
