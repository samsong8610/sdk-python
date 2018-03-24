# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
import testtools

from keystoneauth1 import exceptions
from openstack.compute.v2 import server

IDENTIFIER = 'IDENTIFIER'


class TestTag(testtools.TestCase):

    def setUp(self):
        super(TestTag, self).setUp()
        self.tags_result = {"tags": ["baz", "foo", "qux"]}

    def test_list_tags_from_server(self):
        sot = server.Server(id=IDENTIFIER)
        self._test_list_tags(sot)

    def test_list_tags_from_server_detail(self):
        sot = server.ServerDetail(id=IDENTIFIER)
        self._test_list_tags(sot)

    def _test_list_tags(self, sot):
        response = mock.Mock()
        response.json.return_value = self.tags_result
        sess = mock.Mock()
        sess.get.return_value = response
        sess.get_service.return_value = sot.service

        result = sot.list_tags(sess)

        self.assertEqual(self.tags_result['tags'], result)
        sess.get.assert_called_once_with("servers/IDENTIFIER/tags",
                                         headers={},
                                         endpoint_filter=sot.service,
                                         endpoint_override=None,
                                         microversion=None)

    def test_set_tags(self):
        response = mock.Mock()
        response.json.return_value = self.tags_result
        sess = mock.Mock()
        sess.put.return_value = response

        sot = server.Server(id=IDENTIFIER)
        sess.get_service.return_value = sot.service
        result = sot.set_tags(sess, "baz", "foo", "qux")

        self.assertEqual(self.tags_result['tags'], result)
        sess.put.assert_called_once_with("servers/IDENTIFIER/tags",
                                         headers={},
                                         json={'tags': ["baz", "foo", "qux"]},
                                         endpoint_filter=sot.service,
                                         endpoint_override=None,
                                         microversion=None)

    def test_delete_tags(self):
        sess = mock.Mock()
        sot = server.Server(id=IDENTIFIER)
        sess.get_service.return_value = sot.service
        result = sot.delete_tags(sess)

        self.assertIsNone(result)
        sess.delete.assert_called_once_with("servers/IDENTIFIER/tags",
                                            headers={"Accept": ""},
                                            endpoint_filter=sot.service,
                                            endpoint_override=None,
                                            microversion=None)

    def test_add_tag(self):
        response = mock.Mock()
        response.code = 201
        sess = mock.Mock()
        sess.put.return_value = response

        sot = server.Server(id=IDENTIFIER)
        tag = 'new_tag'
        sess.get_service.return_value = sot.service
        result = sot.add_tag(sess, tag)

        self.assertIsNone(result)
        sess.put.assert_called_once_with("servers/IDENTIFIER/tags/" + tag,
                                         headers={},
                                         endpoint_filter=sot.service,
                                         endpoint_override=None,
                                         microversion=None)
        response.json.assert_not_called()

    def test_has_tag(self):
        response = mock.Mock()
        response.code = 204
        sess = mock.Mock()
        sess.put.return_value = response

        sot = server.Server(id=IDENTIFIER)
        tag = 'tag_id'
        sess.get_service.return_value = sot.service
        result = sot.has_tag(sess, tag)

        self.assertTrue(result)
        sess.get.assert_called_once_with("servers/IDENTIFIER/tags/" + tag,
                                         headers={},
                                         endpoint_filter=sot.service,
                                         endpoint_override=None,
                                         microversion=None)
        response.json.assert_not_called()

    def test_has_tag_not_exists(self):
        sess = mock.Mock()
        sess.get.side_effect = exceptions.NotFound()

        sot = server.Server(id=IDENTIFIER)
        tag = 'not_exists'
        sess.get_service.return_value = sot.service
        result = sot.has_tag(sess, tag)

        self.assertFalse(result)
        sess.get.assert_called_once_with("servers/IDENTIFIER/tags/" + tag,
                                         headers={},
                                         endpoint_filter=sot.service,
                                         endpoint_override=None,
                                         microversion=None)

    def test_delete_tag(self):
        sess = mock.Mock()

        sot = server.Server(id=IDENTIFIER)
        tag = 'tag_id'
        sess.get_service.return_value = sot.service
        result = sot.delete_tag(sess, tag)

        self.assertIsNone(result)
        sess.delete.assert_called_once_with("servers/IDENTIFIER/tags/" + tag,
                                            headers={"Accept": ""},
                                            endpoint_filter=sot.service,
                                            endpoint_override=None,
                                            microversion=None)
