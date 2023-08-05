"""
Downstream users should not depend on the precise implementations of these serialization functions.
We only assert that:

>>> payload == deserialize(serialize(payload))
"""
import json
import string

from .exceptions import ParsingError
from .model import Model


def serialize(model: Model) -> str:
    data = model.json()

    # Assumes charset is sorted
    output = []
    for letter in model.charset:
        output.append([
            data[letter][next_letter]
            for next_letter in model.charset
        ])
    
    return json.dumps(output)


def deserialize(payload: str) -> Model:
    """
    :raises: ParsingError
    """
    try:
        raw_data = json.loads(payload)
    except json.decoder.JSONDecodeError:
        raise ParsingError

    data = {}

    # TODO: Handle modifiable charset
    charset = string.ascii_letters
    for index, row in enumerate(raw_data):
        data[charset[index]] = {}

        for next_index, value in enumerate(row):
            data[charset[index]][charset[next_index]] = value

    return Model.from_dict(data)
