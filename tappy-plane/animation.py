import sfml as sf


class Animation:
    def __init__(self):
        self.texture = None
        self.frames = []

    def add_frame(self, rect):
        self.frames.append(rect)


class AnimatedSprite(sf.TransformableDrawable):
    def __init__(self, frametime=sf.seconds(0.2), paused=False, looped=True):
        super(AnimatedSprite, self).__init__()

        self.animation = None
        self.frametime = frametime
        self.paused = paused
        self.looped = looped

        self.current_time = None
        self.current_frame = 0

        self.texture = None

        self.vertices = sf.VertexArray(sf.PrimitiveType.QUADS, 4)

    def set_animation(self, animation):
        self.animation = animation
        self.texture = animation.texture
        self.current_frame = 0
        self.set_frame(0)

    def play(self, animation=None):
        if animation and self.animation is not animation:
            self.set_animation(animation)
        self.paused = False

    def pause(self):
        self.paused = True

    def stop(self):
        self.paused = True
        self.current_frame = 0
        self.set_frame(self.current_frame)

    def set_color(self, color):
        for i in self.vertices:
            i.color = color

    def local_bounds(self):
        rect = self.animation.frames[self.current_frame]

        width = abs(rect.width)
        height = abs(rect.height)
        return sf.Rectangle((0.0, 0.0), (width, height))

    @property
    def global_bounds(self):
        return self.transform.transform_rectangle(self.local_bounds())

    def set_frame(self, frame, reset_time=True):
        if self.animation:
            rect = self.animation.frames[frame]

            self.vertices[0].position = sf.Vector2(0.0, 0.0)
            self.vertices[1].position = sf.Vector2(0.0, rect.height)
            self.vertices[2].position = sf.Vector2(rect.width, rect.height)
            self.vertices[3].position = sf.Vector2(rect.width, 0.0)

            left = rect.left + 0.0001
            right = left + rect.width
            top = rect.top
            bottom = top + rect.height

            self.vertices[0].tex_coords = sf.Vector2(left, top)
            self.vertices[1].tex_coords = sf.Vector2(left, bottom)
            self.vertices[2].tex_coords = sf.Vector2(right, bottom)
            self.vertices[3].tex_coords = sf.Vector2(right, top)

        if reset_time:
            self.current_time = sf.Time.ZERO

    def update(self, delta):
        if not self.paused and self.animation:
            self.current_time += delta

            if self.current_time >= self.frametime:
                self.current_time -= self.frametime

                if self.current_frame + 1 < len(self.animation.frames):
                    self.current_frame += 1

                else:
                    self.current_frame = 0

                    if not self.looped:
                        self.paused = True

                self.set_frame(self.current_frame, False)

    def draw(self, target, states):
        if self.animation and self.texture:
            states.transform *= self.transform
            states.texture = self.texture
            target.draw(self.vertices, states)