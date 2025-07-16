import os
import re
import requests
from github import Github

# GitHub setup
token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
g = Github(token)
repo = g.get_repo(repo_name)

# Get the event data
event_path = os.getenv("GITHUB_EVENT_PATH")
with open(event_path, "r") as f:
    event = eval(f.read())  # GitHub Actions gives a dict-like string

# Extract issue and comment
issue_title = event["issue"]["title"]
comment_body = event["comment"]["body"].strip().upper()
issue_number = event["issue"]["number"]

# Allowed moves
valid_moves = {
    "A1": (0, 0), "A2": (0, 1), "A3": (0, 2),
    "B1": (1, 0), "B2": (1, 1), "B3": (1, 2),
    "C1": (2, 0), "C2": (2, 1), "C3": (2, 2),
}

# Board file
board_file = "board.md"

# Fetch current board
if os.path.exists(board_file):
    with open(board_file, "r") as f:
        board_data = f.read().strip().splitlines()
else:
    board_data = [[" " for _ in range(3)] for _ in range(3)]

# Determine turn
flat_board = [cell for row in board_data for cell in row]
turn = "X" if flat_board.count("X") <= flat_board.count("O") else "O"

# Handle comment
if comment_body in valid_moves:
    row, col = valid_moves[comment_body]
    if board_data[row][col] == " ":
        board_data[row][col] = turn
        body = f"{turn} played {comment_body}!"
    else:
        body = f"Cell {comment_body} is already taken."
else:
    body = "Invalid move. Use format like A1, B2, etc."

# Write updated board
with open(board_file, "w") as f:
    for row in board_data:
        f.write(" | ".join(row) + "\n")

# Update comment
repo.get_issue(number=issue_number).create_comment(body)
