#!/usr/bin/python
#coding=utf-8

import subprocess
import time

max_flow_num = 6
delay = 60

def getAge(age_str):
    age_index = age_str.find('idle_age')
    age_index = age_index + 9
    comma_index = age_str.find(',', age_index)
    idle_age = age_str[age_index:comma_index]
    print(idle_age)
    return idle_age

def joint(d):
    s = ""
    needed = ('nw_dst', 'nw_src', 'in_port')
    for k, v in d.items():
        if k in needed:
            s = s + k + "=" + v + ","
    return s[:len(s) - 1]

def remo(sw):
    tik = 60
    
    # print("Thread sw stared.")
    while True:
        time.sleep(1)
        tik = (tik - 1 + delay) % delay
        if tik == 0:
            remove_rules(sw)
    

def remove_rules(sw):
    ret = subprocess.check_output("sudo ovs-ofctl dump-flows %s" % sw, shell=True)
    lines = ret.split('\n')
    if len(lines) > max_flow_num:
        tables = {}

        for i in xrange(1, len(lines)):
            if lines[i] == "":
                continue
            # print("-----The %d th flow-----" % i)
            sections = lines[i].split(',')
            match = {}
            for sec in sections:
                kv = sec.split('=')
	        if len(kv) != 2:
                    continue
                match[kv[0].strip()] = kv[1].strip()
            match_str = joint(match)
            # print(match_str)
            tables[match_str] = match['idle_age']

        # print(tables)
        sorted_tables = sorted(tables.items(), key=lambda d: d[1], reverse=True)    # 大到小
        # print(sorted_tables)

        del_count = len(sorted_tables) - max_flow_num
        for k, v in sorted_tables:
            if del_count <= 0:
                break
            # print("---Flow to be removed:", k)
            logfile = "/home/ubuntu/pox/remove_flows.log"
            subprocess.check_output("sudo ovs-ofctl del-flows %s %s 2>&1 | tee %s > /dev/null" % (sw, k, logfile), shell=True)
            del_count = del_count - 1

