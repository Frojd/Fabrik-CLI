import unittest
import os
import shutil
import git
from click.testing import CliRunner
from frojd_fabric_cli.scaffolding import generator
from frojd_fabric_cli.scaffolding.scripts import init
from frojd_fabric_cli import utils


def read_file(path):
    with file(path) as f:
        s = f.read()

    return s


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        try:
            os.makedirs("./tmp/")
        except OSError as exception:  # NOQA
            pass

    def tearDown(self):
        try:
            shutil.rmtree("./tmp/")
        except OSError as exception:  # NOQA
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
        self.assertTrue(os.path.exists("./tmp/fabfile.py"))
        self.assertTrue(os.path.exists("./tmp/stages/__init__.py"))

        with self.assertRaises(OSError) as cm:  # NOQA
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

        self.assertTrue("def demo():" in contents)

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

        with self.assertRaises(Exception) as cm:  # NOQA
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

    def test_fabricrc_settings(self):
        stages = [{
            "NAME": "stage",
            "FORWARD_AGENT": "True"
        }, {
            "NAME": "prod",
            "FORWARD_AGENT": "True"
        }]

        gen = generator.Generator(stages=stages, path="./tmp")
        gen.create_index()

        self.assertTrue(os.path.exists("./tmp/fabricrc.txt"))

        contents = read_file("./tmp/fabricrc.txt")
        self.assertTrue("STAGE_HOST=" in contents)


class GitDetection(unittest.TestCase):
    def tearDown(self):
        try:
            shutil.rmtree("./tmp/")
        except OSError as exception:  # NOQA
            pass

    def test_invalid_repro(self):
        assert utils.has_git_repro("./tmp/") == False

    def test_detect_repro(self):
        git_url = "git@github.com:Frojd/Frojd-Fabric.git"

        repo = git.Repo.clone_from(git_url, "./tmp")

        assert utils.has_git_repro("./tmp/") == True
        assert utils.get_git_remote("./tmp/") == git_url


class ConsoleScriptTest(unittest.TestCase):
    def setUp(self):
        try:
            os.makedirs("./tmp/")
        except OSError as exception:  # NOQA
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

    def test_git_promp(self):
        # TODO: Update setUp/tearDown logic
        try:
            shutil.rmtree("./tmp/")
        except OSError as exception:
            pass

        git_url = "git@github.com:Frojd/Frojd-Fabric.git"
        repo = git.Repo.clone_from(git_url, "./tmp")

        runner = CliRunner()

        result = runner.invoke(init.main, [
            "--stages=local,dev,live",
            "--path=./tmp"
        ])

        assert result.exit_code == 0
        assert result.output.startswith("git repository [%s]" % git_url)

        self.assertTrue(os.path.exists("./tmp/stages"))
        self.assertTrue(os.path.exists("./tmp/stages/local.py"))

        contents = read_file("./tmp/stages/__init__.py")
        self.assertTrue("env.repro_url" in contents)

    def test_recipe_prompt(self):
        try:
            shutil.rmtree("./tmp/")
        except OSError as exception:
            pass

        git_url = "git@github.com:Frojd/Frojd-Fabric.git"
        repo = git.Repo.clone_from(git_url, "./tmp")

        runner = CliRunner()

        result = runner.invoke(init.main, [
            "--stages=local,dev,live",
            "--path=./tmp",
            "--recipe=wordpress"
        ])

        assert result.exit_code == 0
        assert result.output.startswith("git repository [%s]" % git_url)

        self.assertTrue(os.path.exists("./tmp/stages"))
        self.assertTrue(os.path.exists("./tmp/stages/local.py"))

        contents = read_file("./tmp/stages/live.py")
        self.assertTrue("frojd_fabric.recipes import wordpress" in contents)

