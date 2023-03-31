#!/usr/bin/env python3
import argparse
import cmd, sys
import pandas as pd
import readline
from playhouse.db_url import connect


class SqlShell(cmd.Cmd):
    def __init__(self,completekey='tab', stdin=None, stdout=None,sql_uri=None):
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        self.uri = sql_uri or "sqlite:///:memory:"
        self.db = connect(self.uri)
        self.db.connect()
        self.intro = 'Welcome to the sql shell.   Type help or ? to list commands.\n'
        self.prompt = "("+self.uri.split("://")[0]+" <<<)"
        self.file = None
        self.sql_string = ""
    
    
    def _run_sql(self):
        try:
            q = self.db.execute_sql(self.sql_string,require_commit=False)
        except Exception as e:
            print(type(e))
            print(str(e))
        else:
            if q.description:
                titles = [i[0] for i in q.description]
                rows = q.fetchall()
                t = [{t:v for (t,v) in zip(titles,i)} for i in rows]
                table = pd.DataFrame(t)
                print("+++++++++++Result+++++++++++")
                print(table.to_string())
                #print(titles)
                #print(rows)
                print("++++++++++++++++++++++++++++")
            else:
                print('done!')

    # ----- basic turtle commands -----
    def default(self, string):
        self.sql_string += string.strip()
        if self.sql_string.endswith(";"):
            print(self.sql_string)
            self._run_sql()
            self.sql_string = ""
            
    def do_uri(self, arg):
        print(self.uri)
    
    def do_bye(self, arg):
        'Stop recording, close the sqlshell window, and exit:  BYE'
        print('Thank you for using This tool')
        self.close()
        self.db.close()
        return True
    
    def do_exit(self, arg):
        return self.do_bye(arg)
    
    def do_quit(self, arg):
        return self.do_bye(arg)

    # ----- record and playback -----
    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')
    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())
    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line
    def close(self):
        if self.file:
            self.file.close()
            self.file = None
            
def shell(args):
    SqlShell(sql_uri = args.dburi).cmdloop()
            
def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--dburi", help=u"指定dburi",type=str)
    parser.set_defaults(func=shell)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main(argv=sys.argv[1:])