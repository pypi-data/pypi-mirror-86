import os
from sys import exit
from .generator import UfwConfigGenerator


def main():
    os.system("clear")
    print(
        "\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015"
    )
    print("Thank you for using the UFW configure tool")
    print("Made by NeonDevelopment")
    print("\u00A9 WeLikeToCodeStuff 2020 - Current year")
    print(
        "\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015\u2015"
    )

    generator = UfwConfigGenerator()

    acceptdeny = input(
        "Would you like to accept or deny a port? \n(You can also type portrange to specify a portrange to accept/deny): "
    )
    if acceptdeny == "accept":
        acceptport = input("What port would you like to accept?: ")
        generator.generate(acceptport, True)
        print(f"Port '{acceptport}' has been set to allowed")
        exit()

    elif acceptdeny == "deny":
        denyport = input("What port would you like to deny?: ")
        generator.generate(denyport, True)
        print(f"Port '{denyport}' has been set to denied")
        exit()
    elif acceptdeny == "portrange":
        rangenum = input("Please type a port range to accept/deny. \nUse the format: startport:stopport Example: 100:200 :")
        rangestatus = input("Would you like to accept or deny this port range?: ")
        rangetype = input("What type of these ports? tcp/udp :")
        rangetypelower = rangetype.lower()
        if rangestatus == "accept":
            os.system("sudo ufw " + rangestatus + " " + rangenum + " /" + rangetype)
            print(f"Port range '{rangenum}' has been set to accepted")
        elif rangestatus == "deny":
            os.system("sudo ufw " + rangestatus + " " + rangenum + " /" + rangetype)
            print(f"Port range '{rangenum}' has been set to denied")
    else:
        print("That's not a valid option. Please choose 'accept', 'deny', or 'portrange'")
        exit()
