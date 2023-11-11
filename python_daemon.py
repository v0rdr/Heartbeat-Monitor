#!/usr/bin/python3

import datetime
import time
import traceback
from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
            args=command,
            stdout=PIPE,
            shell=True,
            universal_newlines=True
        )
    return process.communicate()[0]

debug = True
while True:
    try:
        print('Reading logs ...')
        the_time = datetime.datetime.now()
        ip = ''
        log_entry = ''
        fast_log = cmdline('cat /var/log/suricata/fast.log')
        fast_log = fast_log.split('\n')
        for i in fast_log:
            if "CUSTOM" in i:
                ip = i.split('-> ')[1].split(':')[0]
                check_ip = cmdline('iptables -nL -t raw')
                if ip not in check_ip:
                    cmdline('iptables -t raw -A PREROUTING -s %s -j DROP'%ip)
                    log_entry = str(the_time) + ' BLOCKED %s\n '%ip
                    
                    print(log_entry)
                    f = open('/var/log/blocks.log','a')
                    f.write(log_entry)
                    f.close()
        print('sleeping ...')
        time.sleep(60)
    except:
        if debug:
            print(traceback.format_exc())
        error_time = datetime.datetime.now()
        g = open('/var/log/python_daemon_error.log','a')
