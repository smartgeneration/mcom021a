import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

ho_nuoc = ctrl.Antecedent(np.arange(0, 2, 0.1), 'ho_nuoc')
gieng_nuoc = ctrl.Antecedent(np.arange(0, 10, 0.1), 'gieng_nuoc')
toc_do_bom = ctrl.Antecedent(np.arange(0, 30, 0.1), 'toc_do_bom')

ho_nuoc['ho-day'] = fuzz.trimf(ho_nuoc.universe, [0, 2, 2]) # Hồ đầy
ho_nuoc['ho-lung'] = fuzz.trimf(ho_nuoc.universe, [0, 1, 2]) # Hồ lưng
ho_nuoc['ho-can'] = fuzz.trimf(ho_nuoc.universe, [0, 0, 2]) # Hồ cạn

# TODO: Sửa lại các chỉ số ở trimf
gieng_nuoc['gieng_cao'] = fuzz.trimf(gieng_nuoc.universe, [0, 0, 20]) # Giếng cao
gieng_nuoc['gieng_vua'] = fuzz.trimf(gieng_nuoc.universe, [0, 0, 20]) # Giếng vừa
gieng_nuoc['gieng_it'] = fuzz.trimf(gieng_nuoc.universe, [0, 0, 20]) # Giếng ít

# TODO: Sửa lại các chỉ số ở trimf
toc_do_bom['bom_vua'] = fuzz.trimf(toc_do_bom.universe, [0, 0, 20]) # Tốc độ vừa
toc_do_bom['bom_lau'] = fuzz.trimf(toc_do_bom.universe, [0, 0, 20]) # Tốc độ lâu
toc_do_bom['bom_hoi_lau'] = fuzz.trimf(toc_do_bom.universe, [0, 0, 20]) # Tốc độ hơi lâu

ho_nuoc.view()
# in_hn = input("demo")