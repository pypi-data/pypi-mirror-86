import pandas as pd

class Error(Exception):
	"""Base class for other exceptions"""
	pass

class ArgumentMissingError(Error):
	def __init__(self, func, vars):
		self.message = "Argument missing or None | Arguments: {}".format(vars)

	def __str__(self):	
		return self.message

class ArgumentError(Error):
	def __init__(self, func, vars):
		self.message = "Argument has incorrect type | Arguments: {}".format(vars)

	def __str__(self):	
		return self.message


def table(df = None, col = None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, justify=None, max_rows=None, max_cols=None, show_dimensions=False, decimal='.', bold_rows=True, classes=None, escape=True, notebook=False, border=None, table_id=None, render_links=False, encoding=None):
	# Input: 
		#   Pandas Dataframe (df): The dataframe containing the data to be converted to html table (Required), 
		#   column order (col): A list item containing the column names of the dataframe in the order in which they are to be displayed. (Default: None (Returns the columns in the order as in the dataFrame)) | (Optional)
		#   The rest is same as pandas to_html: (Refer link)[https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_html.html]

	# Ouput:
		# Returns an html formatted table from the dataframe

	if df == None:
		raise ArgumentMissingError(table, locals())

	if isinstance(df, pd.DataFrame) == False:
		raise ArgumentError(select, locals)

	if col != None:
		df = df[col]

	return pd.DataFrame.to_html(df, col_space = col_space, header = header, index = index, na_rep = na_rep, formatters = formatters, float_format = float_format, sparsify = sparsify, index_names = index_names, justify=justify, max_rows=max_rows, max_cols=max_cols, show_dimensions=show_dimensions, decimal=decimal, bold_rows=bold_rows, classes=classes, escape=escape, notebook=notebook, border=border, table_id=table_id, render_links=render_links, encoding=encoding)


def select(df = None, text = None, value = None, id = None, classes = None, placeholder = None, additional_attributes = "", multiple = False, onchange=None):
	# Input:
		#   Pandas DataFrame (df): The data frame to be converted to html Select | (Required)
		#   text (text): Column to be displayed between the option tage | (Required)
		#   value (value): Column for the value attribute in the option tag | (Required)
		#   id (id): Value for the id attribute in the select tag | (Optional) | (Default None)
		#   classes (classes): Values for the classes attribute for html | Type : (List|Str) | (Optional) ! (Default None)
		#   placeholder (placeholder): Value for placeholder attribute | (Optional) | (Default None)
		#   additional_attribute: Any additional attributes | (Optional) | (Default "")
		#   multiple: Optional | Default False
		#   onchange : Optional | Type: Str | Default None

	# Output:
		#	A html format select statement with the options as the column values of the dataframes

	if df == None or text == None or value == None or text == None:
		raise ArgumentMissingError(table, locals())

	if isinstance(df, pd.DataFrame) == False or isinstance(text, str) or isinstance(value, str) :
		raise ArgumentError(select, locals())

	args_list = ""

	if type(classes) is list:
		classes = " ".join(classes)
	else:
		pass

	args_dict = {"id":id, "class":classes, "data-placeholder": placeholder, "onchange":onchange}
	# print(args_dict)

	for i in args_dict.keys():
		if args_dict[i] != None and args_dict[i]!= False:
			args_list += str(i) + '="' + str(args_dict[i]) + '"	'

	if multiple:
		args_list += "  multiple"
	
	args_list += additional_attributes

	# print(args_list)

	tag_open = """<select {}>
				""".format(args_list)
	# print(tag_open)

	if multiple:
		tag_open += "<option></option>"

	template = """<option value="{}"> {} </option>
				"""
	tag_closed = """</select>
				"""
	for j,i in df.iterrows():
		tag_open += template.format(i[value],i[text])
		# print(i[value],i[text])

	tag_open += tag_closed

	# print(tag_open, args_dict, args_list)

	return tag_open