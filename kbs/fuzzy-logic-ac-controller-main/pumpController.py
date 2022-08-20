import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

ho_nuoc = ctrl.Antecedent(np.arange(0, 2, 0.1), 'ho_nuoc')
gieng_nuoc = ctrl.Antecedent(np.arange(0, 10, 0.1), 'gieng_nuoc')
toc_do_bom = ctrl.Consequent(np.arange(0, 30, 0.1), 'toc_do_bom')

ho_nuoc['day'] = fuzz.trimf(ho_nuoc.universe, [0, 2, 2])  # Hồ đầy
ho_nuoc['lung'] = fuzz.trimf(ho_nuoc.universe, [0, 1, 2])  # Hồ lưng
ho_nuoc['can'] = fuzz.trimf(ho_nuoc.universe, [0, 0, 2])  # Hồ cạn

gieng_nuoc['cao'] = fuzz.trimf(gieng_nuoc.universe, [0, 10, 10])  # Nước giếng cao
gieng_nuoc['vua'] = fuzz.trimf(gieng_nuoc.universe, [0, 5, 10])  # Nước giếng vừa
gieng_nuoc['it'] = fuzz.trimf(gieng_nuoc.universe, [0, 0, 10])  # Nước giếng ít

toc_do_bom['vua'] = fuzz.trimf(toc_do_bom.universe, [0, 15, 30])  # Tốc độ vừa
toc_do_bom['lau'] = fuzz.trimf(toc_do_bom.universe, [0, 30, 30])  # Tốc độ lâu
toc_do_bom['hoi_lau'] = fuzz.trimf(toc_do_bom.universe, [0, 20, 100])  # Tốc độ hơi lâu


def get_pump_speed_control_rules():  # Cac luat mo bieu dien toc do quat
    rule1 = ctrl.Rule(
        ho_nuoc['lung'] & gieng_nuoc['cao'],
        toc_do_bom['vua']
    )

    rule2 = ctrl.Rule(
        ho_nuoc['can'] & gieng_nuoc['cao'],
        toc_do_bom['lau']
    )

    rule3 = ctrl.Rule(
        ho_nuoc['lung'] & gieng_nuoc['vua'],
        toc_do_bom['vua']
    )

    rule4 = ctrl.Rule(
        ho_nuoc['can'] & gieng_nuoc['vua'],
        toc_do_bom['hoi_lau']
    )

    return [
        # rule0a, rule0b, rule0c, rule0d, rule0e,
        rule1, rule2, rule3, rule4
    ]

pump_ctrl = ctrl.ControlSystem(
    get_pump_speed_control_rules()
)

input('Nhấn Enter để tiến hành các luật!')
speed = ctrl.ControlSystemSimulation(pump_ctrl)

ho_nuoc.view()
in_hn = input("Nhap do cao cua nuoc trong ho:")
speed.input['ho_nuoc'] = int(in_hn)

gieng_nuoc.view()

in_gn = input("Nhap do cao cua nuoc trong gieng:")
speed.input['gieng_nuoc'] = int(in_gn)
speed.compute()
print("toc_do_bom", f"{speed.output['toc_do_bom']}")
toc_do_bom.view(sim=speed)

input("Nhấn phím bất kỳ để kết thúc!")