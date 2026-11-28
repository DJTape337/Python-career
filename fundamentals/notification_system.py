from abc import ABC, abstractmethod

class Notifier(ABC):

    @staticmethod
    @abstractmethod
    def send(message: str):
        pass

class EmailNotifier(Notifier):
    @staticmethod
    def send(message: str):
        print(f'Отправлено сообщение по email: {message}')

class TelegramNotifier(Notifier):
    @staticmethod
    def send(message: str):
        print(f'Отправлено сообщение в телеграм: {message}')

class User:
    def __init__(self, name: str, email: str):
        if not '@' in email:
            raise ValueError('Некорректный email')
        self.name = name
        self._email = email

    def get_email(self):
        return self._email

    def set_email(self, email: str):
        if not '@' in email:
            raise ValueError('Некорректный email')
        self._email = email

class NotificationService:

    def __init__(self, notifiers: list):
        if not all([isinstance(x, Notifier) for x in notifiers]):
            raise ValueError('Некорректный список уведомителей')
        self._notifiers = notifiers

    def notify(self, message):
        for notifier in self._notifiers:
            notifier.send(message)