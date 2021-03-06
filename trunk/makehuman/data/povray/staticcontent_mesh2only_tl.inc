// Create a camera definition based on the MakeHuman camera settings when this 
// file was generated. We need to convert between the OpenGL vertical FOV and 
// the horizontal POV-Ray camera angle. We also need to account for the way 
// OpenGL reports its camera data, translating before rotating, which further 
// moves the camera. The x-axis is also reversed to the standard POV-Ray settings.
#declare MakeHuman_Camera = camera {
  perspective
  location <MakeHuman_EyeX, MakeHuman_EyeY, MakeHuman_EyeZ>
  look_at <MakeHuman_FocusX, MakeHuman_FocusY, MakeHuman_FocusZ>
  angle 30
}

// Create a standard light definition based on MakeHuman settings.
#declare MakeHuman_LightSource = light_source {
    <MakeHuman_LightX, MakeHuman_LightY, MakeHuman_LightZ>
    color rgb 1
    spotlight
    radius 1000
    falloff 1000
    tightness 1
    point_at < MakeHuman_TranslateX, MakeHuman_TranslateY, MakeHuman_TranslateZ>
}

// Assign default values.
// This texture uses the standard pigment map as a uv-mapped pigment and adds a
// little disruption to the surface normals.  
#ifndef (MakeHuman_Material)

    #declare DIFFUSE = pigment { 
        image_map { png "texture.png"}
    }

    #declare NORMAL = normal {
        wrinkles %%wrinkles%% scale 0.0002
    }
 
    #declare FINISH = finish { 
        specular %%skinoil%%  // Max highlight intensity: 0 -> 1
        roughness %%rough%%  // surface roughness: 0.0005 -> 1
        phong 0 phong_size 0  // Phong specular disabled

        ambient 0.3 // rgb <0.00,0.00,0.00>
        diffuse 2.0
        reflection{0 }
        conserve_energy
    }

//material{
#declare MakeHuman_Material = material {
        texture { uv_mapping
                pigment { DIFFUSE }
                normal  { NORMAL }
                finish  { FINISH }
        }
        interior{ior 1.33}
}

#end

                                                                            