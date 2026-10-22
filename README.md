# Solaris Dev Shop for Gemini CLI

**61 specialist employees + 1 chief-of-staff coordinator = 62 native workflows.**

A native Gemini CLI extension with the pinned Solaris delivery, recovery and evidence runtime. Skills load on demand. The host supplies tools and approvals; local Python helpers require Python 3.10 or later. This is a workflow package, not 61 independently running model instances.

## Install

```sh
gemini extensions install https://github.com/Shaisolaris/solaris-dev-shop-gemini
```

Review the CLI's installation and skill-activation prompts. Use `gemini skills list --all` to inspect discovery. For a reproducible installation, add `--ref <full reviewed commit SHA>` from this repository. Disable or uninstall using Gemini CLI's native extension commands.

## Source and verification

Version **0.64.0** retains the reviewed native source at [b13ca3c](https://github.com/Shaisolaris/solaris-dev-shop-plugins/commit/b13ca3c172a18491f8097926112520970a70e2cd) and canonical core at [3a577e4](https://github.com/Shaisolaris/solaris-dev-shop/commit/3a577e42c48473f6ef8680950dd55c067820d5d3). `GEMINI-BUILD-SOURCE.json` binds all generated payload bytes and executable modes. `SOLARIS-BUILD-SOURCE.json` binds the 1,197 canonical files. The portable builder verifies against a fresh checkout of the exact upstream revision, rather than trusting a caller-edited payload manifest:

```sh
python -B tools/build_gemini.py --check . --self-test
```

Native Gemini CLI **0.65.0** was tested for 62 enabled workflows, local entrypoint discovery, coordinator self-tests and real local SQLite restore outcomes. CLI management tests make no model calls; they do not establish model quality, Google endorsement, or a vulnerability-free product. Original 61 employees and branding are preserved. This packaging adds **zero new employee capabilities**.

The extension declares no MCP servers, settings, lifecycle hooks, agents or security policies. It does not grant filesystem access beyond the host's tools and permissions. Helpers are not a security sandbox. Review the workflow and its documented runtime requirements before executing it.

Original repository CI snapshots are preserved as data under `source-config/.github`. Five noncanonical manifests/entrypoints for other providers are omitted; all mappings and upstream provenance are retained. Existing core/native release tags and assets are unchanged.

## Publisher and support

Solaris Technologies — [solaristek.com](https://solaristek.com). [Core project](https://github.com/Shaisolaris/solaris-dev-shop), [native distributions and support](https://github.com/Shaisolaris/solaris-dev-shop-plugins/issues). License: [MIT](LICENSE).
