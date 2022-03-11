# github-actions-workflows

Reusable workflows for GitHub Actions.

- [Test a Python package using tox](#test-a-python-package-using-tox)
- [Build and publish a Python package](#build-and-publish-a-python-package)
- [Build and publish a pure Python package](#build-and-publish-a-pure-python-package)

## Test a Python package using tox

This workflow makes it easy to map tox environments to GitHub Actions jobs.
To use this template, your repository will need to have a `tox.ini` file.

```yaml
jobs:
  test:
    uses: OpenAstronomy/github-actions-workflows/.github/workflows/tox.yml@main
    with:
      posargs: '-n 4'
      envs: |
        - linux: pep8
          pytest: false
        - macos: py310
        - windows: py39-docs
          libraries:
            choco:
              - graphviz
      coverage: 'codecov'
    secrets:
      CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

### Inputs

A specification of tox environments must be passed to the `envs` input.
There are a number of other inputs.
All of these inputs (except `submodules`) can also be specified under each tox environment to overwrite the global value.

In the following example `test1` will pass `--arg-local` to pytest, while `test2` will pass `--arg-global` to pytest,
```yaml
uses: OpenAstronomy/github-actions-workflows/.github/workflows/tox.yml@main
with:
  posargs: '--arg-global'
  envs: |
    - linux: test1
      posargs: '--arg-local'
    - linux: test2
```

#### envs
Array of tox environments to test.
Required input.

```yaml
uses: OpenAstronomy/github-actions-workflows/.github/workflows/tox.yml@main
with:
  envs: |
    - <os>: <toxenv>
    - <os>: <toxenv>
```

where `<os>` is the either `linux`, `macos` or `windows`, and `<toxenv>` is the name of the tox environment to run.

***Note:** `envs` is a **string** and must be specified as a literal block scalar using the `|`. (Without the `|`, it must also be valid YAML.)*

Example:

```yaml
uses: OpenAstronomy/github-actions-workflows/.github/workflows/tox.yml@main
with:
  envs: |
    - linux: pep8
    - linux: py39
    - macos: py38-docs
      name: build_docs
    - windows: py310-conda
```

The name of the GitHub Actions job can be changed with the `name` option as shown above.
By default, `name` will be the name of the tox environment.

#### libraries
Additional packages to install using apt (only on Linux), brew and brew cask (only on macOS), and choco (only on Windows).

Global definition:
```yaml
uses: OpenAstronomy/github-actions-workflows/.github/workflows/tox.yml@main
with:
  libraries: |
    apt:
      - package1
      - package2
    brew:
      - package3
    brew-cask:
      - package4
    choco:
      - package5
```

***Note:** `libraries` is a **string** and must be specified as a literal block scalar using the `|`. (Without the `|`, it must also be valid YAML.)*

`envs` definition:
```yaml
with:
  envs: |
    - linux: py39
      libraries:
        apt:
          - package1
```

#### posargs
Positional arguments for the `{posargs}` replacement in an underlying test command within tox.
Default is none.

#### toxdeps
Additional tox dependencies.
This string is included at the end of the `pip install` command when installing tox.
Default is none.

#### toxargs
Positional arguments for tox.
Default is none.

#### pytest
Whether pytest is run by the tox environment.
This determines if additional pytest positional arguments should be passed to tox.
These arguments are to assist with saving test coverage reports.
Default is `true`.

Coverage will not be uploaded if this is `false`.

#### coverage
A space separated list of coverage providers to upload to.
Currently only `codecov` is supported.
Default is to not upload coverage reports.

See also, `CODECOV_TOKEN` secret.

#### conda
Whether to test within a conda environment using `tox-conda`.
Options are `'auto'` (default), `'true'` and `'false'`.

If `'auto'`, conda will be used if the tox environment names contains "conda".
For example, `'auto'` would enable conda for tox environments named `py39-conda`, `conda-test` or even `py38-secondary`.

#### display
Whether to setup a headless display.
This uses the `pyvista/setup-headless-display-action@v1` GitHub Action.
Default is `false`.

#### runs-on
Choose an alternative image for the runner to use for each OS.
By default, `linux` is `ubuntu-latest`, `macos` is `macos-latest` and `windows` is `windows-latest`.
None, some or all OS images can be specified, and the global value can be overridden in each environment.

It can be defined globally:
```yaml
uses: OpenAstronomy/github-actions-workflows/.github/workflows/tox.yml@main
with:
  runs-on: |
    linux: ubuntu-18.04
    macos: macos-10.15
    windows: windows-2019
```
```yaml
uses: OpenAstronomy/github-actions-workflows/.github/workflows/tox.yml@main
with:
  runs-on: |
    macos: macos-10.15
```

***Note:** `runs-on` is a **string** and must be specified as a literal block scalar using the `|`. (Without the `|`, it must also be valid YAML.)*

`envs` definition:
```yaml
uses: OpenAstronomy/github-actions-workflows/.github/workflows/tox.yml@main
with:
  envs: |
    - windows: py39
      runs-on: windows-2019
```

#### default_python
The version of Python to use if the tox environment name does not start with `py(2|3)[0-9]+`.
Default is `3.x`.

For example, a tox environment `py39-docs` will run on Python 3.9, while a tox environment `build_docs` will refer to the value of `default_python`.

#### submodules
Whether to checkout submodules.
Default is `true`.

### Secrets

#### CODECOV_TOKEN
If your repository is private, in order to upload to Codecov you need to set the `CODECOV_TOKEN` environment variable or pass it as a secret to the workflow.

## Build and publish a Python package

Build, test and publish a Python source distribution and collection of platform-dependent wheels.

```yaml
jobs:
  publish:
    uses: OpenAstronomy/github-actions-workflows/.github/workflows/publish.yml@main
    with:
      test_extras: test
      test_command: pytest --pyargs test_package
      targets: |
        - linux
        - cp3?-macosx_x86_64
    secrets:
      pypi_token: ${{ secrets.pypi_token }}
```

### Inputs

#### targets
List of build targets for cibuildwheel.
The list of targets must be specified as demonstrated by the default value below.
Each target is built within a separate matrix job.

If the target is `linux`, `macos` or `windows`, cibuildwheel is run on the latest version of that OS.

Any other target is assumed to be a value for the `CIBW_BUILD` environment variable (e.g. `cp3?-macosx_x86_64`).
In this case the OS to run cibuildwheel on is extracted from the target.

Targets that end with ``aarch64``, ``arm64`` and ``universal2`` are also supported without any additional configuration of cibuildwheel.

***Note:** `targets` is a **string** and must be specified as a literal block scalar using the `|`. (Without the `|`, it must also be valid YAML.)*

Default is:
```yaml
targets: |
  - linux
  - macos
  - windows
```

To not build any wheels:
```yaml
targets: ''
```

#### sdist
Whether to build a source distribution.
Default is `true`.

#### test_extras
Any `extras_requires` modifier that should be used to install the package for testing.
Default is none.

#### test_command
The command to run to test the package.
Will be run in a temporary directory.
Default is no testing.

#### libraries
Packages needed to build the source distribution for testing. Must be a string of space-separated apt packages.
Default is install nothing extra.

#### upload_to_pypi
A boolean indicating whether to upload to PyPI after successful builds. This defaults to
``(github.event_name == 'push' && startsWith(github.event.ref, 'refs/tags/v'))``,
meaning that packages are only uploaded to PyPI when a tag starting with ``v`` is
pushed. This can be set to a different condition, or ``true`` to always upload packages
and ``false`` to never upload them.

#### repository_url
The PyPI repository URL to use.
Default is the main PyPI repository.

#### submodules
Whether to checkout submodules.
Default is `true`.

### Secrets

#### pypi_token
The authentication token to access the PyPI repository.

## Build and publish a pure Python package

This the workflow is similar to the `publish.yml` workflow, except, instead of building wheels using cibuildwheel, a pure Python wheel and a source distribution are build, tested and published instead.

```yaml
jobs:
  publish:
    uses: OpenAstronomy/github-actions-workflows/.github/workflows/publish_pure_python.yml@main
    with:
      test_extras: test
      test_command: pytest --pyargs test_package
    secrets:
      pypi_token: ${{ secrets.pypi_token }}
```

### Inputs

#### test_extras
Any `extras_requires` modifier that should be used to install the package for testing.
Default is none.

#### test_command
The command to run to test the package.
Will be run in a temporary directory.
Default is no testing.

#### libraries
Packages needed to build the source distribution for testing. Must be a string of space-separated apt packages.
Default is install nothing extra.

#### upload_to_pypi
A boolean indicating whether to upload to PyPI after successful builds. This defaults to
``(github.event_name == 'push' && startsWith(github.event.ref, 'refs/tags/v'))``,
meaning that packages are only uploaded to PyPI when a tag starting with ``v`` is
pushed. This can be set to a different condition, or ``true`` to always upload packages
and ``false`` to never upload them.

#### repository_url
The PyPI repository URL to use.
Default is the main PyPI repository.

#### submodules
Whether to checkout submodules.
Default is `true`.

### Secrets

#### pypi_token
The authentication token to access the PyPI repository.
