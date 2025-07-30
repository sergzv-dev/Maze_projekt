'''User interface for terminal'''

class UI():
    def ask(self, text):
        answer = input(text)
        return answer

    def choose(self, options):
        create_opt = '\n'.join(f'{i}: {num + 1}' for num, i in enumerate(options))
        while True:
            answer = self.ask(f'{create_opt}\n...')
            try:
                if 0 < int(answer) <= len(options):
                    return options[int(answer)-1]
                else: raise ValueError
            except ValueError:
                self.say('Darkness envelops your mind.. Try again!\n')
                continue

    def say(self, text):
        print(text)