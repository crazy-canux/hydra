#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copyright (C) 2015 Faurecia (China) Holding Co.,Ltd.

All rights reserved.
Name: wmi_sh.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0.0
Time: Mon 08 Aug 2016 04:43:40 PM CST

Description:
    [1.0.0.0] 20160728 init for basic function.
"""
import csv
import subprocess

from sh import wmic

from monitor import Monitor


class Wmi(Monitor):

    """Basic class for wmi."""

    def __init__(self, *args, **kwargs):
        super(Wmi, self).__init__(*args, **kwargs)
        self.logger.debug("Init Wmi")

    def query(self, wql):
        """Connect by wmi and run wql."""
        try:
            self.__wql = ['-U',
                          self.args.domain + '\\' + self.args.user + '%' + self.args.password,
                          '//' + self.args.host,
                          '--namespace', self.args.namespace,
                          '--delimiter', self.args.delimiter,
                          wql]
            self.logger.debug("wql: {}".format(self.__wql))
            self.__output = wmic(self.__wql)
            self.logger.debug("output: {}".format(self.__output))
            self.logger.debug("wmi connect succeed.")
            self.__wmi_output = self.__output.splitlines()[1:]
            self.logger.debug("wmi_output: {}".format(self.__wmi_output))
            self.__csv_header = csv.DictReader(self.__wmi_output, delimiter='|')
            self.logger.debug("csv_header: {}".format(self.__csv_header))
            return list(self.__csv_header)
        except subprocess.CalledProcessError as e:
            self.unknown("Connect by wmi and run wql error: %s" % e)

    def define_sub_options(self):
        super(Wmi, self).define_sub_options()
        self.wmi_parser = self.parser.add_argument_group("WMI Options",
                                                         "options for WMI connect.")
        self.subparsers = self.parser.add_subparsers(title="WMI Action",
                                                     description="Action mode for WMI.",
                                                     help="Specify your action for WMI.")
        self.wmi_parser.add_argument('-d', '--domain',
                                     required=False,
                                     help='wmi server domain.',
                                     dest='domain')
        self.wmi_parser.add_argument('--namespace',
                                     default='root\cimv2',
                                     required=False,
                                     help='namespace for wmi, default is %(default)s',
                                     dest='namespace')
        self.wmi_parser.add_argument('--delimiter',
                                     default='|',
                                     required=False,
                                     help='delimiter for wmi, default is %(default)s',
                                     dest='delimiter')