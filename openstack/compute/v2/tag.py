# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import six

from keystoneauth1 import exceptions
from openstack import utils


class TagMixin(object):

    def _tag(self, method, key=None, delete=False, tags=None, session=None):
        if tags:
            for v in tags:
                if not isinstance(v, six.string_types):
                    raise ValueError("The value for %s must be "
                                     "a text string" % v)

        # If we're in a ServerDetail, we need to pop the "detail" portion
        # of the URL off and then everything else will work the same.
        pos = self.base_path.find("detail")
        if pos != -1:
            base = self.base_path[:pos]
        else:
            base = self.base_path

        if key is not None:
            url = utils.urljoin(base, self.id, "tags", key)
        else:
            url = utils.urljoin(base, self.id, "tags")

        endpoint_filter = self.get_endpoint_filter(self, session)
        endpoint_override = self.service.get_endpoint_override()
        kwargs = {"endpoint_filter": endpoint_filter,
                  "microversion": endpoint_filter.microversion,
                  "endpoint_override": endpoint_override}
        if tags:
            kwargs["json"] = {'tags': tags}
        headers = {"Accept": ""} if delete else {}

        response = method(url, headers=headers, **kwargs)

        # DELETE doesn't return a JSON body
        # PUT a special tag doesn't return a JSON body
        return response.json() if not delete and key is None else None

    def list_tags(self, session):
        """List all tags of the server

        :param session: The session to use for this request.
        :type session: :class:`~openstack.session.Session`

        :returns: A list of the requested tags. All tags are Unicode text.
        :rtype: list
        """
        result = self._tag(session.get, session=session)
        return result['tags']

    def set_tags(self, session, *tags):
        """Replace all tags of the server with the new set of tags

        :param session: The session to use for this request.
        :type session: :class:`~openstack.session.Session`
        :param args tags: A list of tags.

        :returns: A list of the tags after being updated.
        :rtype: list
        """
        if not tags:
            return list()

        result = self._tag(session.put, tags=list(tags), session=session)
        return result['tags']

    def delete_tags(self, session):
        """Delete all tags from the server

        :param session: The session to use for this request.
        :type session: :class:`~openstack.session.Session`

        :rtype: ``None``
        """
        self._tag(session.delete, delete=True, session=session)

    def has_tag(self, session, tag):
        """Checks tag existence on the server

        :param session: The session to use for this request.
        :type session: :class:`~openstack.session.Session`
        :param str tag: The tag to check.

        :returns: ``True`` if the tag existed, otherwise ``False``.
        :rtype: bool
        """
        if not tag:
            return False

        try:
            self._tag(session.get, key=tag, session=session)
            return True
        except exceptions.NotFound:
            return False

    def add_tag(self, session, tag):
        """Add a single tag to the server

        :param session: The session to use for this request.
        :type session: :class:`~openstack.session.Session`
        :param str tag: The tag to add.

        :rtype: ``None``
        """
        self._tag(session.put, key=tag, session=session)

    def delete_tag(self, session, tag):
        """Deletes a single tag from the server

        :param session: The session to use for this request.
        :type session: :class:`~openstack.session.Session`
        :param str tag: The tag to delete.

        :rtype: ``None``
        """
        self._tag(session.delete, key=tag, delete=True, session=session)
