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
                            
    def execute(self):        
        if self.arguments is None:
            self.arguments = []
        operation_func = getattr(self, self.operation, self.unknown_operation)
        try:
            result = operation_func(self.arguments)
            logging.info(f"{self.operation} executed successfully with arguments {self.arguments}")
            return result
        except Exception as e:
            logging.exception(f"Unexpected error while executing {self.operation} with arguments {self.arguments}")
            return json.dumps({'error': str(e)})

    def unknown_operation(self, args):
        return json.dumps({'error': f'Unknown operation: {self.operation}. Please check the operation name and try again.'})

    # Git operations
    def add(self, args):
        self.repo.git.add(*args)
        return json.dumps({'success': f'Files {args} added successfully'})

    def commit(self, args):
        self.repo.git.commit(m=args[0], author="Dev Assistant AI <devassistant@tonet.dev>")
        return json.dumps({'success': f'Commit successful with message: {args[0]}'})

    def push(self, args):
        self.repo.git.push(*args)
        return json.dumps({'success': f'Push to {args} successful'})

    def pull(self, args):
        self.repo.git.pull(*args)
        return json.dumps({'success': f'Pull from {args} successful'})

    def checkout(self, args):
        self.repo.git.checkout(*args)
        return json.dumps({'success': f'Checkout to {args} successful'})

    def status(self, args):
        status = self.repo.git.status()
        return json.dumps({'status': f'Current status: {status}'})

    def clone(self, args):
        self.repo.git.clone(*args)
        return json.dumps({'success': f'Clone from {args} successful'})

    def branch(self, args):
        self.repo.git.branch(*args)
        return json.dumps({'success': f'Branch {args} created successfully'})

    def merge(self, args):
        self.repo.git.merge(*args)
        return json.dumps({'success': f'Merge {args} successful'})

    def rebase(self, args):
        self.repo.git.rebase(*args)
        return json.dumps({'success': f'Rebase {args} successful'})

    def reset(self, args):
        self.repo.git.reset(*args)
        return json.dumps({'success': f'Reset {args} successful'})

    def tag(self, args):
        self.repo.git.tag(*args)
        return json.dumps({'success': f'Tag {args} created successfully'})

    def init(self, args):
        self.repo.git.init(*args)
        return json.dumps({'success': f'Initialized empty Git repository in {args}'})

    def remotes(self, args):
        remotes = self.repo.git.remotes(*args)
        return json.dumps({'remotes': remotes})

    def tags(self, args):
        tags = self.repo.git.tags(*args)
        return json.dumps({'tags': tags})

    def branches(self, args):
        branches = self.repo.git.branches(*args)
        return json.dumps({'branches': branches})

    def head(self, args):
        head = self.repo.git.head(*args)
        return json.dumps({'head': head})

    def index(self, args):
        index = self.repo.git.index(*args)
        return json.dumps({'index': index})

    def blame(self, args):
        blame = self.repo.git.blame(*args)
        return json.dumps({'blame': blame})

    def diff(self, args):
        diff = self.repo.git.diff(*args)
        return json.dumps({'diff': diff})

    def stash(self, args):
        self.repo.git.stash(*args)
        return json.dumps({'success': f'Stashed changes in {args}'})

    def fetch(self, args):
        self.repo.git.fetch(*args)
        return json.dumps({'success': f'Fetched updates from {args}'})

    def log(self, args):
        log = self.repo.git.log(*args)
        return json.dumps({'log': log})

    def show(self, args):
        show = self.repo.git.show(*args)
        return json.dumps({'show': show})

    def rev_parse(self, args):
        rev_parse = self.repo.git.rev_parse(*args)
        return json.dumps({'rev_parse': rev_parse})

    def remote(self, args):
        remote = self.repo.git.remote(*args)
        return json.dumps({'remote': remote})

    def submodule(self, args):
        submodule = self.repo.git.submodule(*args)
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
        config = self.repo.config(*args)
        return json.dumps({'config': config})

    def set_config(self, args):
        self.repo.config(*args)
        return json.dumps({'success': f'Set config {args}'})

    def unset_config(self, args):
        self.repo.config(*args)
        return json.dumps({'success': f'Unset config {args}'})

    def get_remotes(self, args):
        remotes = self.repo.remotes(*args)
        return json.dumps({'remotes': remotes})

    def get_branches(self, args):
        branches = self.repo.branches(*args)
        return json.dumps({'branches': branches})

    def get_tags(self, args):
        tags = self.repo.tags(*args)
        return json.dumps({'tags': tags})

    def get_head(self, args):
        head = self.repo.head(*args)
        return json.dumps({'head': head})

    def get_index(self, args):
        index = self.repo.index(*args)
        return json.dumps({'index': index})

    def get_blame(self, args):
        blame = self.repo.blame(*args)
        return json.dumps({'blame': blame})

    def get_diff(self, args):
        diff = self.repo.diff(*args)
        return json.dumps({'diff': diff})

    def get_stash(self, args):
        stash = self.repo.stash(*args)
        return json.dumps({'stash': stash})

    def get_fetch(self, args):
        fetch = self.repo.fetch(*args)
        return json.dumps({'fetch': fetch})
