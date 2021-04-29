import math
from dataclasses import dataclass

from backend_test.constants.numToEnglish import units, tens, teens, thousands
from backend_test.constants.payload import NOT_OK, NUM_NOT_NUM, NUM_NOT_SENT, NUM_IS_FLOAT, OK, TOO_BIG


@dataclass(init=False)
class NumToEnglish:
    number: str

    def __init__(self, number: str):
        self.number = number

    def validate_number(self) -> (bool, str):
        if type(self.number) != str:
            self.number = str(self.number)
        number = self.number.lstrip("-")
        if not number:
            return False, NUM_NOT_SENT
        if not number.isnumeric():
            return False, NUM_NOT_NUM
        if not number.isdecimal():
            return False, NUM_IS_FLOAT
        if len(number) > 35:
            return False, TOO_BIG

        return True, ""

    def _get_groups(self) -> int:
        return (len(self.number) + 2) // 3

    def _split_by_type(self, index) -> (int, int, int):
        return int(self.number[index]), int(self.number[index + 1]), int(self.number[index + 2])

    def number_to_english(self) -> str:
        if int(self.number) == 0:
            return "zero"
        results = []
        if int(self.number) < 0:
            results.append("minus")
            self.number = str(abs(int(self.number)))

        groups = self._get_groups()
        self.number = self.number.zfill(groups * 3)
        for index in range(0, groups * 3, 3):
            position = groups-(index//3+1)
            group_hundredths, group_tens, group_units = self._split_by_type(index)
            if group_hundredths:
                results.append(f"{units[group_hundredths]} hundredth")
            if group_tens == 1:
                if group_units > 1:
                    results.append(f"{teens[group_units]}")
                else:
                    results.append(f"{tens[group_tens]}")
            elif group_tens > 1:
                results.append(f"{tens[group_tens]}")
            if group_units and group_tens != 1:
                results.append(f"{units[group_units]}")
            if position > 0 and (group_tens or group_units or group_hundredths):
                results.append(f"{thousands[position]}")
        return " ".join(results)

    def process(self) -> (str, str):
        is_valid, msg = self.validate_number()
        if not is_valid:
            return msg, ""
        result = self.number_to_english()
        if not result:
            return TOO_BIG, result
        return OK, result
