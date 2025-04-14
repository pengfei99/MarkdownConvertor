# Introduction of sas file

In SAS, the **.sas7bdat** file is a `binary data file` that stores datasets, and their metadata such as:
- variable (column) names
- types
- formats
- informat. 

Below is an example of sas file metadatat(contents).

| id | Variable     | Type | Len | Format    | Informat  | Label                                                                | 
|----|--------------|------|-----|-----------|-----------|----------------------------------------------------------------------|
| 1  | dt           | Num  | 8   | DATETIME. | DATETIME. | a very long label for testing accuracy of transformations            |
| 2  | string_dt    | Char | 19  | null      | null      | datetime (UTC) as character string                                   |
| 3  | timezone     | Char | 3   | null      | null      | null                                                                 | 
| 4  | dates        | Num  | 8   | DATE.     | DATE.     | null                                                                 |
| 5  | string_dates | Char | 10  | null      | null      | null                                                                 |       
| 6  | times        | Num  | 8   | TIME.     | TIME.     | null                                                                 | 
| 7  | string_times | Char | 8   | null      | null      | time of day as character string                                      |
| 8  | seconds      | Num  | 8   | 12.       | null      | this variable counts the number of seconds since 1960-01-01T00:00:00 | 
| 9  | missings     | Num  | 8   | null      | null      | a variable with some values missing                                  |

You can use below `sas code` to print the metadata of a sas file.
```sass
libname mylib 'D:\path\to\sas_sample';
proc contents data=mylib.project order=varnum;
run;
```

If you don't have SAS, you can use [pyreadstat](https://github.com/Roche/pyreadstat).

```python
import pyreadstat

df, meta = pyreadstat.read_sas7bdat("sas_sample.sas7bdat")

# Show column names
print("Column Names:")
print(meta.column_names)

# Show column types
print("\nColumn Types:")
print(meta.column_types)  # {'colname': 'numeric' or 'string'}

# Show column formats
print("\nColumn Formats:")
print(meta.column_formats)

# Show column informats (may be empty if not stored)
print("\nColumn Informats:")
print(meta.column_measure_levels)  # often used as a proxy

```

> We will use this example to illustrate how sas manages its metadata.

## 1. Column Type

`Column Type` defines how SAS internally stores the data in a column. In sas, a column can only have two possible types:
- Numeric (Num) :  is used for storing numeric data, including **integers, real numbers, and dates**
                           (since SAS stores dates as numeric values, representing the number of days `since January 1, 1960`).
                     The value is stored as `8-byte` floating-point numbers
- Character (Char): is used for storing text or string data. Character variables can include letters, numbers, 
                     and special characters. The length of a character variable is specified when the variable is created.
                      The max size of characters is 32,767.


## 2. Column Length


 The **column length (also called variable length)** refers to the `number of bytes` used to store the data for 
 that column in each row.
 
- For Numeric (Num) columns : The value is fixed as `8(8-bytes)`.
- For Character (Char) columns: The value can be between 1 and 32,767

## 3. Column Format

The **column format** controls how the data is displayed when output or printed. Below are some of the most 
commonly used SAS formats:
- General Numeric formats
- Currency Formats
- Character formats
- Date, Datetime, time, seconds formats
- Custom formats

### 3.1 General Numeric Formats:

- **w.d**: General numeric format, where w is the total width, and d is the number of decimal places. 
           Example: 8.2.
- **BESTw.**: The best representation of the data in w width. Example: BEST12..
- **COMMAw.d**: Numeric format with commas and a specified number of decimal places. Example: COMMA10.2.
- **Fw.d**:	Fixed width with decimals. The real value in the sas file is `12.3456`, with format `F6.2`, the display value will be `12.35`.
- **Zw.**:	Zero-padded integers. The real value in the sas file is `23`, with format `Z5.`, the display value will be `00023`.
- **PERCENTw.d**: Numeric format with a percent sign. Example: PERCENT8.2.

### 3.2 Currency Formats

- **DOLLARw.d**: Displays numbers with a dollar sign. Example: DOLLAR12.2 (produces $1,234.56).
- **EUROXw.d**: Displays numbers with an euro symbol. Example: EUROX12.2 (produces €1,234.56).

### 3.3 Special Numeric Formats:

