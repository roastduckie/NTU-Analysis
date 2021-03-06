import math
import numpy as np

shell_steam_pressure = float(input('What is the shell-side steam pressure? '))
shell_steam_temp = float(input('What is the shell-side steam temperature? '))
shell_conv_coeff = float(input('What is the shell-side convection coefficient? '))
shell_density = float(input('What is the steam density? '))
shell_enthalpy = float(input('What is the shel-side steam enthalpy? '))
print('   ')
tube_num = int(input('How many tubes are in the exchanger? '))
tube_cond_k = float(input('What is the heat conduction coefficient of the tube material? '))
tube_passes = int(input('How many tube passes? '))
tube_d_i = float(input('What is the inner diameter of the tube (m)? '))
tube_d_o = float(input('What is the outer diameter of the tube (m)? '))
tube_length = float(input('How long are the tubes (m)? '))
print('   ')
water_temp = float(input('What is the water temperature at the inlet? '))
water_vel = float(input('What is the mean velocity of the water? '))
water_visc = float(input('What is the viscosity of the water? '))
water_prandtl = float(input('What is the Prandtl number of the water? '))
water_cond_k = float(input('what is the conduction coefficient of the water? '))
water_cp = float(input('What is the pressure specific heat capacity of the water? '))
water_density = float(input('What is the density of the water? '))
water_purpose = input('what is the purpose of the water? Heating/Cooling ')

# Nusselt number coefficient, based on HX water purpose
if water_purpose in ['Cooling']:
    nuss_coeff = 0.4
else:
    nuss_coeff = 0.3

reyn = (water_density * water_vel * tube_d_i) / water_visc
print(f'The Reynolds number is {reyn}.')

if reyn > 2500:
    print('The flow is turbulent.')
    nusselt = 0.023 * water_prandtl ** nuss_coeff * reyn ** 0.8
    print(f'The Nusselt number is {nusselt}.')
else:
    print('The flow is laminar.')
    nusselt = 4.364
    print(f'The Nusselt number is {nusselt}.')

# Internal heat transfer coefficient
ht_coeff = (water_cond_k * nusselt) / tube_d_i
print(f'The internal heat transfer coefficient is {ht_coeff}.')

#  overall heat transfer coefficient
overall_coeff = ((1 / shell_conv_coeff) + tube_d_o * math.log((tube_d_o / 2) / (tube_d_i / 2)) / tube_cond_k
                 + (tube_d_o / tube_d_i) * (1 / ht_coeff)) ** -1
print(f'The overall heat transfer coefficient is {overall_coeff}.')

#  mass flow rate of water
m_dot = water_density * water_vel * tube_num * (np.pi * (tube_d_i ** 2) / 2)
print(f'The mass flow rate of the water is {m_dot}.')

#  external tube area
tube_area = np.pi * tube_d_o * tube_length * tube_num * tube_passes
print(f'The total tube external area is {tube_area}.')

#  C_min
c_min = water_cp * m_dot

#  NTU
ntu = overall_coeff * tube_area / c_min
print(f'The NTU value is {ntu}.')

#  Effectiveness
eff = 1 - np.exp(-1 * ntu)
print(f'The effectiveness of the exchanger is {eff}.')

#  water outlet temp
out_temp = water_temp + eff * (shell_steam_temp - water_temp)
print(f'The outlet water temp is {out_temp}.')

#  total heat transfer rate
ht_rate = c_min * (out_temp - water_temp) / 1000
print(f'The total heat transfer rate is {ht_rate} kW.')

#  Steam condensation rate
steam_condense = ht_rate / shell_enthalpy
print(f'The steam condensation rate is {steam_condense} kg/s.')
