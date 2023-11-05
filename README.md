# Database Table Copy

Database Table Copy is a simple Microsoft bcp wrapper to copy all table data from one database to another.

Please note that this tool only works with Microsoft SQL Server and Microsoft Azure SQL.

I hope you find this tool useful, but use it at your own risk.

## Background

When writing software, you often need to copy database data from production to UAT or from production to development.

One way of doing this is to create a database backup (.bak file) and restore it to the other server. The problem
with this approach is that the .bak file is not backward compatible, meaning that you cannot restore a SQL Server 2022
database backup to a SQL Server 2019 instance.

The next option is to use the Generate Scripts feature in SSMS, but this inserts the data one row at a time, which can
be
slow when copying a table with over two million rows.

Finally, the last option is to create a SQL Server BACPAC file. The advantage of this solution is that the BACPAC file
is
backward compatible with older versions of SQL Server. However, this solution is much slower than creating a regular
backup
file. You also have the added risk when restoring the database in Azure of accidentally selecting the wrong tier and
which can
be a very costly mistake.

I looked for an alternative solution and as I didn't find anything that worked for me. I've built my own solution to
solve this
problem and it even works with Microsoft Azure SQL.

## Requirements

* bcp version 18.2 or greater (included in SQL Server 2022 tools)
* ODBC Driver 17 or 18 for SQL Server

## Usage

* Download the version of the tool intended for your operating system.
* Add the tool to your path in environment variables
* Copy and tweak the example config.example.json file

After adding the program to your environment path run the script below to run the application

```bash
database-table-copy config_file
```

The structure of the config.json file:

* **source** - the database connection settings for the data that you want to export
* **target** - the database connection settings for the database that you want to import the source data into
* **working_folder** - the temp folder where the binary table data is written to which can be deleted after the import
* **exclude_table_list** - the list of tables which you want to skip (useful for log and auditing tables)

## Docker Usage

The docker version does not need the bcp or odbc drivers installed locally.

For the docker version, please do not edit the bcp_path. For getting started, copy contents of the **test** folder to 
your local. Now make a copy of **config.example.json** and name it **config.json**

Edit the **source**, **target** and **exclude_table_list** sections in the config file.

Note: If you are trying to import the table data to your local machine, use the ip address 172.17.0.1 in your config
file.

Note 2: You need to enable Mixed Mode authentication and TCP/IP connectivity for this solution to work on Windows
(only needed if you are using your local machine as the source or target).

Run the sh script with ```bash docker-run.sh```

If you get any errors, look at the log output and debug.

## Building

* Python 3.12 or greater
* pipenv (python virtual environment tool)
* pyenv (you can skip this one if you edit the version of python needed in the Pipfile)

Run build.sh or build.bat to build the application


