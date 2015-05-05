import unittest
import os
import shutil
from click.testing import CliRunner
from frojd_fabric_cli import generator
from frojd_fabric_cli.scripts import init


def read_file(path):
    with file(path) as f:
        s = f.read()

    return s


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        try:
            os.makedirs("./tmp/")
        except OSError as exception:
            pass

    def tearDown(self):
        try:
            shutil.rmtree("./tmp/")
        except OSError as exception:
            pass

    def test_index_generation(self):
        stages = [{
            "NAME": "demo",
            }, {
            "NAME": "stage"
        }]

        gen = generator.Generator(stages=stages, path="./tmp")
        gen.create_index()

        self.assertTrue(os.path.exists("./tmp/stages"))
        self.assertTrue(os.path.exists("./tmp/stages/__init__.py"))

        with self.assertRaises(OSError) as cm:
            gen.create_index()

        contents = read_file("./tmp/stages/__init__.py")
        self.assertTrue("from demo import demo" in contents)

    def test_stage_generation(self):
        stages = [{
            "NAME": "demo",
            }, {
            "NAME": "stage"
        }]

        gen = generator.Generator(stages=stages, path="./tmp")
        gen.create_stage(name="demo")

        self.assertTrue(os.path.exists("./tmp/stages/demo.py"))
        contents = read_file("./tmp/stages/demo.py")

        self.assertTrue("def demo:" in contents)

    def test_stages_generation(self):
        stages = [{
            "NAME": "demo",
            }, {
            "NAME": "stage"
        }]

        gen = generator.Generator(stages=stages, path="./tmp")
        gen.create_stages()

        self.assertTrue(os.path.exists("./tmp/stages/demo.py"))
        self.assertTrue(os.path.exists("./tmp/stages/stage.py"))

    def test_invalid_stagename(self):
        stages = [{
            "NAME": "demo!"
        }]

        with self.assertRaises(Exception) as cm:
            generator.Generator(stages=stages, path="./tmp")

    def test_ssh_stage_info(self):
        stages = [{
            "NAME": "stage",
            "FORWARD_AGENT": "True"
        }]

        gen = generator.Generator(stages=stages, path="./tmp")
        gen.create_stages()

        contents = read_file("./tmp/stages/stage.py")
        self.assertTrue("env.forward_agent = True" in contents)


class ConsoleScriptTest(unittest.TestCase):
    def setUp(self):
        try:
            os.makedirs("./tmp/")
        except OSError as exception:
            pass

    def tearDown(self):
        try:
            shutil.rmtree("./tmp/")
        except OSError as exception:
            pass
    def test_init(self):
        runner = CliRunner()

        result = runner.invoke(init.main, [
            "--stages=local,dev,live",
            "--path=./tmp"
        ])

        assert result.exit_code == 0

        self.assertTrue(os.path.exists("./tmp/stages"))
        self.assertTrue(os.path.exists("./tmp/stages/local.py"))
