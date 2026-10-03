"""Generate public APK metadata; no signing keys or app activation keys are used."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request
from urllib.parse import quote, urlsplit

MAX_APK = 100 * 1024 * 1024


def timestamp(value):
    return int(dt.datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp() * 1000)


def from_releases(releases, repository):
    choices = []
    for release in releases:
        published = release.get('published_at')
        if release.get('draft', True) or not published:
            continue
        for asset in release.get('assets', []):
            if asset.get('state') != 'uploaded' or not asset.get('name', '').lower().endswith('.apk'):
                continue
            digest = asset.get('digest') or ''
            if not digest.startswith('sha256:') or len(digest) != 71:
                continue  # The API fallback can see it once GitHub finishes hashing.
            size = asset.get('size', 0)
            url = asset.get('browser_download_url', '')
            if not 0 < size <= MAX_APK or not url.startswith(f'https://github.com/{repository}/releases/download/'):
                continue
            uploaded = max(timestamp(published), timestamp(asset.get('created_at') or published))
            choices.append(dict(assetId=asset['id'], uploadedAt=uploaded, size=size, apkUrl=url,
                                sha256=digest[7:].lower(), notes=(release.get('body') or '').strip()[:4000]))
    return choices


def repository_apks(repository):
    choices = []
    files = subprocess.check_output(['git', 'ls-files', '-z']).decode('utf8').split('\0')
    for name in files:
        p = Path(name)
        if not name.lower().endswith('.apk') or not p.is_file() or p.is_symlink():
            continue
        size = p.stat().st_size
        if not 0 < size <= MAX_APK:
            continue
        raw = p.read_bytes()
        if not raw.startswith(b'PK'):
            continue
        stamp = subprocess.check_output(['git', 'log', '-1', '--format=%ct', '--', name]).decode().strip()
        if not stamp:
            continue
        uploaded = int(stamp) * 1000
        digest = hashlib.sha256(raw).hexdigest()
        identity = uploaded * 1000 + int(hashlib.sha256((name + digest).encode()).hexdigest()[:8], 16) % 1000
        choices.append(dict(assetId=identity, uploadedAt=uploaded, size=size,
                            apkUrl=f'https://raw.githubusercontent.com/{repository}/main/{quote(name, safe="/")}',
                            sha256=digest, notes=''))
    return choices


def generate(releases, repository, files=()):
    choices = from_releases(releases, repository) + list(files)
    latest = max(choices, key=lambda item: (item['uploadedAt'], item['assetId']), default=None)
    return {'schema': 1, 'latest': latest}


def main():
    repository = os.environ['GITHUB_REPOSITORY']
    request = urllib.request.Request(f'https://api.github.com/repos/{repository}/releases?per_page=100',
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json',
                 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'VPro-Update-Feed'})
    with urllib.request.urlopen(request, timeout=30) as response:
        releases = json.load(response)
    feed = generate(releases, repository, repository_apks(repository))
    Path('update-live.json').write_text(json.dumps(feed, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    print('Update metadata generated; APK content and credentials are not logged.')


if __name__ == '__main__':
    main()

