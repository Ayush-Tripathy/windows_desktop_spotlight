import os.path
import win32com.client
import sys
import constants
import pywintypes


def create_task(argv, script_path, task_name, trigger_delay_minutes=0) -> None:
    try:
        with open(constants.STARTUP_FILE, "r") as startup_file:
            choice = startup_file.readline()
            if choice in constants.CHOICES:
                script_args = "-" + choice

        # Create an instance of the Task Scheduler object
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()

        # Get the root folder for tasks
        root_folder = scheduler.GetFolder("\\")
        task_definition = scheduler.NewTask(0)

        # Create the action to run the Python script
        action = task_definition.Actions.Create(0)
        action.ID = constants.ACTION_ID

        if argv[0].split("/")[-1] == "desktop_spotlight.py":
            action.Path = f'"{sys.executable}"'
            action.Arguments = (
                f'"{script_path}" "{script_args}" "{constants.flags.NOSAVE_FLAG}"'
            )
        else:
            script_path = os.path.join(
                constants.SCRIPT_DIRECTORY, "desktop_spotlight.exe"
            )
            action.Path = f'"{script_path}"'
            action.Arguments = f'"{script_args}" "{constants.flags.NOSAVE_FLAG}"'

        # Create the logon trigger with delay
        trigger = task_definition.Triggers.Create(
            constants.LOGON_TRIGGER
        )  # 8 for BootTrigger, 9 for LogonTrigger
        trigger.ID = constants.LOGON_TRIGGER_ID
        trigger.UserId = ""  # Run the task for all users
        trigger.Delay = f"PT{trigger_delay_minutes}M"

        task_definition.RegistrationInfo.Description = constants.TASK_DESCRIPTION
        task_definition.Settings.Enabled = True
        task_definition.Settings.DisallowStartIfOnBatteries = False
        task_definition.Settings.StopIfGoingOnBatteries = False

        # Register the task in the root folder
        create_or_update_task = 6
        root_folder.RegisterTaskDefinition(
            task_name, task_definition, create_or_update_task, "", "", 0
        )

    except Exception as e:
        print(f"Failed to create the task: {e}")


def delete_task(task_name) -> None:
    try:
        # Create an instance of the Task Scheduler object
        scheduler = win32com.client.Dispatch("Schedule.Service")
        scheduler.Connect()

        # Get the root folder for tasks
        root_folder = scheduler.GetFolder("\\")

        try:
            # Get the task to be deleted
            task = root_folder.GetTask(task_name)

            # Delete the task
            root_folder.DeleteTask(task.Name, 0)
        except pywintypes.com_error as e:
            if e.hresult == -2147024894:
                return None

    except Exception as e:
        print(f"Failed to delete the task: {e}")
