import os 
import datetime

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def epoch_to_datetime(epoch_time):
	'''
	this function converts epoch into datetime
	'''
	date_conv = datetime.datetime.fromtimestamp(epoch_time)
	return date_conv

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size

def file_name(file_path):
	'''
	this function will return the file name
	'''
	if os.path.isfile(file_path):
		file_name = os.path.basename(file_path)
	return file_name

def file_creation(file_path):
	'''
	this function will return the file creation date
	'''
	if os.path.isfile(file_path):
		file_creation = os.path.getctime(file_path)
		file_creation_time = epoch_to_datetime(file_creation)
		
	return file_creation_time

def file_last_modified(file_path):
	'''
	this function will return the file modified datetime
	'''
	if os.path.isfile(file_path):
		file_modif = os.path.getmtime(file_path)
		file_modif_time = epoch_to_datetime(file_modif)
		
	return file_modif_time

def file_summary(file_path):
	name = file_name(file_path)
	size = file_size(file_path)
	creation = file_creation(file_path)
	modification = file_last_modified(file_path)
	return name, size, creation, modification