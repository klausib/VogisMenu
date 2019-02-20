# -*- coding: utf-8 -*-





from __future__ import absolute_import
def name():

    return "Vogismenue"

def description():

    return "Zugriff auf Geodaten des Landes Vorarlberg"

def version():

    return "1.4.0"

def qgisMinimumVersion():

    return "3.0"

def authorName():

    return "Nikolaus Batlogg LVG"

def classFactory(iface):

    from .VogismenuMain import VogismenuMain

    return VogismenuMain(iface)

