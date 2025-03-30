import requests

def get_github_user(username: str):

    response = requests.get(f"https://api.github.com/users/{username}")
    if response.status_code == 200:
         return response.json()
    else:
        return None


if __name__ == "__main__":
    username = input("Enter a GitHub username: ")
    user_data = get_github_user(username)
    if user_data:
        print(f"User: {user_data['login']}")
        print(f"Name: {user_data['name']}")
        print(f"Public Repos: {user_data['public_repos']}")
    else:
        print("User not found.")