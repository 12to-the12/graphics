:::mermaid
%%{ init: { 'flowchart': { 'curve': 'linear' } } }%%
graph TB
    classDef default fill:#222 outline:#000

    subgraph application
        user_input
        animation
    end

    
    application   --scene_data--> rast & ray_cast
    
    
    subgraph rast

        subgraph geometry
            local..world_transformation -->
            world..camera_transformation -->
            lighting -->
            3d..2d_projection -->
            clipping -->
            window/viewport_transformation
        end

        subgraph rasterization
            rasterize
        end

        

    end

    
    geometry      --screen_space_polygons--> rasterization
    rast & ray_cast --image--> screen


:::


    
    