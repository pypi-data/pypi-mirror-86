# Python library import
import yaml, logging

# logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.WARNING)


class Inventory:
    """
    Class used to read inventory yaml file and select devices that will receive commands


    :param all_devices: A list of dictionaries with the parameters of the devices (ip address, device_type, etc.)
    :type all_devices: list

    :param yaml_host_file_dict: Raw yaml data read from yaml file
    :type yaml_host_file_dict: dict

    """

    def __init__(self, host_yaml="inventory/hosts.yaml"):

        self.all_devices = []
        self.yaml_host_file_dict = {}

        # File to open
        hosts_file = host_yaml

        # Display info message
        logging.info(f"Inventory: reading file '{hosts_file}'")

        try:
            # Open hosts.yaml file
            with open(hosts_file) as stream:

                # Get yaml data
                self.yaml_host_file_dict = yaml.safe_load(stream)

        except OSError:

            # Error while opening the file

            #  Display info message
            logging.info(f"Error while opening file {hosts_file}")

            # Propagate the exception
            raise

        # Display info message
        logging.info(
            f"Inventory: reading file '{hosts_file}' data:\n'{self.yaml_host_file_dict}'"
        )

        # Convert yaml file data (dict) into a list of devices
        self.all_devices = self.convert_yaml_to_list(self.yaml_host_file_dict)

        # Display info message
        logging.info(f"Inventory: all_devices:\n'{self.all_devices}'")

    def convert_yaml_to_list(self, input_data):
        """
        Build a list from yaml data (dictionary)

        :return: the list with the parameters of the devices
        :rtype: list
        """

        # By default no devices
        list_of_devices = []

        # Read all devices from yaml extracted data
        for device in input_data:

            # Convert data (dict + list) into a dictionary (dict)
            device_dict = {**input_data[device], **{"name": device}}

            # Display info message
            logging.info(f"convert_yaml_to_list: device dict: '{device_dict}'")

            # Add the dictionary of a device into a list
            list_of_devices.append(device_dict)

        # Return a list with the devices
        return list_of_devices

    def get_all_devices(self):
        """
        Get all devices in a list

        :return: the list of devices
        :rtype: list
        """

        # By default no devices
        list_of_devices = []

        # Some devices?
        if self.all_devices:

            # Yes

            # Get the devices
            list_of_devices = self.all_devices

        # Return a list with all the devices
        return list_of_devices

    def select(self, **kwargs):
        """
        Select devices from parameters

        :return: the list of devices
        :rtype: list
        """

        # By default no devices
        list_of_devices = []

        # Some devices?
        if self.all_devices:

            # Yes

            # Get the devices
            list_of_devices = self.all_devices

        # Get selections from method parameters

        # "device_type" found?
        if "device_type" in kwargs:

            # Get "device_type" parameter
            device_type = kwargs["device_type"]

            # Display info message
            logging.info(f"select: device_type: {device_type}")

            # By default no device found for this temporary list
            list_temp = []

            # Read all devices to check if the parameter is found
            for device in list_of_devices:

                # Parameter found?
                if device["device_type"] == device_type:

                    # Yes
                    list_temp.append(device)

            # Save the temporary list into the list of devices
            list_of_devices = list_temp

        # "name" found?
        if "name" in kwargs:

            # Get "name" parameter
            name = kwargs["name"]

            # Display info message
            logging.info(f"select: name: {name}")

            # By default no device found for this temporary list
            list_temp = []

            # Read all devices to check if the parameter is found
            for device in list_of_devices:

                # Parameter found?
                if device["name"] == name:

                    # Yes
                    list_temp.append(device)

            # Save the temporary list into the list of devices
            list_of_devices = list_temp

        # Return a list with all the devices
        return list_of_devices
