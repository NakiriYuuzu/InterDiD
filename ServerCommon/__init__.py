import uuid


def unique_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return filename


def print_success(msg):
    print("\033[92m", msg, end="\033[0m \n")


def print_error(msg):
    print("\033[91m", msg, end="\033[0m \n")


def print_warning(msg):
    print("\033[93m", msg, end="\033[0m \n")


def print_info(msg):
    print("\033[94m", msg, end="\033[0m \n")


def print_debug(msg):
    print("\033[95m", msg, end="\033[0m \n")
