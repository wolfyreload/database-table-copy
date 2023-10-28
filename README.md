# Database Table Copy

Database Table Copy is a simple bcp wrapper to copy all the table data from one database
to another using the Microsoft bcp command line tool underneath

Note that this tool only works with Microsoft SQL Server and Microsoft Azure SQL.

I hope that you find this tool useful, however use at your own risk.

## Background

When you write software, you often need to copy database data from production to UAT or from production to development.

Especially if you are working in Azure, getting the data out can be a very time-consuming process. The typical route
would be to create a backup of the database and then restore that backup in another environment. However, you make sure
don't accidentally configure the new database to be in the wrong tier as this can be a very costly mistake. Now, you
could probably script out the backup and restore process, but unfortunately, the scripted process forces you to script
out all the tables, and it is very slow.

So the tool was written to just copy the tables from one database to another, and it even works with Microsoft Azure SQL.

## Requirements

* bcp version 18.2 or greater (included in SQL Server 2022 tools)
* ODBC Driver 17 or 18 for SQL Server

## Usage

* Download the version of the tool intended for your operating system.
* Add the tool to your path in environment variables
* Copy and tweak the example config.example.json file

```bash
database-table-copy config.json
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

Run build.sh or build.bat to build the application


