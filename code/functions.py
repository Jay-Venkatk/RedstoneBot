import json

from format import format

from urls import (
    login_url,
    api_endpoint,
    location_url,
    queue_url,
    accept_url,
    start_url,
    stop_url,
)

# status cheat sheet
#
# 0 -> offline
# 1 -> stopped execution
# 2 -> online
# 3 -> starting up
# 4 -> running setup
# 5 -> closing
# 6 -> in queue
# 7 -> waiting for accept

async def get_status(session):
    # Requesting data to internal internal API
    r_status = session.get(api_endpoint)
    # check if we got some nonsense HTMl or a JSON
    if r_status.text[2] == '<':
        # very hacky solution, I know, I know :-\
        # the third char of the HTML template for the PloudOS.com sites is always a '<'
        # we'll use that to our advantage here

        print("Tried to access API, got nonsense HTML. *sigh*")
        print("Either RedstoneBot is broken or PloudOS is undergoing maintenance.")
        print("Please login to PloudOS.com and visit https://ploudos.com/server for details.")
        print("If you think this is RedstoneBot's fault, please visit github.com/ChromeUniverse/RedstoneBot and open an issue.")

        return 'Something went wrong'

    else:
        # decoding JSON response text
        data = json.loads(r_status.text)

        print("Got the JSON data! Here it is: \n")

        for key in data:
            print(key + ": " + str(data[key]))

        status, title, content = format(data)

        return status, title, content

async def activate(session):

    # getting status
    status, title, content = await get_status(session)

    # only run activation when the server is OFFLINE
    if status == 0:

        # performing GET request to queue_URl in order to enter the queue
        r_queue = session.get(queue_url + '1')
        print(r_queue.text)

        # decoding JSON response text
        data = json.loads(r_queue.text)
        print(data)

        if not data["error"]:
            print('No errors')
            message = 'Server activation sucessful! Check status with `!redstone status`.'
        else:
            message = 'Something went wrong! Please try again.'

    # else, just send the title as the message
    else:
        message = title

    return message

async def confirm(session):

    # getting status
    status, title, content = await get_status(session)

    # only run activation when the server is AWAITING ACCEPT
    if status == 7:

        # performing GET request to accept_url to start up
        r_accept = session.get(accept_url)
        print(r_accept.text)

        # decoding JSON response text
        data = json.loads(r_accept.text)
        print(data)

        if not data["error"]:
            print('No errors')
            message = 'Confirmation sucessful! Server is starting up. Check status with `!redstone status`.'
        else:
            message = 'Something went wrong! Please try again.'

    # else, just send the title as the message
    else:
        message = title

    return message


async def deactivate(session):

    # getting status
    status, title, content = await get_status(session)

    # only run activation when the server is ONLINE
    if status == 2:

        # performing GET request to accept_url to start up
        r_stop = session.get(stop_url)
        print(r_stop.text)

        # decoding JSON response text
        data = json.loads(r_stop.text)
        print(data)

        if not data["error"]:
            print('No errors')
            message = 'Server halted! Check status with `!redstone status`.'
        else:
            message = 'Something went wrong! Please try again.'

    # else, just send the title as the message
    else:
        message = title

    return message

async def reactivate(session):
    # getting status
    status, title, content = await get_status(session)

    # only run activation when the server is STOPPED
    if status == 1:

        # performing GET request to accept_url to start up
        r_start = session.get(start_url)
        print(r_start.text)

        # decoding JSON response text
        data = json.loads(r_start.text)
        print(data)

        if not data['error']:
            print('No errors')
            message = 'Reactivation sucessful! Server is starting up. Check status with `!redstone status`.'
        else:
            message = 'Something went wrong! Please try again.'

    # else, just send the title as the message
    else:
        message = title

    return message
