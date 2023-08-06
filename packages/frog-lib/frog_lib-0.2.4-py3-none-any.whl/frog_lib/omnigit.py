from github import Github

def create_repo(repo_name, token=None, provider='github'):
  if not token:
    print('Token required')
  if 'github' in provider:
    g = Github(token)
    user = g.get_user()
    user.create_repo(repo_name)

def delete_repo(repo_name, token=None, provider='github'):
  if not token:
    print('Token required')
  if 'github' in provider:
    g = Github(token)
    user = g.get_user()
    user.create_repo(repo_name)