- **PIBw.d**: Represents numbers in terms of binary prefixes (e.g., 1K for 1024). Example: PIB4..
- **HEXw.**: Converts numeric values to hexadecimal. Example: HEX4..

### 3.4 Character Formats

- **$w.**: Standard character format. `$` specifies it's a character format, `w` defines the max display width. 
           For example, `$20.` means reads and display data as character string of up to 20 characters(including 
            space). The character after 20 will be truncated.
- **$CHARw.**: Displays character data, maintaining leading and trailing spaces. Example: `$CHAR20.`.
- **$UPCASEw.**: Converts all letters to uppercase. For example, `$UPCASE20.` reads and display data as character, 
                and convert them to uppercase with `20` as max characters number.
- **$LOWCASEw.**: Converts all letters to lowercase. For example, `$LOWCASE10.` reads and display data as character, 
                and convert them to lowercase with `10` as max characters number.
- **$QUOTEw.**: Encloses character strings in quotation marks. For example, a value `casd` with format `$QUOTE20.` will 
                  be displayed as `"casd"`.


> The `width w` in the character formats are required, without it the format will be **invalid**.
>
### 3.5 Date, Datetime and Time Formats

The raw data are stored as numeric values. The format will convert them to human-readable value. We can 
divide them into three main categories:
- Datetime: Represents dates and times as the number of seconds since midnight on `January 1 1960`
- Date: Represents dates as the number of days since `January 1, 1960`. 
- Time: Represents the time of day as the number of seconds since midnight.

#### 3.5.1 Date formats

Dates in SAS are stored as the **number of days since Jan 1, 1960**. The display value depends on the associated format.

- **DATEw.**: Displays dates in the format ddMONyyyy. Example: DATE9. (produces 27AUG2024).
- **MMDDYYw.**: Displays dates in the format mm/dd/yy. Example: MMDDYY10. (produces 08/27/2024). MMDDYY8 (produces 08/27/24)
- **YYMMDDw.**: Displays dates in the format yyyy-mm-dd. Example: YYMMDD10. (produces 2024-08-27). YYMMDD8. (produces 24-08-27).
- **MONYY.**: Displays month and year.  Example: the stored value is 22916, the display value is APR2025.
- **YEAR4.**: Displays dates in the four digits year. Example: the stored value is 22916, the display value is 2025.
- **WEEKDATE.**: Displays day of week and full date. Example: the stored value is 22916, the display value is Friday, April 11, 2025



#### 3.5.2 Time Formats:

Times in SAS are stored as the **number of seconds since midnight**.

- **TIMEw.**: Displays time in the format hh:mm:ss. Example: TIME8. (produces 12:34:56).
- **HHMMw.**: Displays time in hours and minutes. Example: HHMM5. (produces 12:34).

#### 3.5.3 Datetime format

Datetimes in SAS are stored as the **number of seconds since Jan 1, 1960**

- **DATETIME.**: Displays the date and time in the format ddMMMyyyy:hh:mm:ss, where dd is the day of the month, 
          MMM is the abbreviation of the month, yyyy is the year, hh is the hour (in 24-hour format), mm is the minute, and ss is the second.
- **DATETIMEw.**: Displays both date and time. Example: DATETIME18. (produces 27AUG2024:12:34:56).
- **E8601DTw.**: ISO 8601 datetime format. Example: E8601DT20. (produces 2024-08-27T12:34:56).

### 3.6 Custom Formats

Users can create custom formats using the `PROC FORMAT` procedure in SAS.

```shell
# define a new format
proc format;
    value agegroup
        0 - 12 = 'Child'
        13 - 19 = 'Teenager'
        20 - 64 = 'Adult'
        65 - high = 'Senior';
run;

# apply a custom format on a column
data example;
    set old_data;
    format age agegroup.;
run;

```



## 4. Column Informat

The **column informat** tells SAS how to read and interpret raw data when it's being imported or read in 
(e.g., from a CSV or a text file).

Below is a list of informat examples:

- MMDDYY10: SAS will read a string as a date. For example, the input value "04/11/2025" with this `informat` will be translated to date.
- COMMA10: SAS will read "1,000" string as a numeric 1000.
- $CHAR20: SAS will read a `20-character string`. The characters which are larger than 20th character will be ignored.

## 5. Label

Label is the user defined description of the `variables(Columns)`. It can be nullable.