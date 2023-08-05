#!/usr/bin/env python
# -*- coding: utf-8 -*-

# std lib
import json
import os
from time import sleep
import logging

# 3rd party
import requests

# consts
USERS_URL_BASE = "https://{org}.cvpartner.com/api/v1/users?offset={offset}"
CV_URL_BASE = "https://{org}.cvpartner.com/api/v3/cvs/{user_id}/{cv_id}"

# logger
log = logging.getLogger(__name__)


class CVPartner():

    def __init__(self, org, api_key):
        self.auth_header = {"Authorization": f'Token token="{api_key}"'}
        self.org = org

    def _get_users_by_offset(self, offset):
        log.debug(f'{offset} - Retreiving data from API...')
        users_url = USERS_URL_BASE.format(org=self.org, offset=offset)
        r = requests.get(users_url, headers=self.auth_header)
        return r.json()

    def get_users_from_api(self):
        offset = 0
        users = self._get_users_by_offset(offset)
        while len(users) > 0:
            offset += len(users)
            yield from users
            sleep(1)
            users = _get_user_by_offset(offset)

    def get_user_cv(self, user_id, cv_id):
        log.debug(f'Retreiving user {user_id} CV {cv_id} from API...')
        cv_url = CV_URL_BASE.format(org=self.org, user_id=user_id, cv_id=cv_id)
        r = requests.get(cv_url, headers=self.auth_header)
        return r.json()


def main():
    cvp = CVPartner(org='ciber', api_key=os.environ['CVPARTNER_API_KEY'])

    for u in cvp.get_users_from_api():
        if u['name'] != 'Anders L. Hurum':
            continue
        #print(u.keys())
        user_id = u['user_id']
        cv_id = u['default_cv_id']
        user_cv = cvp.get_user_cv(user_id, cv_id)
        #print(user_cv)
        print(f'Got user {user_id}:{cv_id} - {u["name"]}')
        print(f'{user_cv.keys()}')
        print('--------------------------------------')
        for k,v in u.items():
            print(f'{k} :: {str(v)[:500]}')

        print('--------------------------------------')
        for k,v in user_cv.items():
            print(k)
            #print(v)

        with open('user.ndjson', 'w') as f:
            f.write(json.dumps(user_cv))

        break


if __name__ == '__main__':
    main()
