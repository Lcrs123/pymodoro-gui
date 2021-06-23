import importlib.resources as resource


def get_resource_path(fileinfo:tuple) -> str:
  with resource.path(*fileinfo) as filepath:
    return str(filepath.resolve())


BEEP_FILEINFO: tuple = (str(__name__), 'beep.wav')
ICON_FILEINFO: tuple = (str(__name__), 'icon.png')
BEEP_PATH = get_resource_path(BEEP_FILEINFO)
ICON_PATH = get_resource_path(ICON_FILEINFO)

