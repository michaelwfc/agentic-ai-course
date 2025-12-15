from typing import Any, Dict, Type,Optional
from pydantic import BaseModel, Field, create_model, ConfigDict



"""
Field names → Python-side API
Aliases → External formats (JSON, APIs, files)

By default, Pydantic expects input by alias
It will not accept the Python field name unless you explicitly allow it
Pydantic v2 tightened the rules to avoid ambiguity:
"""
class UserModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(..., alias="User Name",description="The name of the person")
    age: Optional[int] = Field(10, alias="User Age",description="The age of the person")
    
    
# Step 1: Map text types to actual Python types
type_map: Dict[str, Type[Any]] = {
    "int": int,
    "str": str,
    "float": float,
    "bool": bool
}

def build_pydantic_model_from_json(field_defs,populate_by_name=False,model_name="LoadedModel"):
    """Create a Pydantic model dynamically from JSON-like field definitions"""
    # Step 2: Build keyword args for create_model
    field_definitions = {}
    for f in field_defs:
        python_type = type_map.get(f["type"], str)  # default to str
        if f.get("optional"):
            python_type = python_type | None
        
        if f.get("optional"):
           default=f.get("default") if f.get("default") else None
        else:
           default= ...
           
        field_definitions[f["field_name"]] = (
            python_type,
            Field(
                default=default,                     # required
                alias = f["alias"],
                description = f["description"]
            )
        )
    
    if populate_by_name:
      model_config = ConfigDict(populate_by_name=True)
    else:
      model_config = None
    # Step 3: Create the model
    # Use create_model() to define a model from schema-like JSON dynamically.
    LoadedModel = create_model(model_name,__config__=model_config,  **field_definitions,)
    return LoadedModel


def build_pydantic_model_from_json_schema(schema: Dict[str, Any], model_name="LoadedModel")->BaseModel:
    """TODO: field_type failed to parse subschema  {'anyOf': [{'type': 'integer'}, {'type': 'null'}], 'default': 10, 'description': 'The age of the person', 'title': 'User Age'}"""
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    fields = {}
    for name, subschema in properties.items():
        field_type = {
            "integer": int,
            "string": str,
            "boolean": bool,
            "number": float,
        }.get(subschema.get("type", "string"), str)

        default = ... if name in required else None
        title = subschema.get("title")
        descr = subschema.get("description")
        
        fields[name] = (
            Optional[field_type] if default is None else field_type,
            Field(default, alias=name, description=descr),
        )

    model =  create_model(model_name, **fields)
    return model

def save_and_load_from_json(json_path, json_data=None,indent=2):
    # json_path = "./user_model.json"
    if json_data:
      with open(json_path, "w") as f:
        json.dump(json_data, f,indent=indent)
      return json_path
    else:
      with open(json_path,"r") as f:
        data = json.load(f)
      return  data

if __name__ == "__main__":
    from pathlib import Path
    import json
    
    # Example JSON-like definition
    field_defs = [
    {"field_name":"name","type":"str","alias":"User Name","description":"User name","optional":False, },
    {"field_name":"age","type":"int","alias":"User Age","description":"User age","optional":True,"default":10},
]
    LoadedModel = build_pydantic_model_from_json(field_defs)
    
    # Test usage
    data = {"User Name": "Alice", "Age": 30, }
    instance01 = LoadedModel(**data)
    print(instance01)
    data = {"User Name": "Alice", "Age1": 30, }
    # LoadedModel.model_validate(data,strict=True)
    
    data = {"User Name": "Michael" }
    instance02 = LoadedModel(**data)
    print(instance02)
    
    
    # instance = UserModel(name="Alice", age=30)
    # You could also pass aliases directly:
    # instance02 = UserModel(**{"User Name": "Alice", "User Age": 30})
    
    # ensures the JSON uses field aliases, not Python names.
    # json_data = instance.model_dump(by_alias=True)
    # instantiate and dump
    # inst_json = instance.model_dump_json(by_alias=True)
    
    # parse JSON string
    # inst = LoadedModel.model_validate_json(saved_json_data)
    # print(inst)
    
    # Pydantic’s model_json_schema() returns a JSON-serializable description of the model that you can use later to rebuild structural info.
    schema = UserModel.model_json_schema()
    # # Save `schema` and `json_data` to disk/DB
    json_schem_path = Path("./user_model_schema.json")
    save_and_load_from_json(json_schem_path, schema)
    
    loaded_schema = save_and_load_from_json(json_schem_path)
    LoadedModel = build_pydantic_model_from_json_schema(loaded_schema)
    # validate data
    inst = LoadedModel(**{"User Name": "Alice", "User Age": 30})
    print(inst)
    