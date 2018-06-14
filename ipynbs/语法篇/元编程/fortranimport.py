import os
import sys
import hashlib
import shutil
import warnings
from pathlib import Path
import importlib
from importlib.abc import (
    MetaPathFinder,
    PathEntryFinder,
    Loader
)
from importlib.machinery import ModuleSpec

from numpy import f2py


class FortranImportLoader(Loader):
    def __init__(self, source_path):
        self._source_path = source_path
        with open(str(self._source_path), "rb") as f:
            self.source = f.read()
        self.source_hash = hashlib.md5(self.source)
        self.wrap_spec = None

    def _check_source(self):
        with open(str(self._source_path), "rb") as f:
            source = f.read()
        source_hash = hashlib.md5(source)
        if self.source_hash == source_hash:
            return False
        else:
            self.source_hash = source_hash
            self.source = source
            return True

    def _compile(self):
        modulename = self._source_path.stem
        suffix = self._source_path.suffix
        complie_result = f2py.compile(
            self.source,
            modulename=modulename,
            verbose=False,
            extra_args="--quiet", 
            extension=suffix
        )
        if complie_result != 0:
            raise ImportError("complie failed")
        else:
            root = Path(".").resolve()
            find_files = [
                i for i in root.iterdir() if i.match(f"{modulename}*.pyd") or i.match(f"{modulename}*.so")
            ]
            if len(find_files) != 1:
                raise ImportError(f"find {len(find_files)} Dynamic Link Library")
            file = find_files[0]
            target_path = self._source_path.with_name(file.name)
            if file != target_path:
                try:
                    shutil.move(str(file), str(target_path))
                except shutil.SameFileError as sfe:
                    pass
                except Exception as e:
                    raise e
            del_target = [i for i in root.iterdir() if i.match(str(file)+".*")]
            for i in del_target:
                try:
                    i.chmod(0o777)
                    i.unlink()
                except Exception as e:
                    warnings.warn(f'can not delete file {i}:{type(e)}--{e}', UserWarning)
            return target_path

    def create_module(self, spec):
        self._check_source()
        target_path = self._compile()
        self.wrap_spec = importlib.util.spec_from_file_location(
            spec.name,
            str(target_path)
        )
        mod = importlib.util.module_from_spec(self.wrap_spec)
        mod = sys.modules.setdefault(spec.name, mod)
        return mod

    def exec_module(self, module):
        """在_post_import_hooks中查找对应模块中的回调函数并执行."""
        self.wrap_spec.loader.exec_module(module)
        


class FortranImportFinder(MetaPathFinder):

    def find_spec(self, fullname, paths=None, target=None):
        relative_path = fullname.replace(".", "/")
        base_path = None
        full_path = None

        for path in sys.path:
            base_path = Path(path).resolve()
            abs_path = base_path.joinpath(relative_path)
            if abs_path.with_suffix(".f").exists():
                full_path = abs_path.with_suffix(".f")
                break
            elif abs_path.with_suffix(".f90").exists():
                full_path = abs_path.with_suffix(".f90")
                break
            elif abs_path.with_suffix(".f95").exists():
                full_path = abs_path.with_suffix(".f95")
                break
        else:
            return None
        warnings.warn(f'FortranImportFinder find_spec: {fullname}', UserWarning)
        loader = FortranImportLoader(full_path)
        spec = ModuleSpec(fullname, loader, origin=paths)
        return spec


finder = FortranImportFinder()
sys.meta_path.insert(0, finder)
warnings.warn('now you can import a fortain file', UserWarning)