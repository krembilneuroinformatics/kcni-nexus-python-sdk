"""
A resource represents a set of organized data represented with JSON. Hence, a resource can handle data such as numbers,
strings, arrays, boolean and complex objects made of those primitive types. In addition, Nexus adds some metadata.
Resources belong to projects and their access rights are defined at the project level.
"""

from urllib.parse import quote_plus as url_encode
from typing import Optional
import builtins

from nexussdk.utils.http import Http


class Resources:
    def __init__(self, http: Http):
        self._http = http

    def fetch(self, org_label, project_label, resource_id, schema_id="_", rev=None, tag=None, source=False):
        """
            Fetches a distant resource and returns the payload as a dictionary.
            In case of error, an exception is thrown.

            :param org_label: The label of the organization that the resource belongs to
            :param project_label: The label of the project that the resource belongs to
            :param resource_id: id of the resource
            :param schema_id: OPTIONAL id of the schema (default: "_" means whatever)
            :param rev: OPTIONAL fetches a specific revision of a resource (default: None, fetches the last)
            :param tag: OPTIONAL fetches the resource version that has a specific tag (default: None)
            :param source: OPTIONAL fetch the /source instead of the framed version (adviced when the purpose id to update a resource)
            :return: Payload of the whole resource as a dictionary
        """

        if rev is not None and tag is not None:
            raise Exception("The arguments rev and tag are mutually exclusive. One or the other must be chosen.")

        # the element composing the query URL need to be URL-encoded
        org_label = url_encode(org_label)
        project_label = url_encode(project_label)
        schema_id = url_encode(schema_id)
        resource_id = url_encode(resource_id)
        path = "/resources/" + org_label + "/" + project_label + "/" + schema_id + "/" + resource_id

        if source:
            path = path + "/source"

        if rev is not None:
            path = path + "?rev=" + str(rev)

        if tag is not None:
            path = path + "?tag=" + str(tag)

        return self._http.get(path, use_base=True)


    def update(self, resource, rev=None, resource_self=None):
        """
        Update a resource. The resource object is most likely the returned value of a
        nexus.resource.fetch(), where some fields where modified, added or removed.
        Note that the returned payload only contains the Nexus metadata and not the
        complete resource.

        :param resource: payload of a previously fetched resource, with the modification to be updated
        :param rev: OPTIONAL The previous revision you want to update from.
            If not provided, the rev from the resource argument will be used.
        :param resource_self: OPTIONAL if the resource does not contain any _self
            (because from a /source), then a self must be provided.
        :return: A payload containing only the Nexus metadata for this updated resource.
        """

        res_self_to_use = None

        if "_self" in resource:
            print("⚠️ Warning: updating a resource should be done from a source version instead of a framed version.")
            res_self_to_use = resource["_self"]

        # overload because the one given in args has priority
        if resource_self:
            res_self_to_use = resource_self

        if res_self_to_use == None:
            raise Exception("The resource_self arg or the _self property must be present.")
            return

        revision = None

        if "_rev" in resource:
            revision = resource["_rev"]

        # we give the priority to the one given in arg
        if rev:
            revision = rev

        path = res_self_to_use + "?rev=" + str(revision)

        # sanitizing the system props
        for k in builtins.list(resource): # builtins because otherwise we have a conflict with this.list
            if k.startswith("_"):
                del resource[k]

        return self._http.put(path, resource, use_base=False)


    def create(self, org_label, project_label, data, schema_id=None, resource_id=None):
        """
            Create a resource. If resource_id is provided, this given ID will be used. If resource_id not provided,
            an ID will be automatically generated for this new resource.

            :param org_label: The label of the organization that the resource belongs to
            :param project_label: The label of the project that the resource belongs to
            :param schema_id: OPTIONAL The schema to constrain the data. Can be None for non constrained data (default: "_")
            :param data: dictionary containing the data to store in this new resource
            :param resource_id: OPTIONAL force the use of a specific id when creating the new resource
            :return: A payload containing only the Nexus metadata for this updated resource.

            If the data does not have a "@context" value, a default one is automatically added.
        """

        # if no schema is provided, we can create a resource with a non-constraining
        # default schema called "_"
        if schema_id is None:
            schema_id = "_"

        # the element composing the query URL need to be URL-encoded
        org_label = url_encode(org_label)
        project_label = url_encode(project_label)
        schema_id = url_encode(schema_id)

        path = "/resources/" + org_label + "/" + project_label + "/" + schema_id

        if resource_id is None:
            return self._http.post(path, data, use_base=True)
        else:
            resource_id = url_encode(resource_id)
            path = path + "/" + resource_id
            return self._http.put(path, data, use_base=True)


    def upsert(self, org_label, project_label, data, resource_id=None, schema_id=None):
        """
            Create a resource if it doesn't exist otherwise update it. 
                        
            :param org_label: The label of the organization that the resource belongs to
            :param project_label: The label of the project that the resource belongs to
            :param schema_id: OPTIONAL The schema to constrain the data. Can be None for non constrained data (default: "_")
            :param data: dictionary containing the data to store in this new resource
            :param resource_id: OPTIONAL The ID of the resource.  It must be in param data if not passed in
            :return: A payload containing only the Nexus metadata for this updated resource.

            If the data does not have a "@context" value, a default one is automatically added.
        """

        # check that resource id is present
        if not resource_id:
            resource_id = data['@id']

            
        # first we need to try to fetch the resource to check if it already exists
        resource_list = self.list(
            org_label, 
            project_label,
            resource_id = resource_id
        )

        if resource_list['_total'] == 1:
            # need to update the file
            existing_file_self = resource_list['_results'][0]['_self']
            existing_file_revision = resource_list['_results'][0]['_rev']
        else:
            existing_file_self = None
            existing_file_revision = None


        if existing_file_self:
            # perform an update
            payload = self.update(
                resource = data,
                rev=existing_file_revision,
                resource_self=existing_file_self
            )
        else:
            # need to insert the file
            payload = self.create(
                org_label,
                project_label,
                data=data,
                schema_id=schema_id,
                resource_id=resource_id
            )
        
        return payload


    def list(self, org_label, project_label, pagination_from=0, pagination_size=20,
             deprecated=None, type=None, rev=None, schema=None, created_by=None, updated_by=None, resource_id=None):
        """
        List the resources available for a given organization and project.

        :param org_label: The label of the organization that the resource belongs to
        :param project_label: The label of the project that the resource belongs to
        :param schema: OPTIONAL Lists only the resource for a given schema (default: None)
        :param pagination_from: OPTIONAL The pagination index to start from (default: 0)
        :param pagination_size: OPTIONAL The maximum number of elements to returns at once (default: 20)
        :param deprecated: OPTIONAL Get only deprecated resource if True and get only non-deprecated results if False.
            If not specified (default), return both deprecated and not deprecated resource.
        :param type: OPTIONAL Lists only the resource for a given type (default: None)
        :param rev: OPTIONAL List only the resource with this particular revision
        :param created_by: OPTIONAL List only the resources created by a certain user
        :param updated_by: OPTIONAL List only the resources that were updated by a certain user
        :param resource_id: OPTIONAL List only the resources with this id. Relevant only when combined with other args
        :return: The raw payload as a dictionary
        """

        org_label = url_encode(org_label)
        project_label = url_encode(project_label)

        path = "/resources/" + org_label + "/" + project_label

        # if schema:
        #     schema = url_encode(schema)
        #     path = path + "/" + schema

        params = {
            "from": pagination_from,
            "size": pagination_size,
            "type": type,
            "deprecated": deprecated,
            "rev": rev,
            "schema": schema,
            "created_by": created_by,
            "updated_by": updated_by,
            "id": resource_id
        }

        return self._http.get(path, use_base=True, params=params)

    def deprecate(self, resource, rev=None):
        """
        Flag a resource as deprecated. Resources cannot be deleted in Nexus, once one is deprecated, it is no longer
        possible to update it.

        :param resource: payload of a previously fetched resource
        :param rev: OPTIONAL The previous revision you want to update from.
            If not provided, the rev from the resource argument will be used.
        :return: A payload containing only the Nexus metadata for this deprecated resource.
        """

        if rev is None:
            rev = resource["_rev"]

        path = resource["_self"] + "?rev=" + str(rev)

        return self._http.delete(path, use_base=False)

    def tag(self, resource, tag_value, rev_to_tag=None, rev=None):
        """
        Add a tag to a a specific revision of the resource. Note that a new revision (untagged) will be created

        :param resource: payload of a previously fetched resource
        :param tag_value: The value (or name) of a tag
        :param rev_to_tag: OPTIONAL Number of the revision to tag. If not provided, this will take the revision number
            from the provided resource payload.
        :param rev: OPTIONAL The previous revision you want to update from.
            If not provided, the rev from the resource argument will be used.
        :return: A payload containing only the Nexus metadata for this resource.
        """

        if rev is None:
            rev = resource["_rev"]

        if rev_to_tag is None:
            rev_to_tag = resource["_rev"]

        path = resource["_self"] + "/tags?rev=" + str(rev)

        data = {
            "tag": tag_value,
            "rev": rev_to_tag
        }

        return self._http.post(path, body=data, use_base=False)

    def tags(self, resource):
        """
        List all the tags added to this resource, along with their version numbers

        :param resource: payload of a previously fetched resource
        :return: payload containing the list of tags and versions
        """

        path = resource["_self"] + "/tags"
        return self._http.get(path, use_base=False)

    def events(self, last_id: Optional[str] = None):
        """
        Fetches resource related events.

        :param last_id: ID of the last processed event, if provided, only events after
                the event with the provided ID will be returned.
        :return: iterator of resource events
        """
        return self._http.sse_request("/resources/events", last_id)

    def project_events(self, org_label: str, project_label: str, last_id: Optional[str] = None):
        """
        Fetches resource related events for a project.

        :param org_label: organization label
        :param project_label: project label
        :param last_id: ID of the last processed event, if provided, only events after
                the event with the provided ID will be returned.
        :return: iterator of resource events for the given project
        """
        return self._http.sse_request("/resources/" + org_label + "/" + project_label + "/events", last_id)

    def org_events(self, org_label: str, last_id: Optional[str] = None):
        """
        Fetches resource related events for a organization.

        :param org_label: organization label
        :param last_id: ID of the last processed event, if provided, only events after
                the event with the provided ID will be returned.
        :return: iterator of resource events for the given organization
        """
        return self._http.sse_request("/resources/" + org_label + "/events", last_id)
