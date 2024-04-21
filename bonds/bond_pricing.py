#!/usr/bin/env python
"""A bond pricing calculator"""
__author__ = "Sumeet Vaidya"


def bond_price(fv: float, t: int, coupon: float, freq: int, y: float) -> float:
    print(f'==> bond_price FV={fv} T={t} coupon={coupon} freq={freq} yield={y}')
    n_periods = t * freq
    ytm = y / 100
    coupon_freq = ((coupon / freq) * fv) / 100
    mtm = 0
    cf_temp = 0
    dt = [(i + 1) / freq for i in range(int(n_periods))]
    for n in dt:
        cf_temp += coupon_freq / (1 + ytm / freq) ** (freq * n)
    mtm = cf_temp + (fv / (1 + ytm / freq) ** (freq * t))
    print(f'<== bond_price FV={fv} T={t} coupon={coupon} freq={freq} yield={y} MTM={mtm:.6f}')
    return mtm


def main():
    face_value = 100
    t = 5
    coupon = 5
    freq = 12
    y = 5.1
    bond_mtm = bond_price(face_value, t, coupon, freq, y)


if __name__ == "__main__":
    main()
