import pandas as pd
from github import Github
from datetime import datetime
import os

def fetch_data(repos):

    issues_data = []
    
    for repo in repos:
        issues = repo.get_issues(state="all")
        
        for issue in issues:
            issues_data.append(
                {
                    'Issue': f"{issue.number} - {issue.title}", 
                    'State': issue.state, 
                    'Created at': issue.created_at, 
                    'Closed at': issue.closed_at,
                    'Last update': issue.updated_at,
                    'Labels': [label.name for label in issue.labels],
                    'Reactions': issue.reactions['total_count'],
                    'Comments': issue.comments,
                    'URL': issue.html_url,
                    'Repository': repo.name,
                    'Author': issue.user.login
                }
            )
    return pd.DataFrame(issues_data)

def get_org_members(repos):
    members = []
    orgs = [repo.organization.login for repo in repos]
    
    for org in orgs:
        organization = g.get_organization(org)
        org_members = organization.get_members()
        for member in org_members:
            members.append(member.login)

    members.extend(['pre-commit-ci[bot]','damianpumar','burtenshaw','sdiazlor','ignacioct'])
    return members

def save_data(repos, data_path):
    df = fetch_data(repos)

    open_issues = df.loc[df['State'] == 'open']

    engagement_df = open_issues[["URL","Issue","Repository","Reactions","Comments"]].sort_values(by=["Reactions", "Comments"], ascending=False).head(10).reset_index()

    members = get_org_members(repos)
    community_issues = df.loc[~df['Author'].isin(members)]
    community_issues_df = community_issues[["URL","Issue","Repository","Created at","Author","State"]].sort_values(by=["Created at"], ascending=False).head(10).reset_index()

    with open(data_path, "w") as f:
        f.write(f"**Most engaging open issues:**\n")
        f.write(f"| Rank | Issue | Reactions | Comments |\n")
        f.write(f"|------|-------|:---------:|:--------:|\n")
        for ix,row in engagement_df.iterrows():
            f.write(f"| {ix+1} | [{row['Issue']}]({row['URL']}) | 👍 {row['Reactions']} | 💬 {row['Comments']} |\n")

        f.write(f"**Latest issues open by the community:**\n")
        f.write(f"| Rank | Issue | Author |\n")
        f.write(f"|------|-------|:------:|\n")
        for ix,row in community_issues_df.iterrows():
            if row['State'] == 'open':
                state = '🟢'
            else:
                state = '🟣'

            f.write(f"| {ix+1} | {state} [{row['Issue']}]({row['URL']}) | by **{row['Author']}** |\n")
        today = datetime.today().date()
        f.write(f"\nLast updated: {today}\n")

if __name__ == "__main__":
    g = Github(os.environ["GITHUB_ACCESS_TOKEN"])
    repos = ["argilla-io/argilla", "argilla-io/argilla-server"]
    repos = [g.get_repo(repo) for repo in repos]
    data_path = "../overview/community/popular_issues.md"
    save_data(repos, data_path)