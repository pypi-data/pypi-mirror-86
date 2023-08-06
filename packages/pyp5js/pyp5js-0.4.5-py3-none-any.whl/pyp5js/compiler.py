import shutil
import subprocess
from cprint import cprint

from pyp5js.templates_renderers import get_target_sketch_content


class Pyp5jsCompiler:

    def __init__(self, sketch_files):
        self.sketch_files = sketch_files

    def compile_sketch_js(self):
        self.prepare()
        self.run_compiler()
        self.clean_up()

    @property
    def target_dir(self):
        """
        Path to directory with the js and assets files
        """
        return self.sketch_files.sketch_dir.joinpath('__target__')

    @property
    def command_line(self):
        """
        Builds transcrypt command line with the required parameters and flags
        """
        pyp5_dir = self.sketch_files.from_lib.install
        target = self.sketch_files.target_sketch
        return ' '.join([str(c) for c in [
            'transcrypt', '-xp', f'"{pyp5_dir}"', '-k', '-ks', '-b', '-m', '-n', f'"{target}"'
        ]])

    def run_compiler(self):
        """
        Execute transcrypt command to generate the JS files
        """
        command = self.command_line
        cprint.info(
            f"Converting Python to P5.js...\nRunning command:\n\t {command}")

        subprocess.call(command, shell=True)

    def clean_up(self):
        """
        Rename the assets dir from __target__ to target and delete target_sketch.py

        This is required because github pages can't deal with assets under a __target__ directory
        """
        if self.sketch_files.target_dir.exists():
            shutil.rmtree(self.sketch_files.target_dir)
        shutil.move(self.target_dir, self.sketch_files.target_dir)

        if self.sketch_files.target_sketch.exists():
            self.sketch_files.target_sketch.unlink()

    def prepare(self):
        """
        Creates target_sketch.py to import the sketch's functions
        """
        with self.sketch_files.target_sketch.open('w') as fd:
            content = get_target_sketch_content(self.sketch_files)
            fd.write(content)


def compile_sketch_js(sketch_files):
    compiler = Pyp5jsCompiler(sketch_files)
    compiler.compile_sketch_js()
