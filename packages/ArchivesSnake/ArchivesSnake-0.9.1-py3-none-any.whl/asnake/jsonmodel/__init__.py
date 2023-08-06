from itertools import chain
from more_itertools import flatten
from copy import deepcopy
from collections.abc import Sequence

import json
import re
from asnake.logging import get_logger

component_signifiers = frozenset({"archival_object", "archival_objects"})
jmtype_signifiers = frozenset({"ref", "jsonmodel_type"})
searchdoc_signifiers = frozenset({"primary_type", "types", "id", "json"})
node_signifiers = frozenset({"node_type", "resource_uri"})
node_data_signifiers = frozenset({"child_count", "waypoints", "waypoint_size"})
solr_route_regexes = [
    re.compile(r'/?repositories/\d+/top_containers/search/?')
]

def dispatch_type(obj):
    '''Determines if object is JSON suitable for wrapping with a JSONModelObject, or a narrower subtype.
Returns either the correct class or False if no class is suitable.

Note: IN GENERAL, it is safe to use this to test if a thing is a JSONModel subtype, but you should
STRONGLY prefer :func:`wrap_json_object` for constructing objects, because some objects are wrapped,
and would need to be manually unwrapped otherwise.  So, usage like this:

.. code-block:: python

    jmtype = dispatch_type(obj, self.client)
    if jmtype:
        return wrap_json_object(obj, self.client)

is fine and expected, but the following is dangerous:

.. code-block:: python

    jmtype = dispatch_type(obj, self.client)
    if jmtype:
        return jmtype(obj, self.client)

because it will break on wrapped or otherwise odd objects.'''

    value = False
    if isinstance(obj, dict):
        # Handle wrapped objects returned by searches
        if searchdoc_signifiers.issubset(set(obj)):
            obj = json.loads(obj['json'])

        ref_type = [x for x in obj['ref'].split("/") if not x.isdigit()][-1] if 'ref' in obj else None
        if obj.get("jsonmodel_type", ref_type) in component_signifiers:
            if node_data_signifiers.issubset(set(obj)):
                return TreeNodeData
            else:
                value = ComponentObject
        elif node_signifiers.intersection(obj.keys()) or ref_type == "tree":
            value = TreeNode
        elif jmtype_signifiers.intersection(obj.keys()):
            value = JSONModelObject

    return value

def wrap_json_object(obj, client=None):
    '''Classify object, and either wrap it in the correct JSONModel type or return it as is.

Prefer this STRONGLY to directly using the output of :func:`dispatch_type`'''
    if isinstance(obj, dict):
        # Handle wrapped objects returned by searches
        if searchdoc_signifiers.issubset(set(obj)):
            obj = json.loads(obj['json'])


    jmtype = dispatch_type(obj)
    if jmtype:
        obj = jmtype(obj, client)
    return obj

def find_subtree(tree, uri):
    '''Navigates a tree object to get a list of children of a specified archival object uri.'''
    subtree = None
    for child in tree['children']:
        if child["record_uri"] == uri:
            subtree = child
            break # subtree found, all done!
        else:
            if not child['has_children']:
                continue # this is a leaf, do not recurse
            subtree = find_subtree(child, uri) # recurse!
            if subtree: break
    return subtree


# Base metaclass for shared functionality
class JSONModel(type):
    '''Mixin providing functionality shared by JSONModel and JSONModelRelation classes.'''

    def __init__(cls, name, parents, dct):
        cls.__default_client = None

    def default_client(cls):
        '''return existing ASnakeClient or create, store, and return a new ASnakeClient'''
        if not cls.__default_client:
            from asnake.client import ASnakeClient
            cls.__default_client = ASnakeClient()
        return cls.__default_client

