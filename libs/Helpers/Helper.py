class Helper:
    def __init__(self):
        self.__VERSION__ = '0.1b'

    def export_json(self, filename, data):
        print(data)
        print(f"Export Json File {self.__VERSION__}")
        f = open(filename, 'w')
        for i in data:
            f.writelines(f"{i}\n")
        f.close()

        return True