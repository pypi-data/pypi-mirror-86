#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import collections

from dracclient import constants
from dracclient.resources import uris
from dracclient import utils

CPU_CHARACTERISTICS_64BIT = '4'

NIC_LINK_SPEED_MBPS = {
    '0': None,
    '1': 10,
    '2': 100,
    '3': 1000,
    '4': 2.5 * constants.UNITS_KI,
    '5': 10 * constants.UNITS_KI,
    '6': 20 * constants.UNITS_KI,
    '7': 40 * constants.UNITS_KI,
    '8': 100 * constants.UNITS_KI,
    '9': 25 * constants.UNITS_KI,
    '10': 50 * constants.UNITS_KI
}

NIC_LINK_DUPLEX = {
    '0': 'unknown',
    '1': 'full duplex',
    '2': 'half duplex'
}

NIC_MODE = {
    '0': 'unknown',
    '2': 'enabled',
    '3': 'disabled'}

CPU = collections.namedtuple(
    'CPU',
    ['id', 'cores', 'speed_mhz', 'model', 'status', 'ht_enabled',
     'cpu_count', 'turbo_enabled', 'vt_enabled', 'arch64'])

Memory = collections.namedtuple(
    'Memory',
    ['id', 'size_mb', 'speed_mhz', 'manufacturer', 'model', 'status'])

NIC = collections.namedtuple(
    'NIC',
    ['id', 'mac', 'model', 'speed_mbps', 'duplex', 'media_type'])

Video = collections.namedtuple(
    'Video',
    ['id', 'description', 'function_number', 'manufacturer', 'pci_device_id',
     'pci_vendor_id', 'pci_subdevice_id', 'pci_subvendor_id'])

System = collections.namedtuple(
    'System',
    ['id', 'lcc_version', 'model', 'service_tag', 'uuid',
     'last_system_inventory_time'])


