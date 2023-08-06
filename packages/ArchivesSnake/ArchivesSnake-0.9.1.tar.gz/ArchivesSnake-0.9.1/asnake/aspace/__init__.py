from asnake.client import ASnakeClient
import asnake.jsonmodel as jm
from asnake.jsonmodel import *
from collections.abc import Sequence
from itertools import chain
from boltons.setutils import IndexedSet
import json
import re

class ASnakeBadReturnCode: pass
class ASpace():
    # this happens when you call ASpace()
    def __init__(self, **config):
        # Connect to ASpace using .archivessnake.yml
        self.client = ASnakeClient(**config)
        self.client.authorize()
        m = re.match(r'\(v?(.+\))', self.client.get('version').text)
        if m:
            self.version = m[1]
        else:
            self.version = 'unknown version'

    def __getattr__(self, attr):
        '''returns the JSONModelRelation representing the route with the same name as the attribute requested.'''
        if not attr.startswith('_'):
            return JSONModelRelation("/{}".format(attr), params={"all_ids": True}, client = self.client)

    @property
    def resources(self):
        '''return all resources from every repo.'''
        return ResourceRelation({}, self.client)


    @property
    def agents(self):
        '''returns an AgentRelation.'''
        return AgentRelation("/agents", {}, self.client)

    @property
    def users(self):
        '''returns a UserRelation.'''
        return UserRelation("/users", {}, self.client)

    def by_external_id(self, external_id, record_types=None):
        '''return any resources fetched from the 'by-external-id' route.

Note: while the route will return differently depending on how many records are returned,
this method deliberately flattens that out - it will _always_ return a generator, even if only
one record is found.'''
        params = {"eid": external_id}
        if record_types: params['type[]'] = record_types

        res = self.client.get('by-external-id', params=params)
        if res.status_code == 404:
            return []
        elif res.status_code == 300: # multiple returns, bare list of uris
            yield from (wrap_json_object({"ref": uri}, self.client) for uri in IndexedSet(res.json()))
        elif res.status_code == 200: # single obj, redirects to obj with 303->200
            yield wrap_json_object(res.json(), self.client)
        else:
            raise ASnakeBadReturnCode("by-external-id call returned '{}'".format(res.status_code))

    def from_uri(self, uri):
        '''returns a JSONModelObject representing the URI passed in'''
        return wrap_json_object(self.client.get(uri).json(), self.client)
