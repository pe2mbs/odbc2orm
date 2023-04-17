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
import os
import yaml
import sys
import pyodbc
import getopt
import traceback
import odbc2orm.template as TEMPLATE
import odbc2orm.version as info
from odbc2orm.convert import convert
import odbc2orm.config as API
from odbc2orm.template import create_template_config


def banner():
    print(f"""Convert ODBC schema to ORM, version {info.version} Copyright (C) {info.copyright} {info.author}
odbc2orm.py comes with ABSOLUTELY NO WARRANTY. This is free software, 
and you are welcome to redistribute under GNU General Public License, version 2 only 
""")
    return


def usage():
    banner()
    print(f"""
Syntex:
    odbc2orm <options> <ODBC database>

or
    python -m odbc2orm <options> <ODBC database>    

Options:
-v                      Verbose output.
-h/--help               This help information. 
-o/--output <filename>  write Python code file, instead of stdout.
                        default STDOUT   
-c/--config <filename>  Configure driver, output and template files.
-d/--driver <driver>    The ODBC driver to be used,
                        default "Microsoft Access Driver (*.mdb, *.accdb)"
-D/--dump               Include dump function in output file.                         
-t/--template <folder>  Create template files and configuration YAML file
                        for personal customizing.                         
""")


def main():
    ALLOWED_TEMPLATES = ( 'leadin', 'table_leadin', 'table_column', 'table_leadout', 'leadout' )
    output_stream = sys.stdout
    odbc_connection = None
    try:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ho:c:vlt:VD", ["help", "licence", "output=", "config=", "template=", "version", "dump" ] )

        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            usage()
            sys.exit(2)

        driver = API.DEFAULT_DRIVER
        dump = False
        for o, a in opts:
            if o == "-v":
                API.CONFIG['verbose'] = True

            elif o in ("-h", "--help"):
                usage()
                sys.exit()

            elif o in ("-V", "--version"):
                print( f"{info.version}" )
                sys.exit()

            elif o in ("-t", "--template"):
                banner()
                create_template_config( a )
                sys.exit()

            elif o in ("-d", "--driver"):
                driver = a

            elif o in ("-D", "--dump"):
                dump = True

            elif o in ("-o", "--output"):
                output_stream = open(a, 'wt')

            elif o in ("-c", "--config"):
                with open(a, 'r') as stream:
                    API.CONFIG = yaml.load(stream, Loader=yaml.Loader)

                API.CONFIG[ 'verbose' ] = API.CONFIG.get( 'verbose', False )
                for name, filename in API.CONFIG.get( 'template', {} ).items():
                    if name not in ALLOWED_TEMPLATES:
                        assert False, f"{name} Is not a correct template name."

                    if filename:
                        if os.path.exists(filename):
                            with open(filename, 'r') as stream:
                                setattr(TEMPLATE, name, stream.read())

                        else:
                            assert False, f"{filename} Doesn't exist."

                output = API.CONFIG.get('output', None)
                if output:
                    output_stream = open(output, 'wt')

            else:
                assert False, "unhandled option"

        API.CONFIG[ 'include_dump' ] = dump
        API.CONFIG[ 'verbose' ] = False if output_stream == sys.stdout else API.CONFIG.get('verbose', False)
        if len(args):
            database_filename = args[0]

        else:
            assert False, "No database filename given."

        banner()
        driver = API.CONFIG.get('driver', driver)


        convert( driver, database_filename, output_stream )

    except SystemExit:
        pass

    except:
        print( traceback.format_exc(), file = sys.stderr )

    finally:
        if odbc_connection:
            odbc_connection.close()

        if output_stream and output_stream != sys.stdout:
            output_stream.close()

    return


if __name__ == '__main__':
    main()
