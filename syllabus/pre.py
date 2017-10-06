"""
Pre-process a syllabus (class schedule) file. 

"""
import arrow   # Dates and times
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

base = arrow.now()   # Default, replaced if file has 'begin: ...'


def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None
    # dictionary
    entry = {}
    # sequence
    cooked = []
    # raw is a file
    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()
        # skip all comments and blank lines
        if len(line) == 0 or line[0] == "#":
            log.debug("Skipping")
            continue
        # split non blank lines
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2:
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) +
                             "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                base = arrow.get(content, "MM/DD/YYYY")
                base_start_date = base.floor('week')
                print("Base date {}".format(base.isoformat()))
                #print("Base date start date {}".format(base_start_date))
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = {}
            #week_start_date = base.shift(weeks=+(int(content) - 1)).isoweekday() 
            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = content
            interval = int(content) - 1
            #entry['date'] = base.shift(weeks=+interval).span('week')[0].format('YYYY-MM-DD')
            day = base_start_date.shift(weeks=+interval)
            entry['date'] = day 
            #first_day_of_current_week = current_span[0]
            #if (first_day_of_current_week == base.shift(weeks=+interval).span('week')[0]):
            #    entry['isCurrent'] = 1 
            #else:
            #    entry['isCurrent'] = 0
            if ((arrow.now() > day) & (arrow.now() < day.shift(weeks=+1))):
                entry['isCurrent'] = 1
            else:
                entry['isCurrent'] = 0

        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry:
        cooked.append(entry)

    return cooked






def main():
    f = open("data/schedule.txt")
    parsed = process(f)
    print(parsed)


if __name__ == "__main__":
    main()
