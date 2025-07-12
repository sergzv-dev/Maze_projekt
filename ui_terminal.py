'''User interface for terminal'''

class UI():
    def ask(self, text):
        answer = input(text)
        return answer

    def choose(self, options):
        create_opt = '\n'.join(f'{i}: {num + 1}' for num, i in enumerate(options))
        answer = input(f'{create_opt}\n...')
        return options[int(answer)-1]

    def say(self, text):
        print(text)