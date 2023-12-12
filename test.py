from herre import github_desktop


with github_desktop(
    client_id="dfdb2c594470db113659",  # This is a demo github oauth2 app
    client_secret="bc59f1e3bc1ed0dcfb3548b457588f3b6e324764",
) as g:
    print(g.get_token())
