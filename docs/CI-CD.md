# SSI CI/CD

This patch adds two GitHub Actions workflows. It does not change SSI runtime code.

## CI (`.github/workflows/ci.yml`)

Runs on pushes to `main`, pull requests, and manual dispatch. Uses Python 3.10 and 3.12. Installs the local package, compiles sources, and executes `unittest` tests. No Ollama server, GPU, search provider, or API credentials are needed. CI does **not** test live web retrieval or model quality.

## Release (`.github/workflows/release.yml`)

Runs when a tag starting with `v` is pushed, or manually. Runs tests, builds a Python wheel and source distribution, and uploads them as GitHub Actions artifacts. For `v*` tags, it also creates a GitHub Release and attaches the distributions. It does not deploy a server or publish to PyPI.

To publish a release after CI is green, update the version in `pyproject.toml` to match the intended release, commit it, and create/push a tag, e.g. `git tag v0.1.0` then `git push origin v0.1.0`.

GitHub repository Settings > Actions > General must permit workflows to run. The release job needs permission to create releases; repository or organization policies may restrict this. Prefer protected `main` and require the CI checks before merging.

## Applying the patch

Extract this ZIP **at the root of the existing SSI repository** so `.github/workflows/` and `docs/` are created in place. Do not nest the extracted files inside another `ssi/` directory.

## Local verification

```powershell
python -m unittest discover -s tests -v
```
