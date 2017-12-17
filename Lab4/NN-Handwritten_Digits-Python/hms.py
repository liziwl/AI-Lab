# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 20:28:35 2016
PythonVersion: 2.7.12
@author: Siyuan Wang

a small tool to convert seconds into hours, minutes and seconds
"""
def hms(t):
    hr = int(t/3600)
    rest = t%3600
    mi = int(rest/60)
    rest = rest%60
    s = rest%60
    return hr, mi, s
