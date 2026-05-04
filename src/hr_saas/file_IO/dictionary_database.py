import json
from typing import Dict, Any, Type
from src.hr_saas.file_IO.logging import Logger
from src.hr_saas.file_IO.config_file import ERROR_LOG_FILE


class DictionaryDatabase:
    @staticmethod
    def save(storage_file: str, type_of_obj: str, database: Dict[str, Any]):
        # Prepare data for JSON serialization
        savable_data = {
            obj_attribute: obj.to_dict()
            for obj_attribute, obj in database.items()
        }

        try:
            with open(storage_file, mode="w", encoding="utf-8") as file_writer:
                json.dump(savable_data, file_writer, indent=4)
        except Exception as e:
            Logger.error(f"Error saving {type_of_obj} | {e}", ERROR_LOG_FILE)

    @staticmethod
    def load_data(storage_file: str, database: Dict[str, Any], object_class: Type, type_of_object: str):
        # Clear existing data
        database.clear()

        try:
            with open(storage_file, mode="r", encoding="utf-8") as file_reader:
                data = json.load(file_reader)

                if isinstance(data, dict):
                    for obj_attribute, obj in data.items():
                        if hasattr(object_class, "from_dict"):
                            new_obj = object_class.from_dict(obj)
                        else:
                            if isinstance(obj, dict):
                                try:
                                    new_obj = object_class(**obj)
                                except Exception as e:
                                    Logger.error(f"Could not reconstruct object for {obj_attribute} | {e}",
                                                 ERROR_LOG_FILE)
                                    continue
                            else:
                                new_obj = obj

                        database[obj_attribute] = new_obj

        except FileNotFoundError as e:
            # First run - file doesn't exist yet
            Logger.error(f"Database file not found, starting fresh | {e}", ERROR_LOG_FILE)
        except json.JSONDecodeError as e:
            # File exists but is empty or corrupted
            Logger.error(f"JSON Decode Error | {e}", ERROR_LOG_FILE)
        except Exception as e:
            Logger.error(f"Error Loading {type_of_object} Database | {e}", ERROR_LOG_FILE)


