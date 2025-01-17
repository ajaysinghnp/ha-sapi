<!-- markdownlint-disable MD024 -->
# Changelog

All notable changes to the SAPI Home Assistant integration will be documented in this file.

## [0.0.4] - 2025-01-17

### Added

- Enhanced integration with new features
- Implemented PAN details service endpoint
- Added frontend automation capabilities

### Changed

- Improved API endpoint handling with better app info integration
- Enhanced devcontainer configuration for better development experience

## [0.0.3] - 2025-01-14

### Added

- Implemented core functionality for SAPI integration
- Added complete sensor data fetching capabilities
- Introduced binary sensor support
- Set up basic configuration flow
- Implemented data coordinator for efficient updates

### Changed

- Optimized API communication
- Enhanced error handling and logging
- Improved state management

## [0.0.2] - 2025-01-13

### Added

- VSCode development configuration
- Comprehensive development container setup

### Changed

- Updated post-create.sh script for better initialization
- Enhanced development requirements in requirements_dev.txt

### Security

- Dependencies updated to latest secure versions

## [0.0.1] - 2025-01-13

### Added

- Initial project structure
- Basic HACS integration setup
- Configuration validation framework
- Test infrastructure setup

### Dependencies

Major dependency updates for development environment:

#### Major Updates

- astral: 2.2 → 3.2
  - Breaking changes in API
  - Improved calculations and performance

#### Minor Updates

- acme: 3.0.1 → 3.1.0 (Minor feature updates)
- tqdm: 4.66.5 → 4.67.1 (Performance improvements)
- respx: 0.21.1 → 0.22.0 (New features for testing)
- pipdeptree: 2.23.4 → 2.24.0 (Enhanced dependency resolution)
- pillow: 11.0.0 → 11.1.0 (New image processing features)

#### Patch Updates

- sqlalchemy: 2.0.36 → 2.0.37 (Bug fixes)
- gitpython: 3.1.41 → 3.1.44 (Performance improvements)
- orjson: 3.10.12 → 3.10.14 (Minor bug fixes)
- smmap: 5.0.1 → 5.0.2 (Memory handling improvements)

### Developer Notes

- Enabled Dependabot for automated dependency updates
- Initialized project with core HACS compatibility
- Set up GitHub Actions for CI/CD

## Types of Changes

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability related changes

## [Pre-release]

The changes listed in this CHANGELOG are part of active development.

## How to Update

1. In Home Assistant, go to HACS → Integrations
2. Click the three dots on the SAPI integration
3. Click "Reinstall"
4. Restart Home Assistant

## Reporting Issues

Please report any issues on the GitHub repository issue tracker.
