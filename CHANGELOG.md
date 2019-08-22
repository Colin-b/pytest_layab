# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2019-08-22
### Changed
- Update CONTRIBUTING documentation to explain how to install pre-commit python module using pip.
- Ensure that exceptions are not propagated to the client when testing APIs as the real HTTP response should be tested.
- Ensure full test coverage.

### Added
- before_service_init fixture that can be overridden to perform actions before initializing service

## [1.0.0] - 2019-08-01
### Changed
- Initial release.

[Unreleased]: https://github.tools.digital.engie.com/GEM-Py/pytest_layab/compare/v1.1.0...HEAD
[1.1.0]: https://github.tools.digital.engie.com/GEM-Py/pytest_layab/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.tools.digital.engie.com/GEM-Py/pytest_layab/releases/tag/v1.0.0
