import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Biến ngôn ngữ be_chua (bể chứa)
be_chua = ctrl.Antecedent(np.arange(0, 2, 0.1), 'be_chua')

# Biến ngôn ngữ gieng_nuoc (giếng nước)
gieng_nuoc = ctrl.Antecedent(np.arange(0, 10, 0.1), 'gieng_nuoc')

# Biến ngôn ngữ toc_do_bom (thời gian bơm nước từ giếng lên bể chứa)
toc_do_bom = ctrl.Consequent(np.arange(0, 30, 0.1), 'toc_do_bom')

# 03 tập mờ cho biến ngôn ngữ be_chua
be_chua['day'] = fuzz.trimf(be_chua.universe, [0, 2, 2])  # Hồ đầy
be_chua['lung'] = fuzz.trimf(be_chua.universe, [0, 1, 2])  # Hồ lưng
be_chua['can'] = fuzz.trimf(be_chua.universe, [0, 0, 2])  # Hồ cạn

# 03 tập mờ cho biến ngôn ngữ gieng_nuoc
gieng_nuoc['cao'] = fuzz.trimf(gieng_nuoc.universe, [0, 10, 10])  # Nước giếng cao
gieng_nuoc['vua'] = fuzz.trimf(gieng_nuoc.universe, [0, 5, 10])  # Nước giếng vừa
gieng_nuoc['it'] = fuzz.trimf(gieng_nuoc.universe, [0, 0, 10])  # Nước giếng ít

# 03 tập mờ cho biến ngôn ngữ toc_do_bom
toc_do_bom['vua'] = fuzz.trimf(toc_do_bom.universe, [0, 15, 30])  # Tốc độ vừa
toc_do_bom['lau'] = fuzz.trimf(toc_do_bom.universe, [0, 30, 30])  # Tốc độ lâu
toc_do_bom['hoi_lau'] = fuzz.trimf(toc_do_bom.universe, [0, 20, 100])  # Tốc độ hơi lâu


def get_pump_speed_control_rules():  # Các luật mờ biểu diễn tốc độ bơm nước từ giếng lên bể chứa nhanh chậm
    # Nếu Bể chứa lưng và giếng nước cao, thì tốc độ bơm vừa
    rule1 = ctrl.Rule(
        be_chua['lung'] & gieng_nuoc['cao'],
        toc_do_bom['vua']
    )

    # Nếu Bể chứa cạn và giếng nước cao, thì tốc độ bơm lâu
    rule2 = ctrl.Rule(
        be_chua['can'] & gieng_nuoc['cao'],
        toc_do_bom['lau']
    )

    # Nếu Bể chứa lưng và giếng nước vừa, thì tốc độ bơm vừa
    rule3 = ctrl.Rule(
        be_chua['lung'] & gieng_nuoc['vua'],
        toc_do_bom['vua']
    )

    # Nếu Bể chứa cạn và giếng nước vừa, thì tốc độ bơm hơi lâu
    rule4 = ctrl.Rule(
        be_chua['can'] & gieng_nuoc['vua'],
        toc_do_bom['hoi_lau']
    )

    return [
        rule1, rule2, rule3, rule4
    ]


# Cho hệ thống học các luật
speed = ctrl.ControlSystemSimulation(
    ctrl.ControlSystem(
        get_pump_speed_control_rules()
    )
)

# Xem đồ thị của bể chứa và tiến hành nhập chiều cao thử nghiệm
be_chua.view()
in_hn = input("Nhập độ cao của nước trong bể chứa (đơn vị mét): ")
speed.input['be_chua'] = int(in_hn)

# Xem đồ thị của giếng nước và tiến hành nhập chiều cao thử nghiệm
gieng_nuoc.view()
in_gn = input("Nhập độ cao của nước trong giếng nước (đơn vị mét): ")
speed.input['gieng_nuoc'] = int(in_gn)

# Tính toán tốc độ bơm
speed.compute()

# In tốc độ bơm ra console và vẽ lên đồ thị
print("Thời gian bơm là:", f"{round(speed.output['toc_do_bom'], 2)}", "phút!")
toc_do_bom.view(sim=speed)

# Lệnh dừng màn hình chờ lệnh tiếp theo
input("Nhấn phím bất kỳ để kết thúc!")