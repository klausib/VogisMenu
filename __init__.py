# -*- coding: utf-8 -*-


def name():
    return "Vogismenue"
def description():
    return "Zugriff auf Geodaten des Landes Vorarlberg"
def version():
    return "1.2.5"
def qgisMinimumVersion():
    return "2.0"
def authorName():
    return "N. B."
def classFactory(iface):
    from VogismenuMain import VogismenuMain
    return VogismenuMain(iface)