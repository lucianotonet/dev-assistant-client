class InterpreterModule:
    import interpreter

    def __init__(self):
        pass

    def execute(self, operation, args):
        if operation == 'run':
            return self.run(args.get('command'))
        else:
            return {'error': f'Unknown operation: {operation}'}

    def run(self, command):
        """
        Run a command in the interpreter
        https://github.com/KillianLucas/open-interpreter#programmatic-chat
        """
        try:
            self.interpreter.auto_run = True
            response = self.interpreter.chat(command)
            return {'response': response}
        except Exception as e:
            return {'error': str(e)}