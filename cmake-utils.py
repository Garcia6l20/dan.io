from pathlib import Path
from dan.cli import click
from dan.make import Make
from dan.core.pm import re_match

@click.group()
def cli():
    pass

@cli.command()
@click.option('-p', '--prefix')
@click.argument('BUILD_PATH')
@click.argument('TARGET')
async def gen_options(prefix, build_path, target):
    make = Make(Path(build_path), quiet=True)
    await make.initialize()
    for makefile in make.context.all_makefiles:
        t = makefile.find(target)
        if t:
            out, err, rc = await t._cmake('-S', './sources', '-LH', log=False)
            cmake_options = dict()
            doc = None
            for line in out.splitlines():
                match re_match(line.strip()):
                    case r'^(.+):(\w+)=(.+)$' as m:
                        name = m[1]
                        tp = m[2]
                        value = m[3]
                        match tp:
                            case 'STRING':
                                pass
                            case 'BOOL':
                                value = value.lower() in ('on', 'true', 'yes')
                            case 'PATH'|'FILEPATH':
                                value = Path(value)
                            case _:
                                t.warning('unhandled cmake type: %s', tp)
                        if prefix is not None:
                            if name.startswith(prefix):
                                dan_name = name.lower().removeprefix(prefix.lower())
                                cmake_options[dan_name] = (name, value, doc)
                        else:
                            dan_name = name.lower()
                            cmake_options[dan_name] = (name, value, doc)
                    case r'^// (.+)$' as m:
                        doc = m[1]
            click.echo(cmake_options)
            return

if __name__ == '__main__':
    import sys
    sys.exit(cli())
