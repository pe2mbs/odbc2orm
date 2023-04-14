# odbc2orm - Convert ODBC schema to sqlalchemy ORM schema
# Copyright (C) 2034  Marc Bertens-Nguyen  <m.bertens@pe2mbs.nl>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
import os.path
from datetime import datetime
from mako.template import Template
from odbc2orm.database import OdbcColumn, OdbcTable, OdbcTables
import odbc2orm.template as TEMPLATE
import odbc2orm.config as API
from odbc2orm.version import *


def convert( mdb_connection, output_stream ):
    def write_output( output ):
        print( output, file = output_stream, end = '' )
        if API.CONFIG.get( 'verbose', False ):
            print( output, end = '' )

        return

    tables = OdbcTables( mdb_connection )
    write_output( Template( TEMPLATE.leadin ).render( config = API.CONFIG,
                                                      datetime = datetime,
                                                      version = version,
                                                      copyright = copyright,
                                                      author = author,
                                                      username = os.environ.get( 'USERNAME', 'unknown' ) ) )
    for table in tables:
        table: OdbcTable
        print( f"Writing table {table.name}")
        write_output( Template( TEMPLATE.table_leadin ).render( config = API.CONFIG, table = table ) )
        for column in table:
            write_output(Template( TEMPLATE.table_column ).render( config = API.CONFIG, table = table, column = column ) )

        write_output( Template( TEMPLATE.table_leadout ).render( config = API.CONFIG, table = table ) )

    write_output( Template( TEMPLATE.leadout ).render( config = API.CONFIG,
                                                       datetime = datetime,
                                                       version = version,
                                                       copyright = copyright,
                                                       author = author,
                                                       username = os.environ.get( 'USERNAME', 'unknown' ) ) )
    return

