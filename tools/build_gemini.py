"""Build a genuine Gemini extension from the immutable, reviewed native profile.

Provider-specific manifests are changed; original role/source bytes are retained.
Repository CI snapshots are relocated so importing a distribution cannot activate
the source project's workflows in its destination repository.
"""
from pathlib import Path
import argparse
import hashlib
import shutil
import sys
import tempfile
import io
import json
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
NATIVE_URL = 'https://github.com/Shaisolaris/solaris-dev-shop-plugins.git'
REVISION = '085ebb9e9c137c5046c2153b9413d9badd102ce7'
CORE = 'ee38d3de3d4b0d5467a589d5cb908f4964f593fe'
OMIT = {'.claude-plugin/plugin.json', 'plugin.json', 'package.json', 'server.mjs', 'native/opencode.mjs'}
CONTEXT = '''# Solaris Dev Shop

This extension provides 61 specialist workflows and a coordinating chief-of-staff skill. Use native skills on demand. For multi-domain requests, chief-of-staff can produce a bounded assignment; specialists perform the work. Follow each activated skill's pinned workflow and local entrypoint. Host tools, approvals and documented runtime requirements apply.
'''


def sha(data):
    return hashlib.sha256(data).hexdigest()


def build(native, output):
    NATIVE, OUT = native, output
    assert not OUT.exists(), 'Preserve an existing candidate instead of overwriting it.'
    archive = subprocess.check_output(['git', '-C', str(NATIVE), 'archive', '--format=tar', REVISION, 'copilot/plugin'])
    original = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        for item in source:
            if item.isdir():
                continue
            assert item.isfile(), item.name
            prefix = 'copilot/plugin/'
            assert item.name.startswith(prefix)
            name = item.name[len(prefix):]
            assert '..' not in Path(name).parts and not Path(name).is_absolute()
            original[name] = (source.extractfile(item).read(), bool(item.mode & 0o111))
    assert len(original) == 1973
    native_provenance = json.loads(original['SOLARIS-BUILD-SOURCE.json'][0])
    assert native_provenance['source_commit'] == CORE
    assert not OMIT.intersection(native_provenance['canonical_files'])
    relocated = {name: 'source-config/' + name for name in original if name.startswith('.github/')}
    maps = dict(relocated)
    maps['COPILOT-LAYOUT.json'] = 'SOURCE-COPILOT-LAYOUT.json'
    for name, (data, executable) in original.items():
        if name in OMIT:
            continue
        target = OUT / maps.get(name, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o755 if executable else 0o644)
    (OUT/'SOURCE-NATIVE-PROVENANCE.json').write_bytes(original['SOLARIS-BUILD-SOURCE.json'][0])
    provenance = json.loads(original['SOLARIS-BUILD-SOURCE.json'][0])
    provenance['canonical_files'] = {maps.get(name, name): digest for name, digest in provenance['canonical_files'].items()}
    provenance['source_path_map'].update(relocated)
    (OUT/'SOLARIS-BUILD-SOURCE.json').write_text(json.dumps(provenance, indent=2)+'\n')
    manifest = {'name':'solaris-dev-shop','version':'0.63.0',
                'description':'61 specialist workflows and a chief of staff, backed by local delivery, recovery and evidence tools. Host tools and approvals apply.',
                'contextFileName':'GEMINI.md'}
    (OUT/'gemini-extension.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (OUT/'GEMINI.md').write_text(CONTEXT)
    (OUT/'README.md').write_text("# Solaris Dev Shop for Gemini CLI\n\n**61 specialist employees + 1 chief-of-staff coordinator = 62 native workflows.**\n\nA native Gemini CLI extension with the pinned Solaris delivery, recovery and evidence runtime. Skills load on demand. The host supplies tools and approvals; local Python helpers require Python 3.10 or later. This is a workflow package, not 61 independently running model instances.\n\n## Install\n\n```sh\ngemini extensions install https://github.com/Shaisolaris/solaris-dev-shop-gemini\n```\n\nReview the CLI's installation and skill-activation prompts. Use `gemini skills list --all` to inspect discovery. For a reproducible installation, add `--ref <full reviewed commit SHA>` from this repository. Disable or uninstall using Gemini CLI's native extension commands.\n\n## Source and verification\n\nVersion **0.63.0** retains the reviewed native source at [085ebb9](https://github.com/Shaisolaris/solaris-dev-shop-plugins/commit/085ebb9e9c137c5046c2153b9413d9badd102ce7) and canonical core at [ee38d3d](https://github.com/Shaisolaris/solaris-dev-shop/commit/ee38d3de3d4b0d5467a589d5cb908f4964f593fe). `GEMINI-BUILD-SOURCE.json` binds all generated payload bytes and executable modes. `SOLARIS-BUILD-SOURCE.json` binds the 1,196 canonical files. The portable builder verifies against a fresh checkout of the exact upstream revision, rather than trusting a caller-edited payload manifest:\n\n```sh\npython -B tools/build_gemini.py --check . --self-test\n```\n\nNative Gemini CLI **0.65.0** was tested for 62 enabled workflows, local entrypoint discovery, coordinator self-tests and real local SQLite restore outcomes. CLI management tests make no model calls; they do not establish model quality, Google endorsement, or a vulnerability-free product. Original 61 employees and branding are preserved. This packaging adds **zero new employee capabilities**.\n\nThe extension declares no MCP servers, settings, lifecycle hooks, agents or security policies. It does not grant filesystem access beyond the host's tools and permissions. Helpers are not a security sandbox. Review the workflow and its documented runtime requirements before executing it.\n\nOriginal repository CI snapshots are preserved as data under `source-config/.github`. Five noncanonical manifests/entrypoints for other providers are omitted; all mappings and upstream provenance are retained. Existing core/native release tags and assets are unchanged.\n\n## Publisher and support\n\nSolaris Technologies — [solaristek.com](https://solaristek.com). [Core project](https://github.com/Shaisolaris/solaris-dev-shop), [native distributions and support](https://github.com/Shaisolaris/solaris-dev-shop-plugins/issues). License: [MIT](LICENSE).\n", encoding='utf-8')
    for name, digest in provenance['canonical_files'].items():
        assert sha((OUT/name).read_bytes()) == digest, name
    for name in ['hooks/hooks.json', 'policies', 'agents']:
        assert not (OUT/name).exists(), 'Unexpected automatic extension surface: '+name
    files = {str(f.relative_to(OUT)):{'sha256':sha(f.read_bytes()),'executable':bool(f.stat().st_mode&0o111)}
             for f in sorted(OUT.rglob('*')) if f.is_file()}
    record = {'prototype':False,'profile':'Gemini CLI extension','source_native_commit':REVISION,
              'source_core_commit':CORE,'version':'0.63.0','canonical_files':len(provenance['canonical_files']),
              'workflows':62,'new_employee_capabilities':0,'omitted_other_provider_files':sorted(OMIT),
              'relocated_repository_configuration':relocated,'source_file_map':maps,'files':files}
    (OUT/'GEMINI-BUILD-SOURCE.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    return {'candidate':str(OUT),'canonical_files':record['canonical_files'],
                      'workflows':62,'payload_files':len(files)+1,'relocated_configuration_files':len(relocated)}


EXTRAS = {'tools/build_gemini.py', '.github/workflows/validate.yml', '.gitignore'}


def inventory(root):
    found = {}
    for path in root.rglob('*'):
        relative = path.relative_to(root).as_posix()
        if '.git' in path.relative_to(root).parts:
            continue
        if path.is_symlink():
            raise ValueError('Symlink forbidden: ' + relative)
        if path.is_file() and relative not in EXTRAS:
            found[relative] = (sha(path.read_bytes()), bool(path.stat().st_mode & 0o111))
    return found


def compare(expected, actual):
    wanted, found = inventory(expected), inventory(actual)
    missing = sorted(wanted.keys() - found.keys())
    extra = sorted(found.keys() - wanted.keys())
    changed = sorted(k for k in wanted.keys() & found.keys() if wanted[k] != found[k])
    if missing or extra or changed:
        raise ValueError(json.dumps({'missing': missing, 'extra': extra, 'changed': changed}))
    return len(wanted)


def self_test(expected):
    with tempfile.TemporaryDirectory(prefix='solaris-gemini-controls-') as temp:
        trial = Path(temp)/'trial'
        shutil.copytree(expected, trial)
        compare(expected, trial)
        target = trial/'gemini-extension.json'
        original = target.read_bytes()
        controls = []
        def reject(name):
            try:
                compare(expected, trial)
            except ValueError:
                controls.append(name)
            else:
                raise ValueError('False acceptance: ' + name)
        target.write_bytes(b'{}')
        reject('altered manifest')
        target.write_bytes(original)
        target.chmod(0o755)
        reject('changed executable mode')
        target.chmod(0o644)
        extra = trial/'hooks/hooks.json'
        extra.parent.mkdir()
        extra.write_text('{}')
        reject('unexpected lifecycle hook')
        extra.unlink()
        extra.parent.rmdir()
        target.unlink()
        target.symlink_to(expected/'gemini-extension.json')
        reject('symlink payload')
        target.unlink()
        target.write_bytes(original)
        compare(expected, trial)
        return controls


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='Existing Git checkout containing the exact native source commit')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--output', type=Path, help='New output directory; never overwritten')
    mode.add_argument('--check', type=Path, help='Verify a distribution against the exact upstream source')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='solaris-gemini-build-') as temp:
        temporary = Path(temp)
        source = args.source
        if source is None:
            source = temporary/'upstream'
            subprocess.run(['git', 'init', '-q', str(source)], check=True)
            subprocess.run(['git', '-C', str(source), 'fetch', '-q', '--depth=1', NATIVE_URL, REVISION], check=True)
        resolved = subprocess.check_output(['git', '-C', str(source), 'rev-parse', REVISION+'^{commit}'], text=True).strip()
        if resolved != REVISION:
            raise ValueError('Wrong upstream revision')
        expected = args.output if args.output else temporary/'expected'
        result = build(source, expected)
        if args.check:
            result['verified_payload_files'] = compare(expected, args.check)
        if args.self_test:
            result['negative_controls'] = self_test(expected)
        print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, AssertionError, OSError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
