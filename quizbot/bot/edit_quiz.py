"""
Module with methods to rename and remove a quiz with a telegram bot
"""
import logging
import pymongo
import os
from telegram.chataction import ChatAction
from telegram.ext.conversationhandler import ConversationHandler

db = pymongo.MongoClient(os.environ.get('MONGODB')).quizzes

# user data
user_dict = dict()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start_remove(update, _):
    """Start a process to remove a quiz."""

    logger.info('[%s] Removing process initialized',
                update.message.from_user.username)
    update.message.reply_text(
        "Какую викторину хотите удалить? 🙂"
    )
    return 'ENTER_NAME'


def enter_name_remove(update, context):
    """Deltes a quiz after entering its' name."""

    quiz_creator = update.message.from_user.username
    quiz_name = update.message.text

    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    user_col = db[quiz_creator]

    # Checks if the quiz exists
    if user_col.find_one({'quizname': quiz_name}) is None:
        logger.info('[%s] Entered quiz %s doesn\'t exist',
                    update.message.from_user.username, quiz_name)
        update.message.reply_text(
            "Викторина '{}' не найдена 😕\nВведите другое название или отмените изменения, введя /cancelEdit 🙆‍♂️".format(
                quiz_name)
        )
        return 'ENTER_NAME'

    # Deletes the quiz
    user_col.delete_one({'quizname': quiz_name})
    logger.info('[%s] Removed %s',
                update.message.from_user.username, quiz_name)
    update.message.reply_text(
        "Викторина '{}' удалена 👍".format(quiz_name)
    )
    return ConversationHandler.END


def start_rename(update, _):
    """Starts a process to rename a quiz."""

    logger.info('[%s] Renaming process initialized',
                update.message.from_user.username)
    update.message.reply_text(
        "Какую викторину хотите переименовать? ✏️"
    )
    return 'ENTER_OLD_NAME'


def enter_old_name(update, context):
    """After entering the old quiz name, it asks for the new one."""

    quiz_creator = update.message.from_user.username
    old_quiz_name = update.message.text

    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    user_col = db[quiz_creator]

    # Checks if a quiz with this name exists
    if user_col.find_one({'quizname': old_quiz_name}) is None:

        logger.info("[%s] Entered old quiz '%s' doesn\'t exist",
                    update.message.from_user.username, old_quiz_name)
        update.message.reply_text(
            "Викторина '{}' не найдена 😕\nВведите другое название или отмените изменения, введя /cancelEdit 🙆‍♂️".format(
                old_quiz_name)
        )
        return 'ENTER_OLD_NAME'

    logger.info("[%s] Entered old quiz name '%s'",
                update.message.from_user.username, old_quiz_name)
    # Saves the new quiz name
    user_dict[quiz_creator] = old_quiz_name
    update.message.reply_text(
        "Как назовём? 🤔"
    )
    return 'ENTER_NEW_NAME'


def enter_new_name(update, context):
    """After entering the new name of the quiz, it renames it."""

    quiz_creator = update.message.from_user.username
    new_quiz_name = update.message.text

    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    user_col = db[quiz_creator]

    # Check if a quiz with the name already exists
    if not user_col.find_one({'quizname': new_quiz_name}) is None:

        logger.info("[%s] Entered new quiz '%s' already exists",
                    update.message.from_user.username, new_quiz_name)
        update.message.reply_text(
            "Викторина '{}' уже есть 😕\nВведите другое название или отмените изменения, введя /cancelEdit 🙆‍♂️".format(
                new_quiz_name)
        )
        return 'ENTER_NEW_NAME'

    # Get old quizname and update database
    old_quiz_name = user_dict[quiz_creator]
    user_col.update_one({'quizname': old_quiz_name}, {
                        "$set": {"quizname": new_quiz_name}})
    update.message.reply_text(
        "Переименовали '{}' в '{}' 🥳".format(old_quiz_name, new_quiz_name)
    )
    logger.info("[%s] Updated quiz '%s' to '%s'",
                update.message.from_user.username, new_quiz_name, old_quiz_name)

    # delete user data
    user_dict.pop(quiz_creator)
    return ConversationHandler.END


def cancel_edit(update, _):
    """Cancels the process of deletion or renaming."""
    client = pymongo.MongoClient(os.environ.get('MONGODB'))
    db = client.quizzes
    update.message.reply_text(
        "Изменения отменены."
    )
    logger.info("[%s] Canceled editing process by user",
                update.message.from_user.username)

    # delete user data
    user_dict.pop(update.message.from_user.username, None)
    return ConversationHandler.END
