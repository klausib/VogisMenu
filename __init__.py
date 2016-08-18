# -*- coding: utf-8 -*-


def name():
    return "Vogismenue"
def description():
    return "Zugriff auf Geodaten des Landes Vorarlberg"
def version():
    return "1.2.7"
def qgisMinimumVersion():
    return "2.0"
def authorName():
    return "Nikolaus Batlogg LVG"
def classFactory(iface):
    from VogismenuMain import VogismenuMain
    return VogismenuMain(iface)
