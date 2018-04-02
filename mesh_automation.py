import bpy
import os
import math

import_dae = True
import_stl = True
recursive = False
mesh_folder = "/home/dniewinski/Desktop/meshes/"

def createScene(new_name):
    try:
        scene = bpy.data.scenes[new_name]
        bpy.context.screen.scene = scene
        print("Scene Already Exists <" + new_name + ">")
        return scene
    except:
        print("Creating new Scene <" + new_name + ">")
        bpy.ops.scene.new()
        bpy.context.scene.name = new_name
        scene = bpy.data.scenes[new_name]
        
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    return scene

def getObjectBounds(ob):
    p1 = ob.bound_box[0]
    p2 = ob.bound_box[6]
    
    o_x = (p1[0] + p2[0]) / 2
    o_y = (p1[1] + p2[1]) / 2
    o_z = (p1[2] + p2[2]) / 2
    
    l_x = p2[0] - p1[0]
    l_y = p2[1] - p1[1]
    l_z = p2[2] - p1[2]

    return o_x, o_y, o_z, l_x, l_y, l_z

def addCollisionStarterMeshes(scene):
    for ob in scene.objects:
        if ob.type == 'MESH':
            print("Working on " + ob.name)
            
            o_x, o_y, o_z, l_x, l_y, l_z = getObjectBounds(ob)
            diameter = math.sqrt(l_x * l_x + l_y * l_y + l_z * l_z)
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.mesh.primitive_cube_add(radius=1.0, location=[o_x, o_y, o_z])
            bpy.context.selected_objects[0].name = ob.name + "_bounding"
            bpy.context.selected_objects[0].scale = [l_x/2, l_y/2, l_z/2]
            #bpy.ops.object.move_to_layer(layers=(False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False))

            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=[o_x, o_y, o_z], size=diameter)
            bpy.context.selected_objects[0].name = ob.name + "_complex_2"
            bpy.ops.object.modifier_add(type='SHRINKWRAP')
            bpy.context.object.modifiers["Shrinkwrap"].target = bpy.data.objects[ob.name]
            bpy.context.object.modifiers["Shrinkwrap"].wrap_method = "NEAREST_VERTEX"
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")
            #bpy.ops.object.move_to_layer(layers=(False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False))
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, location=[o_x, o_y, o_z], size=diameter)
            bpy.context.selected_objects[0].name = ob.name + "_complex_3"
            bpy.ops.object.modifier_add(type='SHRINKWRAP')
            bpy.context.object.modifiers["Shrinkwrap"].target = bpy.data.objects[ob.name]
            bpy.context.object.modifiers["Shrinkwrap"].wrap_method = "NEAREST_VERTEX"
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")
            #bpy.ops.object.move_to_layer(layers=(False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False))
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, location=[o_x, o_y, o_z], size=diameter)
            bpy.context.selected_objects[0].name = ob.name + "_complex_4"
            bpy.ops.object.modifier_add(type='SHRINKWRAP')
            bpy.context.object.modifiers["Shrinkwrap"].target = bpy.data.objects[ob.name]
            bpy.context.object.modifiers["Shrinkwrap"].wrap_method = "NEAREST_VERTEX"
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")
            #bpy.ops.object.move_to_layer(layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False))
            
            print("Done")

def cleanModels(scene):
    for ob in scene.objects:
        if ob.type == 'MESH':
            print("Working on " + ob.name)
            bpy.ops.object.select_all(action='DESELECT')
            ob.select = True
            bpy.context.scene.objects.active = ob
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            
            print("Removing Doubles")
            bpy.ops.mesh.remove_doubles()
            
            print("Fixing normals")
            bpy.ops.mesh.normals_make_consistent()

            bpy.ops.object.mode_set(mode = 'OBJECT')
            print("Done")
    
def main():
    original_type = bpy.context.area.type
    bpy.context.area.type = "VIEW_3D"
    
    for file in os.listdir(mesh_folder):
        if file.lower().endswith(".stl") and os.path.isfile(mesh_folder + file):
            scene = createScene(file)
            bpy.ops.import_mesh.stl(filepath= mesh_folder + file)
            addCollisionStarterMeshes(scene)
            cleanModels(scene)
        if file.lower().endswith(".dae") and os.path.isfile(mesh_folder + file):
            scene = createScene(file)
            bpy.ops.wm.collada_import(filepath= mesh_folder + file)
            addCollisionStarterMeshes(scene)
            cleanModels(scene)
        if not os.path.isfile(mesh_folder + file):
            pass
        
    bpy.context.area.type = original_type

main()