# Classes dealing with JSONModel imports
class JSONModelObject(metaclass=JSONModel):
    '''A wrapper over the JSONModel representation of a single object in ArchivesSpace.'''

    def __init__(self, json_rep, client = None):
        self._json = json_rep
        self._client = client or type(self).default_client()
        self.is_ref = 'ref' in json_rep

    def reify(self):
        '''Convert object from a ref into a realized object.'''
        if self.is_ref:
            if '_resolved' in self._json:
                self._json = self._json['_resolved']
            else:
                self._json = self._client.get(self._json['ref']).json()
            self.is_ref = False
        return self

    @property
    def id(self):
        '''Return the id for the object if it has a useful ID, or else None.

Note: unlike uri, an id is Not fully unique within some collections returnable
by API methods.  For example, searches can return different types of objects, and
agents have unique ids per agent_type, not across all agents.'''
        candidate = self._json.get('uri', self._json.get('ref', None))
        if candidate:
            val = candidate.split('/')[-1]
            if val.isdigit(): return(int(val))

    def __dir__(self):
        self.reify()
        return sorted(chain(self._json.keys(),
                    (x for x in self.__dict__.keys() if not x.startswith("_{}__".format(type(self).__name__)))))

    def __repr__(self):
        result = "#<{}".format(self._json['jsonmodel_type'] if not self.is_ref else "ref" )

        if 'uri' in self._json:
            result += ':' + self._json['uri']
        elif self.is_ref:
            result += ':' + self._json['ref']
        elif 'resource_uri' in self._json:
            result += ':' + self._json['resource_uri']
        return result + '>'


    def __getattr__(self, key):
        '''Access to properties on the JSONModel object and objects from  descendant API routes.

attr lookup for JSONModel object is provided from the following sources:

    - objects, lists of objects, and native values present in the wrapped JSON
    - API methods matching the object's URI + the attribute requested

If neither is present, the method raises an AttributeError.'''
        if key not in self._json and self.is_ref:
            if key == 'uri': return self._json['ref']
            self.reify()

        if not key.startswith('_') and not key == 'is_ref':
            if (not key in self._json.keys()) and 'uri' in self._json:
                uri = "/".join((self._json['uri'].rstrip("/"), key,))
                # Existence of route isn't enough, need to discriminate by type
                # example: .../resources/:id/ordered_records which ALSO ought to be maybe treated as plural?
                # This works, at the cost of a "wasted" full call if not a JSONModelObject
                resp = self._client.get(uri, params={"all_ids":True})
                if resp.status_code == 404:
                    raise AttributeError("'{}' has no attribute or route named '{}'".format(repr(self), key))
                else:
                    jmtype = dispatch_type(resp.json())
                    if (jmtype):
                        return wrap_json_object(resp.json(), client=self._client)
                    if any(r.match(uri) for r in solr_route_regexes):
                        return SolrRelation(uri, client=self._client)
                    return JSONModelRelation(uri, client=self._client)


            if isinstance(self._json[key], list) and len(self._json[key]) > 0:
                jmtype = dispatch_type(self._json[key][0])
                if len(self._json[key]) == 0 or jmtype:
                    return [wrap_json_object(obj, self._client) for obj in self._json[key]]
                else:
                    # bare lists of Not Jsonmodel Stuff, ding dang note contents and suchlike
                    return self._json[key]
            elif dispatch_type(self._json[key]):
                return wrap_json_object(self._json[key], self._client)
            else:
                return self._json[key]
        else: return self.__getattribute__(key)

    def __str__(self):
        return json.dumps(self._json, indent=2)

    def __bytes__(self):
        return str(self).encode('utf8')

    def json(self):
        '''return safe-to-edit copy wrapped dict representing JSONModelObject contents.'''
        self.reify()
        return deepcopy(self._json)

class ComponentObject(JSONModelObject):
    '''Specialized JSONModel subclass representing Archival Objects. Mostly exists to provide a way to get TreeNodes from AOs rather than having to start at the resource.'''
    @property
    def tree(self):
        '''Returns a TreeNode object for children of archival objects'''

        try:
            tree_object = find_subtree(self.resource.tree.json(), self.uri)
        except:
            raise AttributeError("'{}' has no attribute '{}'".format(repr(self), "tree"))
        return wrap_json_object(tree_object, self._client)

class TreeNode(JSONModelObject):
    '''Specialized JSONModel subclass representing nodes in trees, as returned
from `/repositories/:repo_id/resources/:id/tree <https://archivesspace.github.io/archivesspace/api/#get-a-resource-tree>`_.'''

    def __repr__(self):
        result = "#<TreeNode:{}".format(self._json['node_type'])
        if "resource_uri" in self._json:
            result += ":" + self._json['resource_uri']
        elif "identifier" in self._json:
            result += ":" + self._json['identifier']
        return result + ">"

    @property
    def record(self):
        '''returns the full JSONModelObject for a node'''
        resp = self._client.get(self.record_uri)
        return wrap_json_object(resp.json(), self._client)

    @property
    def walk(self):
        '''Serial walk of all objects in tree and children (depth-first traversal)'''
        yield self.record
        yield from flatten(child.walk for child in self.children)

    def node(self, node_uri):
        '''A sub-route existing on resources, which returns info on the node passed in.

Returned as an instance of :class:`TreeNodeData`.'''

        self.reify()
        if self._json['node_type'] != 'resource':
            raise NotImplementedError('This route only exists on resources')
        else:
            resp = self._client.get("/".join((self._json['record_uri'], 'tree/node',)), params={"node_uri": node_uri})
            return wrap_json_object(resp.json(), self._client)

