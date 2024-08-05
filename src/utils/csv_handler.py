import csv
from typing import Dict, Union

class CSVHandler:
    def __init__(self):
        self.locations: Dict[str, int] = {}
        self.languages: Dict[str, str] = {}

    def load_csv(self, file_path: str, csv_type: str) -> None:
        data = {}
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if csv_type == 'location':
                    data[row['location_name']] = int(row['location_code'])
                elif csv_type == 'language':
                    data[row['language_name']] = row['language_code']
        
        if csv_type == 'location':
            self.locations = data
        elif csv_type == 'language':
            self.languages = data

    def get_options(self, option_type: str) -> Dict[str, Union[int, str]]:
        if option_type == 'location':
            return self.locations
        elif option_type == 'language':
            return self.languages
        else:
            raise ValueError("Invalid option type. Use 'location' or 'language'.")

    def display_options(self, option_type: str) -> None:
        options = self.get_options(option_type)
        print(f"\nAvailable {option_type}s:")
        for i, option in enumerate(options.keys(), 1):
            print(f"{i}. {option}")

    def get_user_choice(self, option_type: str) -> tuple:
        options = self.get_options(option_type)
        self.display_options(option_type)
        choice = int(input(f"Enter the number of your desired {option_type}: "))
        selected_option = list(options.keys())[choice - 1]
        option_code = options[selected_option]
        return selected_option, option_code