"""Collection of utils."""
import pathlib
from typing import Any, Dict, List, Tuple, Union

import toml
import yaml

from ihsan.schema import ADFHActionsType, ADFHFieldsType, ADFHModelsType


def read_adfh_file(file: str) -> Tuple[Union[Dict, str], bool]:
    """Parse an ADFH file into dict."""
    file_path = pathlib.Path(file)
    file_name, file_extension = file_path.name.rsplit(".")

    if file_path.exists() and file_path.is_file():

        if file_extension in ["yaml", "yml"]:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
            return data, False

        elif file_extension == "toml":
            data = toml.load(f"{file_path}")
            return data, False
        else:
            return "You can only pick toml or yaml file.", True
    return "File doesn't exist.", True


def sdl_data_type_converter(data: str) -> str:
    """Converting ADFH data type into sdl data type."""
    types = {
        "unique id": "String",
        "text": "String",
        "checkbox": "Boolean",
        "number": "Int",
    }
    return types.get(data, "String")


def find_action(actions: List[ADFHActionsType], command: str) -> List[Dict[str, Any]]:
    """Search for a certain action."""
    return [action.dict() for action in actions if action.type == command]


def find_field(fields: List[ADFHFieldsType], field_id: str) -> ADFHFieldsType:
    """Search for a certain field."""
    field_dict = {}
    for field in fields:
        if field.id == field_id:
            data_type = sdl_data_type_converter(field.type)
            field_dict.update(
                {
                    "id": field.id,
                    "name": field.name,
                    "type": data_type,
                    "mandatory": "!" if field.mandatory == "yes" else "",
                }
            )
    return ADFHFieldsType(**field_dict)


def find_model(fields: List[ADFHModelsType], model_id: str) -> ADFHModelsType:
    """Search for a certain model."""
    model_dict = {}
    for field in fields:
        if field.id == model_id:
            model_dict.update({"id": field.id, "name": field.name})
    return ADFHModelsType(**model_dict)
