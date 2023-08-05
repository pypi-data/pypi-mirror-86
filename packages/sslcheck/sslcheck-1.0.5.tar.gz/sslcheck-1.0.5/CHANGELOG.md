# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.0.5] - 2020-11-19
### Fixed
- Show warning when non-www version is not in certificate common names.
- Support TLS 1.1 method for connections.

## [1.0.4] - 2018-03-06
### Fixed
- Properly handle wildcard certificates for 4th+ level domains.

## [1.0.3] - 2018-03-06
### Changed
- When certificate has less than 10 days to expire, show it in yellow.

## [1.0.2] - 2018-03-04
### Fixed
- Properly handle self-signed certificates.

## [1.0.1] - 2018-02-27
### Changed
- Use TLS 1.2 when server refuses TLS 1.0 connection.

## 1.0.0 - 2018-02-23
### Added
- Initial version of this CLI SSL checker.

[1.0.1]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.0...v1.0.1
[1.0.2]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.1...v1.0.2
[1.0.3]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.2...v1.0.3
[1.0.4]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.3...v1.0.4
[1.0.5]: https://gitlab.com/radek-sprta/mariner/compare/v1.0.4...v1.0.5
