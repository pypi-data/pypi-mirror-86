﻿# -*- coding: utf-8 -*-
r"""
see crl_stack.py
"""
__author__ = "Konstantin Klementiev, Roman Chernikov"
__date__ = "08 Mar 2016"
import matplotlib as mpl
mpl.use('agg')
import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import numpy as np
import matplotlib.pyplot as plt

import xrt.backends.raycing as raycing
import xrt.backends.raycing.sources as rs
import xrt.backends.raycing.oes as roe
import xrt.backends.raycing.run as rr
import xrt.backends.raycing.materials as rm
import xrt.backends.raycing.screens as rsc

import xrt.plotter as xrtp
import xrt.runner as xrtr

parabolaParam = 1.  # mm
zmax = 1.  # mm
E0 = 9000.  # eV
p = 1000.  # source to 1st lens
q = 5000.  # 1st lens to focus
xyLimits = -5, 5

#Lens = roe.ParaboloidFlatLens
Lens = roe.DoubleParaboloidLens
#Lens = roe.ParabolicCylinderFlatLens
if Lens == roe.DoubleParaboloidLens:
    lensName = '2-'
elif Lens == roe.ParaboloidFlatLens:
    lensName = '1-'
else:
    lensName = '3-'


def build_beamline(nrays=1e4):
    beamLine = raycing.BeamLine(height=0)
#    rs.CollimatedMeshSource(beamLine, 'CollimatedMeshSource', dx=2, dz=2,
#      nx=21, nz=21, energies=(E0,), withCentralRay=False, autoAppendToBL=True)
    rs.GeometricSource(
        beamLine, 'CollimatedSource', nrays=nrays,
        dx=0.5, dz=0.5, distxprime=None, distzprime=None, energies=(E0,))

    beamLine.fsm1 = rsc.Screen(beamLine, 'FSM1', (0, p - 100, 0))

    beamLine.lens = Lens(
        beamLine, 'Lenslet', pitch=np.pi/2, t=0,
        focus=parabolaParam, zmax=zmax, alarmLevel=0.1)

    beamLine.fsm2 = rsc.Screen(beamLine, 'FSM2')
#    beamLine.fsm2.dqs = np.linspace(-140, 140, 71)
    beamLine.fsm2.dqs = np.linspace(-70, 70, 15)
    return beamLine


def run_process(beamLine):
    beamSource = beamLine.sources[0].shine()
    outDict = {'beamSource': beamSource}
    beamFSM1 = beamLine.fsm1.expose(beamSource)
    outDict['beamFSM1'] = beamFSM1
    beamIn = beamSource
    for ilens in range(int(round(beamLine.curMaterial.nCRL))):
        if Lens == roe.ParabolicCylinderFlatLens:
            if ilens % 2 == 0:
                beamLine.lens.roll = -np.pi / 4
            else:
                beamLine.lens.roll = np.pi / 4
        lglobal, llocal1, llocal2 = beamLine.lens.double_refract(
            beamIn, needLocal=False)
        beamIn = lglobal
#        outDict['beamLensGlobal_{0:02d}'.format(ilens)] = lglobal
#        outDict['beamLensLocal1_{0:02d}'.format(ilens)] = llocal1
#        outDict['beamLensLocal2_{0:02d}'.format(ilens)] = llocal2
        beamLine.lens.center[1] += zmax
    for i, dq in enumerate(beamLine.fsm2.dqs):
        beamLine.fsm2.center[1] = p + q + dq
        outDict['beamFSM2_{0:02d}'.format(i)] = beamLine.fsm2.expose(lglobal)
    return outDict
rr.run_process = run_process


def get_nCRL(material, parabParam, f, E, nFactor):
    material.nCRL = 2 * parabParam / f /\
        (1 - material.get_refractive_index(E).real) * nFactor


def define_plots(beamLine):
    plots = []

    xrtp.yTextPosNraysR = 0.82
    xrtp.yTextPosNrays1 = 0.52

    plot0 = xrtp.XYCPlot(
        'beamFSM1', (1,),
        xaxis=xrtp.XYCAxis(
            r'$x$', 'mm', limits=[-1.2, 1.2], fwhmFormatStr=None),
        yaxis=xrtp.XYCAxis(
            r'$z$', 'mm', limits=[-1.2, 1.2], fwhmFormatStr=None),
        ePos=0, title=beamLine.fsm1.name)
    plots.append(plot0)

