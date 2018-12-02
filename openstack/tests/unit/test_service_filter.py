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
#      Huawei has modified this source file.
#            Copyright 2018 Huawei Technologies Co., Ltd.
#            Licensed under the Apache License, Version 2.0 (the "License"); you may not
#            use this file except in compliance with the License. You may obtain a copy of
#            the License at
#
#                http://www.apache.org/licenses/LICENSE-2.0
#
#            Unless required by applicable law or agreed to in writing, software
#            distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#            WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#            License for the specific language governing permissions and limitations under
#            the License.

import fixtures
import testtools

from openstack.identity import identity_service
from openstack import service_filter


class TestValidVersion(testtools.TestCase):
    def test_constructor(self):
        sot = service_filter.ValidVersion('v1.0', 'v1')
        self.assertEqual('v1.0', sot.module)
        self.assertEqual('v1', sot.path)


class TestServiceFilter(testtools.TestCase):
    def test_init(self):
        sot = service_filter.ServiceFilter(
            'ServiceType', region='REGION1', service_name='ServiceName',
            version='1', api_version='1.23', requires_project_id=True,
            microversion='1.18', min_version='1.1', max_version='1.23')
        self.assertEqual('servicetype', sot.service_type)
        self.assertEqual('REGION1', sot.region)
        self.assertEqual('ServiceName', sot.service_name)
        self.assertEqual('1', sot.version)
        self.assertEqual('1.23', sot.api_version)
        self.assertTrue(sot.requires_project_id)
        self.assertEqual('1.18', sot.microversion)
        self.assertEqual('1.1', sot.min_version)
        self.assertEqual('1.23', sot.max_version)

    def test_get_module(self):
        sot = identity_service.IdentityService()
        self.assertEqual('openstack.identity.v3', sot.get_module())
        self.assertEqual('identity', sot.get_service_module())

    def test_setter(self):
        sot = service_filter.ServiceFilter('compute')
        sot.interface = service_filter.ServiceFilter.INTERNAL
        sot.region = 'new-region1'
        sot.service_name = 'new-service-name'
        sot.version = '2'
        sot.api_version = '2.3'
        sot.requires_project_id = False
        sot.microversion = '2.2'
        sot.min_version = '2.1'
        sot.max_version = '2.26'
        self.assertEqual(service_filter.ServiceFilter.INTERNAL, sot.interface)
        self.assertEqual('new-region1', sot.region)
        self.assertEqual('new-service-name', sot.service_name)
        self.assertEqual('2', sot.version)
        self.assertEqual('2.3', sot.api_version)
        self.assertFalse(sot.requires_project_id)
        self.assertEqual('2.2', sot.microversion)
        self.assertEqual('2.1', sot.min_version)
        self.assertEqual('2.26', sot.max_version)

    def test_get_endpoint_override(self):
        sot = service_filter.ServiceFilter('compute')
        self.useFixture(fixtures.EnvironmentVariable(
            'OS_COMPUTE_ENDPOINT_OVERRIDE', 'url'))
        endpoint_override = sot.get_endpoint_override()
        self.assertEqual('url', endpoint_override)
