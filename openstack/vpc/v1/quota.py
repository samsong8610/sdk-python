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


class Quota(resource.Resource):
    resource_key = 'quota'
    resources_key = 'quotas.resources'
    base_path = '/%(project_id)s/quotas'
    service = vpc_service.VPCService()

    # capabilities
    allow_get = False
    allow_update = False
    allow_delete = False
    allow_list = True

    _query_mapping = resource.QueryParameters('type')

    # Properties
    #: The resource type.
    type = resource.Body('type')
    #: The number of created network resources.
    used = resource.Body('used')
    #: The maximum quota values for the resources.
    quota = resource.Body('quota')
    #: The minimum quota value allowed.
    min = resource.Body('min')
