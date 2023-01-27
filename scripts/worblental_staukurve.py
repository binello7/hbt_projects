from hbt import hydraulics as hd

loc_params = {
    'Biglen': {
        'ho': 0.38, # m (705.25 - 704.97) + 10 cm
        'hm': 0.164, # m Wassertiefe an der Messstelle
        'Q': 106e-3, # m3/s
        'D': 0.500, # m
        'k_st': 85,
        'J': 0.0083, # -
        'Rs': 0.350, # m
        'rv': 0 # mm
    },
    'Ittigen': {
        'ho': 2.96, # m (515.65 - 512.69)
        'hm': 0.242, # m Wassertiefe an der Messstelle
        'Q': 1000e-3, # m3/s
        'D': 1.000, # m
        'k_st': 85,
        'J': 0.0169, # -
        'Rs': 0.750, # m
        'rv': 0 # mm
    },
    'Stettlen': {
        'ho': 0.74, # m
        'hm': 0.096, # m Wassertiefe an der Messstelle
        'Q': 80e-3, # m3/s
        'D': 0.350, # m
        'k_st': 95,
        'J': 0.0059, # -
        'Rs': 0.225, # m
        'rv': 0 # mm
    },
    'Zollikofen': {
        'S_931': 519.14, # m ü. M.
        'E1_932': 518.75, # m ü. M.
        'J_932_933': 0.0162, # -
        'L_931_932': 68.03, # m
        'D_931_932': 0.6, # m
        'D_932_933': 0.7, # m
        'k_st': 85,
        'Q': 194e-3, # m3/s
        'hm': 0.195, # m Wassertiefe an der Messstelle
        'hn_932_933': 0.180 # m Normale Wassertiefe 932-933

    }
}

for loc, params in loc_params.items():
    if loc != 'Zollikofen':
        ho = params['ho']
        hm = params['hm']
        Q = params['Q']
        D = params['D']
        k_st = params['k_st']
        J = params['J']
        Rs = params['Rs']
        rv = params['rv']

        print(loc)
        print(f'D = {D:0.3f} m')
        print(f'J = {J:0.4f}\n')

        s = hd.s_gvalve(D, Rs, Q, rv, ho)
        print(f's = {s:0.3f} m')

        As = hd.A_scircle(D, Rs, s)
        print(f'As = {As:0.5f} m^2')

        Cd = hd.Cd_gvalve(D, s, rv)
        print(f'Cd = {Cd:0.3f}\n')

        hu = Cd * s
        print(f'hu = {hu:0.2f} m')
        print(f'hm = {hm:0.3f} m')
        hn = hd.strickler_circ_h(k_st, J, Q, D)
        print(f'hn = {hn:0.3f} m\n')

        print(f'Q = {Q:0.3f} m^3/s')
        Qnm = hd.strickler_circ_q(k_st, J, D, hm)
        print(f'Qnm  = {Qnm:0.3f} m^3/s')
        perc_diff = Qnm / Q * 100
        print(f'{perc_diff:0.1f} % vom SOLL Abfluss')
        print(((25*'-') + '\n'))

    else:
        k_st = params['k_st']
        Q = params['Q']
        S_931 = params['S_931']
        E1_932 = params['E1_932']
        J_932_933 = params['J_932_933']
        L_931_932 = params['L_931_932']
        D_931_932 = params['D_931_932']
        D_932_933 = params['D_932_933']
        hn_932_933 = params['hn_932_933']
        hm = params['hm']

        print(loc)

        J_931_932 = abs((E1_932 - S_931) / L_931_932)
        print(f'J_931_932 = {J_931_932:0.4f}')
        print(f'J_932_933 = {J_932_933:0.4f}\n')

        hn_931_932 = hd.strickler_circ_h(k_st, J_931_932, Q, D_931_932)
        print(f'hn_931_932 = {hn_931_932:0.3f} m')
        print(f'hn_932_933 = {hn_932_933:0.3f} m')
        print(f'hm = {hm:0.3f} m\n')

        print(f'Q = {Q:0.3f} m^3/s')
        Qnm = hd.strickler_circ_q(k_st, J_932_933, D_932_933, hm)
        print(f'Qnm  = {Qnm:0.3f} m^3/s')
        perc_diff = Qnm / Q * 100
        print(f'{perc_diff:0.1f} % vom SOLL Abfluss')
        print(((25*'-') + '\n'))
