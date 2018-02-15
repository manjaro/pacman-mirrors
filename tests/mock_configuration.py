# http constants
URL_MIRROR_JSON = "http://repo.manjaro.org/mirrors.json"
URL_STATUS_JSON = "http://repo.manjaro.org/status.json"
# etc
CONFIG_FILE = "tests/mock/etc/pacman-mirrors.conf"
MIRROR_LIST = "tests/mock/etc/mirrorlist"
# pacman-mirrors
WORK_DIR = "tests/mock/var/"
CUSTOM_FILE = "tests/mock/var/custom-mirrors.json"
MIRROR_FILE = "tests/mock/usr/mirrors.json"
STATUS_FILE = "tests/mock/var/status.json"
# repo constants
BRANCHES = ("stable", "testing", "unstable")
X32_BRANCHES = ("x32-stable", "x32-testing", "x32-unstable")
PROTOCOLS = ("https", "http", "ftp", "ftps")
METHODS = ("rank", "random")
SSL = ("True", "False")
REPO_ARCH = "/$repo/$arch"
# special cases
O_CUST_FILE = "tests/mock/var/Custom"
TO_BE_REMOVED = "tests/mock/var/mirrors.json"
