
install:
	install -D -m 0755 bin/pacman-mirrors $(DESTDIR)/usr/bin/pacman-mirrors
	install -D -m 0644 data/pacman-mirrors.conf $(DESTDIR)/etc/pacman-mirrors.conf
