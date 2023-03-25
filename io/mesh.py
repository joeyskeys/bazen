
import bpy, bmesh
import xml.etree.ElementTree as ET
from .base import BaseIO
from ..utils.obj_export import obj_export
from ..utils import triangulate as tr
import pyzen.mat as pzmat


class MeshIO(BaseIO):
    """
    """

    def __init__(self):
        pass

    def get_mesh_infos(self, obj, matrix=False):
        if obj.active_material is None:
            material_name = 'Error'
        else:
            material_name = obj.active_material.name

        if matrix:
            ret_matrix = (
                *tuple(obj.matrix_world[0]),
                *tuple(obj.matrix_world[1]),
                *tuple(obj.matrix_world[2]),
                *tuple(obj.matrix_world[3]),
            )
            return ret_matrix, material_name
        else:
            translation = tuple(obj.location)

            prev_rot_mode = obj.rotation_mode
            obj.rotation_mode = 'AXIS_ANGLE'
            angle_axis = tuple(obj.rotation_axis_angle)
            obj.rotation_mode = prev_rot_mode

            scale = tuple(obj.scale)
            
            return translation, angle_axis, scale, material_name

    def write_description(self, handle, obj, path):
        obj_export(obj, path)

        translate, angle_axis, scale, material_name = self.get_mesh_infos(obj)

        mesh_props = {
            'filename' : 'string meshes/{}.obj'.format(obj.name),
            'shader_name' : material_name
        }

        if abs(translate.x) + abs(translate.y) + abs(translate.z) > 1e-6:
            mesh_props.update({'translate' : 'float3 {} {} {}'.format(translate[0], translate[2], -translate[1])})
        if abs(angle_axis[0]) > 1e-6:
            mesh_props.update({'rotate' : 'float4 {} {} {} {}'.format(angle_axis[1], angle_axis[3], -angle_axis[2], angle_axis[0])})
        if abs(scale.x - 1) + abs(scale.y - 1) + abs(scale.z - 1) > 1e-6:
            mesh_props.update({'scale' : 'float3 {} {} {}'.format(scale[0], scale[2], scale[1])})

        # Restore the rotation mode
        obj.rotation_mode = prev_mode

        mesh_node = ET.SubElement(handle, 'Mesh', mesh_props)

    def feed_api(self, scene, obj):
        matrix, mat_name = self.get_mesh_infos(obj, True)

        # From James Tompkin's work
        depgraph = bpy.context.evaluated_depsgraph_get()
        bm = bmesh.new()
        bm.verts.ensure_lookup_table()
        bm.from_object(obj, depgraph)

        has_uvs = obj.data.uv_layers != None and len(obj.data.uv_layers) > 0
        if not has_uvs:
            # By default every mesh in blender will have a default UV set
            # and kazen currently only support mesh with UV
            raise Exception("Mesh {} doesn't have a UV set".format(obj.name))

        verts, normals, uvs, faces = tr.triangulateUV(obj, bm)
        # Currently leave it as a simple mesh..
        scene.add_mesh(pzmat.Mat4f(*matrix), verts, normals, uvs, faces, mat_name)
        