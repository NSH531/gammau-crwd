
import django as D
from django.db import models as model
class parser():
    def parse_json(self,DATA):
        class_dict = {}
        self.parse_json_recursive(class_dict, "Root", DATA)
        return class_dict

    def parse_json_recursive(self,class_dict, class_name, data):
       # models=django.db.models()
        
        if isinstance(data, dict):
            model_attrs = {}

            for attr_name, attr_value in data.items():
                if isinstance(attr_value, dict):
                    nested_class_name = f"{class_name}_{attr_name}"
                    nested_class_dict = {}
                    self.parse_json_recursive(nested_class_dict, nested_class_name, attr_value)
                    model_attrs[attr_name] = model.ForeignKey(nested_class_dict[nested_class_name], on_delete=models.CASCADE)
                else:
                    model_attrs[attr_name] = self.convert_to_model_field(attr_value)

            new_class = type(class_name, (models.Model,), model_attrs)
            class_dict[class_name] = new_class

        elif isinstance(data, list):
            if data:
                # Assume all items in the list have the same structure
                self.parse_json_recursive(class_dict, class_name, data[0])

        else:
            # Non-dict types (e.g., string, number, boolean)
            class_dict[class_name] = self.convert_to_model_field(data)

    def convert_to_model_field(value):
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
