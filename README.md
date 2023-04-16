# odbc2orm
This package convert an ODBC schema into a sqlalchemy ORM schema.
Its primary written for MS Access schemas, but it should work for all ODBC 
relational databases. for this only the driver should be configured. And for 
the target project extra packages may be needed (see **Required packages for target project**).


# Licence
This package is under GNU GENERAL PUBLIC LICENSE, Version 2 only
See LICENCE file for the GNU GENERAL PUBLIC LICENSE, Version 2, June 1991


# Required packages for target project
Assumming **sqlalchemy** is already in your project. The following two 
packages are required when accessing MS Access databases; 
* sqlalchemy-access
* pyodbc

For other ODBC database connections other packages may be required. 
Currently this package is tested with MS Access databases.


# Usage
```shell

> python -m odbc2orm database.mdb

```


## Options
The following options are available at command line. 

    -v                      Verbose output.

    -V/--version            version output 

    -h/--help               This help information.
   
    -o/--output <filename>  write Python code file, instead of stdout.
                            default STDOUT   
    
    -c/--config <filename>  Configure driver, output and template files.

    -d/--driver <driver>    The ODBC driver to be used,
                            default "Microsoft Access Driver (*.mdb, *.accdb)"

    -D/--dump               Include the dump_tables() function in the output,
                            default: False

    -t/--template <folder>  Create template files and configuration YAML file
                            for personal customizing.                         

When using a configuration file **--output** and **--driver** may override the configuration 
by setting those after the configuration option.


# Configuration 
A default configuration file can be created through the **--template** option.

Typical configuration file looks like this;
```YAML
driver: Microsoft Access Driver (*.mdb, *.accdb)
template:
  leadin: custom\template\leadin,templ
  leadout: custom\template\leadout.templ
  table_column: custom\template\table_column.templ
  table_leadin: custom\template\table_leadin.templ
  table_leadout: custom\template\table_leadout.templ
verbose: false
include_dump: false,
```
The **template** section are the Mako template files to generate the ORM schema 
Python file.


# Templates
By using the **--template** command line option the standard templates and configuration
is exported to a specified folder. This gives the opportunity to customize the generation
of the output of the application.


## leadin and leadout
The leadin and leadout templates receive the following variables;
* **config**; dictionary with configuration as being used during generation.
* **datetime**; Python datetime module.
* **version**; string with the version of odbf2orm module.
* **copyright**; string with the copyright of odbf2orm module.
* **author**; string with the author of odbf2orm module.
* **username**; string with the current username from the Operating System.


## table_leadin and table_leadout 
The table_leadin and table_leadout templates receive the following variables;
* **config**; dictionary with configuration as being used during generation.
* **table**; OdbcTable object


## table_column
The table_column template receive the following variables;
* **config**; dictionary with configuration as being used during generation.
* **table**; OdbcTable object
* **column**; OdbcColumn object


# ODBC objects
## OdbcTable
The OdbcTable object is actual a list object with extra properties, the list contains the OdbcColumn objects.


## Extra properies
* **name**; string with the table name.
* **catalog**; string with catalog name where the table belong to.
* **schema**; string with schema name where the table belong to.


## OdbcColumn
The OdbcColumn object contains the column properies;  

* **table_cat**; string with catalog name where the column belong to.
* **schema**; string with schema name where the column belong to.
* **table_name**; string with the table name.
* **column_name**; string with column name. 
* **data_type**; integer with the column data type, see for more information https://github.com/mkleehammer/pyodbc/wiki/Data-Types
* **type_name**; string with the column type name, see for more information https://github.com/mkleehammer/pyodbc/wiki/Data-Types
* **column_size**; the number of octets that are used to store the column data
* **buffer_length**; the number of octets that are used for the internal buffer in pyodbc
* **decimal_digit**; the number of decimal fraction digitis. 
* **num_spec_radix**; ?
* **nullable**; integer (1/0) (**True**/**False**) if the column is nullable. 
* **remarks**; string a description of the column.
* **column_default**: the column dafault value
* **sql_data_type**; ? 
* **sql_datetime_sub**; ?
* **char_octet_length**; integer 
* **ordinal_position**; integer with the column position in the row.
* **is_nullable**; string (**"YES"**/**"NO"**) if the column is nullable. 
* **ordina**l; integer same as **ordinal_position**.

For some databases there are more properies available, those are not supported.
