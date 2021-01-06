import brainrender
from brainrender.scene import Scene
from brainrender.Utils.data_manipulation import get_coords, flatten_list, is_any_item_in_list
from vtkplotter import Text2D, closePlotter, embedWindow, settings, Plane, Text

class ZXScene(Scene):
    def apply_render_style(self):
        if brainrender.SHADER_STYLE is None:  # No style to apply
            return

        # Get all actors in the scene
        actors = self.get_actors()

        for actor in actors:
            if actor is not None:
                try:
                    actor.lighting(style='ambient',ambient=1, diffuse=0, specular=0,specularPower=1,specularColor=(0,0,0))
                except:
                    pass  # Some types of actors such as Text 2D don't have this attribute!


    def get_none_root_actors(self):
        all_actors = []
        for k, actors in self.actors.items():
            if isinstance(actors, dict):
                if len(actors) == 0: continue
                all_actors.extend(list(actors.values()))
            elif isinstance(actors, list):
                if len(actors) == 0: continue
                for act in actors:
                    if isinstance(act, dict):
                        all_actors.extend(flatten_list(list(act.values())))
                    elif isinstance(act, list):
                        all_actors.extend(act)
                    else:
                        all_actors.append(act)
            else:
                # all_actors.append(actors)
                pass
        return all_actors


    def cut_actors_with_plane(self, plane, actors=None, showplane=False,
                              returncut=False,
                              close_actors=False,
                              **kwargs):
        # Check arguments
        if isinstance(plane, (list, tuple)):
            planes = plane.copy()
        else:
            planes = [plane]

        if actors is None:
            actors = self.get_none_root_actors()
        else:
            if not isinstance(actors, (list, tuple)):
                actors = [actors]

        # Loop over each plane
        to_return = []
        for plane in planes:
            # Get the plane actor
            if isinstance(plane, str):
                if plane == 'sagittal':
                    plane = self.atlas.get_sagittal_plane(**kwargs)
                elif plane == 'coronal':
                    plane = self.atlas.get_coronal_plane(**kwargs)
                elif plane == 'horizontal':
                    plane = self.atlas.get_horizontal_plane(**kwargs)
                else:
                    raise ValueError(f'Unrecognized plane name: {plane}')
            else:
                if not isinstance(plane, Plane):
                    raise ValueError(f'The plane arguments should either be a Plane actor or'
                                     + 'a string with the name of predefined planes.' +
                                     f' Not: {plane.__type__}')

            # Show plane
            if showplane:
                self.add_vtkactor(plane)

            # Cut actors
            for actor in actors:
                if actor is None: continue
                actor = actor.cutWithPlane(origin=plane.center, normal=plane.normal, returnCut=returncut)
                if returncut:
                    to_return.append(actor)

                if close_actors:
                    actor.cap()

        if len(to_return) == 1:
            return to_return[0]
        else:
            return to_return

    def cut_root_with_plane(self, plane, actors=None, showplane=False,
                              returncut=False,
                              close_actors=False,
                              **kwargs):
        # Check arguments
        if isinstance(plane, (list, tuple)):
            planes = plane.copy()
        else:
            planes = [plane]

        # Loop over each plane
        to_return = []
        for plane in planes:
            # Get the plane actor
            if isinstance(plane, str):
                if plane == 'sagittal':
                    plane = self.atlas.get_sagittal_plane(**kwargs)
                elif plane == 'coronal':
                    plane = self.atlas.get_coronal_plane(**kwargs)
                elif plane == 'horizontal':
                    plane = self.atlas.get_horizontal_plane(**kwargs)
                else:
                    raise ValueError(f'Unrecognized plane name: {plane}')
            else:
                if not isinstance(plane, Plane):
                    raise ValueError(f'The plane arguments should either be a Plane actor or'
                                     + 'a string with the name of predefined planes.' +
                                     f' Not: {plane.__type__}')

            # Show plane
            if showplane:
                self.add_vtkactor(plane)

            self.actors['root'] = self.actors['root'].cutWithPlane(origin=plane.center, normal=plane.normal, returnCut=returncut)

            if returncut:
                to_return.append(self.actors['root'])

            if close_actors:
                self.actors['root'].cap()

        if len(to_return) == 1:
            return to_return[0]
        else:
            return to_return