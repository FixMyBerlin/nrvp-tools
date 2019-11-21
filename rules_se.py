#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
def needs_layer(data, lname, experiment):
    if lname.endswith("Basis.png"):
        return True

    return False