#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os, re
from datetime import datetime
from fabric.api import *

env.hosts =['139.224.235.140',]
env.user='root'
env.password='hubang1994.'

def pre_deploy():
    lcd('..')
    local('git add .')

def host_type():
    run('pwd')