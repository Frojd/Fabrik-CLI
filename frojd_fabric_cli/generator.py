import os
import jinja2


class Generator(object):
    stages = None
    path = None
    loader = None
    environment = None

    def __init__(self, stages=None, path=None, *args, **kwargs):
        self.stages = stages
        self.path = path

        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir,  "templates")
        self.loader = jinja2.FileSystemLoader(templates_dir)
        self.environment = jinja2.Environment(loader=self.loader)

    def get_stages_path(self):
        return os.path.join(self.path, "stages")

    def create_index(self):
        template = self.environment.get_template("index.py.txt")
        output = template.render(stages=self.stages)

        stage_dir = self.get_stages_path()
        os.makedirs(stage_dir)

        index_path = os.path.join(stage_dir, "__init__.py")
        with open(index_path, "w") as fout:
            fout.write(output)

    def create_stage(self, name=None):
        pass