class TreeNodeData(JSONModelObject):
    '''Object representing data about a node in a tree.'''
    def __repr__(self):
        return "#<TreeNodeData:{}:{}>".format(self._json['jsonmodel_type'], self._json['uri'])

    def __getattr__(self, key):
        if key not in self._json:
            raise AttributeError("Property not present in tree data - it may exist on the record instead")
        else:
            return self._json[key]

    @property
    def record(self):
        resp = self._client.get(self.uri)
        return wrap_json_object(resp.json(), self._client)

class JSONModelRelation(metaclass=JSONModel):
    '''A wrapper over index routes and other routes that represent groups of items in ASpace.

It provides two means of accessing objects in these collections:

    - you can iterate over the relation to get all objects
    - you can call the relation as a function with an id to get an object with a known id

e.g.

.. code-block:: python

    for repo in ASpace().repositories:
        # do stuff with repo here

    ASpace.repositories(12) # object at uri /repositories/12

This object wraps the route and parameters, and does no caching - each iteration through a relation fetches data from ASpace fresh.

Additionally, JSONModelRelations implement `__getattr__`, in order to handle nested and subsidiary routes, such as the routes for individual types of agents.'''

    def __init__(self, uri, params = {}, client = None):
        self.uri = uri
        self.client = client or type(self).default_client()
        self.params = params

    def __repr__(self):
        return "#<JSONModelRelation:{}:{}>".format(self.uri, self.params)

    def __iter__(self):
        for jm in self.client.get_paged(self.uri, params=self.params):
            yield wrap_json_object(jm, self.client)

    def __call__(self, myid=None, **params):
        '''Fetch a JSONModelObject from the relation by id.'''
        # Special handling for resolve because it takes a string or an array and requires [] for array
        if 'resolve' in params:
            params['resolve[]'] = params['resolve']
            del params['resolve']
        if myid:
            resp = self.client.get("/".join((self.uri.rstrip("/"), str(myid),)), params=params)
            jmtype = dispatch_type(resp.json())
            if (jmtype):
                return wrap_json_object(resp.json(), client=self.client)
            return resp.json()
        else:
            return self.with_params(**params)


    def with_params(self, **params):
        '''Return JSONModelRelation with same uri and client, but add kwargs to params.

Usage:

.. code-block:: python

    for thing in ASpace().repositories(2).search.with_params(q="primary_type:resource"):
        # do something with the things

'''
        merged = {}

        merged.update(self.params, **params)
        return type(self)(self.uri, merged, self.client)

    def __getattr__(self, key):
        full_uri = "/".join((self.uri, key,))
        if any(r.match(full_uri) for r in solr_route_regexes):
            return SolrRelation(full_uri, params=self.params, client=self.client)
        return type(self)(full_uri, params=self.params, client=self.client)


class ResourceRelation(JSONModelRelation):
    '''subtype of JSONModelRelation for returning all resources from every repository

Usage:

.. code-block:: python

    ASpace().resources      # all resources from every repository
    ASpace().resources(42)  # resource with id=42, regardless of what repo it's in
'''
    def __init__(self, params={}, client = None):
        super().__init__(None, params, client)

    def __iter__(self):
        repo_uris = [r['uri'] for r in self.client.get('repositories').json()]
        for resource in chain(*[self.client.get_paged('{}/resources'.format(uri), params=self.params) for uri in repo_uris]):
            yield wrap_json_object(resource, self.client)

    def __call__(self, myid=None, **params):
        if 'resolve' in params:
            params['resolve[]'] = params['resolve']
            del params['resolve']
        if myid:
            repo_uris = [r['uri'] for r in self.client.get('repositories').json()]
            for uri in repo_uris:
                if myid in self.client.get(uri + '/resources', params={'all_ids': True}).json():
                    resp = self.client.get(uri + '/resources/{}'.format(myid), params=params)
                    jmtype = dispatch_type(resp.json())
                    if (jmtype):
                        return wrap_json_object(resp.json(), client=self.client)
                    return resp.json()
            return {'error': 'Resource not found'}
        else:
            return self.with_params(**params)

    def with_params(self, **params):
        merged = {}
        merged.update(self.params, **params)
        return type(self)(self.params, self.client)

