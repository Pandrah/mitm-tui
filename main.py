from src import app
import argparse

if __name__ =="__main__":
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

    parser.add_argument('-n', '--no-tui',action='store_true')  # on/off flag

    args = parser.parse_args()
    # print(args.no_tui)

    if not args.no_tui:
        app.main()
