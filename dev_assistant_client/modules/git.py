import json
import os
import logging
from git import Repo
from ..utils import StateManager

class GitModule:
    def __init__(self, instruction):
        self.client_id = instruction.get("client_id")
        self.feedback = instruction.get("feedback")
        self.operation = instruction.get("operation")
        self.arguments = instruction.get("arguments")

        self.state_manager = StateManager()
        self.state = self.state_manager.get_state()  # Load the state or set default values
        self.repo = Repo(self.state.get("cwd", os.getcwd()))  # Load the Git repository

        self.operations = {
            "add": self.add,
            "commit": self.commit,
            "push": self.push,
            "pull": self.pull,
            "checkout": self.checkout,
            "status": self.status,
            "clone": self.clone,
            "branch": self.branch,
            "merge": self.merge,
            "rebase": self.rebase,
            "reset": self.reset,
            "tag": self.tag,
            "init": self.init,
            "remotes": self.remotes,
            "tags": self.tags,
            "branches": self.branches,
            "head": self.head,
            "index": self.index,
            "blame": self.blame,
            "diff": self.diff,
            "stash": self.stash,
            "fetch": self.fetch,
            "log": self.log,
            "show": self.show,
            "rev_parse": self.rev_parse,
            "remote": self.remote,
            "submodule": self.submodule,
            "git_dir": self.git_dir,
            "working_tree_dir": self.working_tree_dir,
            "is_dirty": self.is_dirty,
            "is_clean": self.is_clean,
            "is_repo": self.is_repo,
            "get_config": self.get_config,
            "set_config": self.set_config,
            "unset_config": self.unset_config,
            "get_remotes": self.get_remotes,
            "get_branches": self.get_branches,
            "get_tags": self.get_tags,
            "get_head": self.get_head,
            "get_index": self.get_index,
            "get_blame": self.get_blame,
            "get_diff": self.get_diff,
            "api_spec": self.get_api_spec
        }

    def get_api_spec(self, *args):
        return {
            "module": "Git",
            "operations": {
                "add": {"summary": "Add files to the staging area.", "params": ["files"]},
                "commit": {"summary": "Create a new commit with the staged changes.", "params": ["message"]},
                "push": {"summary": "Push the local repository to a remote repository.", "params": ["remote", "branch"]},
                "pull": {"summary": "Pull changes from a remote repository and merge them into the local repository.", "params": ["remote", "branch"]},
                "checkout": {"summary": "Switch to a different branch or commit.", "params": ["branch", "commit"]},
                "status": {"summary": "Show the current status of the repository.", "params": []},
                "clone": {"summary": "Clone a remote repository to the local machine.", "params": ["url", "directory"]},
                "branch": {"summary": "Create a new branch.", "params": ["name"]},
                "merge": {"summary": "Merge two branches together.", "params": ["branch"]},
                "rebase": {"summary": "Rebase the current branch onto another branch.", "params": ["branch"]},
                "reset": {"summary": "Reset the repository to a previous state.", "params": ["commit"]},
                "tag": {"summary": "Create a new tag for a commit.", "params": ["name", "commit"]},
                "init": {"summary": "Initialize a new Git repository.", "params": []},
                "remotes": {"summary": "List all configured remotes.", "params": []},
                "tags": {"summary": "List all tags.", "params": []},
                "branches": {"summary": "List all branches.", "params": []},
                "head": {"summary": "Get the current branch.", "params": []},
                "index": {"summary": "Get the current index.", "params": []},
                "blame": {"summary": "Show the blame information for a file.", "params": ["file"]},
                "diff": {"summary": "Show the differences between two files or commits.", "params": ["file", "commit"]},
                "stash": {"summary": "Stash the current changes.", "params": []},
                "fetch": {"summary": "Fetch changes from a remote repository.", "params": ["remote"]},
                "log": {"summary": "Show the commit history.", "params": []},
                "show": {"summary": "Show the details of a commit.", "params": ["commit"]},
                "rev_parse": {"summary": "Parse a revision reference.", "params": ["revision"]},
                "remote": {"summary": "Get or set the URL of a remote.", "params": ["name", "url"]},
                "submodule": {"summary": "Add, delete, or update a submodule.", "params": ["command", "name", "url"]},
                "git_dir": {"summary": "Get the Git directory of the repository.", "params": []},
                "working_tree_dir": {"summary": "Get the working tree directory of the repository.", "params": []},
                "is_dirty": {"summary": "Check if the repository has uncommitted changes.", "params": []},
                "is_clean": {"summary": "Check if the repository has no uncommitted changes.", "params": []},
                "is_repo": {"summary": "Check if the current directory is a Git repository.", "params": []},
                "get_config": {"summary": "Get the value of a configuration variable.", "params": ["name"]},
                "set_config": {"summary": "Set the value of a configuration variable.", "params": ["name", "value"]},
                "unset_config": {"summary": "Unset a configuration variable.", "params": ["name"]},
                "get_remotes": {"summary": "Get the list of configured remotes.", "params": []},
                "get_branches": {"summary": "Get the list of branches.", "params": []},
                "get_tags": {"summary": "Get the list of tags.", "params": []},
                "get_head": {"summary": "Get the current branch or commit.", "params": []},
                "get_index": {"summary": "Get the current index.", "params": []},
                "get_blame": {"summary": "Get the blame information for a file.", "params": ["file"]},
                "get_diff": {"summary": "Get the differences between two files or commits.", "params": ["file", "commit"]},
            }
        }

    def execute(self):
        if self.arguments is None:
            self.arguments = []
        operation_func = self.operations.get(self.operation, self.unknown_operation)
        try:
            result = operation_func(self.arguments)
            if not isinstance(result, str):
                result = json.dumps(result)
            logging.info(f"{self.operation} executed successfully with arguments {self.arguments}")
            return result
        except Exception as e:
            logging.exception(f"Unexpected error while executing {self.operation} with arguments {self.arguments}")
            return json.dumps({'error': str(e)})

    def unknown_operation(self, args):
        return json.dumps({'error': f'Unknown operation: {self.operation}. Please check the operation name and try again.'})
    # Git operations
    def add(self, args):
        self.repo.git.add(args[0])
        return json.dumps({'success': f'Files {args[0]} added successfully'})

    def commit(self, args):
        self.repo.git.commit(m=args[0], author="Dev Assistant AI <devassistant@tonet.dev>")
        return json.dumps({'success': f'Commit successful with message: {args[0]}'})

    def push(self, args):
        self.repo.git.push(args[0], args[1])
        return json.dumps({'success': f'Push to {args[0]} successful'})

    def pull(self, args):
        self.repo.git.pull(args[0], args[1])
        return json.dumps({'success': f'Pull from {args[0]} successful'})

    def checkout(self, args):
        self.repo.git.checkout(args[0])
        return json.dumps({'success': f'Checkout to {args[0]} successful'})

    def clone(self, args):
        self.repo.git.clone(args[0], args[1])
        return json.dumps({'success': f'Clone from {args[0]} successful'})

    def branch(self, args):
        self.repo.git.branch(args[0])
        return json.dumps({'success': f'Branch {args[0]} created successfully'})

    def merge(self, args):
        self.repo.git.merge(args[0])
        return json.dumps({'success': f'Merge {args[0]} successful'})

    def rebase(self, args):
        self.repo.git.rebase(args[0])
        return json.dumps({'success': f'Rebase {args[0]} successful'})

    def reset(self, args):
        self.repo.git.reset(args[0])
        return json.dumps({'success': f'Reset {args[0]} successful'})

    def tag(self, args):
        self.repo.git.tag(args[0], args[1])
        return json.dumps({'success': f'Tag {args[0]} created successfully'})

    def init(self, args):
        self.repo.git.init(args[0])
        return json.dumps({'success': f'Initialized empty Git repository in {args[0]}'})

    def remotes(self, args):
        remotes = self.repo.git.remotes(args[0])
        return json.dumps({'remotes': remotes})

    def tags(self, args):
        tags = self.repo.git.tags(args[0])
        return json.dumps({'tags': tags})

    def branches(self, args):
        branches = self.repo.git.branches(args[0])
        return json.dumps({'branches': branches})

    def head(self, args):
        head = self.repo.git.head(args[0])
        return json.dumps({'head': head})

    def index(self, args):
        index = self.repo.git.index(args[0])
        return json.dumps({'index': index})

    def blame(self, args):
        blame = self.repo.git.blame(args[0])
        return json.dumps({'blame': blame})

    def diff(self, args):
        diff = self.repo.git.diff(args[0], args[1])
        return json.dumps({'diff': diff})

    def stash(self, args):
        self.repo.git.stash(args[0])
        return json.dumps({'success': f'Stashed changes in {args[0]}'})

    def fetch(self, args):
        self.repo.git.fetch(args[0])
        return json.dumps({'success': f'Fetched updates from {args[0]}'})

    def log(self, args):
        log = self.repo.git.log(args[0])
        return json.dumps({'log': log})

    def show(self, args):
        show = self.repo.git.show(args[0])
        return json.dumps({'show': show})

    def rev_parse(self, args):
        rev_parse = self.repo.git.rev_parse(args[0])
        return json.dumps({'rev_parse': rev_parse})

    def remote(self, args):
        remote = self.repo.git.remote(args[0])
        return json.dumps({'remote': remote})

    def submodule(self, args):
        submodule = self.repo.git.submodule(args[0])
        return json.dumps({'submodule': submodule})

    def git_dir(self, args):
        git_dir = self.repo.git_dir
        return json.dumps({'git_dir': git_dir})

    def working_tree_dir(self, args):
        working_tree_dir = self.repo.working_tree_dir
        return json.dumps({'working_tree_dir': working_tree_dir})
    
    def is_dirty(self, args):
        is_dirty = self.repo.is_dirty()
        return json.dumps({'is_dirty': is_dirty})

    def is_clean(self, args):
        is_clean = self.repo.is_clean()
        return json.dumps({'is_clean': is_clean})

    def is_repo(self, args):
        is_repo = self.repo.is_repo()
        return json.dumps({'is_repo': is_repo})

    def get_config(self, args):
        config = self.repo.config(args[0])
        return json.dumps({'config': config})

    def set_config(self, args):
        self.repo.config(args[0], args[1])
        return json.dumps({'success': f'Set config {args[0]}'})

    def unset_config(self, args):
        self.repo.config(args[0])
        return json.dumps({'success': f'Unset config {args[0]}'})

    def get_remotes(self, args):
        remotes = self.repo.remotes(args[0])
        return json.dumps({'remotes': remotes})

    def get_branches(self, args):
        branches = self.repo.branches(args[0])
        return json.dumps({'branches': branches})

    def get_tags(self, args):
        tags = self.repo.tags(args[0])
        return json.dumps({'tags': tags})

    def get_head(self, args):
        head = self.repo.head(args[0])
        return json.dumps({'head': head})

    def get_index(self, args):
        index = self.repo.index(args[0])
        return json.dumps({'index': index})

    def get_blame(self, args):
        blame = self.repo.blame(args[0])
        return json.dumps({'blame': blame})

    def get_diff(self, args):
        diff = self.repo.diff(args[0], args[1])
        return json.dumps({'diff': diff})

    def get_stash(self, args):
        stash = self.repo.stash(args[0])
        return json.dumps({'stash': stash})

    def get_fetch(self, args):
        fetch = self.repo.fetch(args[0])
        return json.dumps({'fetch': fetch})

    def status(self, args):
        status = self.repo.git.status(args[0])
        return json.dumps({'status': status})