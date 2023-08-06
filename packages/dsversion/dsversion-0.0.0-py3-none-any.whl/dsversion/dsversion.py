#!/usr/bin/env python

import os
import re
import subprocess


_CHANGELOG_REGEX = r'##\s*\[\s*Unreleased\s*:\s*(\d+).(\d+).(\d+)\s*\]'


def get_is_devops_build():
    """
    Check if the build is an Azure Devops build.
    This is done by checking if the BUILD_REQUESTEDFOR environment variable exists.

    Returns:
        bool: True if Azure Devops build, False if development build
    """
    return 'BUILD_REQUESTEDFOR' in os.environ


def get_git_version():
    """
    Get the current commit id and check if the repo is clean or dirty.

    Returns:
        (str, bool): the short git commit id and a bool indicating whether your
            local work directory is clean
    """
    try:
        r = subprocess.run(
            ['git', 'describe', '--always', '--dirty', '--match', ';notag;'],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        out = r.stdout.strip()
        git_version = out.split('-')
        if len(git_version) == 1:
            commit_id, is_dirty = (git_version[0], False)
        elif len(git_version) == 2:
            commit_id, is_dirty = (git_version[0], True)
        else:
            raise ValueError('Invalid git describe version: %s' % out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit_id = 'unknown'
        is_dirty = True

    return commit_id, is_dirty


def get_version_from_changelog(changelog_path=None):
    """
    Get the version from the [Unreleased:d.d.d] title in the changelog.

    Args:
        changelog_path (str or None): Path to the changelog, if None, Changelog.md
            relative to the current working directory is used.

    Returns:
        (str, str, str): The major, minor and bugfix version found in the changelog

    Raises:
        ValueError: When no version was found in the changelog.
        FileNotFoundError: If no changelog file could be found.
    """
    if changelog_path is None:
        changelog_path = os.path.join(os.getcwd(), 'Changelog.md')

    with open(changelog_path, 'rt') as fid:
        text = fid.read()

    unreleased_match = re.findall(_CHANGELOG_REGEX, text, flags=re.IGNORECASE)
    try:
        return unreleased_match[0][0], unreleased_match[0][1], unreleased_match[0][2]
    except IndexError:
        raise ValueError(
            'No unreleased version match was found in Changelog.md, '
            'correct the changelog.'
        )


def get_version_info(changelog_path=None):
    """
    Get the version info.
    The `main_version` is based on the version from the [Unreleased:d.d.d] title in
    the changelog.
    The `post_version` is only used for non-devops builds and based on git describe
    (commit id + dirty).
    The `is_devops_build` indicates if the build is an Azure Devops build.

    Args:
        changelog_path (str or None): Path to the changelog, if None, Changelog.md
            relative to this python file is used.

    Returns:
        (str, str or None, bool):
            The `main_version`, the `post_version` and the `is_devops_build` bool.
    """
    version = get_version_from_changelog(changelog_path=changelog_path)
    is_devops_build = get_is_devops_build()
    main_version = '.'.join(version)

    if is_devops_build:
        post_version = None
    else:
        commit_id, is_dirty = get_git_version()
        post_version = ['dev', commit_id]
        if is_dirty:
            post_version += ['dirty']
        post_version = '.'.join(post_version)

    return main_version, post_version, is_devops_build


def get_version(changelog_path=None):
    """
    Get the complete version string.
    If the build is an Azure Devops build, the version does not have
    a post version: 0.0.1 .
    If the build is a local development build, the version will have
    a main and post version: 0.0.1+dev.a8452ass.dirty

    Args:
        changelog_path (str or None): Path to the changelog, if None, Changelog.md
            relative to this python file is used.

    Returns:
        str: The version string
    """
    main_version, post_version, _ = get_version_info(changelog_path=changelog_path)
    if post_version is not None:
        return main_version + '+' + post_version
    else:
        return main_version
