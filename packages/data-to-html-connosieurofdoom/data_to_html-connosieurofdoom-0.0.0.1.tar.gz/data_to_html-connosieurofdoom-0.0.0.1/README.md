# data_to_html
Library to convert pandas Dataframes to different html elements

## Table:
### Input: 
    1. Pandas Dataframe (df): The dataframe containing the data to be converted to html table (Required), 
    2. column order (col): A list item containing the column names of the dataframe in the order in which they are to be displayed. (Default: None (Returns the columns in the order as in the dataFrame)) | (Optional)
    3. The rest is same as pandas to_html: (Refer link)[https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html]

### Ouput:
    1. Returns an html formatted table from the dataframe

### Sample:

```python
dtl = table(dtl)
```


## Select:
### Input:
    1. Pandas DataFrame (df): The data frame to be converted to html Select | (Required)
    2. text (text): Column to be displayed between the option tage | (Required)
    3. value (value): Column for the value attribute in the option tag | (Required)
    4. id (id): Value for the id attribute in the select tag | (Optional) | (Default None)
    5. classes (classes): Values for the classes attribute for html| Type : List |(Optional) ! (Default None)
    6. placeholder (placeholder): Value for placeholder attribute | (Optional) | (Default None)
    7. additional_attribute: Any additional attributes | (Optional) | (Default "")
    8. multiple: Optional | Default False
    9. onchange : Optional | Default None

### Output:
    1.	A html format select statement with the options as the column values of the dataframes

```python
dtl = select(dtl, text = "col1", value = "col2", id = "id", classes = ["class1", "class2"], placeholder="data-placeholder")
```