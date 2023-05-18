from dan import self
from dan.cxx import Library
from dan.src.github import GitHubReleaseSources

version = self.options.add('version', '3.7.2')
description = 'Compile Time Regular Expression in C++'


class CompileTimeRegularExpressionsSources(GitHubReleaseSources):
    name = 'ctre-source'
    user = 'hanickadot'
    project = 'compile-time-regular-expressions'


class CompileTimeRegularExpressions(Library):
    name = 'ctre'
    preload_dependencies = CompileTimeRegularExpressionsSources,
    installed = True

    async def __initialize__(self):
        root = self.get_dependency(CompileTimeRegularExpressionsSources).output
        self.includes.add(root  / 'include', public=True)
        await super().__initialize__()
