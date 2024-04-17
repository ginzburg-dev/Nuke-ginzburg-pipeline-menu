####################################################################
#
# Copyright (c) 2023, Dmitri Ginzburg.  All Rights Reserved.
#
####################################################################

import nuke
import os.path
import re
import glob

def getFramerange(seqPath,SEF):
    frames = []
    filepath_glob = seqPath.split('.%04d.')[0] + '.*.exr'
    glob_search_results = glob.glob(filepath_glob)
    if len(glob_search_results) == 0:
       print(filepath_glob + ': is empty')
       SEF[2] = 0;
       SEF[0] = 1;
       SEF[1] = 1;
    else:
       oldFNumber = 0;
       SEF[2] = 1;
       SEF[0] = int(glob_search_results[0].split('.')[len(glob_search_results[0].split('.'))-2])
       SEF[1] = int(glob_search_results[len(glob_search_results)-1].split('.')[len(glob_search_results[len(glob_search_results)-1].split('.'))-2])
       for i in glob_search_results:
           fnumber = int(i.split('.')[len(i.split('.'))-2]);
           if fnumber == 1:
              oldFNumber = 1;
           else:
              if fnumber - 1 != oldFNumber:
                 n = 1;
                 for k in range((fnumber - oldFNumber)-1):
                     print(i.replace(i.split('.')[len(i.split('.'))-2]+'.exr'
                     ,'{:04d}'.format(oldFNumber+n)+'.exr') + ': is missing')
                     n+=1;  
              oldFNumber = fnumber;

def mg_setup_scene():
	# set global vars
	globalRange = [100000000,1]
	nkSceneName = nuke.root().name();
	projPath = nkSceneName.split('/MG/episodes')[0];
	episode = nkSceneName.split('MG/episodes/')[1].split('/')[0];
	scNumber = nkSceneName.split('MG/episodes/')[1].split('compose/')[1].split('.nk')[0].split('_')[1];
	print(nkSceneName)
	print(episode)
	print(scNumber)
	for  read in nuke.allNodes('Read'):
		path = read.knob('file').value();
		if len(path.split('OUT/RENDER/')) > 1:
			separatePath = path.split('OUT/RENDER/');
			oldEpisode = separatePath[1].split('/')[0];
			oldScName = separatePath[1].split('/')[1];
			newPath = path.replace(oldScName,episode+'_'+scNumber).replace(oldEpisode, episode);
			newPath = projPath + '/OUT/RENDER' + newPath.split('OUT/RENDER')[1];
			read.knob('file').setValue(newPath);
			FRS = [1,1,1]
			getFramerange(newPath, FRS);
			read['origfirst'].setValue(FRS[0]);
			read['origlast'].setValue(FRS[1]);
			read['first'].setValue(FRS[0]);
			read['last'].setValue(FRS[1]);
			read['on_error'].setValue("nearest frame");
			if FRS[0] < globalRange[0]:
				globalRange[0] = FRS[0];
			if FRS[1] > globalRange[1]:
				globalRange[1] = FRS[1];
		else:
			if len(path.split('MG/assets')) > 1:
				separatePath = path.split('MG/assets/');
				newPath = projPath + '/MG/assets' + path.split('MG/assets')[1];
				read.knob('file').setValue(newPath);
				FRS = [1,1,1]
				getFramerange(newPath, FRS);
				read['origfirst'].setValue(FRS[0]);
				read['origlast'].setValue(FRS[1]);
				read['first'].setValue(FRS[0]);
				read['last'].setValue(FRS[1]);
				read['on_error'].setValue("nearest frame");
				if FRS[0] < globalRange[0]:
					globalRange[0] = FRS[0];
				if FRS[1] > globalRange[1]:
					globalRange[1] = FRS[1];

	for  read in nuke.allNodes('Write'):
		path = read.knob('file').value();
		if len(path.split('OUT/COMPOSE/')) > 1:
			separatePath = path.split('OUT/COMPOSE/');
			oldEpisode = separatePath[1].split('/')[0];
			oldScName = separatePath[1].split('/')[1];
			newPath = path.replace(oldScName,episode+'_'+scNumber).replace(oldEpisode, episode);
			newPath = projPath + '/OUT/COMPOSE' + newPath.split('OUT/COMPOSE')[1];
			read.knob('file').setValue(newPath);
	
	isExistAf = 0
	for i in nuke.allNodes():
		if i.name().startswith('afanasy'):
			isExistAf = 1

	wln = len(nuke.allNodes('Write'))
	print("Is there any Write node: "+str(wln))

	if (isExistAf == 0) and (wln != 0):
		af = nuke.createNode("afanasy")
		xp = nuke.allNodes('Write')[0]['xpos'].value()
		yp = nuke.allNodes('Write')[0]['ypos'].value()+200
		af.setXpos(int(xp))
		af.setYpos(int(yp))
		af.setInput(0, nuke.allNodes('Write')[0])
		af['framespertask'].setValue("5");

	for i in nuke.allNodes():
		if i.name().startswith('afanasy'):
			i['framefirst'].setValue(globalRange[0]);
			i['framelast'].setValue(globalRange[1]);

	nuke.knob("root.first_frame",str(globalRange[0]))
	nuke.knob("root.last_frame",str(globalRange[1]))
	nuke.knob("root.lock_range", "1")
	nuke.knob("root.fps", "25")
