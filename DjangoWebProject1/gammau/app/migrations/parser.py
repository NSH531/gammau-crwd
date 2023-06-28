
import django as D
from django.db import models as model
x=0
out={}
import os
from django.db import models as model

class Parser():
    def __init__(self):
        self.x = 0

    def parse_json(self, data):
        class_dict = {}
        self.parse_json_recursive(dict(class_dict), "Root", data)
        return class_dict

    def CLASS_GEN(self, class_name, model_attrs):
        base_class = model.Model

        # Create a new file and write the class definition
        with open(f"{class_name}.py", "w") as file:
            file.write(f"class {class_name}({base_class.__name__}):\n")
            for attr, value in model_attrs.items():
                file.write(f"    {attr} = {repr(value)}\n")
            file.close()

    def parse_json_recursive(self, class_dict, class_name, data, out=None):
        if self.x<8:

            if out is None:
                out = []

            if isinstance(data, model.Field):
                class_dict[class_name] = data
                return

            if isinstance(data, model.ForeignKey):
                class_dict[class_name] = data
                return

            if isinstance(data, dict):
                model_attrs = {}
                for attr_name, attr_value in data.items():
                    if isinstance(attr_value, dict):
                        nested_class_name = f"{class_name}_{attr_name}"
                        nested_class_dict = {}
                        self.parse_json_recursive(nested_class_dict, nested_class_name, attr_value)
                        model_attrs[attr_name] = model.ForeignKey(nested_class_dict[nested_class_name], on_delete=model.CASCADE)
                    else:
                        model_attrs[attr_name] = self.convert_to_model_field(attr_value, out)

                new_class = type(class_name, (model.Model,), model_attrs)
                class_dict[class_name] = new_class
                self.CLASS_GEN(class_name, model_attrs)
                return new_class

            elif isinstance(data, list):
                if data:
                    # Assume all items in the list have the same structure
                    self.parse_json_recursive(class_dict, class_name, data[0], out)

            else:
                if(type(class_dict)==list):
                    pass
                else:
                    # Non-dict types (e.g., string, number, boolean)
                    class_dict[class_name] = self.convert_to_model_field(data, out)
        else:
            return class_dict

    def convert_to_model_field(self, value, out):
        if isinstance(value, str):
            return model.CharField(max_length=255)
        elif isinstance(value, int):
            return model.IntegerField()
        elif isinstance(value, float):
            return model.FloatField()
        elif isinstance(value, bool):
            return model.BooleanField()
        else:
            self.x += 1
            class_name = f"Root_{int(self.x)}"
            self.parse_json_recursive(out, class_name, value)
            return model.CharField(max_length=255)

