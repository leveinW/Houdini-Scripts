import hou
import voptoolutils

selected_nodes_list = hou.selectedNodes()   #creates list with all selected items



for index, item in enumerate(selected_nodes_list):
  # create sopimport node for each item  
  sopimport_newname = "IMPORT_" + selected_nodes_list[index].name()
  sopimport = hou.node("/stage").createNode("sopimport", sopimport_newname)      
  
       #get absolute path for each item
  node_path = item.path()                                    
  
       #change soppath parameter to node_path
  sopimport.parm("soppath").set(node_path)                   
 
       # extract only last part including "/"
  last_slash_index = node_path.rfind("/")
  usd_node_path = node_path[last_slash_index:]
      # set the primitive path
  sopimport.parm("pathprefix").set(usd_node_path)
          #adjust position
  sopimport.setPosition((index*4,0))
 
  #create a material libary node
  material_library = hou.node("/stage").createNode("materiallibrary") 
          #connect both nodes and adjust position
  material_library.setInput(0, sopimport)
          #adjust position
  material_library.setPosition((index*4,-1))
           # set the primitive path
  material_library.parm("geopath1").set(usd_node_path)
  material_library.parm("assign1").set(1)
    
  karmamaterial_name = "MTLX_" + str(selected_nodes_list[index].name())
  mask = voptoolutils.KARMAMTLX_TAB_MASK
  voptoolutils._setupMtlXBuilderSubnet(destination_node=material_library, name=karmamaterial_name, mask=mask, folder_label='Karma Material Builder')
  
  
 
 
  
  #create a rendergeometrysettings node
  rr_geosettings = hou.node("/stage").createNode("rendergeometrysettings") 
          #connect both nodes and adjust position
  rr_geosettings.setInput(0, material_library)
          #adjust position
  rr_geosettings.setPosition((index*4,-2))
           # set the primitive path
  rr_geosettings.parm("primpattern").set(usd_node_path)