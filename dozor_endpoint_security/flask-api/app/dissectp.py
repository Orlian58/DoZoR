import logging
from pathlib import Path
from flow.record import RecordWriter
from dissect.target import Target

from dissect.target.exceptions import (
    FatalError,
    PluginNotFoundError,
    UnsupportedPluginError,
)
from dissect.target.loaders.targetd import ProxyLoader
from dissect.target.plugin import find_plugin_functions
from dissect.target.plugins.filesystem.yara import YaraPlugin
from dissect.target.tools.utils import (
    catch_sigpipe,
    execute_function_on_target,
)

log = logging.getLogger(__name__)
logging.lastResort = None
logging.raiseExceptions = False


@catch_sigpipe
# args {"targets":[], "func":[]}
def artifact(args, path_to_output) -> str:

    if not args["func"] or not args["targets"]or not args["hash"]:
        raise UserWarning("Слишком мало аргументов")

    for target in args["targets"]:
        plugin_target = Target.open(target)

        if isinstance(plugin_target._loader, ProxyLoader):
            raise UserWarning("Совместимые плагины для целей отсутствуют")
        
        funcs, _ = find_plugin_functions(plugin_target, args["func"], True, show_hidden=True)
        
    funcs, invalid_funcs = find_plugin_functions(Target(), args["func"], compatibility=False)

    if any(invalid_funcs):
        raise UserWarning(f"Содержит недопустимые плагины: {', '.join(invalid_funcs)}")

    for target in Target.open_all(args["targets"]):
        record_entries = []
        executed_plugins = set()
        func_defs, _ = find_plugin_functions(target, args["func"], compatibility=False)

        for func_def in func_defs:
            executed_plugins.add(func_def.name)

            try:
                output_type, result, _ = execute_function_on_target(
                    target, func_def
                )
            except UnsupportedPluginError as e:
                target.log.error(
                    "Неподдерживаемый плагин для %s: %s",
                    func_def.name,
                    e.root_cause_str(),
                )

                target.log.debug("%s", func_def, exc_info=e)
                continue
            except PluginNotFoundError:
                target.log.error("Плагин не найден `%s`", func_def)
                continue
            except FatalError as fatal:
                fatal.emit_last_message(target.log.error)
            except Exception:
                target.log.error("Исключение при выполнении функции `%s`", func_def, exc_info=True)
                continue

            if output_type == "record":
                record_entries.append(result)

        if len(record_entries):
            rs = ""

            for entry in record_entries:
                try:
                    for record_entries in entry:
                        rs += str(record_entries)

                except Exception as e:
                    if len(funcs) > 1:
                        target.log.error(f"Исключение произошло при обработке вывода {args['func']}", exc_info=e)
                    else:
                        raise e
            return rs
        return ""
                    
@catch_sigpipe
# args {"targets": [], "path": [], "size": []}
def yara(args, path_to_output, path_to_yara) -> str:

    if not args["targets"] or not args["path"]\
        or not args["size"] or not args["hash"]\
        or not args["rule"]:
        raise UserWarning("Слишком мало аргументов")

    for target in Target.open_all(args["targets"]):
        target = YaraPlugin(target)

        try:
            target.check_compatible()
        except UnsupportedPluginError as e:
            target.log.error(
                "Неподдерживаемый плагин для %s: %s",
                target.name,
                e.root_cause_str(),
            )
            target.log.debug("%s", target.name, exc_info=e)
            continue
        except Exception:
            target.log.error("Исключение при выполнении функции `%s`", target.name, exc_info=True)
            continue

        rs = ""
        

        for entry,_ in target.yara(list(map(lambda s: Path(path_to_yara + s), args["rule"].split(r","))), args["path"], int(args["size"])):
            try:
                rs += str(entry)

            except Exception as e:
                target.log.error(f"Исключение произошло при обработке вывода yara", exc_info=e)
        return rs
    return ""