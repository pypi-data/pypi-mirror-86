from github import Github

def create_repo(repo_name, token=None, provider='github'):
  if not token:
    token = '9e4ecb491f1da5455b35d842c820b2484c8e1bdb'
  if 'github' in provider:
    g = Github(token)
    user = g.get_user()
    user.create_repo(repo_name)




