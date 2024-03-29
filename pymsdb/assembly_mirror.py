from . import sdbtypes
from . import constants
from .utilities import BufferStream


class AssemblyMirror:
    def __init__(self, agent, id):
        self._agent = agent
        self._filename = None
        self._name = None
        self._object_id = None
        self._entry_point_id = None
        self._manifest_module_id = None

        self._types_names_cache = {}

        self.id = id

    def __str__(self):
        return "Assembly Mirror, name = {0}, filename = {1}".format(
            self.get_name(), self.get_filename())

    def get_filename(self):
        if self._filename is None:
            answer = self._agent.send_command(
                constants.CMDSET_ASSEMBLY,
                constants.CMD_ASSEMBLY_GET_LOCATION,
                sdbtypes.encode_int(self.id))

            self._filename = BufferStream(answer.data).get_string()

        return self._filename

    def get_name(self):
        if self._name is None:
            answer = self._agent.send_command(
                constants.CMDSET_ASSEMBLY,
                constants.CMD_ASSEMBLY_GET_NAME,
                sdbtypes.encode_int(self.id))

            self._name = BufferStream(answer.data).get_string()

        return self._name

    def get_type_by_name(self, type_name):
        if type_name not in self._types_names_cache:
            params = (
                sdbtypes.encode_int(self.id) +
                sdbtypes.encode_string(type_name) +
                sdbtypes.encode_byte(1))
            answer = self._agent.send_command(
                constants.CMDSET_ASSEMBLY,
                constants.CMD_ASSEMBLY_GET_TYPE,
                params)

            type_id = BufferStream(answer.data).get_int()
            self._types_names_cache[type_name] = type_id

        if self._types_names_cache[type_name] == 0:
            return None
        else:
            return self._agent.vm.get_type(self._types_names_cache[type_name])

    def get_object(self):
        if self._object_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_ASSEMBLY,
                constants.CMD_ASSEMBLY_GET_OBJECT,
                sdbtypes.encode_int(self.id))

            self._object_id = BufferStream(answer.data).get_int()

        return self._agent.vm.get_object(self._object_id)

    def get_entry_point(self):
        if self._entry_point_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_ASSEMBLY,
                constants.CMD_ASSEMBLY_GET_ENTRY,
                sdbtypes.encode_int(self.id))

            self._entry_point_id = BufferStream(answer.data).get_int()

        if self._entry_point_id == 0:
            return None
        else:
            return self._agent.vm.get_method(self._entry_point_id)

    def get_manifest_module(self):
        if self._manifest_module_id is None:
            answer = self._agent.send_command(
                constants.CMDSET_ASSEMBLY,
                constants.CMD_ASSEMBLY_GET_MANIFEST_MODULE,
                sdbtypes.encode_int(self.id))

            self._manifest_module_id = BufferStream(answer.data).get_int()

        return self._agent.vm.get_module(self._manifest_module_id)
