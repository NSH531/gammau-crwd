
import importlib
import django as D
from django.db import models as model

import os

class parser:
    def parse_json(self, DATA):
        class_dict = {}
        for i in dir(DATA):
            class_dict = self.parse_json_recursive(self, class_dict=class_dict, class_name=f"Root_{i}", data=DATA)
        return class_dict

    def parse_json_recursive(self, class_dict, class_name, data):
        if isinstance(data, dict):
            model_attrs = {}

            for attr_name, attr_value in data.items():
                if isinstance(attr_value, dict):
                    nested_class_name = f"{class_name}_{attr_name}"
                    nested_class_dict = {}
                    self.parse_json_recursive(self,class_dict=nested_class_dict, class_name=nested_class_name, data=attr_value)
                    model_attrs[attr_name] = model.ForeignKey(nested_class_dict[nested_class_name], on_delete=model.CASCADE)
                else:
                    model_attrs[attr_name] = self.convert_to_model_field(self,value=attr_value)
            model_attrs['__module__'] = __name__  # Add the __module__ attribute
            self.generate_python_file(self,class_name.split("__class__")[1],model_attrs)
            new_class = type(class_name.split("__class__")[1], (model.Model,), model_attrs)
            class_dict[class_name] = new_class

        elif isinstance(data, list):
            if data:
                # Assume all items in the list have the same structure
                self.parse_json_recursive(class_dict, class_name, data[0])

        else:
            return self.generate_python_file(self,class_name=type(data),class_dict=data)

            # Non-dict types (e.g., string, number, boolean)
            #class_dict[class_name] = self.convert_to_model_field(self,value=data)
        return class_dict

    def convert_to_model_field(self, value):
        if isinstance(value, str):
            return model.CharField(max_length=255)
        elif isinstance(value, int):
            return model.IntegerField()
        elif isinstance(value, float):
            return model.FloatField()
        elif isinstance(value, bool):
            return model.BooleanField()
        else:
            return model.CharField(max_length=255)
    def generate_python_file(self, class_name, class_dict):
        class_str = ''
        for name, cls in class_dict.items():
            class_str += f"class {name}():\n"
            if(type(cls)==str):
                cls=self.convert_to_model_field(self,value=cls)
            else:
                for attr_name, attr_value in cls.__dict__.items():
                    if not attr_name.startswith('__'):
                        class_str += f"    {attr_name} = {attr_value}\n"
            class_str += '\n'

        file_name = f"{class_name}.py"
        full_path = os.path.join(os.getcwd(), file_name)

        with open(full_path, 'w') as file:
            file.write(class_str)

        # Import the newly generated class
        module_name = os.path.splitext(file_name)[0]
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
