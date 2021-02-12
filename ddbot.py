# https://www.devdungeon.com/content/make-discord-bot-python
# https://www.devdungeon.com/content/make-discord-bot-python-part-2
# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import os
import time
import typing
import asyncio
from functools import partial

import discord

from . import models

TOKEN = os.environ.get('DDBOT_DISCORD_TOKEN')
QUORUM = 2

client = discord.Client()

# will work horirbly for tons of servers FIXME many collisions
# won't work for async
vote_db = {}
passed_votes = []
failed_votes = []


# NOTE: vote key will be the id of proposal
def create_proposal(server_name: str, channel_name: str, text: str, choice_strings: list) -> int:
    proposal = models.Proposal(
        server_name=server_name,
        channel_name=channel_name,
        text=text,
        choices=[models.Choice(text=t) for t in choice_strings],
    )
    db.session.add(proposal)
    db.session.commit()

    return proposal.id


def cast_vote():
    vote = models.Vote(choice_id=lol, username_hash=lol)


async def announce_vote_results(channel: discord.Channel, vote_key: str):
    await asyncio.sleep(15)
    # was quorum met?
    if sum(vote_db[vote_key]) < QUORUM:
        await client.send_message(channel, vote_key + ' did not reach quorum! totals: %s' % vote_db[vote_key])
        return

    # calculate the winner. fails if tie...
    winner_indexes = []
    current_index = 0
    for i, votes in enumerate(vote_db[vote_key]):
        if i == 0:
            winner_indexes.append(i)
            continue

        latest_winning_index = winner_indexes[current_index]
        latest_winning_value = vote_db[vote_key][latest_winning_index]

        if votes > latest_winning_value:
            winner_indexes[current_index] = i
        elif votes == latest_winning_value:
            winner_indexes.append(i)
            current_index += 1

    if len(winner_indexes) > 1:
        await client.send_message(channel, vote_key + ' ties between options: %s' % winner_indexes)
        return

    winner_option_index = winner_indexes[0]
    passed_votes.append(vote_key)
    message = "Vote %s passes in favor of option #%d!\n\nTotals: %s" % (vote_key, winner_option_index, vote_db[vote_key])
    await client.send_message(channel, message)
    return


def find_by_name(objects_with_name_attribs: list, find_name: str):
    for thing in objects_with_name_attribs:
        if thing.name == find_name:
            return thing
    else:
        return None


def message_to_arguments(message: str) -> list:
    raw_arguments = message.split(';')[1:]  # trim off command
    arguments = {}
    arguments['server'] = find_by_name(client.servers, raw_arguments[0])
    arguments['channel'] = find_by_name(arguments['server'].channels, raw_arguments[1])
    arguments['arguments'] = raw_arguments[2:]
    return arguments


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!passed'):
        await client.send_message(message.channel, str(passed_votes))
    elif message.content.startswith('!status'):
        arguments = message.content.split(';')[1:]
        vote_key = arguments[0]
        await client.send_message(message.channel, str(vote_db[vote_key]))
    elif message.content.startswith('!vote'):
        arguments = message.content.split(';')[1:]
        vote_key = arguments[0]
        vote_option = int(arguments[1])
        vote_db[vote_key][vote_option] += 1
    elif message.content.startswith('!propose'):
        arguments = message_to_arguments(message.content)
        vote_text = arguments['arguments'][0]
        vote_options = arguments['arguments'][1:]

        if not arguments['channel']:
            return

        # FIXME: this should be from repr of proposal?
        option_text = ', '.join(['%d: %s' % (i,a) for i,a in enumerate(vote_options)])

        new_proposal_id = create_proposal(
            server_name=arguments['server'].name,
            channel_name=arguments['channel'].name,
            text=vote_text,
            choice_strings=vote_options,
        )

        #msg = 'Hello {0.author.mention}'.format(message)
        msg = (
            'VOTING TIME!\n\nProposal: %s (vote key: %d)\n\nOptions: %s'
            % (vote_text, new_proposal_id, option_text)
        )


        await client.send_message(arguments['channel'], msg)
        announce_this_votes_results = partial(announce_vote_results, arguments['channel'], vote_key)
        await announce_this_votes_results()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
