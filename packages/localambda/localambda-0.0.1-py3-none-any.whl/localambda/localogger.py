
class bcolors:
    # https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ERROR = '\033[91m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LOG_GRP_0 = '\x1b[7;37;41m'
    LOG_GRP_1 = '\x1b[0;30;43m'
    LOG_GRP_2 = '\x1b[40;30;47m'
    LOG_GRP_3 = '\x1b[6;30;46m'
    LOG_GRP_4 = '\x1b[6;37;41m'
    LOG_GRP_5 = '\x1b[0;31;47m'
    LOG_GRP_6 = '\x1b[6;30;42m'
    LOG_GRP_7 = '\x1b[6;32;47m'
    LOG_GRP_8 = '\x1b[6;32;45m'
    LOG_GRP_9 = '\x1b[0;34;45m'


class ConsoleLogCounter(object):
        _count = 0

        def get_group_id(self):
            ConsoleLogCounter._count += 1
            return ConsoleLogCounter._count


LOG_COUNTER = ConsoleLogCounter()


class LocaLogger(object):

    def __init__(self, group_name, group_id: int = None):
        self.group_name = group_name
        self.group_id = group_id or LOG_COUNTER.get_group_id()
        self.group_col = bcolors.LOG_GRP_0
        self.set_group_col()

    def set_group_col(self):
        """Retrieves the proper color for the given group ID. Colors are recycled every 10 groups."""
        grp = self.group_id % 10
        grp_col = getattr(bcolors, f'LOG_GRP_{grp}')
        self.group_col = grp_col

    @property
    def get_group_highlight(self):
        return f'{self.group_col}{self.group_name}{bcolors.ENDC}:'

    def log_info_for_group(self, msg):
        print(f"{self.get_group_highlight} {msg}")

    def log_error_msg(self, msg):
        print(f"{self.get_group_highlight} {bcolors.ERROR}ERROR: {msg}{bcolors.ENDC}")

    def log_warning_msg(self, msg):
        print(f"{self.get_group_highlight} {bcolors.ERROR}WARNING: {msg}{bcolors.ENDC}")

    def log_info_msg(self, msg):
        self.log_info_for_group(msg)

    def log_success_msg(self, msg):
        print(f"{self.get_group_highlight} {bcolors.OKGREEN}{msg}{bcolors.ENDC}")



