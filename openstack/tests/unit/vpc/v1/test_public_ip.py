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

from openstack.vpc.v1 import public_ip

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'id': IDENTIFIER,
    'status': 'ACTIVE',
    'type': '5_bgp',
    "public_ip_address": "161.17.101.12",
    "tenant_id": "8b7e35ad379141fc9df3e178bd64f55c",
    "private_ip_address": "192.168.10.5",
    "create_time": "2015-07-16 04:32:50",
    "port_id": "f588ccfa-8750-4d7c-bf5d-2ede24414706",
    "bandwidth_id": "49c8825b-bed9-46ff-9416-704b96d876a2",
    "bandwidth_share_type": "PER",
    "bandwidth_size": 10,
    "bandwidth_name": "bandwidth-test"
}


class TestPublicIP(testtools.TestCase):

    def test_basic(self):
        sot = public_ip.PublicIP()
        self.assertEqual('publicip', sot.resource_key)
        self.assertEqual('publicips', sot.resources_key)
        self.assertEqual('/%(project_id)s/publicips', sot.base_path)
        self.assertEqual('network', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)
        self.assertDictEqual({'limit': 'limit', 'marker': 'marker'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = public_ip.PublicIP(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['public_ip_address'],
                         sot.public_ip_address)
        self.assertEqual(EXAMPLE['public_ip_address'], sot.name)
        self.assertEqual(EXAMPLE['private_ip_address'], sot.private_ip_address)
        self.assertEqual(EXAMPLE['port_id'], sot.port_id)
        self.assertEqual(EXAMPLE['tenant_id'], sot.project_id)
        self.assertEqual(EXAMPLE['create_time'], sot.create_time)
        self.assertEqual(EXAMPLE['bandwidth_id'], sot.bandwidth_id)
        self.assertEqual(EXAMPLE['bandwidth_name'], sot.bandwidth_name)
        self.assertEqual(EXAMPLE['bandwidth_share_type'],
                         sot.bandwidth_share_type)
        self.assertEqual(EXAMPLE['bandwidth_size'], sot.bandwidth_size)

    def test_create(self):
        response = mock.Mock()
        response.json.return_value = {'publicip': EXAMPLE}
        response.headers = {}
        sess = mock.Mock()
        sess.post.return_value = response
        sess.get_project_id.return_value = 'uuid'

        sot = public_ip.PublicIP(type='5_sbgp',
                                 ip_address='192.168.0.2',
                                 bandwidth_name='my-bd',
                                 bandwidth_size=1,
                                 bandwidth_share_type='PER',
                                 bandwidth_charge_mode='bandwidth')
        sot.create(sess)

        uri = sot.base_path % {'project_id': 'uuid'}
        expected_body = {
            'publicip': {
                'type': '5_sbgp',
                'ip_address': '192.168.0.2'
            },
            'bandwidth': {
                'name': 'my-bd',
                'size': 1,
                'share_type': 'PER',
                'charge_mode': 'bandwidth'
            }
        }
        sess.post.assert_called_once_with(
            uri,
            endpoint_filter=sot.service,
            endpoint_override=sot.service.get_endpoint_override(),
            json=expected_body,
            headers={}
        )
