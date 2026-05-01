# Contributing to Supra Connect

Thanks for helping make Supra Connect useful in Home Assistant.

## Local Checks

Run the lightweight syntax check before opening a pull request:

```bash
python -m compileall custom_components/supraconnect
```

If you use pre-commit, run:

```bash
pre-commit run --all-files
```

## Scope

This integration should stay production-honest:

- Prefer official or user-authorized telemetry paths.
- Do not reintroduce the blocked MyBMW app API flow as the default path.
- Add remote commands only when the authentication and transport are verified to work reliably for real Supra Connect users.
- Keep entity descriptors generic enough to handle different payload shapes, then add explicit metadata hints for known Supra descriptors as they are confirmed.
