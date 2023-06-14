import warnings
import sys
import importlib.abc
from importlib.machinery import ModuleSpec
import imp
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser

# Get links from a given URL
def _get_links(url):
    """在指定url查找包含的其他url"""
    class LinkParser(HTMLParser):
        """解析html文件,从中获取a标签中的url"""
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                attrs = dict(attrs)
                links.add(attrs.get('href').rstrip('/'))
    links = set()
    try:
        warnings.warn(f'Getting links from {url}',UserWarning)
        u = urlopen(url)
        parser = LinkParser()
        parser.feed(u.read().decode('utf-8'))
    except Exception as e:
        warnings.warn(f'Could not get links. {e}',UserWarning)
    warnings.warn(f'links: {links}',UserWarning)
    return links

class UrlPathFinder(importlib.abc.PathEntryFinder):
    """查找url及其中a标签中指向的url中的模块."""
    def __init__(self, baseurl):
        self._links = None # 保存一个baseurl中指定的可用url路径
        #self._loader = UrlModuleLoader(baseurl) # 指定默认的loader
        self._baseurl = baseurl # 
    def find_spec(self, fullname, paths=None, target=None):
        warnings.warn(f'find_loader: {fullname}', UserWarning)
        parts = fullname.split('.')
        basename = parts[-1]
        # 查看links和初始化links
        if self._links is None:
            self._links = [] 
            self._links = _get_links(self._baseurl)
        spec = None
        
        # 检查links是不是package,判断的标准是有没有.py
        if basename in self._links:
            warnings.warn(f'find_loader: trying package {fullname}', UserWarning)
            fullurl = self._baseurl + '/' + basename
            try:
                loader = UrlPackageLoader(fullurl)
                loader.load_module(fullname)#
                warnings.warn(f'find_loader: package {fullname} loaded', UserWarning)
                spec = ModuleSpec(fullname, loader, origin=paths)
            except ImportError as ie:
                warnings.warn(f'find_loader: {fullname} is a namespace package', UserWarning)
                spec = None
            except Exception as e:
                raise e
            

        elif (basename + '.py') in self._links:
            # 正常module的处理
            warnings.warn(f'find_loader: module {fullname} found', UserWarning)
            loader = UrlModuleLoader(self._baseurl)
            spec = ModuleSpec(fullname, loader, origin=paths)
        else:
            warnings.warn(f'find_loader: module {fullname} not found', UserWarning)
            
        return spec

    def invalidate_caches(self):
        warnings.warn("invalidating link cache", UserWarning)
        self._links = None


# Module Loader for a URL
class UrlModuleLoader(importlib.abc.SourceLoader):
    def __init__(self, baseurl):
        self._baseurl = baseurl
        self._source_cache = {}

    def create_module(self,spec):
        """这边只要调用父类的实现即可."""
        
        mod = sys.modules.setdefault(spec.name, imp.new_module(spec.name))
        mod.__file__ = self.get_filename(spec.name)
        mod.__loader__ = self
        mod.__package__ = spec.name.rpartition('.')[0]
        return mod
        

    def exec_module (self, module):
        """在_post_import_hooks中查找对应模块中的回调函数并执行."""
        code = self.get_code(module.__name__)
        exec(code, module.__dict__)

    # Optional extensions
    def get_code(self, fullname):
        src = self.get_source(fullname)
        return compile(src, self.get_filename(fullname), 'exec')

    def get_data(self, path):
        pass

    def get_filename(self, fullname):
        return self._baseurl + '/' + fullname.split('.')[-1] + '.py'

    def get_source(self, fullname):
        filename = self.get_filename(fullname)
        warnings.warn(f'loader: reading {filename}', UserWarning)
        if filename in self._source_cache:
            warnings.warn(f'loader: cached {fullname} not found', UserWarning)
            return self._source_cache[filename]
        try:
            u = urlopen(filename)
            source = u.read().decode('utf-8')
            warnings.warn(f'loader: {filename} loaded', UserWarning)
            self._source_cache[filename] = source
            return source
        except (HTTPError, URLError) as e:
            warnings.warn(f'loader: {filename} failed. {e}', UserWarning)
            raise ImportError("Can't load %s" % filename)

    def is_package(self, fullname):
        return False

# Package loader for a URL
class UrlPackageLoader(UrlModuleLoader):
    def create_module(self, spec):
        mod = super().create_module(spec)
        mod.__path__ = [ self._baseurl ]
        mod.__package__ = spec.name
        return mod

    def get_filename(self, fullname):
        return self._baseurl + '/' + '__init__.py'

    def is_package(self, fullname):
        return True

        


# Check path to see if it looks like a URL
_url_path_cache = {}
def handle_url(path):
    if path.startswith(('http://', 'https://')):
        warnings.warn(f'Handle path? {path}. [Yes]', UserWarning)
        if path in _url_path_cache:
            finder = _url_path_cache[path]
        else:
            finder = UrlPathFinder(path)
            _url_path_cache[path] = finder
        return finder
    else:
        warnings.warn(f'Handle path? {path}. [No]', UserWarning)

def install_path_hook():
    sys.path_hooks.append(handle_url)
    sys.path_importer_cache.clear()
    warnings.warn('Installing handle_url', UserWarning)

def remove_path_hook():
    sys.path_hooks.remove(handle_url)
    sys.path_importer_cache.clear()
    warnings.warn('Removing handle_url', UserWarning)
    
install_path_hook()