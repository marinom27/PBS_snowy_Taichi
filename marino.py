import taichi as ti
import time

ti.init(arch=ti.gpu)


@ti.data_oriented
class PendulumSystem(object):
    def __init__(self, g=9.81, dt=0.001):
        self.g = g
        self.dt = dt
        self.t = ti.field(float, ())
        self.pause = ti.field(int, ())
        self.x = ti.field(float, ())
        self.y = ti.field(float, ())
        self.minmax = ti.Vector.field(2, float, 1)

    @ti.kernel
    def init(self):
        self.t[None] = 0
        self.pause[None] = 0
        self.x[None] =0.5
        self.y[None]=0.5
        # (Re)initialize particle position/velocities

        self.minmax[0] = [1, -1]


    def step(self):
        """
        update theta and/or omega given the following 2-order ODE
        d^2 theta / dt = − g / L sin theta (theta << 1)
        how can we separate it to two combined first order ODE? (hint: omega)
        """
        if self.pause[None]:
            return


            # analytic solution
        self.t[None] += self.dt
        self.x[None] += 0
        self.y[None] -=self.g/2*self.t[None]**2


    def render(self, gui):  # Render the scene on GUI

        gui.line(
            [0, 0.75],  # top-left
            [1, 0.75],  # top-right
            radius=1,
            color=0xFFAA88,
        )

        gui.circle([self.x[None],self.y[None]], radius=10, color=0xFFFFFF)
        print(self.x[None])
        print(self.y[None])
        self.minmax[0].x = min(self.x[None], self.minmax[0].x)
        self.minmax[0].y = max(self.y[None], self.minmax[0].y)

        # minbar
        gui.line(
            [self.minmax[0].x, 0.73],
            [self.minmax[0].x, 0.77],
            radius=1,
            color=0xFFAA88,
        )

        # maxbar
        gui.line(
            [self.minmax[0].y, 0.73],
            [self.minmax[0].y, 0.77],
            radius=1,
            color=0xFFAA88,
        )

        gui.text(content="Space: pause", pos=(0, 0.99), color=0xFFFFFF)



pendulum = PendulumSystem()
pendulum.init()

## GUI
gui = ti.GUI("Pendulum")
while gui.running:
    for e in gui.get_events(ti.GUI.PRESS):
        if e.key in [ti.GUI.ESCAPE, ti.GUI.EXIT, "q"]:
            exit()
        elif e.key == gui.SPACE:
            pendulum.pause[None] = not pendulum.pause[None]
        else:
            try:
                if int(e.key) in pendulum.method_name:
                    pendulum.integration_method(
                        int(e.key)
                    )  # change the integration method
                    pendulum.init()
            except:
                pass

    pendulum.step()  # Time integration
    #time.sleep(1)
    pendulum.render(gui)
    gui.show()
