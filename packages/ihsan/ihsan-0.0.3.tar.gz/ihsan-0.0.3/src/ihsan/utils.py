"""Collection of utils."""
import pathlib
from typing import Any, Dict, List, Tuple, Union

import toml
import yaml
from pydantic import ValidationError

from ihsan.schema import ADFHActionsType, ADFHFieldsType, ADFHModelsType


def read_adfh_file(file: str) -> Tuple[Union[Dict, str], bool]:
    """Parse an ADFH file into dict.

    Args:
        file: Path to ADFH file.

    Returns:
        Tuple either with the data or an error message.
    """
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
    """Converting ADFH data type into sdl data type.

    Args:
        data: ADFH data type.

    Examples:
        >>> from ihsan.utils import sdl_data_type_converter
        >>> unique_id = sdl_data_type_converter(data="unique id")
        >>> unique_id == "String"
        True
        >>> text = sdl_data_type_converter(data="text")
        >>> text == "String"
        True
        >>> checkbox = sdl_data_type_converter(data="checkbox")
        >>> checkbox == "Boolean"
        True
        >>> number = sdl_data_type_converter(data="number")
        >>> number == "Int"
        True

    Returns:
        SDL data type.
    """
    types = {
        "unique id": "String",
        "text": "String",
        "checkbox": "Boolean",
        "number": "Int",
    }
    return types.get(data, "String")


def find_action(actions: List[ADFHActionsType], keyword: str) -> List[Dict[str, Any]]:
    """Search for a certain action.

    Args:
        actions: List of ADFHActionsType model.
        keyword: word or the action that has been required.

    Returns:
        List of selected actions.
    """
    return [action.dict() for action in actions if action.type == keyword]


def find_field(
    fields: List[ADFHFieldsType], field_id: str
) -> Union[ADFHFieldsType, str]:
    """Search for a certain field.

    Args:
        fields: List of ADFHFieldsType model.
        field_id: The id of the field.

    Returns:
        ADFHFieldsType model.
    """
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
    try:
        return ADFHFieldsType(**field_dict)

    except ValidationError as error:
        return error.json()


def find_model(
    models: List[ADFHModelsType], model_id: str
) -> Union[ADFHModelsType, str]:
    """Search for a certain model.

    Args:
        models: List of ADFHModelsType model.
        model_id: The id of the model.

    Returns:
        ADFHModelsType model.
    """
    model_dict = {}
    for field in models:
        if field.id == model_id:
            model_dict.update({"id": field.id, "name": field.name})
    try:
        return ADFHModelsType(**model_dict)

    except ValidationError as error:
        return error.json()
