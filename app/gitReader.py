from github import Github
from github import Auth


def login(ACCESS_KEY):
    return Github(ACCESS_KEY)

def getRepo(g, repoName):
    return g.get_user().get_repo(repoName)

def getAllContents(repo):
    return repo.get_contents("")

def makeList(repo, contents):
    res = []
    for content_file in contents:
        if content_file.name.endswith((".txt", ".DS_Store", ".tar.gz", ".zip" , ".pdf", ".tgz", ".exe")):
            continue
        if content_file.type == "file":
            try:
                curContent = repo.get_contents(content_file.path)
                curContent_txt = curContent.decoded_content.decode("utf-8")
                res.append((content_file.path, curContent_txt))
            except:
                continue

        elif content_file.type == "dir":
            contents.extend(repo.get_contents(content_file.path))
    return res
# print(g.get_repo("PyGithub/PyGithub"))
# contents = repo.get_contents("")
# for content_file in contents:
#     if content_file.type == "dir":
#         print(f"Directory: {content_file.name}")
#     else:
#         print(f"File: {content_file.name}")
# readme_contents = repo.get_contents("spec.md")
# readme_text = readme_contents.decoded_content.decode("utf-8")
# print(readme_text)

# TEST = repo.get_contents("TableEntry.cpp")
# TEST_TXT = TEST.decoded_content.decode("utf-8")
# print(TEST_TXT)