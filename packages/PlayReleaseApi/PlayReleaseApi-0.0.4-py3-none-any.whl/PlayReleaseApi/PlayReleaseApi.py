# Publishes a release in line with continuous integration

#!/usr/bin/env python3

import json
import os
import re
import requests
import subprocess as sp
import sys
from datetime import datetime


class PlayReleaseApi:
    delims = '\n\n'
    pipeline = os.getenv('CIRCLECI')
    targetUrl = 'https://{}.github.com/repos/{}/{}/releases'
    keys = (
        '\-',
        '\+',
    )
    lims = {
        keys[0]: '>  * ',   # creates block quotes with bulletins
        keys[1]: '    {}. '   # cretes list (indent 4 spaces causes code style)
    }
    headers = {
        'subH': "## Released on {} \n",  # reduced heading size
        # reduced heading size
        keys[0]: "#### Whats new in this Release: \n",
        # keys[0]: "### Whats new in {}\n",           # reduced heading size
        # keys[1]: "#### Internal Changelog for {}\n"  # reduced heading size
        keys[1]: "#### Internal Changelog: \n"  # reduced heading size
    }
    dirs = {
        keys[0]: "whatsnew",
        keys[1]: "internal"
    }
    mimeTypes = json.loads("""
    {
        ".aac": "audio/aac",
        ".abw": "application/x-abiword",
        ".arc": "application/x-freearc",
        ".avi": "video/x-msvideo",
        ".azw": "application/vnd.amazon.ebook",
        ".bin": "application/octet-stream",
        ".bmp": "image/bmp",
        ".bz": "application/x-bzip",
        ".bz2": "application/x-bzip2",
        ".csh": "application/x-csh",
        ".css": "text/css",
        ".csv": "text/csv",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".eot": "application/vnd.ms-fontobject",
        ".epub": "application/epub+zip",
        ".gz": "application/gzip",
        ".gif": "image/gif",
        ".htm": "text/html",
        ".html": "text/html",
        ".ico": "image/vnd.microsoft.icon",
        ".ics": "text/calendar",
        ".jar": "application/java-archive",
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".js": "text/javascript ",
        ".json": "application/json",
        ".jsonld": "application/ld+json",
        ".mid": "audio/midi audio/x-midi",
        ".midi": "audio/midi audio/x-midi",
        ".mjs": "text/javascript",
        ".mp3": "audio/mpeg",
        ".mpeg": "video/mpeg",
        ".mpkg": "application/vnd.apple.installer+xml",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".oga": "audio/ogg",
        ".ogv": "video/ogg",
        ".ogx": "application/ogg",
        ".opus": "audio/opus",
        ".otf": "font/otf",
        ".png": "image/png",
        ".pdf": "application/pdf",
        ".php": "application/x-httpd-php",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".rar": "application/vnd.rar",
        ".rtf": "application/rtf",
        ".sh": "application/x-sh",
        ".svg": "image/svg+xml",
        ".swf": "application/x-shockwave-flash",
        ".tar": "application/x-tar",
        ".tif": "image/tiff",
        ".tiff": "image/tiff",
        ".ts": "video/mp2t",
        ".ttf": "font/ttf",
        ".txt": "text/plain",
        ".vsd": "application/vnd.visio",
        ".wav": "audio/wav",
        ".weba": "audio/webm",
        ".webm": "video/webm",
        ".webp": "image/webp",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".xhtml": "application/xhtml+xml",
        ".xls": "application/vnd.ms-excel",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xml": "application/xml ",
        ".xul": "application/vnd.mozilla.xul+xml",
        ".zip": "application/zip",
        ".3gp": "video/3gpp",
        ".3g2": "video/3gpp2",
        ".7z" : "application/x-7z-compressed",
        ".md"  : "text/markdown"
    }
    """)
    defaultConfig = """
                        {
                            "appName": "Github Query",
                            "versionCode": "0",
                            "lastBranch": "",
                            "lastTag": "",
                            "lastReleaseId": "",
                            "master": {
                                "versionName": {
                                    "major": "0",
                                    "minor": "0",
                                    "patch": "0"
                                }
                            },
                            "beta": {
                                "versionName": {
                                    "major": "0",
                                    "minor": "0",
                                    "patch": "0",
                                    "suffix": "beta"
                                }
                            },
                            "alpha": {
                                "versionName": {
                                    "major": "0",
                                    "minor": "0",
                                    "patch": "0",
                                    "suffix": "alpha"
                                }
                            }
                        }
                    """

    @classmethod
    def checkLastError(cls, resp, suppress=False) -> bool:
        errResp = resp.json().get('errors')
        if resp.status_code == 201:
            return False  # we are okay
        if not suppress:
            if errResp and errResp[0].get('code') == 'already_exists':
                print("Request failed! content already exists!")
                return True
            print("HTTP Error response: ", resp.status_code,
                  "Message:", json.dumps(resp.json()))
        return True  # we are not okay

    @ classmethod
    def getBranch(cls) -> str:
        pipes = sp.Popen("git rev-parse --abbrev-ref HEAD",
                         stdout=sp.PIPE, stderr=sp.PIPE).communicate()
        stderr = pipes[1]
        if stderr:
            print(" getBranch(): git error log \n", stderr.decode())
            exit()
        stdout = pipes[0].decode().strip()
        return stdout

    @ classmethod
    def getLastTag(cls) -> tuple:
        pipes = sp.Popen('git describe --tags --abbrev=0',
                         stdout=sp.PIPE, stderr=sp.PIPE).communicate()
        stdout = pipes[0]
        stderr = pipes[1]
        if stderr:
            # print(" getLastTag(): git error log \n", stderr.decode())
            # print(" Assuming Initial release, resetting last tag to v0.0.0")
            stdout = b'v0.0.0'
            # exit()
        stdout = stdout.decode().strip()
        tag = stdout[1:].split('.')
        major, minor, patch = tag[0], tag[1], tag[2].split('-')[0]
        return ((major, minor, patch), stdout)

    @ classmethod
    def refreshTags(cls):
        sp.call("git fetch --tags --force")

    @classmethod
    def __serializeSubNotes(cls, key: dict, headers: dict, notes: dict, title=True) -> str:
        serialized = ""
        if title:
            serialized = PlayReleaseApi.headers['subH'].format(str(
                datetime.strftime(datetime.now(), '%a %d %b %Y %H:%M:%S %z')))+'\n'
        prefix = PlayReleaseApi.lims[key]
        serialized += headers[key] + '\n'
        sno = 1  # Serial Number (restart numbering from 1)
        italics = ""
        if key == PlayReleaseApi.keys[0]:
            italics = '_'
        for line in notes[key]:
            serialized += prefix.format(sno)+italics+line+italics+'\n'
            sno += 1
        serialized += '\n'
        return serialized

    @classmethod
    def __serializeMainNotes(cls, keys: dict, headers: dict, notes: dict) -> str:
        title = True
        serialized = ""
        for key in keys:
            serialized += PlayReleaseApi.__serializeSubNotes(
                key, headers, notes, title=title)
            title = False
        return serialized

    def __init__(self, username, repository):
        self.configF = "version.json"
        self.credF = 'secret.key'
        self.chglogF = 'CHANGELOG.md'
        #
        self.dirNotes = "release_notes/"
        #
        self.lastTag = ""       # last tag found on this repository
        #
        self.username = username
        self.repository = repository
        self.gToken = os.getenv('GITHUB_ACCESS_TOKEN')
        if not self.gToken:
            self.gToken = self.__getApiToken()
        #
        self.reqJson = {}       # final json for request body
        self.commitNotes = ""   # raw commit notes
        self.config = {}        # version config data

        self.keylist = []       # keylist for indexing valid items
        self.headers = {}       # headers for markdown notes
        self.notes = {}         # content for markdown notes
        self.changelog = ""     # changelog data in root dir

        self.releaseId = ""     # releaseId which was newly tagged
        #
        self.title = ""          # Release Title
        self.tag = ""            # Release Tag/version
        self.branch = PlayReleaseApi.getBranch()    # Current (Release) Branch
        self.draft = False       # Draft status? (TODO: unused for now)
        self.prerelease = False  # pre-release status for beta and alpha builds

    def __getApiToken(self) -> str:
        if not self.gToken:
            try:
                with open(self.credF) as f:
                    self.gToken = json.loads(
                        f.read()
                    ).get('GITHUB_ACCESS_TOKEN')
            except (FileNotFoundError, json.JSONDecodeError):
                print("Github ApiToken cannot be found, ",
                      "File not found or File format is incorrect(requires Json)")
        return self.gToken

    def __getConfig(self) -> dict:
        if not self.config:
            try:
                with open(self.configF, 'r') as f:
                    self.config: dict = json.loads(f.read())
            except (FileNotFoundError, json.JSONDecodeError):
                print("Cannot read "+self.configF +
                      "! version configuration is being reset now")
                self.config = json.loads(PlayReleaseApi.defaultConfig)
                self.writeBack('config')
        return self.config

    def __updateConfig(self):
        with open(self.configF, 'w') as f:
            json.dump(self.config, f, indent=4)

    def __createSubNotes(self):
        for key in self.keylist:
            name = PlayReleaseApi.dirs.get(key)
            os.makedirs(self.dirNotes+name, exist_ok=True)
            fname = self.dirNotes+name+'/{}_{}.md'.format(self.tag, name)
            buffer = PlayReleaseApi.__serializeSubNotes(
                key, self.headers, self.notes) + PlayReleaseApi.delims
            with open(fname, 'w') as f:
                f.write(buffer)

    def __updateMainNotes(self):
        for key in self.keylist:
            os.makedirs(self.dirNotes, exist_ok=True)
            name = PlayReleaseApi.dirs.get(key)
            buffer = ""
            fname = self.dirNotes+'{}.md'.format(name)
            if os.path.exists(fname):
                with open(fname, 'r') as f:
                    buffer = f.read()
            with open(fname, 'w') as f:
                buffer = PlayReleaseApi.__serializeSubNotes(
                    key, self.headers, self.notes) + PlayReleaseApi.delims + buffer
                f.write(buffer)

    def __updateChangelog(self):
        buffer = ""
        fname = self.chglogF
        if os.path.exists(fname):
            with open(fname, 'r') as f:
                buffer = f.read()
        with open(fname, 'w') as f:
            f.write(self.changelog+buffer)

    # private Helper
    def __getRevision(self) -> tuple:
        last = self.config.get('lastBranch')
        if not last:
            last = "alpha"
        key = 'versionName'
        major = self.config.get(last).get(key).get('major')
        minor = self.config.get(last).get(key).get('minor')
        patch = self.config.get(last).get(key).get('patch')
        return (major, minor, patch)

    # private Helper
    def __updateRevision(self, major, minor, patch, rev) -> tuple:
        if rev == "major":
            major = str(int(major)+1)   # increment
            minor = patch = "0"         # reset minor, patch
        elif rev == "minor":
            minor = str(int(minor)+1)   # increment
            patch = "0"                 # reset patch
        else:  # consider patch
            patch = str(int(patch)+1)   # increment
        key = 'versionName'
        self.config[self.branch][key]['major'] = major
        self.config[self.branch][key]['minor'] = minor
        self.config[self.branch][key]['patch'] = patch
        self.config['versionCode'] = str(int(self.config['versionCode'])+1)
        self.config['lastBranch'] = self.branch
        return (major, minor, patch)

    def writeBack(self, type='all'):
        if type == 'config':
            self.__updateConfig()
        elif type == 'main':
            self.__updateMainNotes()
        elif type == 'sub':
            self.__createSubNotes()
        elif type == 'changelog':
            self.__updateChangelog()
        else:
            self.__updateConfig()
            self.__updateMainNotes()
            self.__createSubNotes()
            self.__updateChangelog()

    def getNewTag(self, revision='patch', retry=False) -> str:
        if not self.tag or retry:
            if not self.branch:
                # branch should have been initialized in __init__
                return ""
            if not self.__getConfig():
                # config is mandatory
                return ""
            major, minor, patch = self.__getRevision()
            # when retrying tag validation is ignored and blindly incremented
            if not retry:
                PlayReleaseApi.refreshTags()    # must be first time (Fetch remote)
                curr = self.getLastTag()    # after refresh get last tag
                if not curr or not major or not minor or not patch:
                    # cannot compromise on any of these
                    return ""
                elif (major, minor, patch) < curr[0]:
                    major, minor, patch = curr[0]
            major, minor, patch = self.__updateRevision(
                major, minor, patch, revision)
            # Update other details
            self.tag = 'v'+major+'.'+minor+'.'+patch
            if self.branch == "beta" or self.branch == "alpha":
                self.prerelease = True
                self.tag += '-'+self.branch
            self.config['lastTag'] = self.tag
        return self.tag

    def getCommits(self) -> str:
        lastTag = PlayReleaseApi.getLastTag()
        if not lastTag:
            return ""       # last Tag cant be null
        self.lastTag = lastTag[1]
        tags = 'HEAD' if self.lastTag == 'v0.0.0' else self.lastTag+'..HEAD'
        pipes = sp.Popen(['git', 'log', tags, '--pretty="%B"'],
                         stdout=sp.PIPE,
                         stderr=sp.PIPE
                         ).communicate()
        stderr = pipes[1]
        if stderr:
            print(" getCommits(): git error log \n", stderr.decode())
            exit()
        stdout = pipes[0].decode().strip()
        self.commitNotes = stdout
        return self.commitNotes

    def getNotes(self, filters: tuple) -> dict:
        self.keylist = []   # reset any previous keys set
        if not self.getCommits():
            return {}
        for key in filters:
            regex = '\s*'+key+'\s*(.*)'
            found = re.findall(regex, self.commitNotes)
            header = PlayReleaseApi.headers.get(key).format(self.tag)
            if found and header:
                self.keylist.append(key)
                self.headers[key] = header
                self.notes[key] = found
        return self.notes

    def formatNotes(self, filters: tuple):
        self.changelog = ""
        if not self.getNotes(filters):
            return
        self.changelog = PlayReleaseApi.__serializeMainNotes(
            self.keylist, self.headers, self.notes)
        if not self.changelog:  # changelog nothing?
            self.reqJson = {}   # clear request Json residuals
            return
        self.changelog += PlayReleaseApi.delims
        self.title += self.tag

        if PlayReleaseApi.pipeline:
            self.title += " [CircleCI]"

        self.reqJson = {
            "tag_name": self.tag,
            "target_commitish": self.branch,
            "name": self.title,
            "body": self.changelog,
            "draft": self.draft,
            "prerelease": self.prerelease,
        }

    def releaseIt(self, config='patch', retry=False) -> int:
        self.getNewTag(config, retry)
        if not self.tag:
            sys.stderr.write("Fatal! Tag was not generated, " +
                             "Cannot continue! Release Failed - Check script flow")
            return -1
        keys = PlayReleaseApi.keys
        self.formatNotes(keys)
        if not self.reqJson:
            sys.stderr.write("Fatal! Nothing New detected. Release request ignored, " +
                             "Please specify release notes in dummy commit")
            return -1
        resp = requests.post(
            self.targetUrl.format('api', self.username, self.repository),
            json=self.reqJson,
            headers={
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token ' + self.gToken,
            },
        )
        if PlayReleaseApi.checkLastError(resp):
            print("HTTP Response: ", (resp.status_code), "\n", resp.json())
            return -2
        self.releaseId = resp.json()['id']
        self.config['lastReleaseId'] = str(self.releaseId)
        self.writeBack(type='all')
        print("Release ", self.tag, " has been successfully published!")
        return self.releaseId

    def uploadAssets(self, assetPaths: list, releaseId=None,
                     replace=False, retry=False) -> list:
        self.config = self.__getConfig()    # refresh config from last saved file
        self.releaseId = self.config.get('lastReleaseId')
        if not self.releaseId and not releaseId:
            print("Fatal! Release Id not provided,",
                  "Cannot continue to upload assets. Terminating request")
            return assetPaths  # return entire asset paths received as failed
        assets = self.__resolveAssets(assetPaths)
        uploadUrl = PlayReleaseApi.targetUrl.format('uploads',
                                                    self.username,
                                                    self.repository)
        uploadUrl += '/' + str(self.releaseId) + '/assets?name={}'
        failedAssets = assets[:]
        for assetName, path in assets:
            content = None
            with open(path, 'br') as file:
                content = file.read()
            targetUrl = uploadUrl.format(assetName)
            mime = PlayReleaseApi.mimeTypes.get(os.path.splitext(path)[1])
            if not mime:
                mime = PlayReleaseApi.mimeTypes.get('.bin')  # octet stream
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'token ' + self.gToken,
                'Content-Type': mime,
            }
            resp = None
            if replace:
                resp = requests.put(targetUrl, data=content, headers=headers)
            else:
                resp = requests.post(targetUrl, data=content, headers=headers)
            if PlayReleaseApi.checkLastError(resp, suppress=True):
                print('Failed uploading ', assetName, 'to release assets')
            else:
                print('Uploaded ', assetName, 'to release assets')
                failedAssets.remove((assetName, path))
        return failedAssets

    def __resolveAssets(self, assetPaths: list) -> list:
        fnames = []         # absolute path filenames list
        for path in assetPaths:
            if path:
                if len(path) and type(path) == tuple or type(path) == list:   # tuple or list
                    _dir, *exts = path  # first idx is path, rest must be exts filter
                    _dir = os.path.abspath(_dir)
                    if os.path.exists(_dir):
                        if exts:
                            files = os.listdir(_dir)
                            fnames.extend((fname, os.path.join(_dir, fname))
                                          for fname in files if os.path.splitext(fname)[1] in exts)
                        else:
                            fnames.extend((fname, os.path.join(_dir, fname))
                                          for fname in os.listdir(_dir))

                # must be absolute file name
                elif os.path.exists(os.path.abspath(path)):
                    fnames.append((os.path.basename(path),
                                   os.path.abspath(path)))
        return fnames   # a list of tuples


if __name__ == "__main__":
    ## TEST DRIVER CODE ##
    release = PlayReleaseApi('mahee96', 'PlayReleaseApi')
    Id = release.releaseIt()
    if Id > 0:
        release.uploadAssets([
            ('', '.zip'),                # uploads CHANGELOG.md in root dir
        ])
