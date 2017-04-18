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
REPO_ARCH = "/$repo/$arch"
# special cases
O_CUST_FILE = "tests/mock/var/Custom"
TO_BE_REMOVED = "tests/mock/var/mirrors.json"

test_conf = {
    "to_be_removed": TO_BE_REMOVED,
    "branch": "stable",
    "branches": BRANCHES,
    "config_file": CONFIG_FILE,
    "custom_file": CUSTOM_FILE,
    "method": "rank",
    "work_dir": WORK_DIR,
    "mirror_file": MIRROR_FILE,
    "mirror_list": MIRROR_LIST,
    "no_update": False,
    "only_country": [],
    "protocols": [],
    "repo_arch": REPO_ARCH,
    "status_file": STATUS_FILE,
    "ssl_verify": True,
    "url_mirrors_json": URL_MIRROR_JSON,
    "url_status_json": URL_STATUS_JSON
}
