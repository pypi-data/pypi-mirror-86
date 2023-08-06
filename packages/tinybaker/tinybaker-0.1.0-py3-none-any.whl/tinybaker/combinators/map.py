from typing import Set, Dict
from ..exceptions import BakerError
from ..step_definition import StepDefinition, FileRef


def _map_names(name_set: Set[str], mapping: Dict[str, str]):
    result = set()
    for name in name_set:
        if name in mapping:
            result.add(mapping[name])
        else:
            result.add(name)
    return result


def _map_filerefs_to_new_paths(file_dict: Dict[str, FileRef], mapping: Dict[str, str]):
    result = {}
    for name in file_dict:
        if name in mapping:
            result[mapping[name]] = file_dict[name].path
        else:
            result[name] = file_dict[name].path
    return result


def _invert_mapping(mapping: Dict[str, str]):
    result = {}
    for key in mapping:
        result[mapping[key]] = key
    return result


def map_tags(base_step: StepDefinition, input_mapping={}, output_mapping={}):
    extra_input_keys = set(input_mapping.values()) - base_step.input_file_set
    if len(extra_input_keys) > 0:
        msg = "Unexpected key(s) for input mapping: {}".format(
            ", ".join(extra_input_keys)
        )
        raise BakerError(msg)

    extra_output_keys = set(output_mapping) - base_step.output_file_set
    if len(extra_output_keys) > 0:
        msg = "Unexpected key(s) for output mapping: {}".format(
            ", ".join(extra_output_keys)
        )
        raise BakerError(msg)

    mapping_input_file_set = _map_names(
        base_step.input_file_set, _invert_mapping(input_mapping)
    )
    mapping_output_file_set = _map_names(base_step.output_file_set, output_mapping)

    class TagMapping(StepDefinition):
        nonlocal mapping_input_file_set, mapping_output_file_set, base_step, input_mapping, output_mapping
        input_file_set = mapping_input_file_set
        output_file_set = mapping_output_file_set

        _base_step = base_step
        _input_mapping = input_mapping
        _output_mapping = output_mapping

        def script(self):

            input_paths = _map_filerefs_to_new_paths(
                self.input_files, self._input_mapping
            )
            output_paths = _map_filerefs_to_new_paths(
                self.output_files, _invert_mapping(self._output_mapping)
            )

            self._base_step(input_paths=input_paths, output_paths=output_paths).build(
                overwrite=True
            )

    return TagMapping
