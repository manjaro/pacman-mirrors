
install:
	install -D -m 0755 bin/pacman-mirrors $(DESTDIR)/usr/bin/pacman-mirrors
	install -D -m 0755 lib/pacman-mirrors/pacman_mirrors_gui.py $(DESTDIR)/usr/lib/pacman-mirrors/pacman_mirrors_gui.py
	install -D -m 0644 data/pacman-mirrors.conf $(DESTDIR)/etc/pacman-mirrors.conf
	mkdir -p $(DESTDIR)/etc/pacman.d/mirrors
	install -D -m 0644 data/mirrors/* $(DESTDIR)/etc/pacman.d/mirrors/
