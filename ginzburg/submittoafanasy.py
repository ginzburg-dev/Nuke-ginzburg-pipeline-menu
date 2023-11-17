import nuke
import os.path
import re
import sys
import glob

sys.path.insert(1,'c:\cgru\plugins/nuke/scripts')

import cgru

def submit_to_afanasy():
	nuke.scriptSave()
	for i in nuke.allNodes():
		if i.name().startswith('afanasy'):
			i.setSelected(True);
	cgru.render()