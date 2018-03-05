# Python Common Test Changelog #

List all changes in various categories:
* Release notes: Contains all worth noting changes (breaking changes mainly)
* Enhancements
* Bug fixes
* Known issues

## Version 1.7.0 (2018-03-05) ##

### Enhancements ###

- Introduce flask_restplus_mock.TestAPI to mock a Flask Rest Plus API.

## Version 1.6.1 (2017-12-13) ##

### Bug fixes ###

- service_tester.assert_json now consider lists as unordered.

## Version 1.6.0 (2017-12-12) ##

### Enhancements ###

- services_handler can be called with more than the port argument.

## Version 1.5.0 (2017-12-07) ##

### Enhancements ###

- Introduce services_handler module to start and stop test services.

## Version 1.4.0 (2017-11-13) ##

### Enhancements ###

- Use SERVER_ENVIRONMENT instead of deprecated ENVIRONMENT variable.

## Version 1.3.1 (2017-10-24) ##

### Bug fixes ###

- Assert Swagger does not manage path without parameters

## Version 1.3.0 (2017-10-16) ##

### Enhancements ###

- Added kwargs to put/post methods so that headers/auth can be provided.

## Version 1.2.1 (2017-10-16) ##

### Enhancements ###

- Logging start and end of a test case should not be considered as a test by itself.

## Version 1.2.0 (2017-10-16) ##

### Enhancements ###

- Ability to validate a JSON Swagger response.

## Version 1.1.0 (2017-10-16) ##

### Enhancements ###

- Ability to check JSON response with fields as regex.

## Version 1.0.0 (2017-10-16) ##

### Release notes ###

- Initial release.
