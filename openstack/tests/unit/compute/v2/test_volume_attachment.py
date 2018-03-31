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

import testtools

from openstack.compute.v2 import volume_attachment

EXAMPLE = {
    'device': '/dev/sdc',
    'id': 'a26887c6-c47b-4654-abb5-dfadf7d3f803',
    'serverId': '4d8c3732-a248-40ed-bebc-539a6ffd25c0',
    'volumeId': 'a26887c6-c47b-4654-abb5-dfadf7d3f803',
}


class TestVolumeAttachment(testtools.TestCase):

    def test_basic(self):
        sot = volume_attachment.VolumeAttachment()
        self.assertEqual('volumeAttachment', sot.resource_key)
        self.assertEqual('volumeAttachments', sot.resources_key)
        self.assertEqual('/servers/%(server_id)s/os-volume_attachments',
                         sot.base_path)
        self.assertEqual('compute', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)
        self.assertDictEqual({"limit": "limit",
                              "offset": "offset",
                              "marker": "marker"},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = volume_attachment.VolumeAttachment(**EXAMPLE)
        self.assertEqual(EXAMPLE['device'], sot.device)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['serverId'], sot.server_id)
        self.assertEqual(EXAMPLE['volumeId'], sot.volume_id)
