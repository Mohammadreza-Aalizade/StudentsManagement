from telegram import Update
from telegram.ext import CallbackContext
from abc import ABC, abstractmethod

from bot import DatabaseConnector


class Responder(ABC):
    def __init__(self, dbc: DatabaseConnector):
        self.dbc = dbc

    @abstractmethod
    def handel_command(self, update: Update, context: CallbackContext, user): pass

    @abstractmethod
    def handel_private_message(self, update: Update, context: CallbackContext, user): pass

    @abstractmethod
    def handel_call_back_query(self, update: Update, context: CallbackContext, user): pass


