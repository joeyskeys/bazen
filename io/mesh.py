
import bpy, bmesh
import xml.etree.ElementTree as ET
from .base import BaseIO
from ..utils.obj_export import obj_export
from ..utils import triangulate as tr
from ..utils.frame import to_kazen_frame
from ..utils.shader_utils import get_shader_from_material
from ..pyzen import vec as pv
from ..pyzen import mat as pm


class MeshIO(BaseIO):
    """
    """

    def __init__(self):
        pass

    def get_mesh_infos(self, obj):
        if obj.active_material is None:
            material_name = 'Error'
        else:
            material_name = obj.active_material.name

        translation = to_kazen_frame(obj.location)

        prev_rot_mode = obj.rotation_mode
        obj.rotation_mode = 'AXIS_ANGLE'
        angle_axis = tuple(obj.rotation_axis_angle)
        angle_axis = (angle_axis[0], angle_axis[1], angle_axis[3], -angle_axis[2])
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

    @staticmethod
    def is_zero(socket):
        eps = 0.00000001
        if socket.bl_idname == 'NodeSocketFloat':
            return socket.default_value < eps
        elif socket.bl_idname == 'NodeSocketColor':
            v = socket.default_value
            return v[0] < eps and v[1] < eps and v[2] < eps
        else:
            raise Exception('Zero check for node socket only supports float and color now')

    def feed_api(self, scene, obj):
        translation, angle_axis, scale, mat_name = self.get_mesh_infos(obj)
        matrix = pm.translate3f(pv.create_vec3f(translation))
        matrix *= pm.rotate3f(pv.Vec3f(angle_axis[1], angle_axis[2], angle_axis[3]), angle_axis[0])
        matrix *= pm.scale3f(pv.create_vec3f(scale))

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
        verts = tr.convert_to_vecs(pv.create_vec3f, verts)
        normals = tr.convert_to_vecs(pv.create_vec3f, normals)
        uvs = tr.convert_to_vecs(pv.create_vec2f, uvs)
        faces = tr.convert_to_vecs(pv.create_vec3i, faces)

        # According to emissive properties' value to set the mesh
        # as light or not
        is_light = False
        shader = get_shader_from_material(obj.active_material, 'ShaderNodeOutputMaterial', 0)
        for emissive_prop in shader.emissive_props:
            if not self.is_zero(shader.inputs[emissive_prop]):
                is_light = True
                break

        # Currently leave it as a simple mesh..
        scene.add_mesh(matrix, verts, normals, uvs, faces, mat_name, is_light)
        