#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from core.alert import error
from core.alert import write
from core.alert import warn
from core.alert import info
from core.alert import messages
from core.compatible import check
from core.compatible import version
from core.compatible import os_name
from core.load_modules import load_all_graphs
from config import get_config
from core.config_builder import _builder
from core._die import __die_success
from core._die import __die_failure
from core.color import finish
from core.wizard import __wizard
from core.config_builder import all_config_keys
from core.config_builder import all_profiles
from config import get_profiles

# temporary use fixed version of argparse
if os_name() == 'win32' or os_name() == 'win64':
    if version() is 2:
        from lib.argparse.v2 import argparse
    else:
        from lib.argparse.v3 import argparse
else:
    import argparse


def load_all_args(module_names, graph_names):
    # Language Options
    # import libs
    default_config = _builder(get_config(), all_config_keys())
    _all_profiles = [key for key in _builder(get_profiles(), all_profiles())]
    _all_profiles.append('all')
    language_list = [lang for lang in messages(-1, 0)]
    if "-L" in sys.argv or "--language" in sys.argv:
        try:
            index = sys.argv.index("-L") + 1
        except:
            index = sys.argv.index("--language") + 1
    else:
        index = -1
    if index is -1:
        language = "en"
    else:
        _error_flag = False
        try:
            language = sys.argv[index]
        except:
            _error_flag = True
        if _error_flag or language not in language_list:
            __die_failure("Please select one of these languages {0}".format(language_list))

    # Check if compatible
    check(language)
    finish()
    # Start Parser
    parser = argparse.ArgumentParser(prog="Nettacker", add_help=False)

    # parser = OptionParser(usage=messages(language, 1),
    #                      description=messages(language, 2),
    #                      epilog=messages(language, 3))

    # Engine Options
    engineOpt = parser.add_argument_group(messages(language, 4), messages(language, 5))
    engineOpt.add_argument("-L", "--language", action="store",
                           dest="language", default=default_config["language"],
                           help=messages(language, 6).format(language_list))
    engineOpt.add_argument("-v", "--verbose", action="store",
                           dest="verbose_level", default=default_config["verbose_level"],
                           help=messages(language, 59))
    engineOpt.add_argument("-V", "--version", action="store_true",
                           default=default_config["show_version"], dest="show_version",
                           help=messages(language, 60))
    engineOpt.add_argument("-c", "--update", action="store_true",
                           default=default_config["check_update"], dest="check_update",
                           help=messages(language, 61))
    engineOpt.add_argument("-o", "--output", action="store",
                           default=default_config["log_in_file"], dest="log_in_file",
                           help=messages(language, 11))
    engineOpt.add_argument("--graph", action="store",
                           default=default_config["graph_flag"], dest="graph_flag",
                           help=messages(language, 86).format(graph_names))
    engineOpt.add_argument("-h", "--help", action="store_true",
                           default=default_config["help_menu_flag"], dest="help_menu_flag",
                           help=messages(language, 2))
    engineOpt.add_argument("-W", "--wizard", action="store_true",
                           default=default_config["wizard_mode"], dest="wizard_mode",
                           help=messages(language, 107))
    engineOpt.add_argument('--profile', action="store",
                           default=default_config["profile"], dest='profile',
                           help=messages(language, 136).format(_all_profiles))

    # Target Options
    target = parser.add_argument_group(messages(language, 12), messages(language, 13))
    target.add_argument("-i", "--targets", action="store", dest="targets",
                        default=default_config["targets"], help=messages(language, 14))
    target.add_argument("-l", "--targets-list", action="store", dest="targets_list",
                        default=default_config["targets_list"], help=messages(language, 15))

    # Exclude Module Name
    exclude_names = module_names[:]
    exclude_names.remove('all')

    # Methods Options
    method = parser.add_argument_group("Method", messages(language, 16))
    method.add_argument("-m", "--method", action="store",
                        dest="scan_method", default=default_config["scan_method"],
                        help=messages(language, 17).format(module_names))
    method.add_argument("-x", "--exclude", action="store",
                        dest="exclude_method", default=default_config["exclude_method"],
                        help=messages(language, 18).format(exclude_names))
    method.add_argument("-u", "--usernames", action="store",
                        dest="users", default=default_config["users"],
                        help=messages(language, 19))
    method.add_argument("-U", "--users-list", action="store",
                        dest="users_list", default=default_config["users_list"],
                        help=messages(language, 20))
    method.add_argument("-p", "--passwords", action="store",
                        dest="passwds", default=default_config["passwds"],
                        help=messages(language, 21))
    method.add_argument("-P", "--passwords-list", action="store",
                        dest="passwds_list", default=default_config["passwds_list"],
                        help=messages(language, 22))
    method.add_argument("-g", "--ports", action="store",
                        dest="ports", default=default_config["ports"],
                        help=messages(language, 23))
    method.add_argument("-T", "--timeout", action="store",
                        dest="timeout_sec", default=default_config["timeout_sec"], type=float,
                        help=messages(language, 24))
    method.add_argument("-w", "--time-sleep", action="store",
                        dest="time_sleep", default=default_config["time_sleep"], type=float,
                        help=messages(language, 25))
    method.add_argument("-r", "--range", action="store_true",
                        default=default_config["check_ranges"], dest="check_ranges",
                        help=messages(language, 7))
    method.add_argument("-s", "--sub-domains", action="store_true",
                        default=default_config["check_subdomains"], dest="check_subdomains",
                        help=messages(language, 8))
    method.add_argument("-t", "--thread-connection", action="store",
                        default=default_config["thread_number"], type=int, dest="thread_number",
                        help=messages(language, 9))
    method.add_argument("-M", "--thread-hostscan", action="store",
                        default=default_config["thread_number_host"], type=int,
                        dest="thread_number_host", help=messages(language, 10))
    method.add_argument("-R", "--socks-proxy", action="store",
                        dest="socks_proxy", default=default_config["socks_proxy"],
                        help=messages(language, 62))
    method.add_argument("--retries", action="store",
                        dest="retries", type=int, default=default_config["retries"],
                        help=messages(language, 64))
    method.add_argument('--ping-before-scan', action="store_true",
                        dest='ping_flag', default=default_config["ping_flag"],
                        help=messages(language, 99))
    method.add_argument('--method-args', action="store",
                        dest="methods_args", default=default_config["methods_args"],
                        help=messages(language, 35))
    method.add_argument('--method-args-list', action='store_true',
                        dest='method_args_list', default=default_config["method_args_list"],
                        help=messages(language, 111))
    # Return Options
    return [parser, parser.parse_args(), default_config["startup_check_for_update"]]


