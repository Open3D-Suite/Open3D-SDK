# SPDX-License-Identifier: GPL-3.0-or-later
"""Where OpenExample keeps its files, and in which language it speaks, from what every Open3D app shares
(open3d_settings).

Its settings go to %APPDATA%\\Open3D\\OpenExample and everything else it writes (logs, caches) to
%LOCALAPPDATA%\\Open3D\\OpenExample, or to OpenExample inside the folders that OPEN3D_SETTINGS_DIR and
OPEN3D_DATA_DIR name. Nothing here creates them: the code that first writes into one does.
"""

from . import APP, open3d_settings

# The words describe() uses, in each language every Open3D app can be shown in.
_WORDS = {
    "en": {
        "language": "Language",
        "name": "English",
        "settings": "Settings",
        "data": "Other files",
        "none": "no folder",
    },
    "es": {
        "language": "Idioma",
        "name": "español",
        "settings": "Ajustes",
        "data": "Otros archivos",
        "none": "ninguna carpeta",
    },
}


def settings_dir():
    """%APPDATA%\\Open3D\\OpenExample, or OpenExample in the folder OPEN3D_SETTINGS_DIR names; None without
    either variable."""
    return open3d_settings.app_settings_dir(APP)


def data_dir():
    """%LOCALAPPDATA%\\Open3D\\OpenExample, or OpenExample in the folder OPEN3D_DATA_DIR names; None without
    either variable."""
    return open3d_settings.app_data_dir(APP)


def language():
    """The language to show, "en" or "es": the shared preference, or the language of Windows without one."""
    return open3d_settings.language(open3d_settings.settings_dir())


def describe(language, settings, data, separator="\n"):
    """The language and the two folders, in that language, one after the other."""
    words = _WORDS[language]

    def shown(folder):
        return str(folder) if folder is not None else f"({words['none']})"

    return separator.join(
        (
            f"{words['language']}: {words['name']}",
            f"{words['settings']}: {shown(settings)}",
            f"{words['data']}: {shown(data)}",
        )
    )