class ASNakeBadAgentType(Exception): pass

agent_types = ("corporate_entities", "people", "families", "software",)
agent_types_set = frozenset(agent_types)
class AgentRelation(JSONModelRelation):
    '''subtype of JSONModelRelation for handling the `/agents` route hierarchy.

Usage:

.. code-block:: python

    ASpace().agents                        # all agents of all types
    ASpace().agents.corporate_entities     # JSONModelRelation of corporate entities
    ASpace().agents["corporate_entities"]  # see above
    ASpace().agents["people", "families"]  # Multiple types of agents

'''

    def __iter__(self):
        for agent_type in agent_types:
            yield from JSONModelRelation("/".join((self.uri.rstrip("/"), agent_type,)),
                                         {"all_ids": True},
                                         self.client)

    def __getitem__(self, only):
        '''filter the AgentRelation to only the type or types passed in'''
        if isinstance(only, str):
            if not only in agent_types_set:
                raise ASnakeBadAgentType("'{}' is not a type of agent ASnake knows about".format(only))
            return JSONModelRelation("/".join((self.uri.rstrip("/"), only,)),
                                         {"all_ids": True},
                                         self.client)
        elif isinstance(only, Sequence) and set(only) < agent_types_set:
            return chain(*(JSONModelRelation("/".join((self.uri.rstrip("/"), agent_type,)),
                                             {"all_ids": True},
                                             self.client) for agent_type in only))
        else:
            raise ASnakeBadAgentType("'{}' is not a type resolvable to an agent type or set of agent types".format(only))

    def __repr__(self):
        return "#<AgentRelation:/agents>"

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("__call__ is not implemented on AgentRelation")

    # override parent __getattr__ because needs to return base class impl for descendant urls
    def __getattr__(self, key):
        return type(self).__bases__[0]("/".join((self.uri, key,)), params=self.params, client=self.client)

def parse_jsondoc(doc, client):
    return wrap_json_object(json.loads(doc['json']), client)

class SolrRelation(JSONModelRelation):
    '''Sometimes, the API returns solr responses, so we have to handle that. Facets are still tbd, but should be doable, but also I'm not sure if they're widely used and thus need to be handled?.'''
    def __iter__(self):
        res = self.client.get(self.uri, params=self.params).json()
        for doc in res['response']['docs']:
            yield parse_jsondoc(doc, self.client)

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("__call__ is not implemented for SolrRelations")

class UserRelation(JSONModelRelation):
    '''"Custom" relation to deal with the API's failure to properly populate permissions for the `/users` index route'''
    def __iter__(self):
        for user in self.client.get_paged('/users', params=self.params):
            yield wrap_json_object(self.client.get(user['uri']).json(), self.client)

    @property
    def current_user(self):
        '''`/users/current-user` route.'''
        return wrap_json_object(self.client.get('users/current-user', params=self.params).json(), self.client)

    # override parent __getattr__ because needs to return base class impl for descendant urls
    def __getattr__(self, key):
        p = {k:v for k, v in self.params.items()}
        if len(p) == 0:
            p['all_ids'] = True

        return type(self).__bases__[0]("/".join((self.uri, key,)), params=p, client=self.client)

class _JMeta(type):
    def __getattr__(self, key):
        def jsonmodel_wrapper(**kwargs):
            out = {"jsonmodel_type": key}
            out.update(**kwargs)
            return out

        if key.startswith('_'):
            return super().__getattr__(self, key)
        else:
            return jsonmodel_wrapper

class JM(metaclass=_JMeta):
    '''Helper class for creating hashes suitable for POSTing to ArchivesSpace.

Usage:

.. code-block:: python

    JM.resource(title="A Resource's Title", ...) == {"jsonmodel_type": "resource", "title": "A Resource's Title", ...}
    JM.agent_software(name="ArchivesSnake") == {"jsonmodel_type": "agent_software", "name": "ArchivesSnake"}

'''
    pass # all functionality is provided by _JMeta
