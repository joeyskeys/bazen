
import bpy
import bmesh
import os


def obj_export(obj, path):
    path = os.path.join(path, 'meshes')
    os.makedirs(path, exist_ok=True)
    file_name = os.path.join(path, obj.name + '.obj')
    with open(file_name, 'w') as f:
        depgraph = bpy.context.evaluated_depsgraph_get()
        bm = bmesh.new()
        bm.verts.ensure_lookup_table()
        bm.from_object(obj, depgraph)
        has_uv = obj.data.uv_layers != None and len(obj.data.uv_layers) > 0

        for v in bm.verts:
            f.write('v {} {} {}\n'.format(v.co.x, v.co.z, -v.co.y))
        f.write('\n')

        if has_uv:
            for uv_obj in obj.data.uv_layers.active.data:
                f.write('vt {} {}\n'.format(uv_obj.uv.x, uv_obj.uv.y))
            f.write('\n')

        #for v in bm.verts:
            #f.write('vn {} {} {}\n'.format(v.normal.x, v.normal.z, -v.normal.y))
        #f.write('\n')

        obj.data.calc_loop_triangles()
        for tri in obj.data.loop_triangles:
            f.write('f')
            for i in range(3):
                vert_idx = tri.vertices[i]
                loop_idx = tri.loops[i]
                
                if has_uv:
                    #f.write(' {}/{}/{}'.format(vert_idx + 1, loop_idx + 1, vert_idx + 1))
                    f.write(' {}/{}'.format(vert_idx + 1, loop_idx + 1))
                else:
                    #f.write(' {}//{}'.format(vert_idx + 1, vert_idx + 1))
                    f.write(' {}'.format(vert_idx + 1))
            f.write('\n')