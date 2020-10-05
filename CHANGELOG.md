# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2020-10-05
### Changed
- There is no dependency anymore. You need to specify your version of `pytest-flask` and everything that was within `pytest_layab` is now within `pytest_layab.flask`.
- Run tests against `pytest-flask` version `1.*` instead of `0.15.*`.
- `service_module_name` pytest fixture is now expected to return the full python module name containing the flask application and is now mandatory.
- Update `black` version from `master` to `20.8b1`.

### Removed
- `pytest_layab.async_service_module` fixture is no longer available.
- `pytest_layab.assert_async` function is no longer available.
- `pytest_layab.assert_204` function is no longer available.
- `pytest_layab.assert_202_regex` function is no longer available.
- `pytest_layab.assert_303_regex` function is no longer available.
- `pytest_layab.assert_items_equal` function is no longer available.
- `pytest_layab.before_service_init` fixture is no longer available. Should you need to execute something before importing the service module, do it in the now required `service_module_name` fixture.
- `pytest_layab.test_module_name` fixture is no longer available. As `service_module_name` fixture is now mandatory.
- `pytest_layab.service_module` fixture is no longer available. As `service_module_name` fixture is now mandatory. If you want to execute something after, create your own fixture relying on `app` fixture.

## [1.3.0] - 2019-12-02
### Added
- First release.

[Unreleased]: https://github.com/Colin-b/pytest_layab/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/Colin-b/pytest_layab/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/Colin-b/pytest_layab/releases/tag/v1.3.0
