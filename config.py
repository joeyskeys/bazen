import os

# This field should align with the name set in bl_info
engine_name = "bazen"
engine_label = "Bazen"

film_props = [
    {
        'type' : 'string',
        'name' : 'output',
        'text' : 'Output',
        'props' : {
            'description' : 'Output path of the render',
            'default' : './output.png',
            'subtype' : 'FILE_PATH'
        }
    }
]

camera_props = [
    {
        'type' : 'float',
        'name' : 'near_plane',
        'text' : 'Near Plane',
        'props' : {
            'description' : 'Near clipping plane',
            'default' : 1,
            'min' : 0.1,
            'max' : 100,
        }
    },
    {
        'type' : 'float',
        'name' : 'far_plane',
        'text' : 'Far Plane',
        'props' : {
            'description' : 'Far clipping plane',
            'default' : 1000,
            'min' : 10,
            'max' : 100000,
        }
    },
]

accelerator_props = [
    {
        'type' : 'enum',
        'name' : 'accelerator_type',
        'text' : 'AcceleratorType',
        'props' : {
            'items' : (
                ('Accelerator', 'BasicAccel', ''),
                ('BVHAccelerator', 'BVHAccel', ''),
                ('EmbreeAccelerator', 'EmbreeAccel', ''),
            ),
            'default' : 'EmbreeAccelerator',
        }
    }
]

integrator_props = [
    {
        'type' : 'enum',
        'name' : 'integrator_type',
        'text' : 'IntegratorType',
        'props' : {
            'items' : (
                ('NormalIntegrator', 'Normal', ''),
                ('AmbientOcclusionIntegrator', 'AmbientOcculusion', ''),
                ('WhittedIntegrator', 'Whitted', ''),
                ('PathMatsIntegrator', 'PathMats', ''),
                ('PathEmsIntegrator', 'PathEms', ''),
                ('PathIntegrator', 'Path', ''),
            ),
            'default' : 'PathIntegrator',
        }
    }
]

light_props = []

sampler_props = []

world_props = []

preference_props = [
    {
        'type' : 'int',
        'name' : 'sample_cnt',
        'text' : 'Sample Count',
        'props' : {
            'description' : 'Sample count for each pixel',
            'default' : 5,
        }
    },
    {
        'type' : 'int',
        'name' : 'thread_cnt',
        'text' : 'Thread Count',
        'props' : {
            'description' : 'Thread count setting',
            'default' : os.cpu_count(),
        }
    }
]

category_name = 'BAZEN'

node_categories = [
    ('BazenMaterial', 'Material'),
    ('BazenTexture', 'Texture'),
]

use_seprate_node_editor = False
node_editor_name = 'Bazen Shader Editor'
node_editor_convert_text = 'Use Bazen Material Nodes'
node_editor_recover_text = 'Use Cycles Material Nodes'
output_node_label = 'BazenOutput'