from services.chatbot import chat
from services.common.gi import name, __copyright__, __version__, __author__
from services.common.wcrawler import print_info

verbose = 0


def decor_line():
    print("_____________________________________________________________________________")


def decor_header():
    decor_line()
    print(__copyright__)
    print(f"Author: {__author__}")
    print(f"Version: {__version__}")
    decor_line()


def app_main():
    decor_header()
    while True:
        text_message = input("You: ").strip()

        if text_message is None or "" == text_message:
            print("Please say something!")
            continue

        response = chat(text_message=text_message,
                        verbose=verbose)

        if verbose > 0:
            print(f"context: {response['context']}={response['probability']}")

        print(f"{name}: {response['response']}")

        match response['context']:
            case "weather":
                print_info()
            case "quit":
                decor_line()
                if input("Do you want to quit ([Y]/n)? ").lower().strip() in ("y", ""):
                    break
                else:
                    continue
            case _:
                # Wildcard case
                pass
        decor_line()


if __name__ == "__main__":
    app_main()
    print("---END---")