def check_all_required(targets, targets_list, thread_number, thread_number_host,
                       log_in_file, scan_method, exclude_method, users, users_list,
                       passwds, passwds_list, timeout_sec, ports, parser, module_names,
                       language, verbose_level, show_version, check_update, socks_proxy,
                       retries, graph_flag, help_menu_flag, methods_args, method_args_list,
                       wizard_mode, profile):
    # Checking Requirements
    # import libs
    from core import compatible
    # Check Help Menu
    if help_menu_flag:
        parser.print_help()
        write('\n\n')
        write(messages(language, 3))
        __die_success()
    # Check if method args list called
    if method_args_list:
        from core.load_modules import load_all_method_args
        load_all_method_args(language)
        __die_success()
    # Check version
    if show_version:
        from core import color
        info(messages(language, 84).format(color.color('yellow'), compatible.__version__, color.color('reset'),
                                           color.color('cyan'), compatible.__code_name__, color.color('reset'),
                                           color.color('green')))
        __die_success()
    # Wizard mode
    if wizard_mode:
        (targets, thread_number, thread_number_host,
         log_in_file, scan_method, exclude_method, users,
         passwds, timeout_sec, ports, verbose_level,
         socks_proxy, retries, graph_flag) = \
            __wizard(
                targets, thread_number, thread_number_host,
                log_in_file, module_names, exclude_method, users,
                passwds, timeout_sec, ports, verbose_level,
                socks_proxy, retries, load_all_graphs(), language
            )
    # Select a Profile
    if profile is not None:
        _all_profiles = _builder(get_profiles(), all_profiles())
        if scan_method is None:
            scan_method = ''
        else:
            scan_method += ','
        if profile == 'all':
            profile = ','.join(_all_profiles)
        tmp_sm = scan_method
        for pr in profile.rsplit(','):
            try:
                for sm in _all_profiles[pr]:
                    if sm not in tmp_sm.rsplit(','):
                        tmp_sm += sm + ','
            except:
                __die_failure(messages(language, 137).format(pr))
        if tmp_sm[-1] == ',':
            tmp_sm = tmp_sm[0:-1]
        scan_method = ','.join(list(set(tmp_sm.rsplit(','))))
    # Check Socks
    if socks_proxy is not None:
        e = False
        if socks_proxy.startswith('socks://'):
            socks_flag = 5
            socks_proxy = socks_proxy.replace('socks://', '')
        elif socks_proxy.startswith('socks5://'):
            socks_flag = 5
            socks_proxy = socks_proxy.replace('socks5://', '')
        elif socks_proxy.startswith('socks4://'):
            socks_flag = 4
            socks_proxy = socks_proxy.replace('socks4://', '')
        else:
            socks_flag = 5
        if '://' in socks_proxy:
            socks_proxy = socks_proxy.rsplit('://')[1].rsplit('/')[0]
        try:
            if len(socks_proxy.rsplit(':')) < 2 or len(socks_proxy.rsplit(':')) > 3:
                e = True
            elif len(socks_proxy.rsplit(':')) is 2 and socks_proxy.rsplit(':')[1] == '':
                e = True
            elif len(socks_proxy.rsplit(':')) is 3 and socks_proxy.rsplit(':')[2] == '':
                e = True
        except:
            e = True
        if e:
            __die_failure(messages(language, 63))
        if socks_flag is 4:
            socks_proxy = 'socks4://' + socks_proxy
        if socks_flag is 5:
            socks_proxy = 'socks5://' + socks_proxy
    # Check update
    if check_update:
        from core.update import _update
        _update(compatible.__version__, compatible.__code_name__, language, socks_proxy)
        __die_success()
    # Check the target(s)
    if targets is None and targets_list is None:
        parser.print_help()
        write("\n")
        __die_failure(messages(language, 26))
    else:
        if targets is not None:
            targets = list(set(targets.rsplit(",")))
        elif targets_list is not None:
            try:
                targets = list(set(open(targets_list, "rb").read().rsplit()))
            except:
                __die_failure(messages(language, 27).format(targets_list))
    # Check thread number
    if thread_number > 101 or thread_number_host > 101:
        warn(messages(language, 28))
    # Check timeout number
    if timeout_sec is not None and timeout_sec >= 15:
        warn(messages(language, 29).format(timeout_sec))
    # Check scanning method
    if scan_method is not None and scan_method == "all":
        scan_method = module_names
        scan_method.remove("all")
    elif scan_method is not None and scan_method not in module_names:
        if "*_" in scan_method:
            scan_method = scan_method.rsplit(',')
            tmp_scan_method = scan_method[:]
            for sm in scan_method:
                if sm.startswith('*_'):
                    scan_method.remove(sm)
                    found_flag = False
                    for mn in module_names:
                        if mn.endswith('_' + sm.rsplit('*_')[1]):
                            scan_method.append(mn)
                            found_flag = True
                    if found_flag is False:
                        __die_failure(messages(language, 117).format(sm))
            scan_method = ','.join(scan_method)
        if "," in scan_method:
            scan_method = scan_method.rsplit(",")
            for sm in scan_method:
                if sm not in module_names:
                    __die_failure(messages(language, 30).format(sm))
                if sm == "all":
                    scan_method = module_names
                    scan_method.remove("all")
                    break
        else:
            __die_failure(messages(language, 31).format(scan_method))
    elif scan_method is None:
        __die_failure(messages(language, 41))
    else:
        scan_method = scan_method.rsplit()
    # Check for exluding scanning method
    if exclude_method is not None:
        exclude_method = exclude_method.rsplit(",")
        for exm in exclude_method:
            if exm in scan_method:
                if "all" == exm:
                    __die_failure(messages(language, 32))
                else:
                    scan_method.remove(exm)
                    if len(scan_method) is 0:
                        __die_failure(messages(language, 33))
            else:
                __die_failure(messages(language, 34).format(exm))
    # Check port(s)
    if type(ports) is not list and ports is not None and "-" in ports:
        ports = ports.rsplit("-")
        ports = range(int(ports[0]), int(ports[1]) + 1)
    elif type(ports) is not list and ports is not None:
        ports = ports.rsplit(",")
    # Check user list
    if users is not None:
        users = list(set(users.rsplit(",")))
    elif users_list is not None:
        try:
            users = list(set(open(users_list).read().rsplit("\n")))  # fix later
        except:
            __die_failure(messages(language, 37).format(targets_list))
    # Check password list
    if passwds is not None:
        passwds = list(set(passwds.rsplit(",")))
    if passwds_list is not None:
        try:
            passwds = list(set(open(passwds_list).read().rsplit("\n")))  # fix later
        except:
            __die_failure(messages(language, 39).format(targets_list))
    # Check output file
    try:
        tmpfile = open(log_in_file, "w")
    except:
        __die_failure(messages(language, 40).format(log_in_file))
    # Check Graph
    if graph_flag is not None:
        if graph_flag not in load_all_graphs():
            __die_failure(messages(language, 97).format(graph_flag))
        if not (log_in_file.endswith('.html') or log_in_file.endswith('.htm')):
            warn(messages(language, 87))
            graph_flag = None
    # Check Methods ARGS
    if methods_args is not None:
        new_methods_args = {}
        methods_args = methods_args.rsplit('&')
        for imethod_args in methods_args:
            if len(imethod_args.rsplit('=')) is 2:
                if imethod_args.rsplit('=')[1].startswith('read_from_file:'):
                    try:
                        read_data = list(set(open(imethod_args.rsplit('=read_from_file:')[1]).read().rsplit('\n')))
                    except:
                        __die_failure(messages(language, 36))
                    new_methods_args[imethod_args.rsplit('=')[0]] = read_data
                else:
                    new_methods_args[imethod_args.rsplit('=')[0]] = imethod_args.rsplit('=')[1].rsplit(',')
            else:
                new_methods_args[imethod_args.rsplit('=')[0]] = ""
        methods_args = new_methods_args
    # Return the values
    return [targets, targets_list, thread_number, thread_number_host,
            log_in_file, scan_method, exclude_method, users, users_list,
            passwds, passwds_list, timeout_sec, ports, parser, module_names,
            language, verbose_level, show_version, check_update, socks_proxy,
            retries, graph_flag, help_menu_flag, methods_args, method_args_list,
            wizard_mode, profile]
