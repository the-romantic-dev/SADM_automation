import sympy as sp
from sympy import symbols as smb
from sympy import Eq
from sympy import Rational

rho = Rational(10)
P = {
    "800": smb("P_800"),
    "701": smb("P_701"),
    "611": smb("P_611"),
    "521": smb("P_521"),
    "431": smb("P_431"),
    "341": smb("P_341"),
    "251": smb("P_251"),
    "161": smb("P_161"),
    "071": smb("P_071"),
    "602": smb("P_602"),
    "512": smb("P_512"),
    "422": smb("P_422"),
    "332": smb("P_332"),
    "242": smb("P_242"),
    "152": smb("P_152"),
    "062": smb("P_062"),
    "503": smb("P_503"),
    "413": smb("P_413"),
    "323": smb("P_323"),
    "233": smb("P_233"),
    "143": smb("P_143"),
    "053": smb("P_053"),
    "404": smb("P_404"),
    "314": smb("P_314"),
    "224": smb("P_224"),
    "134": smb("P_134"),
    "044": smb("P_044"),
    "305": smb("P_305"),
    "215": smb("P_215"),
    "125": smb("P_125"),
    "035": smb("P_035"),
    "206": smb("P_206"),
    "116": smb("P_116"),
    "026": smb("P_026"),
    "107": smb("P_107"),
    "017": smb("P_017"),
    "008": smb("P_008"),
}
mu = 10
nu = 1
equations = [
    Eq(P["800"] * mu, P["701"] * nu),
    Eq(P["701"] * (mu + nu), mu * P["800"] + P["602"] * 2 * nu + P["611"] * nu),
    Eq(P["611"] * (mu + nu), 0.1 * mu * P["701"] + P["521"] * nu + P["512"] * nu),
    Eq(P["521"] * (mu + nu), 0.1 * mu * P["611"] + P["431"] * nu + P["422"] * nu),
    Eq(P["431"] * (mu + nu), 0.1 * mu * P["521"] + P["341"] * nu + P["332"] * nu),
    Eq(P["341"] * (mu + nu), 0.1 * mu * P["431"] + P["251"] * nu + P["242"] * nu),
    Eq(P["251"] * (mu + nu), 0.1 * mu * P["341"] + P["161"] * nu + P["152"] * nu),
    Eq(P["161"] * (mu + nu), 0.1 * mu * P["251"] + P["071"] * nu + P["062"] * nu),
    Eq(P["071"] * nu, 0.1 * mu * P["161"]),
    Eq(P["602"] * (mu + 2 * nu), 0.9 * mu * P["701"] + P["503"] * 3 * nu + P["512"] * nu),
    Eq(P["512"] * (mu + 2 * nu), 0.9 * mu * P["611"] + 0.2 * mu * P["602"] + P["413"] * 2 * nu + P["422"] * nu),
    Eq(P["422"] * (mu + 2 * nu), 0.9 * mu * P["521"] + 0.2 * mu * P["512"] + P["323"] * 2 * nu + P["332"] * nu),
    Eq(P["332"] * (mu + 2 * nu), 0.9 * mu * P["431"] + 0.2 * mu * P["422"] + P["233"] * 2 * nu + P["242"] * nu),
    Eq(P["242"] * (mu + 2 * nu), 0.9 * mu * P["341"] + 0.2 * mu * P["332"] + P["143"] * 2 * nu + P["152"] * nu),
    Eq(P["152"] * (mu + 2 * nu), 0.9 * mu * P["251"] + 0.2 * mu * P["242"] + P["053"] * 2 * nu + P["062"] * nu),
    Eq(P["062"] * 2 * nu, 0.9 * mu * P["161"] + 0.2 * mu * P["152"]),
    Eq(P["503"] * (mu + 3 * nu), 0.8 * mu * P["602"] + P["404"] * 4 * nu + P["413"] * nu),
    Eq(P["413"] * (mu + 3 * nu), 0.8 * mu * P["512"] + 0.3 * mu * P["503"] + P["314"] * 3 * nu + P["323"] * nu),
    Eq(P["323"] * (mu + 3 * nu), 0.8 * mu * P["422"] + 0.3 * mu * P["413"] + P["224"] * 3 * nu + P["233"] * nu),
    Eq(P["233"] * (mu + 3 * nu), 0.8 * mu * P["332"] + 0.3 * mu * P["323"] + P["134"] * 3 * nu + P["143"] * nu),
    Eq(P["143"] * (mu + 3 * nu), 0.8 * mu * P["242"] + 0.3 * mu * P["233"] + P["044"] * 3 * nu + P["053"] * nu),
    Eq(P["053"] * 3 * nu, 0.8 * mu * P["152"] + 0.3 * mu * P["143"]),
    Eq(P["404"] * (mu + 4 * nu), 0.7 * mu * P["503"] + P["305"] * 5 * nu + P["314"] * nu),
    Eq(P["314"] * (mu + 4 * nu), 0.7 * mu * P["413"] + 0.4 * mu * P["404"] + P["215"] * 4 * nu + P["224"] * nu),
    Eq(P["224"] * (mu + 4 * nu), 0.7 * mu * P["323"] + 0.4 * mu * P["314"] + P["125"] * 4 * nu + P["134"] * nu),
    Eq(P["134"] * (mu + 4 * nu), 0.7 * mu * P["233"] + 0.4 * mu * P["224"] + P["035"] * 4 * nu + P["044"] * nu),
    Eq(P["044"] * 4 * nu, 0.7 * mu * P["143"] + 0.4 * mu * P["134"]),
    Eq(P["305"] * (mu + 5 * nu), 0.6 * mu * P["404"] + P["206"] * 6 * nu + P["215"] * nu),
    Eq(P["215"] * (mu + 5 * nu), 0.6 * mu * P["314"] + 0.5 * mu * P["305"] + P["116"] * 5 * nu + P["125"] * nu),
    Eq(P["125"] * (mu + 5 * nu), 0.6 * mu * P["224"] + 0.5 * mu * P["215"] + P["026"] * 5 * nu + P["035"] * nu),
    Eq(P["035"] * 5 * nu, 0.6 * mu * P["134"] + 0.5 * mu * P["125"]),
    Eq(P["206"] * (mu + 6 * nu), 0.5 * mu * P["305"] + P["107"] * 7 * nu + P["116"] * nu),
    Eq(P["116"] * (mu + 6 * nu), 0.5 * mu * P["215"] + 0.6 * mu * P["206"] + P["017"] * 6 * nu + P["026"] * nu),
    Eq(P["026"] * 6 * nu, 0.5 * mu * P["125"] + 0.6 * mu * P["116"]),
    Eq(P["107"] * (mu + 7 * nu), 0.4 * mu * P["206"] + P["008"] * 8 * nu + P["017"] * nu),
    Eq(P["017"] * 7 * nu, 0.4 * mu * P["116"] + 0.7 * mu * P["107"]),
    Eq(P["008"] * 8 * nu, 0.3 * mu * P["107"]),
    sp.Eq(sum(P.values()), 1),
]
solution = sp.solve(equations, *list(P.values()), dict=True)[0]
for s in solution:
    print(f"{sp.pretty(s)}:")
    print(float(solution[s]))

ps = [solution[P[f"0{8-i-1}{i+1}"]] for i in range(8)]
print(1 - sum(ps))
ks = [f"{i}{j-1}{8-i-j+1}" for i in range(2, 8 + 1) for j in range(1, 8 - i + 1)]
ks.append("800")
ksm = ([int(i[0]) - 1 for i in ks])
ksm_res = [solution[P[ks[i]]] * ksm[i] for i in range(len(ks))]

print(sum(ksm_res))

fsm = {f"{8-i-j}{j}{i}": i for i in range(1, 8 + 1) for j in range(8 - i + 1)}

print(sum([solution[P[i]] * fsm[i] for i in fsm]))

print(sum([solution[P[i]] * int(i[1]) for i in P]))
