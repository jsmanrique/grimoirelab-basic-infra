#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 J. Manrique Lopez de la Fuente
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# Authors:
#     J. Manrique Lopez <jsmanrique@bitergia.com>
#

import os
import sys

import yaml

import github3

def read_config_file(filename):
    with open(filename) as data_file:
    	config_data = yaml.load(data_file)

    return config_data

def git(sources, env_vars):
    cmd_gral_part = cmd_composer(env_vars, 'git')

    for repository in sources['repositories']:
        cmd = cmd_gral_part + ' ' + repository
        os.system(cmd)

def github(sources, env_vars):

    cmd_gral_part = cmd_composer(env_vars, 'github')

    git_repositories = {'repositories':[]}

    for organization in sources['repositories']:
        gh_organization = github3.organization(organization)
        for repo in gh_organization.iter_repos():
            repo_url = 'https://github.com/' + organization + '/' + repo.name + '.git'
            git_repositories['repositories'].append(repo_url)

        git(git_repositories, env_vars)

        for repo in gh_organization.iter_repos():
            cmd_github_part = '--owner '+ organization + ' --repository ' + repo.name + ' -t ' + sources['token']
            cmd = cmd_gral_part + cmd_github_part
            os.system(cmd)

def meetup(sources, env_vars):
    cmd_gral_part = cmd_composer(env_vars, 'meetup')

    for repository in sources['repositories']:
        cmd = cmd_gral_part + ' ' + repository + ' -t ' + sources['token'] + ' --tag ' + repository
        os.system(cmd)

def exec_analysis(config_data):

    data_sources = config_data['sources']

    env_vars = config_data['environment']

    for backend in data_sources:
        switcher = {
            'git':git,
            'github-org':github,
            'meetup':meetup
        }

        get_data = switcher.get(backend)
        get_data(data_sources[backend], env_vars)

def cmd_composer(env_vars, backend):
    cmd_common = "p2o.py --enrich --no_incremental --no-cache --debug --index "
    cmd_rich_index_name = env_vars['name'] + '_' + backend
    cmd_raw_index_name = cmd_rich_index_name + '_raw '
    cmd_es_part = ' -e http://' + env_vars['es']['host'] + ':' + str(env_vars['es']['port'])

    cmd = cmd_common + cmd_raw_index_name + ' --index-enrich ' + cmd_rich_index_name + cmd_es_part + ' ' + backend

    return cmd

if __name__ == '__main__':

    #config_data = read_config_file(sys.argv[1])
    config_data = read_config_file('settings/data-sources.yml')
    exec_analysis(config_data)
