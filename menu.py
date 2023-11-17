import os

# Add CGRU to main window menu:
ginzburg_menu = nuke.menu('Nuke').addMenu('GINZBURG')

ginzburg_menu.addCommand('MG Setup Scene', 'ginzburg.mg_setup_scene()')
ginzburg_menu.addCommand('Submit to Afanasy', 'ginzburg.submit_to_afanasy()')

#ginzburg_submenu = ginzburg_menu.addMenu("Paths")
