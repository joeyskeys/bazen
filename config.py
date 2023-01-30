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
        'type' : 'string',
        'name' : 'kazen_install_path',
        'text' : 'Kazen Installation Location',
        'props' : {
            'description' : 'Location of Kazen installation',
            'default' : '/usr/local',
            'subtype' : 'FILE_PATH',
        }
    },
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

node_categories = [
    ('BITTO_MATERIAL', 'Material'),
    ('BITTO_TEXTURE', 'Texture'),
]