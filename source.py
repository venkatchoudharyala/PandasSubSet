from typing import List, Iterable, Tuple
from TimeStamp import logged

# Tasks 2, 3 & 4 Code

class InconsistentRowError(Exception):
    @logged
    def __init__(self, msg: str) -> None:
        print(msg)
class CriteriaNotFoundError(Exception):
    @logged
    def __init__(self, msg: str) -> None:
        print(msg)
class EntryNotFoundError(Exception):
    @logged
    def __init__(self, msg: str) -> None:
        print(msg)
class IllegalComparison(Exception):
    @logged
    def __init__(self, msg: str) -> None:
        print(msg)

class Data:
    """
    A lower level simple implementation of pandas lib (till file organization)
    """
    @logged
    def __init__(self, columns: Iterable | None = [], rows: List[List] | None = []) -> None:
        self.columns = list(columns)
        self.rows = []
        for row in rows:
            self.new_row(row)

    @logged
    def from_csv_file(self, path: str) -> None:
        """
        function to import data from a csv file
        """
        try:
            with open(path, "r", encoding = "utf-8-sig") as file:
                import csv
                rows = csv.reader(file)
                flag = False
                for row in rows:
                    if flag:
                        self.new_row(row)
                    else:
                        self.columns = row.copy()
                        flag = True
        except FileNotFoundError:
            print("File didn't exist")

    @logged
    def from_json_file(self, path: str, mode: str = "1+") -> None:
        """
        function to collect data from Json File
        mode = 1+ for multiple entries which is default or mode = 1 for unit entry
        """
        try:
            with open(path, "r") as file:
                import json
                json_data = json.load(file)
            flag = False
            if mode == "1+":
                for entries in json_data:
                    if not flag:
                        self.columns = list(json_data[entries].keys()).copy()
                        flag = True
                    temp = []
                    for col in self.columns:
                        if col in json_data[entries]:
                            temp.append(json_data[entries][col])
                        else:
                            raise InconsistentRowError("Features are not uniform across the data")
                    if len(temp) != len(json_data[entries].values()):
                        raise InconsistentRowError("Features are not uniform across the data")
                    self.new_row(temp)
            else:
                self.columns = list(json_data.keys())
                temp = []
                for col in self.columns:
                    temp.append(json_data[col])
                self.new_row(temp)
        except FileNotFoundError:
            print("File didn't exist")
    
    @logged
    def to_csv_file(self, path) -> None:
        """
        function to write data to a csv file
        if file doesnt exist, creates files and writes the data
        """
        with open(path, "w", newline = '') as file:
            import csv
            writer = csv.writer(file)
            writer.writerow(self.columns)
            writer.writerows(self.rows)

    @logged
    def to_json_file(self, path) -> None:
        """
        function to write data to a json file
        if file doesnt exist, creates files and writes the data
        """
        final_dict = {}
        for row in self.rows:
            temp_dict = {}
            for col in self.columns:
                temp_dict[col] = row[self.columns.index(col)]
            final_dict[len(final_dict)] = temp_dict
        with open(path, "w") as file:
            import json
            json.dump(final_dict, file)

    @logged
    def new_row(self, row: Iterable) -> None:
        """
        function to append new row to the data
        """
        if len(row) != len(self.columns):
            raise InconsistentRowError(f"Expected {len(self.columns)} columns, {len(row)} given")
        else:
            self.rows.append(list(row))

    @logged
    def delete_row(self, criteria: str | None = None, value: str = None) -> List:
        """
        function to delete a row
        takes criteria and value as the input
        if not given pops last row entry and returns it.
        """
        if criteria is None:
            return self.rows.pop()
        else:
            if criteria not in self.columns:
                raise CriteriaNotFoundError(f"Criteria {criteria} not found")
            ind = self.columns.index(criteria)
            for del_i, row in enumerate(self.rows):
                if row[ind] == value:
                    return self.rows.pop(del_i)
            raise EntryNotFoundError(f"The entry '{value}', not found for the '{criteria}'")

    @logged 
    def delete_column(self, criteria: str) -> List:
        """
        function to delete a column
        """
        if criteria not in self.columns:
            raise CriteriaNotFoundError(f"Criteria {criteria} not found")
        ind = self.columns.index(criteria)
        self.columns.remove(criteria)
        temp = []
        for row in self.rows:
            temp.append(row.pop(ind))
        return temp

    @logged
    def shuffle(self, criteria: str, reverse: bool = False, comp: str | None = None) -> List[List]:
        """
        function to shuffle based on the given criteria
        can even compare and return specific rows but criteria has to be int type
        """
        if criteria not in self.columns:
            raise CriteriaNotFoundError(f"Criteria {criteria} not found")
        else:
            sorty = sorted(self.rows, key = lambda x: x[self.columns.index(criteria)], reverse = reverse)
            if comp != None:
                type_d = type(self.rows[0][self.columns.index(criteria)])
                if type_d != type(1):
                    raise IllegalComparison(f"Cant compare on type {type_d}")
                else:
                    comp = "row[self.columns.index(criteria)]" + comp
                    sorty = [row for row in sorty if eval(comp)]
            return sorty

    @logged     
    def print_data(self, criteria: None | str = None, reverse: bool = False, comp: str | None = None):
        """
        function to print data in tabular form
        can use criteria to shuffle and print the data
        """
        row_format ="{:>10}" * (len(self.columns))
        print(row_format.format(*self.columns))
        print('-' * 10 * (len(self.columns) + 1))
        if criteria == None:
            if reverse:
                rows = self.rows[::-1]
            else:
                rows = self.rows.copy()
        else:
            rows = self.shuffle(criteria, reverse, comp)
        for row in rows:
            print(row_format.format(*row))

