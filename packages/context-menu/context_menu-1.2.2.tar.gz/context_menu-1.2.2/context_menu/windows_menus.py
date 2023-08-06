# all imports ---------------
import os
import ctypes
import sys
from enum import Enum


# registry_shortcuts.py ----------------------------------------------------------------------------------------

try:
    import winreg

    # ------------------------------------------------------------------

    def is_admin():
        '''
        Returns True if the current python instance has admin, and false otherwise.
        '''
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_admin(params=sys.argv[0], force=False):
        '''
        If the python instance does not have admin priviledges, it stops the current execution and runs the program as admin.

        You can customize where it runs/Force it to run regardless.
        '''
        if not is_admin() or force:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1)
            sys.exit()

    # ------------------------------------------------------------------

    def create_key(path: str, hive=winreg.HKEY_CURRENT_USER):
        '''
        Creates a key at the desired path.
        '''
        winreg.CreateKey(hive, path)

    def set_key_value(key_path: str, subkey_name: str, value: 'Value', hive=winreg.HKEY_CURRENT_USER):
        '''
        Changes the value of a subkey. Creates the subkey if it doesn't exist.
        '''

        registry_key = winreg.OpenKey(hive, key_path, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, subkey_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)

    def list_keys(path: str, hive=winreg.HKEY_CURRENT_USER) -> 'List of keys':
        '''
        Returns a list of all the keys at a given registry path.
        '''

        open_key = winreg.OpenKey(hive, path)
        key_amt = winreg.QueryInfoKey(open_key)[0]
        keys = []

        for count in range(key_amt):
            subkey = winreg.EnumKey(open_key, count)
            keys.append(subkey)

        return keys

    def delete_key(path: str, hive=winreg.HKEY_CURRENT_USER):
        '''
        Deletes the desired key and all other subkeys at the given path.
        '''
        open_key = winreg.OpenKey(hive, path)
        subkeys = list_keys(path)

        if len(subkeys) > 0:
            for key in subkeys:
                delete_key(path + '\\' + key)
        winreg.DeleteKey(open_key, "")
except:
    print('Not linux')


# advanced_reg_config.py ----------------------------------------------------------------------------------------


# These are the paths in the registry that correlate to when the context menu is fired.
# For example, FILES is when a file is right clicked
CONTEXT_SHORTCUTS = {
    'FILELOC' : 'Software\\Classes\\',
    'FILES': 'Software\\Classes\\*\\shell',
    'DIRECTORY': 'Software\\Classes\\Directory\\shell',
    'DIRECTORY_BACKGROUND': 'Software\\Classes\\Directory\\Background\\shell',
    'DRIVE': 'Software\\Classes\\Drive\\shell'
}

# Not used yet, but could be useful in the future
COMMAND_PRESETS = {
    'python': sys.executable,
    'pythonw': os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
}

COMMAND_VARS = {
    'FILENAME' : "' '.join(sys.argv[1:]) ",
    'DIR': 'os.getcwd()',
    'DIRECTORY': 'os.getcwd()',
    'PYTHONLOC' : 'sys.executable'
}

def context_registry_format(item: str) -> 'registry path to the desired type':
    '''
    Converts a verbose type into a registry path.

    For example, 'FILES' -> 'Software\\Classes\\*\\shell'
    '''
    item = item.upper()
    if '.' in item:
        return os.path.join(CONTEXT_SHORTCUTS['FILELOC'], item.lower(), 'shell')
    return CONTEXT_SHORTCUTS[item]


def command_preset_format(item: str) -> 'Path to desired python type':
    '''
    Converts a python string to an executable location.

    For example, 'python' -> sys.executable
    '''
    return COMMAND_PRESETS[item.lower()]

def command_var_format(item: str):
    '''
    Converts a python string to a value for a command

    '''
    return COMMAND_VARS[item.upper()]

def create_file_select_command(func_name: str, func_file_name: str, func_dir_path: str, params: str) -> 'Registry valid string to call python function':
    '''
    Creates a registry valid command to link a context menu entry to a funtion, specifically for file selection(FILES, DIRECTORY, DRIVE).

    Requires the name of the function, the name of the file, and the path to the directory of the file.
    '''
    python_loc = sys.executable
    sys_section = f'''import sys; sys.path.insert(0, '{func_dir_path}')'''.replace('\\', '/')
    file_section = f'import {func_file_name}'
    dir_path = """' '.join(sys.argv[1:]) """
    func_section = f'''{func_file_name}.{func_name}([{dir_path}],'{params}')'''
    python_portion = f'''"{python_loc}" -c "{sys_section}; {file_section}; {func_section}"'''
    full_command = f'''{python_portion} \"%1\"'''

    return full_command


def create_directory_background_command(func_name: str, func_file_name: str, func_dir_path: str, params: str) -> 'Registry valid string to call python function':
    '''
    Creates a registry valid command to link a context menu entry to a funtion, specifically for backgrounds(DIRECTORY_BACKGROUND, DESKTOP_BACKGROUND).

    Requires the name of the function, the name of the file, and the path to the directory of the file.
    '''
    python_loc = sys.executable
    sys_section = f'''import sys; import os; sys.path.insert(0, '{func_dir_path}')'''.replace('\\', '/')
    file_section = f'import {func_file_name}'
    dir_path = 'os.getcwd()'
    func_section = f'''{func_file_name}.{func_name}([{dir_path}],'{params}')'''
    full_command = f'''"{python_loc}" -c "{sys_section}; {file_section}; {func_section}"'''

    return full_command


