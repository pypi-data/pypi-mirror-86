#!/usr/bin/env python3
"""
    screenselector (c) 2020 Florian Streibelt <pypi@streibelt.net>

    This software is published under MIT License. 
    ee LICENCE for details.

    See README in the toplevel directory for more information.

    By changing the executable to be executed in your terminal
    emulator, this tool allows you to select between attached
    and detached screen sessions or start a new one, eacht time
    you open a new terminal window.

"""

import re
import sys
import os
import sys
import tty
import termios
import signal
from datetime import datetime
from subprocess import check_output, CalledProcessError


def inkey():
    ckey = None
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())

        step = 0

        while ckey is None:

            ch = sys.stdin.read(1)

            if step == 0 and ch == '\x1b':
                step += 1
                continue

            if step == 1:

                if ch == '[':
                    step += 1
                    continue

                if ch == "\x1b":
                    # at least detect two ESC :/
                    ckey = ch
                    break

            if step == 2 and  ch in ('A','B','C','D'):
                ckey = ch
                break

            if step == 0:
                # allow return
                if ch in ('\n', '\r', chr(3), ' '):
                    ckey = ch
                    break

            # unknown sequence, start over
            step = 0

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ckey


def parse(line):
    try:
        # FIXME: yes, it misses sessions with spaces in the name!
        sm = re.compile('^\s*(\S+)\s+\((\d{2}.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})\)\s+\((\S+)\)$')
        x = sm.match(line)
        if x is not None:
            sname, timespec, state =  x.groups()
            tstamp = datetime.strptime(timespec, "%d.%m.%Y %H:%M:%S")
            return(sname, tstamp, state)
        else:
            return None

    except Exception as e:
        print(e)
        print("error parsing line:")
        print(line)

    return None


def td2s(td):

    s = td.total_seconds()
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))


def showline(name, age, highlight = False, state = None, maxlen=0):

    bg = None
    fg = None

    if highlight:
        bg = 43
        if state == "Attached":
            fg = 30
            bg = 41
        elif state == "Detached":
            fg = 30
            bg = 42
        else:
            fg = 30
    else:
        if state == "Attached":
            fg = 31
        elif state == "Detached":
            fg = 32
        else:
            fg = 37

    ac = ''

    if fg is not None or bg is not None:
        ac = '\033['
    if fg is not None:
        ac += '%s' % fg
        if bg is not None:
            ac += ';'
    if bg is not None:
        ac += '%s' % bg
    if ac:
        ac += 'm'

    if state is None:
        state = ' (State)  '
    else:
        state = " %s " % state


    if age is None:
        age_s = "  (Age) "
    else:
        age_s = td2s(age)

    sys.stdout.write("\033[K")

    if highlight:
        sys.stdout.write(' > ')
    else:
        sys.stdout.write('   ')

    if ac:
        sys.stdout.write(ac)

    nl = len(name)
    if nl < maxlen:
        name += '.' * (maxlen-nl)

    sys.stdout.write(" %s   %s  %s " % (name, age_s, state))

    if fg is not None  or bg is not None:
        # need reset
        sys.stdout.write("\033[0m")

    if highlight:
        sys.stdout.write(' < ')
    else:
        sys.stdout.write('   ')

    sys.stdout.write('\n')

    sys.stdout.flush()


def getSessions():

    lc_all = os.environ.get('LC_ALL', None)
    os.environ['LC_ALL'] = 'de_DE.UTF-8' # want yyyy in dateformat, C/posix has mm/dd/yy  -.-

    try:
        output = check_output(["/usr/bin/screen", "-ls"]).decode('UTF-8')
    except  CalledProcessError as ex:
        print (ex)
        output=""

    attached = set()
    detached = set()

    maxlen = 10 #  = 1+len('start new')

    for line in output.split('\n'):
        if not line:
            continue
        if ' Socket in ' in line:
            continue
        if ' Sockets in ' in line:
            continue
        if 'There are screens' in line:
            continue

        p = parse(line)
        if p is not None:
            (sname, tstamp, state) = p
            sl = len(sname)
            if sl > maxlen:
                maxlen = sl
            if state == "Attached":
                attached.add(p)
            if state == "Detached":
                detached.add(p)

    if lc_all is not None:
        os.environ['LC_ALL'] = lc_all
    else:
        del(os.environ['LC_ALL'])

    al = sorted(list(attached), key = lambda x:x[1], reverse=True)
    dl = sorted(list(detached), key = lambda x:x[1], reverse=True)

    l = dl + al

    return l, maxlen


