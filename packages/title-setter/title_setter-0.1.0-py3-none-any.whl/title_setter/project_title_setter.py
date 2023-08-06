
import string
import pandas as pd
import numpy as np
from pathlib import Path


class StaticReader:
    """
    Leest excel file en geeft pandas dataframe terug
    """

    def read_excel(self, filepath):

        opened_excel_file = pd.read_excel(filepath)

        return opened_excel_file


class TextCleaner:
    """
    maakt de tabel schoon van punctuatie
    """
    @staticmethod
    def remove_punctuation(text):
        if type(text) == str:
            words = text.split()
            table = str.maketrans('', '', string.punctuation)
            stripped = [w.translate(table) for w in words]
            cleaned = " ".join(stripped)
            if not cleaned:
                return np.NaN

            if cleaned.isdigit():
                return int(cleaned)

            return cleaned

        return text


class AlterHeaderRow(TextCleaner):
    """
    vindt de koprij en verandert de tekst van de koprij
    """

    def __init__(self, filepath):
        self.filename = filepath
        self.df = StaticReader().read_excel(filepath)
        self.numeric_data_types = ['int', 'int64', np.number]

    def _clean_file(self):
        df = self.df.dropna(axis=1, how='all')
        df = df.dropna(axis=0, how='all')
        cleaned_df = df.applymap(TextCleaner.remove_punctuation)
        cleaned_df = cleaned_df.reset_index(drop=True)
        return cleaned_df

    def _fill_merged_cells(self):
        df = self._clean_file()
        row_index = self.find_header_row()['index_of_title']
        df.iloc[row_index, :].fillna(method='ffill', inplace=True)
        return df

    def find_header_row(self):
        df = self._clean_file()
        column_iterator = df.columns
        loop_status = False
        matched_int_column = None
        for column in column_iterator:

            for row_numerator in range(len(df[column])):
                preceding_column = df[column][row_numerator::].fillna(0)

                if preceding_column.dtype in self.numeric_data_types:
                    matched_index = row_numerator - 1
                    matched_int_column = column
                    index_row_title = df[column][matched_index]
                    loop_status = True
                    break
            if loop_status:
                break

        if matched_int_column:
            return {
                'index_row_column': matched_int_column,
                'index_row_title': index_row_title,
                'index_of_title': matched_index,
            }
        else:
            raise IndexError('Index Column Not Found')

    def get_first_column_title_letter(self):
        df = self._fill_merged_cells()
        index = self.find_header_row()['index_of_title']
        second_index = index + 1
        letters = []
        for text in df.iloc[second_index, :]:
            if type(text) == str and text != '':
                letter = text[0].upper()
                letters.append("_" + letter)
            else:
                letters.append("")

        return letters

    def set_title(self):

        row_index = self.find_header_row()['index_of_title']
        letter_list = self.get_first_column_title_letter()
        df = self._fill_merged_cells()
        list_of_letter_tuples = list(zip(df.iloc[1, :], letter_list))
        df.iloc[0, :] = [str(a) + str(b) for a, b in list_of_letter_tuples]
        df.drop([row_index, row_index + 1], inplace=True)
        return df

    def export_modifications(self):
        filename = Path(self.filename)
        self.set_title().to_excel(f"{filename.parent}/Altered_{filename.name}" , index=False, header=False)
        print('file exported as: Altered_{}'.format(filename.name))


