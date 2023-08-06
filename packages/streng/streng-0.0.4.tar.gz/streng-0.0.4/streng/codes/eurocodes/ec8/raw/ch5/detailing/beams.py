"""
EC8 detailing functions for beams

    .. uml::

        class beams <<(M,#FF7700)>> {
        .. functions ..
        + ρmin(fck, fyk)
        + ρmax(ρ2, μφ, εsyd, fcd, fyd)
        + ρmax05(μφ, εsyd, fcd, fyd)
        }
"""

from .....ec2.raw.ch3.concrete import strength as conc_strength


def ρmin(fck, fyk):
    return 0.5 * conc_strength.fctm(fck) / fyk


def ρmax(ρ2, μφ, εsyd, fcd, fyd):
    return ρ2 + 0.0018 * fcd / (μφ * εsyd * fyd)


def ρmax05(μφ, εsyd, fcd, fyd):
    return 2 * 0.0018 * fcd / (μφ * εsyd * fyd)
