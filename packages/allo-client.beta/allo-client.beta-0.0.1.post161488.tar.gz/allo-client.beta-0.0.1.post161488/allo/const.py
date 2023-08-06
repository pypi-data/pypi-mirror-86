#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import platform
from uuid import getnode as get_mac

TELEPORT_SHA = "786e399511525889778d2a3e64bc5d18f7ecddf6eaac684c224249657f404b76" \
    if os.getenv("ALLOENV") == "TEST" \
    else "9dc44c571b34ab9c87240b566615e7193f497de0c8f167dcce64aeeaafda1aee"

ALLO_INFO_PATH = '/tmp/allo-infos.yml'

CONFIG_PATH = "/etc/allo-config.dict"

ALLO_URL = "10.204.22.1:3025" \
    if os.getenv("ALLOENV") == "TEST" \
    else "teleport.libriciel.fr:443"

API_PATH = "https://{}/v1/webapi".format("10.204.22.1:3080") \
    if os.getenv("ALLOENV") == "TEST" \
    else "https://{}/v1/webapi".format(ALLO_URL)

CODEPRODUIT = {
    "as@lae": "AS",
    "ComElus": "CE",
    "i-Parapheur": "IP",
    "i-delibRE": "IL",
    "Pastell": "PA",
    "webACTES": "WA",
    "web-delib": "WD",
    "web-GFC": "WG",
    "web-DPO": "DP",
}


def getnode():
    random.seed(platform.node() + str(get_mac()))
    return random.randint(1, 999999999999)
