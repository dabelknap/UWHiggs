"""
Common selections used in DblH
"""

from FinalStateAnalysis.PlotTools.decorators import memo


@memo
def getVar(name, var):
    return name + var


def muSelection(row, name):
    if not getattr(row, getVar(name, 'IsGlobal')):
        return False
    if getattr(row, getVar(name, 'Pt')) < 5.0:
        return False
    if getattr(row, getVar(name, 'AbsEta')) > 2.4:
        return False
    if getattr(row, getVar(name, 'PixHits')) < 1:
        return False
    if getattr(row, getVar(name, 'GlbTrkHits')) <= 10:
        return False
    if getattr(row, getVar(name, 'NormTrkChi2')) >= 10.0:
        return False
    if getattr(row, getVar(name, 'TkLayersWithMeasurement')) <= 8:
        return False
    if getattr(row, getVar(name, 'MuonHits')) < 1:
        return False
    if getattr(row, getVar(name, 'MatchedStations')) < 2:
        return False
    if getattr(row, getVar(name, 'PVDXY')) > 2.0:
        return False
    if getattr(row, getVar(name, 'IP3DS')) >= 4.0:
        return False

    return True


def eleSelection(row, name):
    if getattr(row, getVar(name, 'Pt')) < 15.0:
        return False
    if getattr(row, getVar(name, 'AbsEta')) > 2.5:
        return False
    if getattr(row, getVar(name, 'PVDXY')) > 2.0:
        return False
    if getattr(row, getVar(name, 'IP3DS')) >= 4.0:
        return False

    return True
