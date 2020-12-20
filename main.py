'''
Created on Nov 27, 2020

@author: Anik
'''

from datetime import datetime
import time

import mcrcon


def startCon(rcon):

    try:

        rcon.connect()
        return rcon

    except Exception as e:

        return e


def endCon(rcon):

    try:

        rcon.disconnect()

    except Exception as e:

        return e


def clockSync():

    # Get current time
    now = datetime.now()

    # Return sleep duration
    return ((59 - now.minute) * 60) + (60 - now.second)


def mainLoop(rcon):

    # Initialize looping flag as running
    loopRunning = True

    # Loop execution
    while loopRunning:

        # Sync sleep duration
        sleepDur = clockSync()

        # Sleep
        print("Going to sleep for {} minutes and {} seconds..\n".format(sleepDur // 60, sleepDur % 60))
        delay(sleepDur)
        print("Waking up..\n")

        # Initialize command flag as not sent
        commandSent = False

        while not commandSent:

            # Attempt to establish connection with server
            con = startCon(rcon)

            # Check if the server is online
            if not isinstance(con, Exception):

                # Send notification
                resp = con.command("TribeChatMsg 3 1244167861 Hourly complimentary wishbone distributed. Happy Thanksgiving! - ANIK")

                # Print response
                print(resp)

                # Terminate connection with server
                endCon(con)

            else:

                # Print server unavailability details
                print(con)

            # Force delay
            delay(1)

            # Clear buffer and attempt to reconnect with server
            con = startCon(rcon)

            # Check if the server is online
            if not isinstance(con, Exception):

                # Distribute item
                resp = con.command("GiveItemToAll blueprint'/game/primalearth/coreblueprints/resources/primalitemresource_wishbone.primalitemresource_wishbone' 1 0 0")

                # Print response
                print(resp)

                # Terminate connection with server
                endCon(con)

                # Change command flag to sent
                commandSent = True

            else:

                # Print server unavailability details
                print(con)

            # Force delay before next command send attempt
            delay(1)

        # Force delay before next loop execution
        delay(1)


def delay(t):

    # time.sleep(0.1)
    time.sleep(t)


def main():

    # Initialize server parameters
    ip = "192.168.0.196"
    pw = "quagganland"
    port = 32330

    # Initialize RCON object using server parameters
    rcon = mcrcon.MCRcon(ip, pw, port)

    # Execute looping script
    mainLoop(rcon)


if __name__ == '__main__':

    main()
    pass