def create_shell_command(command: str, command_vars: list) -> 'Shell command':
    '''
    Creates a shell command and replaces '?' with the command_vars list
    '''

    transformed_vars = ["' + " + command_var_format(item) + " + '" for item in command_vars]
    new_command = command.replace("?", '{}').format(*transformed_vars)
    python_section = '''import os; import sys; os.system('{}')'''.format(new_command)
    full_command = '"{}" -c "{}" \"%1\""'.format(sys.executable, python_section)
    return full_command



# windows_menus.py ----------------------------------------------------------------------------------------


# Used to create a Registry entry
class RegistryMenu:
    '''
    Class to convert the general menu from menus.py to a Windows-specific menu.
    '''

    def __init__(self, name: str, sub_items: list, type: str):
        '''
        Handled automatically by menus.py, but requires a name, all the sub items, and a type
        '''
        self.name = name
        self.sub_items = sub_items
        self.type = type.upper()
        self.path = context_registry_format(type)

    def create_menu(self, name: str, path: str) -> 'Path to shell key of new menu':
        '''
        Creates a menu with the given name and path.

        Used in the compile method.
        '''
        key_path = os.path.join(path, name)
        create_key(key_path)

        set_key_value(key_path, 'MUIVerb', name)
        set_key_value(key_path, 'subcommands', '')

        key_shell_path = os.path.join(key_path, 'shell')
        create_key(key_shell_path)

        return key_shell_path

    def create_command(self, name: str, path: str, command: str):
        '''
        Creates a key with a command subkey with the 'name' and 'command', at path 'path'.
        '''
        key_path = os.path.join(path, name)
        create_key(key_path)
        set_key_value(key_path, '', name)

        command_path = os.path.join(key_path, 'command')
        create_key(command_path)
        set_key_value(command_path, '', command)

    def compile(self, items: list = None, path: str = None):
        '''
        Used to create the menu. Recursively iterates through each element in the top level menu.
        '''
        if items == None:
            # run_admin()
            items = self.sub_items
            path = self.create_menu(self.name, self.path)

        for item in items:
            if item.isMenu:
                # if the item is a menu
                submenu_path = self.create_menu(item.name, path)
                self.compile(items=item.sub_items, path=submenu_path)
            else:
                # Otherwise the item is  a command
                if item.command == None:
                    # If a Python function is defined
                    func_name, func_file_name, func_dir_path = item.get_method_info()
                    new_command = None
                    if self.type in ['DIRECTORY_BACKGROUND', 'DESKTOP_BACKGROUND']:
                        # If it requires a background command
                        new_command = create_directory_background_command(
                            func_name, func_file_name, func_dir_path, item.params)
                    else:
                        # If it requires a file command
                        new_command = create_file_select_command(
                            func_name, func_file_name, func_dir_path, item.params)
                    self.create_command(item.name, path, new_command)
                elif item.command_vars != None:
                    # If the item has to be ran from os.system

                    new_command = create_shell_command(item.command, item.command_vars)
                    self.create_command(item.name, path, new_command)
                else:
                    # The item is just a plain old command
                    self.create_command(item.name, path, item.command)


# Fast command class
# Everything is identical to either the RegistryMenu class or code in the menus file
class FastRegistryCommand:
    '''
    Fast command class.

    Everything is identical to either the RegistryMenu class or code in the menus file
    '''

    def __init__(self, name: str, type: str, command: str, python: 'function', params: str, command_vars: list):
        self.name = name
        self.type = type
        self.path = context_registry_format(type)
        self.command = command
        self.python = python
        self.params=params
        self.command_vars = command_vars

    def get_method_info(self):
        import inspect

        func_file_path = os.path.abspath(inspect.getfile(self.python))

        func_dir_path = os.path.dirname(func_file_path)
        func_name = self.python.__name__
        func_file_name = os.path.splitext(os.path.basename(func_file_path))[0]

        return (func_name, func_file_name, func_dir_path)

    def compile(self):
        # run_admin()

        key_path = os.path.join(self.path, self.name)
        create_key(key_path)

        command_path = os.path.join(key_path, 'command')
        create_key(command_path)

        new_command = self.command

        if self.command == None:
            # If a python function is defined
            func_name, func_file_name, func_dir_path = self.get_method_info()
            if self.type in ['DIRECTORY_BACKGROUND', 'DESKTOP_BACKGROUND']:
                # If it requires a background selection
                new_command = create_directory_background_command(
                    func_name, func_file_name, func_dir_path, self.params)
            else:
                # If it requires a file selection
                new_command = create_file_select_command(
                    func_name, func_file_name, func_dir_path, self.params)
        elif self.command_vars != None:
            # If it has command_vars
            new_command = create_shell_command(self.command, self.command_vars)

        set_key_value(command_path, '', new_command)


# Testing section...

try:
    def remove_windows_menu(name: str, type: str):
        '''
        Removes a context menu from the windows registry.
        '''
        # run_admin()
        menu_path = os.path.join(context_registry_format(type), name)
        delete_key(menu_path)
except:
    pass
    # for testing
