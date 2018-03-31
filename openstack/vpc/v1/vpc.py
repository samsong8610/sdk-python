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

from openstack import resource2 as resource
from openstack.vpc import vpc_service


class VPC(resource.Resource):
    resource_key = 'vpc'
    resources_key = 'vpcs'
    base_path = '/%(project_id)s/vpcs'
    service = vpc_service.VPCService()

    # capabilities
    allow_create = True
    allow_get = True
    allow_update = True
    allow_delete = True
    allow_list = True

    #: The range of available subnets in the VPC.
    cidr = resource.Body('cidr')
    #: The status of the VPC. The value can be CREATING, OK, DOWN,
    # PENDING_UPDATE, PENDING_DELETE, or ERROR.
    status = resource.Body('status')
    #: The routing rules of the VPC.
    routes = resource.Body('routes')
