import os
from printlog import printlog

class ReadData:

    def __init__(self, dPrm):
        self.dPrm = dPrm
        self.file = open(dPrm['datafile'], 'rb')


    def newline(self):
        if os.name == 'nt':
            return b"\r\n"
        else:
            return b"\n"

    def get_last_data(self):
        last_line = self.last_line(ignore_ending_newline=True).decode('utf-8')
        d = last_line.split(";")
        d.pop(0)
        return " ".join(d)

    def last_line(self, block_size=80, ignore_ending_newline=False, newline=False):
        if not newline:
            newline = self.newline()
        in_file = self.file
        suffix = b""
        in_file.seek(0, os.SEEK_END)
        in_file_length = in_file.tell()
        seek_offset = 0

        while(-seek_offset < in_file_length):
            # Read from end.
            seek_offset -= block_size
            if -seek_offset > in_file_length:
                # Limit if we ran out of file (can't seek backward from start).
                block_size -= -seek_offset - in_file_length
                if block_size == 0:
                    break
                seek_offset = -in_file_length
            in_file.seek(seek_offset, os.SEEK_END)
            buf = in_file.read(block_size)

            # Search for line end.
            if ignore_ending_newline and seek_offset == -block_size and buf[-len(newline):] == newline:
                buf = buf[:-len(newline)]
            pos = buf.rfind(newline)
            if pos != -1:
                # Found line end.
                return buf[pos+len(newline):] + suffix

            suffix = buf + suffix

        # One-line file.
        return suffix