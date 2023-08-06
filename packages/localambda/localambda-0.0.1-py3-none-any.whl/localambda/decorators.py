import threading


# Taking some help from the community
# https://gist.github.com/awesomebytes/0483e65e0884f05fb95e314c4f2b3db8
def threadify(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper
