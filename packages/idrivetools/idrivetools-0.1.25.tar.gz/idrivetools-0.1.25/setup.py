# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idrivetools', 'idrivetools.file_tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['bmwpack = idrivetools.process_files:pack_files',
                     'bmwunpack = idrivetools.process_files:unpack_files']}

setup_kwargs = {
    'name': 'idrivetools',
    'version': '0.1.25',
    'description': 'iDrive tools for packing and unpacking BMW backups',
    'long_description': 'iDriveTools\n===========\n\nTools for managing BMW iDrive music backups. There are two tools included in this package.\n\n*This tool requires Python 3.7+*\n\nInstallation\n------------\n\nThese utilities can be installed using pip. pip can be installed following the instruction here_\n\n.. _here: https://pip.pypa.io/en/stable/installing/\n\n::\n\n    pip install idrivetools\n\nEventually, this will have standalone executables for Windows and Mac. But for now, pip will also install\non the same operating systems.\n\nbmwunpack\n---------\n\nThis takes a BMW backup and converts everything to regular media files.\n\nTypical arguments contain the source and destination folders.\n\nUsage\n*****\n\n::\n\n    bmwunpack BMWData unpacked\n\nbmwpack\n-------\n\nThis is the opposite of bmwunpack in that it will take a hierarchy of folders and\ncreate a BMW backup that can be restored back into the iDrive system\n\nUsage\n*****\n\n::\n\n    bmwpack unpacked BMWData\n\nNotes\n-----\n\nA typical BMW backup has a single BMWData top folder, a Music sub-folder, USB drive name\nsub-folders below that and then the actual media files themselves.\n\nThere are several metadata files that are required by the backup. These files are\ncalculated by bmwpack and added automatically. Without these metadata files, the\nbackup will not be recognised by the iDrive system.\n\nAn example backup file structure.\n\n::\n\n    BMWData\n    + Music\n      + USB1\n        + Media folder 1\n          + file1.mp3\n          + file2.mp3\n          + file3.mp3\n          + ...\n        + Media folder 2\n          + file4.mp3\n          + file5.mp3\n          + ...\n      + USB2\n        + Media folder 1\n          + file1.mp3\n          + file2.mp3\n          + file3.mp3\n          + ...\n        + Media folder 2\n          + file4.mp3\n          + file5.mp3\n          + ...\n      + data_1\n      + data_1_count\n      + info\n    + BMWBackup.ver\n\nThere are several file types that are supported by this script. I suspect there are more\nfile types that are supported by the iDrive system. These are the ones I have come across\nso far and their "encrypted" extensions:\n\nMedia files\n\n* MP3 (BR4, BR28)\n* MP4 (BR3, BR27)\n* AAC (BR25)\n* FLAC (BR48)\n* WMA (BR5, BR29)\n* JPG (BR67)\n* BMWP (BR30) - A playlist file\n\nPlaylist Support\n----------------\n\nThe BMWP playlist file is a plain text file that contains a list of absolute paths\nlocated on the iDrive system itself. They start from the USB drive name going forwards\nwith a UNIX file format name (forward slashes). They typically look like this:\n\n::\n\n    /USB1/CAKE - Pressure Chief/01 - CAKE - Wheels.mp3\n    /USB1/CAKE - Pressure Chief/02 - CAKE - No Phone.mp3\n    /USB1/CAKE - Pressure Chief/03 - CAKE - Take It All Away.mp3\n    /USB1/CAKE - Pressure Chief/04 - CAKE - Dime.mp3\n    /USB1/CAKE - Pressure Chief/05 - CAKE - Carbon Monoxide.mp3\n    /USB1/CAKE - Pressure Chief/06 - CAKE - The Guitar Man.mp3\n    /USB1/CAKE - Pressure Chief/07 - CAKE - Waiting.mp3\n    /USB1/CAKE - Pressure Chief/08 - CAKE - Baskets.mp3\n    /USB1/CAKE - Pressure Chief/09 - CAKE - End of the Movie.mp3\n    /USB1/CAKE - Pressure Chief/10 - CAKE - Palm of Your Hand.mp3\n    /USB1/CAKE - Pressure Chief/11 - CAKE - Tougher Than It Is.mp3\n\nThese can be edited to keep the same absolute path. They are included in the _Playlists folder.\n\nHow Do I Give Feedback\n======================\n\nThis code lives at this repo_ and there is a section at the top for reporting issues and\ngiving feedback. I\'m pretty friendly and keen on making this better, so make suggestions.\n\n.. _repo: https://github.com/Centurix/idrivetools\n\nWhat\'s Planned\n==============\n\nThere is scope here to provide some more functionality:\n\n* Generate playlists from folders\n* Generate an empty backup structure ready for filling\n* Better command line feedback, like a progress bar\n* An in-place editing mode, where you can edit files without having to unpack\n* Expose core functionality as modules/packages so it can integrated into other projects\n* Maybe some kind of GUI later down the track.\n',
    'author': 'Chris Read',
    'author_email': 'centurix@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Centurix/idrivetools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
