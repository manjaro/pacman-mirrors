# http constants
URL_MIRROR_JSON = "http://repo.manjaro.org/mirrors.json"
URL_STATUS_JSON = "http://repo.manjaro.org/status.json"
# etc
CONFIG_FILE = "tests/mock/etc/pacman-mirrors.conf"
MIRROR_LIST = "tests/mock/etc/mirrorlist"
# pacman-mirrors
MIRROR_DIR = "tests/mock/var/"
CUSTOM_FILE = MIRROR_DIR + "custom-mirrors.json"
MIRROR_FILE = MIRROR_DIR + "mirrors.json"
STATUS_FILE = MIRROR_DIR + "status.json"
# special cases
O_CUST_FILE = MIRROR_DIR + "Custom"
FALLBACK = "tests/mock/usr/mirrors.json"
# repo constants
BRANCHES = ("stable", "testing", "unstable")
REPO_ARCH = "/$repo/$arch"
