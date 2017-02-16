#!/usr/bin/env python3
"""Pacman-Mirror Mirror Functions"""

import datetime


class MirrorFn:
    """Mirror Functions"""

    @staticmethod
    def write_mirrorlist_header(handle, custom=False):
        """Write mirrorlist header
        :param handle: handle to a file opened for writing
        :param custom: controls content of the header
        """
        handle.write("##\n")
        if custom:
            handle.write("## Manjaro Linux Custom mirrorlist\n")
            handle.write("## Generated on {}\n".format(
                datetime.datetime.now().strftime("%d %B %Y %H:%M")))
            handle.write("##\n")
            handle.write("## Use 'pacman-mirrors -c all' to reset\n")
        else:
            handle.write("## Manjaro Linux mirrorlist\n")
            handle.write("## Generated on {}\n".format(
                datetime.datetime.now().strftime("%d %B %Y %H:%M")))
            handle.write("##\n")
            handle.write("## Use pacman-mirrors to modify\n")
        handle.write("##\n\n")

    @staticmethod
    def write_mirrorlist_entry(handle, mirror):
        """Write mirror to mirror list or file
        :param handle: handle to a file opened for writing
        :param mirror: mirror object
        """
        workitem = mirror
        handle.write("## Country       : {}\n".format(workitem["country"]))
        # TODO: approval to remove useless lines
        # Commented since the info after a short time
        # is no longer valid
        # if workitem["resp_time"] == txt.SERVER_RES:
        #     workitem["resp_time"] = "N/A"
        # handle.write("## Response time : {}\n".format(
        #     workitem["resp_time"]))
        # if workitem["last_sync"] == txt.SERVER_BAD or \
        #         workitem["last_sync"] == txt.LASTSYNC_NA:
        #     workitem["last_sync"] = "N/A"
        # handle.write("## Last Upd hh:mm: {}\n".format(
        #     workitem["last_sync"]))
        handle.write("Server = {}\n\n".format(workitem["url"]))