class InventoryManagement(object):

    def __init__(self, client):
        """Creates InventoryManagement object

        :param client: an instance of WSManClient
        """
        self.client = client

    def list_cpus(self):
        """Returns the list of CPUs

        :returns: a list of CPU objects
        :raises: WSManRequestFailure on request failures
        :raises: WSManInvalidResponse when receiving invalid response
        :raises: DRACOperationFailed on error reported back by the DRAC
        """

        doc = self.client.enumerate(uris.DCIM_CPUView)

        cpus = utils.find_xml(doc, 'DCIM_CPUView',
                              uris.DCIM_CPUView,
                              find_all=True)

        return [self._parse_cpus(cpu) for cpu in cpus]

    def _parse_cpus(self, cpu):
        drac_characteristics = self._get_cpu_attr(cpu, 'Characteristics')
        arch64 = (CPU_CHARACTERISTICS_64BIT == drac_characteristics)

        return CPU(
            id=self._get_cpu_attr(cpu, 'FQDD'),
            cores=int(self._get_cpu_attr(cpu, 'NumberOfProcessorCores')),
            speed_mhz=int(self._get_cpu_attr(cpu, 'CurrentClockSpeed')),
            model=self._get_cpu_attr(cpu, 'Model'),
            status=constants.PRIMARY_STATUS[
                self._get_cpu_attr(cpu, 'PrimaryStatus')],
            ht_enabled=bool(self._get_cpu_attr(cpu, 'HyperThreadingEnabled',
                                               allow_missing=True)),
            turbo_enabled=bool(self._get_cpu_attr(cpu, 'TurboModeEnabled',
                                                  allow_missing=True)),
            cpu_count=self._get_cpu_count(
                int(self._get_cpu_attr(cpu, 'NumberOfProcessorCores')),
                bool(self._get_cpu_attr(cpu, 'HyperThreadingEnabled',
                                        allow_missing=True))),
            vt_enabled=bool(self._get_cpu_attr(
                cpu, 'VirtualizationTechnologyEnabled', allow_missing=True)),
            arch64=arch64)

    def _get_cpu_count(self, cores, ht_enabled):
        if ht_enabled:
            return int(cores * 2)
        else:
            return int(cores)

    def _get_cpu_attr(self, cpu, attr_name, allow_missing=False):
        return utils.get_wsman_resource_attr(
            cpu, uris.DCIM_CPUView, attr_name, allow_missing=allow_missing)

    def list_memory(self):
        """Returns the list of installed memory

        :returns: a list of Memory objects
        :raises: WSManRequestFailure on request failures
        :raises: WSManInvalidResponse when receiving invalid response
        :raises: DRACOperationFailed on error reported back by the DRAC
        """

        doc = self.client.enumerate(uris.DCIM_MemoryView)

        installed_memory = utils.find_xml(doc, 'DCIM_MemoryView',
                                          uris.DCIM_MemoryView,
                                          find_all=True)

        return [self._parse_memory(memory) for memory in installed_memory]

    def _parse_memory(self, memory):
        return Memory(
            id=self._get_memory_attr(memory, 'FQDD'),
            size_mb=int(self._get_memory_attr(memory, 'Size')),
            speed_mhz=int(self._get_memory_attr(memory, 'Speed')),
            manufacturer=self._get_memory_attr(memory, 'Manufacturer'),
            model=self._get_memory_attr(memory, 'Model'),
            status=constants.PRIMARY_STATUS[
                self._get_memory_attr(memory, 'PrimaryStatus')])

    def _get_memory_attr(self, memory, attr_name):
        return utils.get_wsman_resource_attr(memory, uris.DCIM_MemoryView,
                                             attr_name)

    def list_nics(self, sort=False):
        """Returns the list of NICs

        :returns: a list of NIC objects
        :raises: WSManRequestFailure on request failures
        :raises: WSManInvalidResponse when receiving invalid response
        :raises: DRACOperationFailed on error reported back by the DRAC
                 interface
        """

        doc = self.client.enumerate(uris.DCIM_NICView)
        drac_nics = utils.find_xml(doc, 'DCIM_NICView', uris.DCIM_NICView,
                                   find_all=True)
        nics = [self._parse_drac_nic(nic) for nic in drac_nics]
        if sort:
            nics.sort(key=lambda nic: nic.id)

        return nics

    def _parse_drac_nic(self, drac_nic):
        fqdd = self._get_nic_attr(drac_nic, 'FQDD')
        drac_speed = self._get_nic_attr(drac_nic, 'LinkSpeed')
        drac_duplex = self._get_nic_attr(drac_nic, 'LinkDuplex')

        return NIC(
            id=fqdd,
            mac=self._get_nic_attr(drac_nic, 'CurrentMACAddress'),
            model=self._get_nic_attr(drac_nic, 'ProductName'),
            speed_mbps=NIC_LINK_SPEED_MBPS[drac_speed],
            duplex=NIC_LINK_DUPLEX[drac_duplex],
            media_type=self._get_nic_attr(drac_nic, 'MediaType'))

    def _get_nic_attr(self, drac_nic, attr_name):
        return utils.get_wsman_resource_attr(drac_nic, uris.DCIM_NICView,
                                             attr_name)

    def list_video_controllers(self):
        """Returns the list of video controllers

        :returns: a list of Video objects
        :raises: WSManRequestFailure on request failures
        :raises: WSManInvalidResponse when receiving invalid response
        :raises: DRACOperationFailed on error reported back by the DRAC
        """

        doc = self.client.enumerate(uris.DCIM_VideoView)

        controllers = utils.find_xml(doc, 'DCIM_VideoView',
                                     uris.DCIM_VideoView,
                                     find_all=True)

        return [self._parse_video_controllers(controller)
                for controller in controllers]

    def _parse_video_controllers(self, controller):
        return Video(
            id=self._get_video_attr(controller, 'FQDD'),
            description=self._get_video_attr(controller, 'Description'),
            function_number=int(self._get_video_attr(controller,
                                                     'FunctionNumber')),
            manufacturer=self._get_video_attr(controller, 'Manufacturer'),
            pci_device_id=self._get_video_attr(controller, 'PCIDeviceID'),
            pci_vendor_id=self._get_video_attr(controller, 'PCIVendorID'),
            pci_subdevice_id=self._get_video_attr(controller,
                                                  'PCISubDeviceID'),
            pci_subvendor_id=self._get_video_attr(controller,
                                                  'PCISubVendorID'))

    def _get_video_attr(self, controller, attr_name, allow_missing=False):
        return utils.get_wsman_resource_attr(
            controller, uris.DCIM_VideoView, attr_name,
            allow_missing=allow_missing)

    def get_system(self):
        """Returns a System object

            :returns: a System object
            :raises: WSManRequestFailure on request failures
            :raises: WSManInvalidRespons when receiving invalid response
        """
        doc = self.client.enumerate(uris.DCIM_SystemView)
        drac_system = utils.find_xml(doc,
                                     'DCIM_SystemView',
                                     uris.DCIM_SystemView,
                                     find_all=False)

        return self._parse_drac_system(drac_system)

    def _parse_drac_system(self, drac_system):
        return System(
            id=self._get_system_attr(drac_system, 'InstanceID'),
            uuid=self._get_system_attr(drac_system, 'UUID'),
            service_tag=self._get_system_attr(drac_system, 'ServiceTag'),
            model=self._get_system_attr(drac_system, 'Model'),
            lcc_version=self._get_system_attr(drac_system,
                                              'LifecycleControllerVersion'),
            last_system_inventory_time=self._get_system_attr(
                drac_system, 'LastSystemInventoryTime').split('.')[0])

    def _get_system_attr(self, drac_system, attr_name):
        return utils.get_wsman_resource_attr(drac_system,
                                             uris.DCIM_SystemView,
                                             attr_name)
