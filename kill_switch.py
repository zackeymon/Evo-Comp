import _thread


class KillSwitch:
    """"
    A class to implement a kill switch for loops.
    """
    _list = []

    @staticmethod
    def input_thread(list_):
        input()
        list_.append(None)

    @classmethod
    def setup(cls):
        _thread.start_new_thread(cls.input_thread, (cls._list,))

    @classmethod
    def is_off(cls):
        return not cls._list
