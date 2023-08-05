# -*- coding:utf-8 -*-
"""
@creation date: 2019-8-23
@last modify: 2020-11-19
"""
import os
from .polling import _runUpdates
from .webhook import _runWebhook
from .teelebot import Bot

name = "teelebot"
__all__ = ['Bot']

bot = Bot()
VERSION = bot.version

if bot._local_api_server != "False":
    api_server = "Local"
else:
    api_server = "Remote"


def main():
    print(" * Self-checking...", end="\r")
    status = bot.getWebhookInfo()
    pending_update_count = status["pending_update_count"]

    if not status:
        print("\nfailed to get running mode!")
        os._exit(0)

    if bot._webhook:
        url = "https://" + str(bot._server_address + ":" + str(
            bot._server_port) + "/bot" + str(bot._key))
        if (bot._drop_pending_updates == True and pending_update_count != 0) \
            or (status["url"] != url) or (status["has_custom_certificate"] != bot._self_signed)\
            or status["max_connections"] != int(bot._pool_size):
            if bot._self_signed:
                status = bot.setWebhook(
                    url=url,
                    certificate=bot._cert_pub,
                    max_connections=bot._pool_size,
                    drop_pending_updates=bot._drop_pending_updates
                )
            else:
                status = bot.setWebhook(
                    url=url,
                    max_connections=bot._pool_size,
                    drop_pending_updates=bot._drop_pending_updates
                )
            if not status:
                print("\nfailed to set Webhook!")
                os._exit(0)

        print(" * The teelebot starts running",
              "\n * Version : v" + VERSION,
              "\n *    Mode : Webhook",
              "\n *  Thread : " + str(bot._pool_size),
              "\n *  Server : " + api_server + "\n")
        _runWebhook(bot=bot,
            host=bot._local_address,port=int(bot._local_port))

    else:
        if status["url"] != "" or status["has_custom_certificate"]:
            status = bot.deleteWebhook()
            if not status:
                print("\nfailed to set getUpdates!")
                os._exit(0)

        print(" * The teelebot starts running",
              "\n * Version : v" + VERSION,
              "\n *    Mode : Polling",
              "\n *  Thread : " + str(bot._pool_size),
              "\n *  Server : " + api_server + "\n")
        if bot._drop_pending_updates == True and \
            pending_update_count != 0:
            results = bot.getUpdates()
            messages = bot._washUpdates(results)
        _runUpdates(bot=bot)