def main():

    l, maxlen = getSessions()

    if len(l) == 0:
        sys.stdout.flush()
        sys.stderr.flush()
        os.execlp("screen", "{myscreen}", "-S", "terminator")

    selected = 0

    first = True

    sys.stdout.write("\033[?25l")

    start_offset = 0

    def sig_winch(sig, frame):
        global maxentries
        global first
        first = True
        rows, columns = map(int, os.popen('stty size', 'r').read().split())
        maxentries = rows-15

    signal.signal(signal.SIGWINCH, sig_winch)

    rows, columns = map(int, os.popen('stty size', 'r').read().split())
    maxentries = rows-15

    while True:

        if first:
            start_offset = max(0,min(selected, len(l)-maxentries))

            sys.stdout.write("\033[H\033[2J")
            sys.stdout.write("\n\nPlease select a screen session to connect:\n\n")

        sys.stdout.write("\033[s")

        showline("start new session" , None, selected==0, maxlen=maxlen)

        for id,screen in enumerate(l):
            if id >= start_offset+maxentries:
                break
            if id >= start_offset:
                index = id + 1
                name, tstamp, state = screen
                age = datetime.now() - tstamp

                showline(name, age, selected==index, state, maxlen=maxlen)

        if first:
            first = False
            sys.stdout.write("\nuse arrow keys up/down to select:\n")
            sys.stdout.write(" LEFT will replace, RIGHT or Return will clone\n")
            sys.stdout.write("SPACE to rename a screen socket.\n")
            sys.stdout.write("Ctrl+C will abort\n")

        sys.stdout.write("\033[u")
        sys.stdout.flush()

        k = inkey()

        if k == 'A' and selected > 0:
            selected -= 1
            if start_offset > 0:
                start_offset -= 1
        if k == 'B' and selected < len(l):
            selected += 1
            if selected > (start_offset+maxentries) and start_offset < len(l)-maxentries:
                start_offset += 1


        if k in ('\r','\n', 'C', 'D'):
            break

        if k in (chr(3), '\x1b'):
            sys.stdout.write("\033[?25h")
            sys.exit(1)

        if k == ' ':
            sys.stdout.write("\033[u")  # restore position
            sys.stdout.write("\033[0J") # delete until end of screen
            old_name = l[selected-1][0]
            print("  renaming session {}:".format(old_name))
            sys.stdout.write("\033[?25h") # cursor on
            new_name = input("  enter new name: ")
            new_name = new_name.replace(' ','_')
            sys.stdout.write("\033[?25l") # cursor off
            first = True
            try:
                output = check_output(["/usr/bin/screen", "-S", old_name, '-X', 'sessionname', new_name]).decode('UTF-8')
                l, maxlen = getSessions()
            except  CalledProcessError as ex:
                output=""

            sys.stdout.write("\033[u")
            sys.stdout.write("\033[0J")

    sys.stdout.write("\033[?25h")

    sys.stdout.write("\033[H\033[2J")

    sys.stdout.flush()
    sys.stderr.flush()

    if selected == 0:
        os.execlp("screen", "{myscreen}", "-S", "terminator")
    else:
        screen = l[selected-1]
        name = screen[0]
        state = screen[2]

        if state=="Attached":
            if k == 'C':
                os.execlp("screen", "{myscreen}", "-x", name)
            if k == 'D':
                os.execlp("screen", "{myscreen}", "-d", "-r", name)

            # default:
            os.execlp("screen", "{myscreen}", "-d", "-r", name)

        else:
            os.execlp("screen", "{myscreen}", "-RR", name)


if __name__ == '__main__':
    main()
