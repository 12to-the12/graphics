
:::mermaid
graph TB
    start((start)) -->
    1[update]-->
        3[event_processing]

        3 --> update_state
        subgraph update_state
            6[rotate]
        end
        update_state --> 8
        8[render]-->
            10[draw_polygons]-->
                12[normal_cull]-->
                13[project_in_camera_space]-->
                14[z_sort]-->
                15[project_in_screen_space]-->
                16[frustrum_cull]-->
                17[project_screen_coordinates]-->
        20[render_to_screen]-->
    End((end))
:::