#    plot1 = xrtp.XYCPlot(
#        'beamLensLocal1_{0:02d}'.format(0), (1,),
#        xaxis=xrtp.XYCAxis(
#            r'$x$', 'mm', limits=[-1.2, 1.2], fwhmFormatStr=None),
#        yaxis=xrtp.XYCAxis(
#            r'$y$', 'mm', limits=[-1.2, 1.2], fwhmFormatStr=None),
#        ePos=0, title='LensFootprint1_00')
#    plots.append(plot1)

    fwhmFormatStrF = '%.2f'
    plotsFSM2 = []
    for i, dq in enumerate(beamLine.fsm2.dqs):
        plot2 = xrtp.XYCPlot(
            'beamFSM2_{0:02d}'.format(i), (1,),
            xaxis=xrtp.XYCAxis(
                r'$x$', u'µm', limits=xyLimits, bins=250, ppb=1),
            yaxis=xrtp.XYCAxis(
                r'$z$', u'µm', limits=xyLimits, bins=250, ppb=1),
            ePos=0, title=beamLine.fsm2.name+'-{0:02d}'.format(i))
        plot2.xaxis.fwhmFormatStr = fwhmFormatStrF
        plot2.yaxis.fwhmFormatStr = fwhmFormatStrF
        plot2.textPanel = plot2.fig.text(
            0.2, 0.75, '', transform=plot2.fig.transFigure, size=14, color='r',
            ha='left')
        plot2.textPanelTemplate = '{0}: d$q=${1:+.0f} mm'.format('{0}', dq)
        plots.append(plot2)
        plotsFSM2.append(plot2)

#        plot3 = xrtp.XYCPlot('beamFSM2_{0:02d}'.format(i), (1,),
#          xaxis=xrtp.XYCAxis(r'$x$', u'µm', limits=xyLimits),
#          yaxis=xrtp.XYCAxis(r'$z$', u'µm', limits=xyLimits),
#          caxis=xrtp.XYCAxis('degree of polarization', '',
#          data=raycing.get_polarization_degree, limits=[0, 1]),
#          ePos=1, title=beamLine.fsm2.name+'PolDegree'+'-{0:02d}'.format(i))
#        plot3.textPanel = plot3.fig.text(
#            0.2, 0.75, '', transform=plot3.fig.transFigure,
#            size=14, color='r', ha='left')
#        plots.append(plot3)
#
#        plot4 = xrtp.XYCPlot('beamFSM2_{0:02d}'.format(i), (1,),
#          xaxis=xrtp.XYCAxis(r'$x$', u'µm', limits=xyLimits),
#          yaxis=xrtp.XYCAxis(r'$z$', u'µm', limits=xyLimits),
#          caxis=xrtp.XYCAxis('circular polarization rate', '',
#          data=raycing.get_circular_polarization_rate, limits=[-1, 1]),
#          ePos=1, title=beamLine.fsm2.name+'CircPolRate'+'-{0:02d}'.format(i))
#        plot4.textPanel = plot4.fig.text(
#            0.2, 0.75, '', transform=plot4.fig.transFigure,
#            size=14, color='r', ha='left')
#        plots.append(plot4)
#
#        plot5 = xrtp.XYCPlot('beamFSM2_{0:02d}'.format(i), (1,),
#          xaxis=xrtp.XYCAxis(r'$x$', u'µm', limits=xyLimits),
#          yaxis=xrtp.XYCAxis(r'$z$', u'µm', limits=xyLimits),
#          caxis=xrtp.XYCAxis('ratio of ellipse axes', '',
#          data=raycing.get_ratio_ellipse_axes, limits=[-1, 1]),
#          ePos=1,
#          title=beamLine.fsm2.name+'PolAxesRatio'+'-{0:02d}'.format(i))
#        plot5.textPanel = plot5.fig.text(
#            0.2, 0.75, '', transform=plot5.fig.transFigure,
#            size=14, color='r', ha='left')
#        plots.append(plot5)
#
#        plot6 = xrtp.XYCPlot('beamFSM2_{0:02d}'.format(i), (1,),
#          xaxis=xrtp.XYCAxis(r'$x$', u'µm', limits=xyLimits),
#          yaxis=xrtp.XYCAxis(r'$z$', u'µm', limits=xyLimits),
#          caxis=xrtp.XYCAxis('angle of polarization ellipse', '',
#          data=raycing.get_polarization_psi, limits=[-90, 90]),
#          ePos=1, title=beamLine.fsm2.name+'PolPsi'+'-{0:02d}'.format(i))
#        plot6.ax1dHistE.set_yticks([-90,-45,0,45,90])
#        plot6.textPanel = plot6.fig.text(
#            0.2, 0.75, '', transform=plot6.fig.transFigure,
#            size=14, color='r', ha='left')
#        plots.append(plot6)
    return plots, plotsFSM2


