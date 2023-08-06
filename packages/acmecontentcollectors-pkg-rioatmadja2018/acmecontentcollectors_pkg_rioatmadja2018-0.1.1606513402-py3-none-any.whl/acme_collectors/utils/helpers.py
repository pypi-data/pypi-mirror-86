#!/usr/bin/env python
import json

"""
Name: Rio Atmadja
Date: November 27, 2020 
Description: Helper utilities for ACME Collectors 
"""

def load_credentials(credential: str = "") -> bool:
    try:
        json.loads(open(credential, 'r').read())
        return True
    except:
        return False