# Task 1 Code

class TextManip:
    """
    A simple class to carry out Text Manipulation from Text files
    """
    def text_reader(self, path: str) -> str:
        """
        a simple text reader function
        """
        with open(path, 'r') as file:
            data = file.read()
        return data

    def text_writer(self, path: str, data: str) -> None:
        """
        a simple text writer function
        """
        with open(path, 'w') as file:
            file.write(data)

    def text_appender(self, path: str, data: str) -> None:
        """
        a simple text appender function
        """
        with open(path, 'a') as file:
            file.write(data)

    def text_finder(self, path: str, text: str) -> int:
        """
        a simple text finder funcion (returns first index)
        """
        data = self.text_reader(path)
        return data.find(text)

    def text_printer(self, path: str) -> None:
        """
        a simple text writer function
        """
        data = self.text_reader(path)
        print(data)

    def text_replace(self, path: str, text: str, new_text: str, freq: int  = -1) -> None:
        """
        function to find and replace text
        """
        data = self.text_reader(path)
        data = data.replace(text, new_text, freq)
        self.text_writer(path, data) 

    def text_deletion(self, path: str, text: str) -> None:
        """
        a simple function to find and delete a text
        """
        self.text_replace(path, text, "")

    def find_and_write(self, path: str, text: str, new_text: str) -> None:
        """
        function to find a given text and append new data from there
        """
        self.text_replace(path, text, text + " " + new_text)

    def findall(self, path: str, text: str, seek: int = 0, data: str = "", out: List[int] = None) -> Tuple[int, List[int]]:
        """
        function to get frequency of text and the indices
        """
        if seek == 0:
            data = self.text_reader(path)
            out = []
        ind = data.find(text)
        out.append(ind)
        next_ind = ind + len(text) + 1
        data = data[next_ind :]
        if ind != -1 and next_ind < len(data) - len(text):
            return self.findall(path, text, next_ind, data, out)
        else:
            return len(out), out
        
    def replace_all(self, path: str, text: str, new_text: str) -> None:
        """
        a function to replace all given text entries
        """
        freq = self.findall(path, text)[0]
        self.text_replace(path, text, new_text, freq)

    def delete_all(self, path: str, text: str) -> None:
        """
        a function to replace delete all given text entries
        """
        self.replace_all(path, text, "")

    def case_change(self, path: str, text: str, to_case: str = "U") -> None:
        """
        a function to case change the given text across all entries
        """
        if to_case == "U":
            self.replace_all(path, text, text.upper())
        else:
            self.replace_all(path, text, text.lower())