def plot_generator(plots, plotsFSM2, beamLine):
    if Lens == roe.DoubleParaboloidLens:
        nFactor = 0.5
    elif Lens == roe.ParaboloidFlatLens:
        nFactor = 1.
    else:
        nFactor = 2.

    mBeryllium = rm.Material('Be', rho=1.848, kind='lens')
    get_nCRL(mBeryllium, parabolaParam, q, E0, nFactor)
    mDiamond = rm.Material('C', rho=3.52, kind='lens')
    get_nCRL(mDiamond, parabolaParam, q, E0, nFactor)
    mAluminum = rm.Material('Al', rho=2.7, kind='lens')
    get_nCRL(mAluminum, parabolaParam, q, E0, nFactor)
    mSilicon = rm.Material('Si', rho=2.33, kind='lens')
    get_nCRL(mSilicon, parabolaParam, q, E0, nFactor)
    mNickel = rm.Material('Ni', rho=8.9, kind='lens')
    get_nCRL(mNickel, parabolaParam, q, E0, nFactor)
    mLead = rm.Material('Pb', rho=11.35, kind='lens')
    get_nCRL(mLead, parabolaParam, q, E0, nFactor)

#    materials = mBeryllium, mDiamond, mAluminum, mSilicon, mNickel, mLead
    materials = mBeryllium, mDiamond

    print('At E = {0} eV and parabola focus = {1} mm:'.format(
          E0, parabolaParam))
    for material in materials:
        print(' n({0}) = {1}'.format(material.elements[0].name, material.nCRL))

#    polarization = [
#        'horizontal', 'vertical', '+45', '-45', 'right', 'left', None]
    polarization = 'hor',

    figDF = plt.figure(figsize=(7, 5), dpi=72)
    ax1 = plt.subplot(111)
    ax1.set_title(r'FWHM size of beam cross-section near focal position')
    ax1.set_xlabel(r'd$q$ (mm)', fontsize=14)
    ax1.set_ylabel(u'FWHM size (µm)', fontsize=14)

    figI = plt.figure(figsize=(7, 5), dpi=72)
    ax2 = plt.subplot(111)
    ax2.set_title(r'relative flux at sample position')
    ax2.set_xlabel('material', fontsize=14)
    ax2.set_ylabel(u'flux (a.u.)', fontsize=14)

    prefix = 'CRL-indiv-'

    for pol in polarization:
        beamLine.sources[0].polarization = pol
        suffix = pol
        if suffix is None:
            suffix = 'none'
        xMaterials = []
        yFlux = []
        for material in materials:
            beamLine.curMaterial = material
            beamLine.lens.material = material
            beamLine.lens.center = [0, p, 0]
            elem = material.elements[0].name
            print(elem)
            for plot in plots:
                fileName = '{0}{1}{2}-{3}-{4}'.format(
                    prefix, lensName, elem, suffix, plot.title)
                plot.saveName = fileName + '.png'
#                plot.persistentName = fileName + '.pickle'
                try:
                    plot.textPanel.set_text(
                        plot.textPanelTemplate.format(elem))
                except AttributeError:
                    pass
            yield
            xCurve = []
            yCurve = []
            for dq, plot in zip(beamLine.fsm2.dqs, plotsFSM2):
                if plot.dx < (xyLimits[1] - xyLimits[0]) * 0.5:
#                    print(dq, plot.dx)
                    xCurve.append(dq)
                    yCurve.append(plot.dx)
            yFlux.append(plotsFSM2[-1].intensity)
            ax1.plot(
                xCurve, yCurve, 'o', label='{0}, n={1:.0f}'.format(
                    elem, round(material.nCRL)))
            xMaterials.append(elem)
    ax1.legend(loc=4)  # lower right
    figDF.savefig(prefix + lensName + 'depthOfFocus.png')
#    plt.close(figDF)

    rects = ax2.bar(np.arange(len(materials)) + 0.1,
                    np.array(yFlux)/max(yFlux), bottom=1e-3, log=True)
    for rect, material in zip(rects, materials):
        height = rect.get_height()
        ax2.text(
            rect.get_x()+rect.get_width()/2., 0.9*height,
            'n=%d' % material.nCRL, ha='center', va='top', color='w')
    ax2.set_xticks(np.arange(len(materials)) + 0.5)
    ax2.set_xticklabels(xMaterials)
    ax2.set_ylim(1e-3, 1)
    figI.savefig(prefix + lensName + 'Flux.png')


def main():
    beamLine = build_beamline()
    plots, plotsFSM2 = define_plots(beamLine)
    xrtr.run_ray_tracing(
        plots, repeats=16, generator=plot_generator,
        generatorArgs=[plots, plotsFSM2, beamLine],
        updateEvery=1, beamLine=beamLine, processes='half')

#this is necessary to use multiprocessing in Windows, otherwise the new Python
#contexts cannot be initialized:
if __name__ == '__main__':
    main()
