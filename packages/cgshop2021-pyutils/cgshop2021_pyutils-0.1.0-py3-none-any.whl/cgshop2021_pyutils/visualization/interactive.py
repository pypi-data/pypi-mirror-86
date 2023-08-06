import matplotlib.pyplot as plt

from cgshop2021_pyutils.instance import Instance


class BaseField:
    def __init__(self, x: int, y: int, axis):
        self.patch = plt.Rectangle((x - 0.5, y - 0.5), 1, 1)
        axis.add_patch(self.patch)
        self.x = x
        self.y = y


class ObstacleField(BaseField):
    def __init__(self, x, y, axis):
        super().__init__(x, y, axis)
        self.patch.set_color('#23395B')


class RobotField(BaseField):
    def __init__(self, axis, x, y, robot_id):
        super().__init__(x=x, y=y, axis=axis)
        self.robot_id = robot_id
        self.patch.set_ec('black')
        self.patch.set_lw(0.05)


class TargetField(RobotField):
    def __init__(self, axis, x, y, robot_id):
        super().__init__(x=x, y=y, axis=axis, robot_id=robot_id)
        self.patch.set_fc('#B9E3C6')

    def highlight(self, active):
        if active:
            self.patch.set_fc('#59C9A5')
        else:
            self.patch.set_fc('#B9E3C6')


class StartField:
    def __init__(self, axis, x, y, robot_id):
        self.robot_id = robot_id
        self.circle = plt.Circle((x, y), 0.5)
        self.circle.set_zorder(2)
        axis.add_patch(self.circle)
        self.x = x
        self.y = y
        self.circle.set_ec('black')
        self.circle.set_lw(0.05)
        self.circle.set_fc('#D81E5B')

    def highlight(self, active: bool):
        if active:
            self.circle.set_lw(0.2)
        else:
            self.circle.set_lw(0.05)


class StartFields:
    def __init__(self, instance, axis):
        self.instance = instance
        self.axis = axis
        self._start_fields = dict()
        self._create_fields()

    def _round(self, x, y):
        return int(round(x)), int(round(y))

    def at(self, x, y):
        return self._start_fields[self._round(x, y)]

    def _create_fields(self):
        for i, (x, y) in enumerate(self.instance.start):
            self._start_fields[(x, y)] = StartField(x=x, y=y, axis=self.axis, robot_id=i)

    def bounding_box(self):
        min_x = min(f.x for f in self._start_fields.values())
        max_x = max(f.x for f in self._start_fields.values())
        min_y = min(f.y for f in self._start_fields.values())
        max_y = max(f.y for f in self._start_fields.values())
        return (min_x, max_x), (min_y, max_y)


class TargetFields:
    def __init__(self, instance, axis):
        self.instance = instance
        self.axis = axis
        self._target_fields = dict()
        self._create_fields()

    def of(self, robot_id):
        return self._target_fields[robot_id]

    def _create_fields(self):
        for i, (x, y) in enumerate(self.instance.target):
            self._target_fields[i] = TargetField(x=x, y=y, axis=self.axis, robot_id=i)

    def bounding_box(self):
        min_x = min(f.x for f in self._target_fields.values())
        max_x = max(f.x for f in self._target_fields.values())
        min_y = min(f.y for f in self._target_fields.values())
        max_y = max(f.y for f in self._target_fields.values())
        return (min_x, max_x), (min_y, max_y)


class ObstacleFields:
    def __init__(self, instance, axis):
        self.instance = instance
        self.axis = axis
        self._fields = []
        self._create_fields()

    def _create_fields(self):
        for (x, y) in self.instance.obstacles:
            self._fields.append(ObstacleField(x=x, y=y, axis=self.axis))

    def bounding_box(self):
        if not self._fields:
            return ((0, 0), (0, 0))
        min_x = min(f.x for f in self._fields)
        max_x = max(f.x for f in self._fields)
        min_y = min(f.y for f in self._fields)
        max_y = max(f.y for f in self._fields)
        return (min_x, max_x), (min_y, max_y)


class StartTargetLine:
    def __init__(self, axis):
        self.line = plt.Line2D(xdata=[0, 0], ydata=[0, 0], visible=False, color='#FFFD98')
        axis.add_line(self.line)

    def show(self, start: StartField, target: TargetField):
        self.line.set_visible(True)
        self.line.set_data([start.x, target.x], [start.y, target.y])

    def hide(self):
        self.line.set_visible(False)


class MotionEventHandler:
    def __init__(self, start_fields, target_fields, figure):
        self.start_fields = start_fields
        self.target_fields = target_fields
        self.figure = figure
        self._current_field = None
        self._current_target_field = None
        self._line = StartTargetLine(axis=figure.gca())

    def _clear(self):
        if self._current_field is None:
            return
        self._current_field.highlight(False)
        self._current_field = None
        self._clear_target()
        self._line.hide()

    def _clear_target(self):
        if self._current_target_field is not None:
            self._current_target_field.highlight(False)
            self._current_target_field = None

    def _set_new_field(self, f):
        self._current_field = f
        f.highlight(True)
        try:
            tf = self.target_fields.of(f.robot_id)
            self._line.show(f, tf)
            tf.highlight(True)
            self._current_target_field = tf
        except KeyError:
            pass

    def _on_interior_move_event(self, x, y):
        try:
            f = self.start_fields.at(x, y)
            if f == self._current_field:
                return
            self._clear()
            self._set_new_field(f)
        except KeyError:
            self._clear()

    def __call__(self, event):
        (x, y) = event.xdata, event.ydata
        if x is not None:
            self._on_interior_move_event(x, y)
        self.figure.canvas.draw()


class InteractiveVisualization:
    """
    Provides an interactive visualization if the backend supports it. Otherwise, the
    visualization will be static and only highlight start positions and target positions.
    The interactive visualization will highlight the matching target for the start
    position below the cursor.
    Start positions are red circles. Target positions are green squares. Obstacles
    are dark squares.
    """
    def __init__(self, instance: Instance, figsize=None, show=True):
        self.instance = instance
        self.fig = plt.figure(figsize=figsize) if figsize else plt.figure()
        self.axis = self.fig.add_subplot(111)
        self.axis.set_aspect('equal', adjustable='box')
        self.start_fields = StartFields(instance, self.axis)
        self.target_fields = TargetFields(instance, self.axis)
        self.obstacle_fields = ObstacleFields(instance, self.axis)

        ((min_x, max_x), (min_y, max_y)) = self._bounding_box()
        plt.xlim([min_x - 10, max_x + 10])
        plt.ylim([min_y - 10, max_y + 10])
        self._event_handler = MotionEventHandler(self.start_fields, self.target_fields,
                                                 self.fig)
        if show:
            self.fig.canvas.mpl_connect('motion_notify_event', self._event_handler)
            plt.show()

    def _bounding_box(self):
        bb1 = self.start_fields.bounding_box()
        bb2 = self.target_fields.bounding_box()
        bb3 = self.obstacle_fields.bounding_box()
        return (
            (min([bb1[0][0], bb2[0][0], bb3[0][0]]),
             max([bb1[0][1], bb2[0][1], bb3[0][1]])),
            (min([bb1[1][0], bb2[1][0], bb3[1][0]]),
             max([bb1[1][1], bb2[1][1], bb3[1][1]])))
