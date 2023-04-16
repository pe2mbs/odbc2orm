import sys
import os
import yaml
import odbc2orm.config


leadin = """#
# This file was created by odbc2orm.py ${version} Copyright (C) ${copyright} ${author}
# odbc2orm.py comes with ABSOLUTELY NO WARRANTY. This is free software,
# and you are welcome to redistribute under GNU General Public License, version 2 only
#
# Source file created: ${username} at ${datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )}
# from ${database} with driver ${config.get( 'driver', 'unknown' )} 
#
from typing import Optional
import pyodbc
from sqlalchemy import Column, String, Integer, Text, Boolean, DECIMAL, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


"""

table_leadin = """
class ${table.name.replace(' ','_')}( Base ):
    __tablename__            = '${table.name}'
"""

table_column = """%if column.type_name in ( "COUNTER", "INTEGER" ):
 %if column.ordinal == 1:
    ${column.column_name.ljust(24)} = Column( Integer, primary_key = True )
 %else:
    ${column.column_name.ljust(24)} = Column( Integer, nullable = ${bool(column.nullable)} )
 %endif    
%elif column.type_name == "VARCHAR":
    ${column.column_name.ljust(24)} = Column( String( ${column.column_size} ), nullable = ${bool(column.nullable)} )
%elif column.type_name == 'DOUBLE':
    ${column.column_name.ljust(24)} = Column( FLOAT, nullable = ${bool(column.nullable)} )
%elif column.type_name == 'DECIMAL':
    ${column.column_name.ljust(24)} = Column( DECIMAL( ${column.column_size}, ${column.decimal_digit} ), nullable = ${bool(column.nullable)} )
%elif column.type_name == 'LONGCHAR':
    ${column.column_name.ljust(24)} = Column( Text, nullable = ${bool(column.nullable)} )
%elif column.type_name == "BIT":
    ${column.column_name.ljust(24)} = Column( Boolean, nullable = ${bool(column.nullable)} )
%else:
    # TODO: This was an undefined/unknown data-type, correct the configuration
    ${ str( column ) }
%endif"""



table_leadout = """<%    
def fields2repr( columns ):
    fields = []
    for column in columns:
        if column.ordinal == 1:
            fields.append( f"{{self.{column.column_name}}}" )

        else:
            fields.append( f"{column.column_name} = '{{self.{column.column_name}}}'" )

    return ", ".join( fields )
%>        
    def __repr__(self):
        return f"<${table.name} ${fields2repr(table[:4])}>"

"""

leadout = """
__engine = None
__session = None
__connection = None


def getEngine( database: Optional[str] = None ):
    driver = '${ config.get('driver','' ) }'
    if not datanase:
        # This the file with this file was created. 
        database = '${database}'
          
    connection_string = f"DRIVER={{{driver}}};DBQ={database};;ExtendedAnsiSQL=1;"
    connection_url = engine.URL.create( "access+pyodbc",
                                        query = { "odbc_connect": connection_string } )
    __engine = create_engine( connection_url )
    __connection = __engine.connect()  
    return __connection 


def getConnection():
    return __connection


def getSession():
    if not __engine:
        raise Exception( "Connection not opened yet." )

    if __session:
        return __session

    SessionObject = sessionmaker( bind = dbengine )
    __session = SessionObject()
    return __session


%if config.get( 'include_dump', False ):
def dump_tables():
    getEngine()
    session = getSession()
%for table in tables:
    # Dump contents of table '${table.name}'
    for rec in session.query( ${table.name.replace(' ','_')} ).all():
        print( rec )

%endfor
    return


if __name__ == '__main__':
    dump_tables()

%endif
"""


def create_template_config( folder ):
    config = {
        "template": {
            "leadin": os.path.join( folder, 'template', 'leadin,templ' ),
            "table_leadin": os.path.join( folder,'template', 'table_leadin.templ' ),
            "table_column": os.path.join( folder, 'template', 'table_column.templ' ),
            "table_leadout": os.path.join( folder, 'template', 'table_leadout.templ' ),
            "leadout": os.path.join( folder, 'template', 'leadout.templ' )
        },
        "driver": odbc2orm.config.DEFAULT_DRIVER,
        "verbose": False,
        "include_dump": False,
    }
    module = sys.modules[ __name__ ]
    os.makedirs( os.path.join( folder, 'template' ), exist_ok=True )
    for name, filename in config.get( 'template', {} ).items():
        with open( filename, 'wt+' ) as stream:
            stream.write( getattr( module, name ) )

    with open( os.path.join( folder, 'config.yaml' ), 'wt+' ) as stream:
        yaml.dump( config, stream, Dumper=yaml.Dumper )

    return

