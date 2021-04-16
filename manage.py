import utils

if __name__ == "__main__":
    if utils.build_requested():
        utils.main()
    elif utils.new_requested():
        utils.new_file()
    else:
        utils.print_command_line_help()
     