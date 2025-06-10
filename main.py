import starkbank

# Get your private key from an environment variable or an encrypted database.
# This is only an example of a private key content. You should use your own key.
private_key_content = """
-----BEGIN EC PARAMETERS-----
BgUrgQQACg==
-----END EC PARAMETERS-----
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIHX3joDOT1x+Wgf9JKh+UykiuBFSOnNk93Z2p1WhfOHXoAcGBSuBBAAK
oUQDQgAE9yvqkZBi2bp+y8JUYolrS1OVCJ94ICrrvfBJl+vavZBSeZ0dLkqu5zMW
3JzTFaGqN9MSfydn3RnMqkPSYrdhzA==
-----END EC PRIVATE KEY-----
"""

project = starkbank.Project(
    environment="challenge-juliano-assine",
    id="5656565656565656",
    private_key=private_key_content
)

