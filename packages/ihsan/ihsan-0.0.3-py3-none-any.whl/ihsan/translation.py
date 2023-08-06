"""Translator module where it change ADFH into json, SDL, openAPI, etc..."""
from .schema import IhsanType
from .utils import find_action, find_field, find_model


def to_sdl(schema: IhsanType, indention: int = 4) -> str:
    """Function that transfer ADFH into SDL aka GraphQL schema.

    Args:
        schema: IhsanType model.
        indention: The indention of the generated SDL.

    Returns:
        SDL aka Graphql schema.
    """
    show_me_list = find_action(schema.adfh.actions, "show me list")
    let_me_remove = find_action(schema.adfh.actions, "let me remove")
    let_me_add = find_action(schema.adfh.actions, "let me add")
    text = ""
    for model in schema.adfh.models:
        text += f"type {model.name} {'{'}\n"

        for pro in model.properties:
            pro = find_field(schema.adfh.fields_list, pro.assign)
            placeholder = f"{pro.name}: {pro.type}{pro.mandatory}\n"
            text += placeholder.rjust(len(placeholder) + indention)
        text += "}\n"

    text += "type Query {\n"
    for item in show_me_list:
        model = find_model(schema.adfh.models, item.get("model"))
        placeholder = f"{item.get('name')}: [{model.name}]\n"
        text += placeholder.rjust(len(placeholder) + indention)
    text += "}\n"

    text += "type Mutation {\n"
    for item in let_me_add:
        placeholder = f"{item.get('name')}("
        text += placeholder.rjust(len(placeholder) + indention)
        for input_action in item.get("input"):
            input_action = find_field(
                schema.adfh.fields_list, input_action.get("assign")
            )
            text += (
                f"{input_action.name}: {input_action.type}{input_action.mandatory}, "
            )

        model = find_model(schema.adfh.models, item.get("model"))
        text += f"): {model.name}\n"

    for item in let_me_remove:
        placeholder = f"{item.get('name')}("
        text += placeholder.rjust(len(placeholder) + indention)
        field = find_field(schema.adfh.fields_list, item.get("subject"))
        text += f"{field.name}: {field.type}{field.mandatory}, "
        model = find_model(schema.adfh.models, item.get("model"))
        text += f"): {model.name}\n"

    text += "}\n"

    text += """schema {
    query: Query,
    mutation: Mutation
}
    """
    return text
