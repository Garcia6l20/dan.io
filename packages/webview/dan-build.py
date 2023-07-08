from dan import self, include
from dan.cxx import Library
from dan.src.tar import TarSources
from dan.src.git import GitSources
from dan.core.version import Version

version = self.options.add('version', '0.10.0')
description = 'Tiny cross-platform webview library for C/C++/Golang.'

class MsWebView(TarSources):
    name = 'ms-webview2-source'
    url = 'https://www.nuget.org/api/v2/package/Microsoft.Web.WebView2/1.0.1823.32'
    archive_name = 'WebView2.zip'
    default = False

class WebViewSources(GitSources):
    name = 'webview-source'
    url = 'https://github.com/webview/webview'
    refspec = '899018ad0e5cc22a18cd734393ccae4d55e3b2b4'
    default = False

    async def available_versions(self) -> list[Version]:
        return ['0.10.0']

class WebView(Library):
    name = 'webview'
    installed = True
    preload_dependencies = WebViewSources,
    dependencies = []
    source_path = WebViewSources
    public_includes = ['.']
    sources = ['webview.cc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.toolchain.system.is_windows:
            self.preload_dependencies.add(MsWebView)
        elif self.toolchain.system.is_linux:
            self.dependencies.add('gtk+-3.0')
            self.dependencies.add('javascriptcoregtk-4.0')
            self.dependencies.add('webkit2gtk-4.0')


    async def __initialize__(self):
        if self.toolchain.system.is_windows:
            self.includes.add(self.get_dependency(MsWebView).output / 'build' / 'native' / 'include', public=True)
            self.link_libraries.add('version', 'ole32', 'shlwapi')

        return await super().__initialize__()
