# -*- coding: utf-8 -*-
# Copyright (C) 2022 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
import os
import subprocess

CONDA_EXE = os.environ.get("CONDA_EXE", "conda")


def load_project(directory=None):
    project = CondaProject(directory)
    return project


class CondaProject:
    def __init__(self, directory=None):
        self.directory = os.path.normcase(os.path.abspath(directory))

    def _call_conda(self, args):
        env = {}

        condarc = os.path.join(self.directory, '.condarc')
        if os.path.exists(condarc):
            env['CONDARC'] = condarc

        subprocess.run(
            [CONDA_EXE] + args,
            env=env
        )

    def default_env(self):
        return os.path.join(self.directory, 'envs', 'default')

    def prepare(self, force=False):
        default_env = self.default_env()
        force = '--force' if force else ''
        self._call_conda(
            ['env', 'create', force, '-p', default_env]
        )
        return default_env

    def clean(self):
        self._call_conda(
            ['env', 'remove', '-p', self.default_env()]
        )
