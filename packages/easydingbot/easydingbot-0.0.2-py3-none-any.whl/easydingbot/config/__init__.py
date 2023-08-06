# MIT License

# Copyright (c) 2020 Seniverse

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
from getpass import getpass


class ConfigNotFound(Exception):
    pass


def add_dingbot(dingbot_id=None, webhook=None, secret=None):
    home = os.path.expanduser('~')
    configfp = os.path.join(home, '.easydingbot')
    if os.path.exists(configfp):
        with open(configfp) as f:
            config_dict = json.load(f)
        if 'default' in config_dict:
            should_input_dingbot_id = True
        else:
            should_input_dingbot_id = False
    else:
        config_dict = {}
        should_input_dingbot_id = False
    
    if should_input_dingbot_id:
        dingbot_id = input('Please input the dingbot id ("default" if empty, "q" to quit) > ')
        if dingbot_id.lower() == 'q':
            exit()  
        if not dingbot_id:
            dingbot_id = 'default'
    else:
        dingbot_id = 'default'

    if not webhook:
        webhook = getpass('Please input the webhook string ("q" to quit)> ')
        if webhook.lower() == 'q':
            exit()  
    if not secret:
        secret = getpass('Please input the secret string ("q" to quit)> ')
        if secret.lower() == 'q':
            exit() 

    config_dict[dingbot_id] = {
        'webhook': webhook,
        'secret': secret
    }

    with open(configfp, 'w') as f:
        json.dump(config_dict, f)
        

def list_dingbots():
    home = os.path.expanduser('~')
    configfp = os.path.join(home, '.easydingbot')
    with open(configfp) as f:
        config_dict = json.load(f)

    amount = len(config_dict)
    if amount > 0:
        print(f'There are {len(config_dict)} dingbots in config as follow:')
        for k in sorted(config_dict.keys()):
            print(f'  * {k}')
    else:
        print(f'There are no dingbot in config, please use "easydingbot-add-dingbot" command to add one')
        
        
def remove_dingbot():
    home = os.path.expanduser('~')
    configfp = os.path.join(home, '.easydingbot')
    list_dingbots()

    with open(configfp) as f:
        config_dict = json.load(f)

    if len(config_dict) > 0:
        dingbot_id = input('Please choose one of above to remove ("q" to quit)> ')
        if dingbot_id.lower() == 'q':
            exit()
        if dingbot_id in config_dict:
            config_dict.pop(dingbot_id)
            with open(configfp, 'w') as f:
                json.dump(config_dict, f)
            print(f'{dingbot_id} removed from config')
        else:
            raise ConfigNotFound(f'The {dingbot_id} is not in config')


home = os.path.expanduser('~')
configfp = os.path.join(home, '.easydingbot')
if not os.path.exists(configfp):
    add_dingbot()
    with open(configfp) as f:
        configs = json.load(f)
else:
    with open(configfp) as f:
        configs = json.load(f)
