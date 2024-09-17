import discord
import asyncio
import os
import json
import aiohttp
import random

# Photofinish created by Penguin and Steve
# Mark 2 less cluster fucked!

# current ver 1.5
# Properly fixed issue with wget blocking function replaced with aiohttp
# taken out meme images for now as they started getting annoying
# fixed issue with infinate looping while demand gathering
# fixed the stupid fucking counter!!!
# fixed iphone upload issue
# fixes requesting negative messages
# fixed saying no to large scarpe
# added if to stop program salting every file name but just iphones


# to do:

# Add current count to auto gather (Dunno whether this is relevant now?)
# Seperate different modes into own functions
# Add option to save images to specified location (local if possible)
# Add date to date gathering
# Add per user gathering
# fix counter issue again
# complete access control
# create toggle for meme images on/off
# kill self



# creating discord object
loop = asyncio.get_event_loop()
photoFinish = discord.Client()

# dict to see whether channel is active or not
ChannelStatus = {}

# blacklisted file names
Blacklist = ["pfcapture.gif",
             "pfcapture2.gif",
             "pfdisapprove.gif",
             "pffallover.gif",
             "pfigo.gif",
             "pfmakemagics.gif",
             "pfrecovery.gif",
             "pfcapture2cut.gif"]

# current directory
cwd = os.getcwd()

# list of avalable commands
CommandHelp = ["All commands are case and space sensitive",
               "'~PFDemand NUMBER' - Looks through channel for images within a specified message count",
               "'~PFAuto Start' - Starts auto image gathering for current channel",
               "'~PFAuto Stop' - Stops auto image gathering for current channel"]


class ImgCount:
    def __init__(self, count):
        self.count = count


# wget gathering function
# Disabled counter file naming for now
async def capture(attachment):
    try:
        load = str(attachment[0]).replace("'", '"')
        data = json.loads(load)
        proxy = data["proxy_url"]
        filename = data["filename"]
        spostcount = 0

        # Filtering out shitposts by looking at file name
        if not str(filename).startswith(tuple(Blacklist)):
            # print(str(filename))
            targetfolder = "D:/OneDrive/Dev/Python/old scripts/Test/"
            if not os.path.exists(targetfolder):
                os.makedirs(targetfolder)

            with aiohttp.ClientSession() as session:
                async with session.get(proxy) as resp2:
                    test = await resp2.read()
                    salt = int(random.random() * 900000)
                    if "image0" in filename:
                        with open(targetfolder + str(salt) + filename, "wb") as f:
                            f.write(test)
                            print("Image %s captured" % filename)
                    else:
                        with open(targetfolder + filename, "wb") as f:
                            f.write(test)
                            print("Image %s captured" % filename)
            print("Capture complete")
        else:
            pass
            print(str(filename))
            print("Shitpost not captured")
            spostcount += 1
    except:
        print("An error occurred")
        raise

    return spostcount


@photoFinish.event
# Currently having everything run in one asyn func
async def on_message(message):
    counter = ImgCount
    counter.count = 0
    # Starts demand capturing goes back as far as user specifies (by message)
    if message.content.startswith("~PFDemand "):
        msglimit = message.content.strip("~PFDemand ")
        msglimit = int(msglimit)
        if msglimit >= 100:
            answer = False
            while not answer:
                await photoFinish.send_message(message.channel, "Oh mein Gott! This is a big image scrape ya? Are you sure you want to continue?")
                # await photoFinish.send_file(message.channel, cwd + "\Response_images\pffallover.gif")
                reply = await photoFinish.wait_for_message(author=message.author)
                if reply.content == "Yes":
                    print("Confirmed")

                    await photoFinish.send_message(message.channel,
                                                   "Ya I will look for images from %s messages ago!" % msglimit)
                    # await photoFinish.send_file(message.channel, cwd + "\Response_images\pfmakemagics.gif")
                    logs = photoFinish.logs_from(message.channel, limit=msglimit)
                    imgcount = 0
                    async for entry in logs:
                        attach = entry.attachments
                        if attach:
                            imgcount += 1
                            imgcount -= await capture(attach)
                    await photoFinish.send_message(message.channel, "Wunderbar %s images have been collected! I go!" % imgcount)
                    # await photoFinish.send_file(message.channel, cwd + "\Response_images\pfigo.gif")

                    answer = True
                elif reply.content == "No":
                    await photoFinish.send_message(message.channel, "OK it's not like I Photofinish could not handle all those images or anything!")
                    # await photoFinish.send_file(message.channel, cwd + "\Response_images\pfrecovery.gif")
                    break
                else:
                    await photoFinish.send_message(message.channel, "That's not the response I was looking for please answer 'Yes' or 'No'" )
        elif msglimit <= 0:
            await photoFinish.send_message(message.channel, "Alright smart arse fuck off and put in a proper number!")

    # Shows available commands as discord message
    elif message.content.startswith("~PFHelp"):
        for x in CommandHelp:
            await photoFinish.send_message(message.channel, x)

    # need to work out how have multiple async funcs play nice together when sharing objects
    else:
        channel = str(message.channel)

        # Starts image gathering for current channel displays message if already started
        if message.content == "~PFAuto Start":
            if ChannelStatus.get(channel):
                await photoFinish.send_message(message.channel, "You fool! Auto gathering is already turned on for {}".format(channel))
                # await photoFinish.send_file(message.channel, cwd + "\Response_images\pfdisapprove.gif")
            else:
                await photoFinish.send_message(message.channel, "Say no more! I Photofinish will start gathering for {}".format(channel))
                ChannelStatus[channel] = True
                # await photoFinish.send_file(message.channel, cwd + "\Response_images\pfcapture2cut.gif")

        # Stops image gathering for current channel displays message if already stopped
        elif message.content == "~PFAuto Stop":
            if not ChannelStatus.get(channel):
                await photoFinish.send_message(message.channel, "You fool! Auto gathering needs to be started before it can be stoped!")
                # await photoFinish.send_file(message.channel, cwd + "\Response_images\pfdisapprove.gif")
            else:
                await photoFinish.send_message(message.channel, "Say no more! I Photofinish will stop gathering for {}".format(channel))
                ChannelStatus[channel] = False

        # else is to check images and call capture if an image is attached
        else:
            if ChannelStatus.get(channel):
                attachment = message.attachments
                if attachment:
                    await asyncio.sleep(1)
                    await capture(attachment)


photoFinish.run('lmao')