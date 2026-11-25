from abc import ABC, abstractmethod

class Notifier(ABC):

    @staticmethod
    @abstractmethod
    def send(message):
        pass

class EmailNotifier(Notifier):

    @staticmethod
    def send(message):
        print(f'Отправлено сообщение по email: {message}')

class TelegramNotifier(Notifier):

    @staticmethod
    def send(message):
        print(f'Отправлено сообщение в telegram: {message}')


e = EmailNotifier()
t = TelegramNotifier()

for obj in (e, t):
    obj.send('сообщение')