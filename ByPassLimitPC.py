#!/usr/bin/python
# -*- coding: utf-8 -*-
from phBot import *
import QtBind
import random
import string
from datetime import datetime
import time
import json
import os

pName = 'ByPassLimitPC'
pVersion = '1.0.0'
pUrl = 'https://www.facebook.com/profile.php?id=100011981130836'
profileName = ''

# ______________________________ Initializing ______________________________ #

commandParams = {}
bot_args = get_command_line_args()

# Graphic user interface

_x = 6
_y = 30

gui = QtBind.init(__name__, pName)
lblMultiAccounts = QtBind.createLabel(gui, 'Welcome to ' + pName + '.',
        6, 10)

cBoxUseMultiAccount = QtBind.createCheckBox(gui,
        'checked_cBoxUseMultiAccount', 'Bypass limit PC', _x, _y)
enableMultiAccount = True
QtBind.setChecked(gui, cBoxUseMultiAccount, True)

_y += 20
cBoxClientMode = QtBind.createCheckBox(gui, 'checked_cBoxClientMode',
        'Clientless mode', _x, _y)
enableClientlesMode = True
QtBind.setChecked(gui, cBoxClientMode, True)

# _y += 20
# cBoxAutoRespawn = QtBind.createCheckBox(gui, 'checked_cBoxAutoRespawn', 'Auto respawn', _x, _y)
# enableAutoRespawn = False

_y += 25
lblMac = QtBind.createLabel(gui, 'Mac', _x, _y + 3)
txtBoxMac = QtBind.createLineEdit(
    gui,
    '',
    _x + 70,
    _y,
    200,
    20,
    )

_y += 25
QtBind.createLabel(gui, 'Serial', _x, _y + 3)
txtBoxSerial = QtBind.createLineEdit(
    gui,
    '819227034',
    _x + 70,
    _y,
    200,
    20,
    )

_y += 25
QtBind.createLabel(gui, 'PC Name', _x, _y + 3)
txtBoxPCName = QtBind.createLineEdit(
    gui,
    'Administrator',
    _x + 70,
    _y,
    200,
    20,
    )

_y += 25
QtBind.createLabel(gui, 'Profile Name', _x, _y + 3)
txtBoxConfigName = QtBind.createLineEdit(
    gui,
    'Profile 1',
    _x + 70,
    _y,
    200,
    20,
    )

_y += 25
btnSaveConfig = QtBind.createButton(gui, 'btnSaveConfig_clicked',
                                    'Save config', _x, _y)


# ______________________________ Methods ______________________________ #

# Return folder path

def getPath():
    return get_config_dir() + pName + '//'


# Return character configs path (JSON)

def getConfig(name):
    if not name:
        name = pName
    return getPath() + name + '.json'


def loadDefaultConfig():
    macStr = '20-07-11-1A-08-35'.split('-')  # dia chi mac
    random.shuffle(macStr)

    macStr = '-'.join(macStr)
    QtBind.setText(gui, txtBoxMac, macStr)

    letters = string.digits
    serialStr = ''.join(random.choice(letters) for i in range(9))
    QtBind.setText(gui, txtBoxSerial, serialStr)
    QtBind.setText(gui, txtBoxPCName, 'Administrator')

    global commandParams
    if 'xAcademy' in commandParams:
        QtBind.setText(gui, txtBoxMac, '76-19-16-4B-64-12')
        QtBind.setText(gui, txtBoxSerial, '172678219')

    if 'macAddress' in commandParams:
        QtBind.setText(gui, txtBoxMac, commandParams['macAddress'])
    if 'serial' in commandParams:
        QtBind.setText(gui, txtBoxSerial, commandParams['serial'])


# Loads all config previously saved

def loadConfigs(fileName=''):
    loadDefaultConfig()
    if os.path.exists(getConfig(fileName)):
        data = {}
        with open(getConfig(fileName), 'r') as f:
            data = json.load(f)
        if 'MAC' in data:
            QtBind.setText(gui, txtBoxMac, data['MAC'])

        if 'Serial' in data:
            QtBind.setText(gui, txtBoxSerial, data['Serial'])

        if 'PC Name' in data:
            QtBind.setText(gui, txtBoxPCName, data['PC Name'])

        return True

    return False


def saveConfigs(fileName=''):
    data = {}
    data['MAC'] = QtBind.text(gui, txtBoxMac)
    data['Serial'] = QtBind.text(gui, txtBoxSerial)
    data['PC Name'] = QtBind.text(gui, txtBoxPCName)

    # Overrides

    with open(getConfig(fileName), 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))


key = bytearray()
n = random.randint(9, 20)
key.append(0)
key.append(1)
key.append(2)
key.append(3)
key.append(4)
key.append(5)


# for x in range(0, n, 1):
#     key.append(random.randint(0, 9))

def btnSaveConfig_clicked():
    strConfigName = QtBind.text(gui, txtBoxConfigName)
    saveConfigs(strConfigName)
    if strConfigName:
        log('Plugin: Profile [' + strConfigName
            + '] config has been saved')
    else:
        log('Plugin: Configs has been saved')


