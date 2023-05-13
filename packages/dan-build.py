from dan import self, include

for d in [d for d in self.source_path.iterdir() if d.is_dir()]:
    include(d.name)
