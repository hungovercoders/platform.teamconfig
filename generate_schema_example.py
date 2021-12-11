import json
import jsonschema
from jsonschema import validate

schema = {
 "$schema": "http://json-schema.org/schema#",
      "type": "object",
      "description": "Teams in a company",
      "properties": {
          "teams": {
            "type": "array",
            "items": { "$ref": "#/$defs/team" }
            }
      },
    "$defs": {
    "team": {
      "type": "object",
      "required": [ "name", "mission" ],
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the team.",
           "enum": ["Team A", "Team B"]
        },
        "mission": {
          "type": "string",
          "description": "The mission of the team."
        }
      }
    }
  }
}

data = """
{
    "teams": [
        {
            "name": "Team A",
            "mission": "Team A does things"
        }
    ]
}
"""

jsonData = json.loads(data)

validate(instance=jsonData, schema=schema)