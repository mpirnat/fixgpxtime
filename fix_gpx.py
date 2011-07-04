import datetime
import optparse
import re
import sys
from dateutil.relativedelta import relativedelta


timestamp_pattern = re.compile('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
time_format = '%Y-%m-%dT%H:%M:%SZ'


class TimeFixer(object):

    def __init__(self, options):
        self.options = options
        self.offset = relativedelta(hours=options.offset)

    def fix_files(self, files):
        for file in files:
            self.fix_file(file)

    def fix_file(self, file):
        data = self.read_file(file)
        data_out = self.walk_data(data)
        self.emit_data(data_out, file)

    def read_file(self, file):
        f = open(file, 'r')
        data = f.readlines()
        f.close()
        return data
    
    def walk_data(self, data):
        data_out = []
        for line in data:
            match = timestamp_pattern.search(line)
            if not match:
                data_out.append(line)
                continue
            data_out.append(self.shift_time(line, match))
        return data_out

    def shift_time(self, line, match):
        timestamp_in = match.group()
        date_in = datetime.datetime.strptime(match.group(), time_format)
        date_out = date_in + self.offset
        timestamp_out = date_out.strftime(time_format)
        line = line.replace(timestamp_in, timestamp_out)
        return line

    def emit_data(self, data, file):
        out = sys.stdout
        if self.options.overwrite:
            out = open(file, 'w')
        out.writelines(data)


def create_parser():
    usage = "usage: %prog [options] [--] HOURS FILES\n" \
            "(Use -- if passing negative HOURS)"
    parser = optparse.OptionParser(usage)
    parser.add_option("-o", "--overwrite", action="store_true",
            dest="overwrite")

    return parser


def main():
    parser = create_parser()
    (options, args) = parser.parse_args()
    try:
        options.offset = float(args[0])
    except IndexError:
        sys.stderr.write("Need an offset to shift times by!\n")
        parser.print_help()
        sys.exit(1)
    files = args[1:]
    fixer = TimeFixer(options)
    fixer.fix_files(files)


if __name__ == '__main__':
    main()
