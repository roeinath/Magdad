from web_framework.server_side.infastructure.components.card import Card
from web_framework.server_side.infastructure.components.container import Container
from web_framework.server_side.infastructure.components.label import Label
import web_framework.server_side.infastructure.constants as constants


class DashboardCard(Card):
    CARD_HEIGHT = 45
    CARD_BG = 'white'
    CARD_PADD = '15px'
    CARD_CORNER_RAD = '2px'
    CARD_TITLE_SIZE = constants.SIZE_MEDIUM
    CARD_SHAD_X_OFF = '2px'
    CARD_SHAD_Y_OFF = '4px'
    CARD_SHAD_BLUR = '9px'
    CARD_SHAD_SPREAD = '3px'
    CARD_SHAD_COLOR = 'black'
    CARD_SHAD_OPACITY = 0.1

    def __init__(self, grid_start, grid_end, title):
        super().__init__(height=f'{self.CARD_HEIGHT * (grid_end[1] - grid_start[1])}vh', padding=self.CARD_PADD,
                         corner_radius=self.CARD_CORNER_RAD,
                         bg_color=self.CARD_BG,
                         grid_start=grid_start,
                         grid_end=grid_end)

        self.apply_shadow(x_off=self.CARD_SHAD_X_OFF, y_off=self.CARD_SHAD_Y_OFF, blur=self.CARD_SHAD_BLUR,
                          spread=self.CARD_SHAD_SPREAD, color=self.CARD_SHAD_COLOR, opacity=self.CARD_SHAD_OPACITY)

        self.title_label = Label(title, size=self.CARD_TITLE_SIZE, bold=True)
        title_cont = Container(height='5%', margin='0 0 20px 0', justify_content='flex_start',
                               orientation='row-reverse')

        title_cont.set_child(self.title_label)
        self.add_child(title_cont)
