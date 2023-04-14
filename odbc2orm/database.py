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


class OdbcColumn( object ):
    def __init__(self, column: list ):
        self.__columns = list( column )
        return

    @property
    def table_cat( self ):
        return self.__columns[ 0 ]

    @property
    def schema( self ):
        return self.__columns[ 1 ]

    @property
    def table_name( self ):
        return self.__columns[ 2 ]

    @property
    def column_name( self ):
        return self.__columns[ 3 ]

    @property
    def data_type( self ):
        return self.__columns[ 4 ]

    @property
    def type_name( self ):
        return self.__columns[ 5 ]

    @property
    def column_size( self ):
        return self.__columns[ 6 ]

    @property
    def buffer_length( self ):
        return self.__columns[ 7 ]

    @property
    def decimal_digit( self ):
        return self.__columns[ 8 ]

    @property
    def num_spec_radix( self ):
        return self.__columns[ 9 ]

    @property
    def nullable( self ):
        return self.__columns[ 10 ]

    @property
    def remarks( self ):
        return self.__columns[ 11 ]

    @property
    def column_default( self ):
        return self.__columns[12]

    @property
    def sql_data_type( self ):
        return self.__columns[ 13 ]

    @property
    def sql_datetime_sub( self ):
        return self.__columns[ 14 ]

    @property
    def char_octet_length( self ):
        return self.__columns[ 15 ]

    @property
    def ordinal_position( self ):
        return self.__columns[ 16 ]

    @property
    def is_nullable( self ):
        return self.__columns[ 17 ]

    @property
    def ordinal( self ):
        return self.__columns[ 18 ]

    def __repr__(self):
        return f"<MdbColumn {self.ordinal} name='{self.column_name}' type='{self.type_name}' length={self.buffer_length} decimal_digit={self.decimal_digit} nullable={self.nullable} default='{self.column_default}'>"


class OdbcTable( list ):
    def __init__( self, table: list ):
        super().__init__()
        self.__catalog = None
        self.__schema = None
        self.__name = None
        for col in table:
            self.append( OdbcColumn( col ) )

        return

    def append( self, item ) -> None:
        super().append( item )
        self.__catalog    = item.table_cat
        self.__scheme     = item.schema
        self.__name       = item.table_name
        return

    @property
    def name( self ):
        return self.__name

    @property
    def scheme( self ):
        return self.__scheme

    @property
    def catalog( self ):
        return self.__catalog


class OdbcTables( list ):
    def __init__( self, mdb_connection ):
        super().__init__()
        crsr = mdb_connection.cursor()
        for table_name in [ x[ 2 ] for x in crsr.tables() if x[ 3 ] == 'TABLE' ]:
            self.append( crsr.columns( table_name ) )

        crsr.close()
        return

    def append( self, table: list ):
        super().append( OdbcTable( [x for x in table] ) )
        return
