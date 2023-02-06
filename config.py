import os

# This field should align with the name set in bl_info
engine_name = "bazen"
engine_label = "Bazen"

film_props = [
    {
        'type' : 'float',
        'name' : 'example',
        'text' : 'Example',
        'props' : {
            'description' : 'this is a example property',
            'default' : 0,
            'min' : 0,
            'max' : 1
        }
    },
    {
        'type' : 'string',
        'name' : 'string_prop',
        'text' : 'BlaBla',
        'props' : {
            'description' : 'this is a example float property',
            'default' : '',
            'subtype' : 'FILE_PATH'
        }
    }
]

camera_props = []

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

node_editor_convert_text = 'Use Bazen Material Nodes'