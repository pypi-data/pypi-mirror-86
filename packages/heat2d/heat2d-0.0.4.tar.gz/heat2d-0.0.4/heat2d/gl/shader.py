import os
import struct

from heat2d import DISPATCHER
from heat2d.libs.utils import sourcepath
from heat2d.math.vector import Vector2


class Shader:
    def __init__(self, vertex=None, fragment=None, ctx=None):
        if ctx: self.ctx = ctx
        else: self.ctx = DISPATCHER.engine.renderer.ctx

        self.texture_coords = [0, 1, 1, 1,
                               0, 0, 1, 0]

        self.world_coords = [-1, -1, 1, -1,
                             -1,  1, 1,  1]

        self.render_ind = [0, 1, 2,
                           1, 2, 3]

        if vertex == None: self.vertex = os.path.join(sourcepath, "shaders", "default.vsh")
        else: self.vertex = vertex

        if fragment == None: self.fragment = os.path.join(sourcepath, "shaders", "default.fsh")
        else: self.fragment = fragment

        self.program = self.ctx.program(
            vertex_shader   = open(self.vertex,   "r").read(),
            fragment_shader = open(self.fragment, "r").read()
        )

        vbo =   self.ctx.buffer(struct.pack('8f', *self.world_coords))
        uvmap = self.ctx.buffer(struct.pack('8f', *self.texture_coords))
        ibo =   self.ctx.buffer(struct.pack('6I', *self.render_ind))

        vao_content = [
            (vbo, '2f', 'vert'),
            (uvmap, '2f', 'in_text'),
        ]

        self.vao = self.ctx.vertex_array(self.program, vao_content, ibo)

    def __repr__(self):
        return f"<heat2d.gl.Shader(vertex={self.vertex}, fragment={self.fragment})>"

    def render(self):
        self.vao.render()

    def set_uniform(self, name, *values):
        uniform = self.program.__getitem__(name)

        if isinstance(values[0], int):
            uniform.write(struct.pack(f"{len(values)}i", *values))

        elif isinstance(values[0], float):
            uniform.write(struct.pack(f"{len(values)}f", *values))

        elif isinstance(values[0], bool):
            uniform.write(struct.pack(f"{len(values)}?", *values))

        elif isinstance(values[0], str):
            uniform.write(struct.pack(f"{len(values)}s", *values))

        elif isinstance(values[0], Vector2):
            uniform.write(struct.pack("2f", values[0].x, values[0].y))

        elif isinstance(values[0], bytes):
            uniform.write(values[0])
