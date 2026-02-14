# Gradual Import Migration

This package provides compatibility modules for a gradual migration to `apps.*`
imports without moving Django apps immediately.

Examples:

- `from apps.patients.models import Patient`
- `from apps.institution.forms import InstForm`
- `include("apps.exams.urls")`

The canonical Django apps remain `patients`, `institution`, `medprofiles`,
`exams`, `login`, and `api` in `INSTALLED_APPS`.