def checked_cBoxUseMultiAccount(checked):
    global enableMultiAccount
    enableMultiAccount = checked


def checked_cBoxClientMode(checked):
    global enableClientlesMode
    enableClientlesMode = checked


def checked_cBoxAutoRespawn(checked):
    global enableAutoRespawn
    enableAutoRespawn = checked


def parserCommand():
    global commandParams
    if bot_args:
        for i in range(len(bot_args)):
            param = bot_args[i].lower()
            if param.startswith('--'):
                if i < len(bot_args) - 1 and '--' not in bot_args[i
                        + 1]:
                    commandParams[bot_args[i].replace('--', '')] = \
                        bot_args[i + 1]
                else:
                    commandParams[bot_args[i].replace('--', '')] = ''


parserCommand()


def stringHexToBye(strData):
    strData = strData.replace(' ', '')
    packet = bytearray()
    strDataLen = len(strData)
    for i in range(0, int(strDataLen), 2):
        packet.append(int(strData[i:i + 2], 16))

    return packet


def byPassLimitPC():
    packet = bytearray()
    strData1 = \
        'FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF'
    strData1 += '20 00'

    strData2 = \
        '63 38 30 61 39 34 37 62 37 64 33 31 66 33 66 33 65 66 34 36 39 32 65 34 66 63 37 64 63 36 37 33'.split(' '
            )  # md5
    random.shuffle(strData2)
    strData2 = ' '.join(strData2)

    strData2 += '11 00'

    # strData3 = '20-07-11-1A-08-35'.split('-') # mac address
    # random.shuffle(strData3)
    # strData3 = '-'.join(strData3)

    strData3 = QtBind.text(gui, txtBoxMac)
    strData3 = ' '.join([hex(ord(x)).replace('0x', '') for x in
                        strData3])

    strData3 += '0A 00'

    # strData4 = '38 31 39 32 32 37 30 33 34' # serial

    letters = string.digits

    # strData4 = ''.join(random.choice(letters) for i in range(9))

    strData4 = QtBind.text(gui, txtBoxSerial)
    strData4 = ' '.join([hex(ord(x)).replace('0x', '') for x in
                        strData4])

    strData4 += '0A 10 00'

    # strData5 = '32 30 32 31 2D 31 30 2D 30 39 20 31 31 3A 34 31' # time

    strData5 = ' '.join([hex(ord(x)).replace('0x', '') for x in
                        datetime.now().strftime('%m-%d-%Y %H:%M')])

    strData6 = \
        'FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF'
    strData6 += '0A 00'

    # strData7 = '4E 47 55 59 45 4E 54 55 41 4E' # PC name
    # strData7 = 'Administrator'

    strData7 = QtBind.text(gui, txtBoxPCName)
    strData7 = ' '.join([hex(ord(x)).replace('0x', '') for x in
                        strData7])

    strData = strData1 + strData2 + strData3 + strData4 + strData5 \
        + strData6 + strData7
    strData = strData.replace(' ', '')
    strDataLen = len(strData)

    # Create packet data and inject it

    for i in range(0, int(strDataLen), 2):
        packet.append(int(strData[i:i + 2], 16))

    # inject it

    inject_joymax(0x1420, packet, False)


def handle_event(t, data):
    if t == 7:
        if enableAutoRespawn:
            time.sleep(0.1)
            packet = bytearray()
            packet.append(2)
            inject_joymax(0x3053, packet, False)
            log('auto respawn')


# All packets received from Silkroad will be passed to this function
# Returning True will keep the packet and False will not forward it to the game server

def handle_silkroad(opcode, data):
    if opcode == 0x1420:
        if enableMultiAccount:
            byPassLimitPC()
            log('bypass on client normal')
            return False

    return True


# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client

def handle_joymax(opcode, data):
    if opcode == 0xA100:
        if enableClientlesMode:
            byPassLimitPC()
            log('bypass on clientless')

    return True


# Plugin loaded

useDefaultConfig = True

if bot_args:
    for i in range(len(bot_args)):
        param = bot_args[i].lower()
        if param.startswith('--profile'):

            # remove command

            configName = bot_args[i + 1]
            if loadConfigs(configName):
                log('Plugin: ' + pName + ' profile [' + configName
                    + '] loaded from commandline')
                useDefaultConfig = False
            else:
                log('Plugin: ' + pName + ' profile [' + configName
                    + '] not found')

            profileName = configName

            break

if len(profileName) > 0:

    # Check configs folder

    if os.path.exists(getPath()):
        if useDefaultConfig:
            loadConfigs(profileName)
            saveConfigs(profileName)

        QtBind.setText(gui, txtBoxConfigName, profileName)
    else:
        os.makedirs(getPath())
        loadConfigs(profileName)
        saveConfigs(profileName)
        log('Plugin: "' + pName + '" folder has been created')
else:
    loadDefaultConfig()
