# Bulkompare

Bulkompare is a tool to compare couples of datasets stored in csv-like files. 
A dataset corresponds to all the files with a same extension in a specified folder.

### Compare multiple sets simultaneously
Bulkompare can compare multiple couples of datasets independantly, each with their own settings.
For example, with directory A and directory B both containing `*.csv` and `*.tsv` files, Bulkcompare will compare
* the data from all merged `*.csv` files in directory A to the one from `*.csv` in directory B
* the data from all merged `*.tsv` files in directory A to the one from `*.tsv` in directory B


### Compare what you want, how you want
Lines do not need to be in the same file or in the same order to be compared. You can select:
* which columns identify a line (it can be a simple index column, or a combination of columns), 
* which columns should be compared
* which columns should be displayed in the results

### Comparison results
The results will show, for each extension:
* the differences found in each compared line
* the lines that could not be compared, 
  either because they were identified more than once in a dataset,
  or because they were found only in one dataset

### Save comparison settings
Configuring all the comparison details (file properties, selected columns ...) can take some time when files are complex.
These details can be exported to json files that can be imported later with a couple of clicks.
You can also define a default selection that is loaded with starting the app.

### Why ?
I developped Bulkompare as a validation tool for a complex software generating multiple kinds of csv files.


Note that this is a work in progress

## License
This project is licensed under GPL License due to the use of GPL libraries
