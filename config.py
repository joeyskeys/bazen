
engine_name = "EXAMPLE_RENDER"
# This field should align with the name set in bl_info
engine_label = "bazen"

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
        'name' : 'osl_query_location',
        'text' : 'Oslinfo Location',
        'props' : {
            'description' : 'Location of oslinfo',
            'default' : 'D:/Program/oslinfo',
            'subtype' : 'FILE_PATH'
        }
    },
    {
        'type' : 'string',
        'name' : 'osl_shader_location',
        'text' : 'OSL Shader Location',
        'props' : {
            'description' : 'Location of OSL shaders',
            'default' : 'D:/Program/osl_shaders',
            'subtype' : 'DIR_PATH'
        }
    }
]

node_categories = [
    ('BITTO_MATERIAL', 'Material'),
    ('BITTO_TEXTURE', 'Texture'),
]