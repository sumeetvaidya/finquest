#!/usr/bin/env python
"""A bond pricing calculator"""
__author__ = "Sumeet Vaidya"

#from scipy import optimize
import numpy as np
import scipy.optimize as optimize
import math


def bond_price(fv: float, t: int, coupon: float, freq: int, y: float) -> float:
    """
    Function to compute a bond price based on face value, term, coupon, frequency
    and yield to compute mark to market or mtm price
    :rtype: float
    """
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


def bond_ytm(price: float, fv: float, t: int, coupon: float, freq: int) -> float:
    """
    Function to compute yield to maturity
    :param price: Price of the bond
    :param fv: Face Value of the bond
    :param t: Time in years
    :param coupon: Coupon rate
    :param freq: Number of times the coupon pays yearly
    :return: float the yield to maturity
    """
    print(f'==> bond_ytm Price={price} FV={fv} T={t} coupon={coupon} freq={freq}')
    guess = 0.5
    n_periods = t * freq
    coupon_freq = ((coupon / freq) * fv) / 100
    dt = [(i + 1) / freq for i in range(int(n_periods))]
    ytm = optimize.newton(
        lambda x: (sum([coupon_freq / (1 + x / freq) ** (freq * t0) for t0 in dt]) + fv / (1 + x / freq) ** (
                freq * t)) - price, guess)
    print(f'<== bond_price Price={price} FV={fv} T={t} coupon={coupon} freq={freq}  YTM={ytm:.2f}')
    return ytm


def calc_spot_rate(price: float, tenors, coupons, fv: float, freq: int):
    """
    Function to compute spot rates based on tenors and coupon rates
    :param price: Price of the bond
    :param tenors: Tenor list
    :param coupons: Coupon by Tenor list
    :param fv: Face value
    :param freq: Frequency
    :return: spot rate array
    """
    print(f'==> calc_spot_rate Price={price} FV={fv} Tenors={tenors.tolist()} coupons={coupons.tolist()} freq={freq}')
    guess = 0.5
    # initialize spot rate array
    spot_array = np.zeros(tenors.shape)

    for i in range(0, len(tenors)):
        if i <= 1:
            spot_array[i] = coupons[i] / 100
        else:
            n_periods = i
            coupon = ((coupons[i] / 100) * fv) / freq
            cf_temp = 0
            counter = 0
            dt = [(j + 1) / freq for j in range(int(n_periods))]

            for t in dt:
                cf_temp = cf_temp + (coupon / (1 + spot_array[counter] / freq) ** (counter + 1))
                counter += 1

            zero_rate = lambda x: (cf_temp + (fv + coupon) / (1 + x / freq) ** (counter + 1)) - price
            opt = optimize.newton(zero_rate, guess)
            spot_array[i] = opt
    print(f'<== calc_spot_rate spot={spot_array.tolist()}')

    return spot_array


def main():
    face_value = 100
    t = 5
    coupon = 5
    freq = 12
    y = 5.1
    bond_mtm = bond_price(face_value, t, coupon, freq, y)
    price = 100
    bond_ytm(price, face_value, t, coupon, freq)

    # setup tenors
    tenors = np.array([0.5, 1, 1.5, 2])

    # setup coupon list
    coupon_list = np.array([3, 4, 5, 5.5])

    freq_semi_annual = 2

    spot_array = calc_spot_rate(price, tenors, coupon_list, face_value, freq_semi_annual)


if __name__ == "__main__":
    main()
