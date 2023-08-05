
export interface FunctionDocumentationObject {
    function: string;
    description: string;
    examples?: (string)[] | null;
    syntax: string;
    syntax_elements?: (SyntaxElementsEntity)[] | null;
}

export interface SyntaxElementsEntity {
    element: string;
    description: string;
}

export const functionDocumentationObjects: FunctionDocumentationObject[] = [{"function": "AVG", "description": "Returns the numerical mean value of the passed numbers and series.", "examples": ["AVG(1, 2)", "AVG(A, B)", "AVG(A, 2)"], "syntax": "AVG(value1, [value2, ...])", "syntax_elements": [{"element": "value1", "description": "The first number or series to consider when calculating the average."}, {"element": "value2, ... [OPTIONAL]", "description": "Additional numbers or series to consider when calculating the average."}]}, {"function": "MULTIPLY", "description": "Returns the product of two numbers.", "examples": ["MULTIPLY(2,3)", "MULTIPLY(A,3)"], "syntax": "MULTIPLY(factor1, [factor2, ...])", "syntax_elements": [{"element": "factor1", "description": "The first number to multiply."}, {"element": "factor2, ... [OPTIONAL]", "description": "Additional numbers or series to multiply."}]}, {"function": "ROUND", "description": "Rounds a number to a given number of decimals.", "examples": ["ROUND(1.3)", "ROUND(A, 2)"], "syntax": "ROUND(value, [decimals])", "syntax_elements": [{"element": "value", "description": "The value or series to round."}, {"element": "decimals", "description": " The number of decimals to round to. Default is 0."}]}, {"function": "SUM", "description": "Returns the sum of the given numbers and series.", "examples": ["SUM(10, 11)", "SUM(A, B, D, F)", "SUM(A, B, D, F)"], "syntax": "SUM(value1, [value2, ...])", "syntax_elements": [{"element": "value1", "description": "The first number or column to add together."}, {"element": "value2, ... [OPTIONAL]", "description": "Additional numbers or columns to sum."}]}, {"function": "CLEAN", "description": "Returns the text with the non-printable ASCII characters removed.", "examples": ["CLEAN('ABC\n')"], "syntax": "CLEAN(string)", "syntax_elements": [{"element": "string", "description": "The string or series whose non-printable characters are to be removed."}]}, {"function": "CONCAT", "description": "Returns the passed strings and series appended together.", "examples": ["CONCAT('Bite', 'the bullet')", "CONCAT(A, B)"], "syntax": "CONCAT(string1, [string2, ...])", "syntax_elements": [{"element": "string1", "description": "The first string or series."}, {"element": "string2, ... [OPTIONAL]", "description": "Additional strings or series to append in sequence."}]}, {"function": "FIND", "description": "Returns the position at which a string is first found within text, case-sensitive. Returns 0 if not found.", "examples": ["FIND(A, 'Jack')", "FIND('Ben has a friend Jack', 'Jack')"], "syntax": "FIND(text_to_search, search_for)", "syntax_elements": [{"element": "text_to_search", "description": "The text or series to search for the first occurrence of search_for."}, {"element": "search_for", "description": "The string to look for within text_to_search."}]}, {"function": "LEFT", "description": "Returns a substring from the beginning of a specified string.", "examples": ["LEFT(A, 2)", "LEFT('The first character!')"], "syntax": "LEFT(string, [number_of_characters])", "syntax_elements": [{"element": "string", "description": "The string or series from which the left portion will be returned."}, {"element": "number_of_characters [OPTIONAL, 1 by default]", "description": "The number of characters to return from the start of string."}]}, {"function": "LEN", "description": "Returns the length of a string.", "examples": ["LEN(A)", "LEN('This is 21 characters')"], "syntax": "LEN(string)", "syntax_elements": [{"element": "string", "description": "The string or series whose length will be returned."}]}, {"function": "LOWER", "description": "Converts a given string to lowercase.", "examples": ["=LOWER('ABC')", "=LOWER(A)", "=LOWER('Nate Rush')"], "syntax": "LOWER(string)", "syntax_elements": [{"element": "string", "description": "The string or series to convert to lowercase."}]}, {"function": "MID", "description": "Returns a segment of a string.", "examples": ["MID(A, 2, 2)", "MID('Some middle characters!', 3, 4)"], "syntax": "MID(string, starting_at, extract_length)", "syntax_elements": [{"element": "string", "description": "The string or series to extract the segment from."}, {"element": "starting_at", "description": "The index from the left of string from which to begin extracting."}, {"element": "extract_length", "description": "The length of the segment to extract."}]}, {"function": "PROPER", "description": "Capitalizes the first letter of each word in a specified string.", "examples": ["=PROPER('nate nush')", "=PROPER(A)"], "syntax": "PROPER(string)", "syntax_elements": [{"element": "string", "description": "The value or series to convert to convert to proper case."}]}, {"function": "RIGHT", "description": "Returns a substring from the beginning of a specified string.", "examples": ["RIGHT(A, 2)", "RIGHT('The last character!')"], "syntax": "RIGHT(string, [number_of_characters])", "syntax_elements": [{"element": "string", "description": "The string or series from which the right portion will be returned."}, {"element": "number_of_characters [OPTIONAL, 1 by default]", "description": "The number of characters to return from the end of string."}]}, {"function": "SUBSTITUTE", "description": "Replaces existing text with new text in a string.", "examples": ["SUBSTITUTE('Better great than never', 'great', 'late')", "SUBSTITUTE(A, 'dog', 'cat')"], "syntax": "SUBSTITUTE(text_to_search, search_for, replace_with, [count])", "syntax_elements": [{"element": "text_to_search", "description": "The text within which to search and replace."}, {"element": "search_for", "description": " The string to search for within text_to_search."}, {"element": "replace_with", "description": "The string that will replace search_for."}, {"element": "count", "description": "The number of times to perform the substitute. Default is all."}]}, {"function": "TRIM", "description": "Returns a string with the leading and trailing whitespace removed.", "examples": ["=TRIM('  ABC')", "=TRIM('  ABC  ')", "=TRIM(A)"], "syntax": "TRIM(string)", "syntax_elements": [{"element": "string", "description": "The value or series to remove the leading and trailing whitespace from."}]}, {"function": "UPPER", "description": "Converts a given string to uppercase.", "examples": ["=UPPER('abc')", "=UPPER(A)", "=UPPER('Nate Rush')"], "syntax": "UPPER(string)", "syntax_elements": [{"element": "string", "description": "The string or series to convert to uppercase."}]}, {"function": "VALUE", "description": "Converts a string series to a number series.", "examples": ["=VALUE(A)", "=VALUE('123')"], "syntax": "VALUE(string)", "syntax_elements": [{"element": "string", "description": "The string or series to convert to a number."}]}, {"function": "DATEVALUE", "description": "Converts a given string to a date series.", "examples": ["DATEVALUE(A)", "DATEVALUE('2012-12-22')"], "syntax": "DATEVALUE(date_string)", "syntax_elements": [{"element": "date_string", "description": "The date string to turn into a date object."}]}, {"function": "DAY", "description": "Returns the day of the month that a specific date falls on, as a number.", "examples": ["DAY(A)", "DAY('2012-12-22')"], "syntax": "DAY(date)", "syntax_elements": [{"element": "date", "description": "The date or date series to get the day of."}]}, {"function": "MONTH", "description": "Returns the month that a specific date falls in, as a number.", "examples": ["MONTH(A)", "MONTH('2012-12-22')"], "syntax": "MONTH(date)", "syntax_elements": [{"element": "date", "description": "The date or date series to get the month of."}]}, {"function": "WEEKDAY", "description": "Returns the day of the week that a specific date falls on. 1-7 corresponds to Monday-Sunday.", "examples": ["WEEKDAY(A)", "WEEKDAY('2012-12-22')"], "syntax": "WEEKDAY(date)", "syntax_elements": [{"element": "date", "description": "The date or date series to get the weekday of."}]}, {"function": "YEAR", "description": "Returns the day of the year that a specific date falls in, as a number.", "examples": ["YEAR(A)", "YEAR('2012-12-22')"], "syntax": "YEAR(date)", "syntax_elements": [{"element": "date", "description": "The date or date series to get the month of."}]}]