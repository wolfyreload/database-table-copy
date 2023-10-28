# Database Table Copy

Database Table Copy is a simple bcp wrapper to copy all the table data from one database
to another using the Microsoft bcp command line tool underneath

Note that this tool only works with Microsoft SQL Server and Microsoft Azure SQL.

I hope that you find this tool useful, however use at your own risk.

## Background

When you write software, you often need to copy database data from production to UAT or from production to development.

One way of doing this is to make a database backup (.bak file) and restore this backup on the other server. The problem
with this approach is that the .bak file is not backward compatible meaning that you cannot restore a SQL Server 2022
database backup to a SQL Server 2019 instance.

The next options is using the Generate Scripts feature in SSMS, however data is inserted one row at a time which can be 
rather slow when copying a 2 million+ row table.

Finally the last options is creating a SQL Server BACPAC file. The advantage of this solution is that the BACPAC file 
is backward compatible with older versions of SQL Server. But this solution much slower than creating a regular backup 
file. You also have the added risk when restoring the database in Azure where you accidently select the wrong tier and 
this can be a very costly mistake. 

I looked for an alternative solution and since I didn't find anything that worked for me. I've built my own solution to this
problem, and it even works with Microsoft Azure SQL.

## Requirements

* bcp version 18.2 or greater (included in SQL Server 2022 tools)
* ODBC Driver 17 or 18 for SQL Server

## Usage

* Download the version of the tool intended for your operating system.
* Add the tool to your path in environment variables
* Copy and tweak the example config.example.json file

After adding the program to your evironment path run the script below to run the application 

```bash
database-table-copy config_file
```

The structure of the config.json file:

* **bcp_path** - filesystem path to the bcp tool
* **source** - the database connection settings for the data that you want to export
* **target** - the database connection settings for the database that you want to import the source data into
* **working_folder** - the temp folder where the binary table data is written to which can be deleted after the import
* **exclude_table_list** - the list of tables which you want to skip (useful for log and auditing tables)

## Building

* Python 3.12 or greater
* pipenv (python virtual environment tool)
* pyenv (you can skip this one if you edit the version of python needed in the Pipfile)

Run build.sh or build.bat to build the application


