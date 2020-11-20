# **************************************************************************
# *
# * Authors:     Federico P. de Isidro Gomez (fp.deisidro@cnb.csi.es) [1]
# *
# * [1] Centro Nacional de Biotecnologia, CSIC, Spain
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os
from pyworkflow.object import Set
import pyworkflow.protocol.params as params
import pyworkflow.utils.path as path
from pwem.protocols import EMProtocol
import tomo.objects as tomoObj
from tomo.protocols import ProtTomoBase
from imod import Plugin
from pwem.emlib.image import ImageHandler


class ProtImodTomoProjection(EMProtocol, ProtTomoBase):
    """
    Re-project a tomogram given a geometric description (axis and angles).
    More info:
        https://bio3d.colorado.edu/imod/doc/man/xyzproj.html
    """

    _label = 'tomo projection'

    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 2

    # -------------------------- DEFINE param functions -----------------------
    def _defineParams(self, form):
        form.addSection('Input')
        form.addParam('inputSetOfTomograms',
                      params.PointerParam,
                      pointerClass='SetOfTomograms',
                      important=True,
                      label='Input set of tomograms')

        form.addParam('minAngle',
                      params.FloatParam,
                      default=-60.0,
                      label='Minimum angle of rotation',
                      important=True,
                      help='Minimum angle of the projection range')

        form.addParam('maxAngle',
                      params.FloatParam,
                      default=60.0,
                      label='Maximum angle of rotation',
                      important=True,
                      help='Maximum angle of the projection range')

        form.addParam('stepAngle',
                      params.FloatParam,
                      default=-60.0,
                      label='Step angle of rotation',
                      important=True,
                      help='Step angle of the projection range')

    # -------------------------- INSERT steps functions ---------------------
    def _insertAllSteps(self):
        for tomo in self.inputSetOfTomograms.get():
            self._insertFunctionStep('projectTomogram', tomo.getObjId())
            self._insertFunctionStep('generateOutputStackStep', tomo.getObjId())

    # --------------------------- STEPS functions ----------------------------
    def convertInputStep(self, tomoObjId):
        tomo = self.inputSetOfTomograms.get()[tomoObjId]
        tsId = tomo.getTsId()
        extraPrefix = self._getExtraPath(tsId)
        tmpPrefix = self._getTmpPath(tsId)
        path.makePath(tmpPrefix)
        path.makePath(extraPrefix)

        """Apply the transformation form the input tilt-series"""
        outputTsFileName = os.path.join(tmpPrefix, tomo.getFirstItem().parseFileName())
        tomo.applyTransform(outputTsFileName)

    def generateOutputStackStep(self, tsObjId):
        outputNormalizedSetOfTiltSeries = self.getOutputNormalizedSetOfTiltSeries()

        ts = self.inputSetOfTiltSeries.get()[tsObjId]
        tsId = ts.getTsId()

        extraPrefix = self._getExtraPath(tsId)
        tmpPrefix = self._getTmpPath(tsId)

        paramsNewstack = {
            'input': os.path.join(tmpPrefix, ts.getFirstItem().parseFileName()),
            'output': os.path.join(extraPrefix, ts.getFirstItem().parseFileName(suffix="_norm")),
            'bin': int(self.binning.get()),
            'imagebinned': 1.0,
        }

        argsNewstack = "-input %(input)s " \
                       "-output %(output)s " \
                       "-bin %(bin)d " \
                       "-imagebinned %(imagebinned)s "

        if self.floatDensities.get() != 0:
            argsNewstack += " -FloatDensities " + str(self.floatDensities.get())

            if self.floatDensities.get() == 2:
                if self.meanSdToggle.get() == 0:
                    argsNewstack += " -MeanAndStandardDeviation " + str(self.scaleMean.get()) + "," + \
                                    str(self.scaleSd.get())

            elif self.floatDensities.get() == 4:
                argsNewstack += " -ScaleMinAndMax " + str(self.scaleMax.get()) + "," + str(self.scaleMin.get())

            else:
                if self.scaleRangeToggle.get() == 0:
                    argsNewstack += " -ScaleMinAndMax " + str(self.scaleRangeMax.get()) + "," + \
                                    str(self.scaleRangeMin.get())

        if self.getModeToOutput() is not None:
            argsNewstack += " -ModeToOutput " + str(self.getModeToOutput())

        Plugin.runImod(self, 'newstack', argsNewstack % paramsNewstack)

        newTs = tomoObj.TiltSeries(tsId=tsId)
        newTs.copyInfo(ts)
        outputNormalizedSetOfTiltSeries.append(newTs)

        if self.binning > 1:
            newTs.setSamplingRate(ts.getSamplingRate() * int(self.binning.get()))

        for index, tiltImage in enumerate(ts):
            newTi = tomoObj.TiltImage()
            newTi.copyInfo(tiltImage, copyId=True)
            newTi.setLocation(index + 1, (os.path.join(extraPrefix, tiltImage.parseFileName(suffix="_norm"))))
            if self.binning > 1:
                newTi.setSamplingRate(tiltImage.getSamplingRate() * int(self.binning.get()))
            newTs.append(newTi)

        ih = ImageHandler()
        x, y, z, _ = ih.getDimensions(newTs.getFirstItem().getFileName())
        newTs.setDim((x, y, z))

        newTs.write(properties=False)
        outputNormalizedSetOfTiltSeries.update(newTs)
        outputNormalizedSetOfTiltSeries.updateDim()
        outputNormalizedSetOfTiltSeries.write()
        self._store()

    # --------------------------- UTILS functions ----------------------------
    def getOutputNormalizedSetOfTiltSeries(self):
        if hasattr(self, "outputNormalizedSetOfTiltSeries"):
            self.outputNormalizedSetOfTiltSeries.enableAppend()
        else:
            outputNormalizedSetOfTiltSeries = self._createSetOfTiltSeries(suffix='Normalized')
            outputNormalizedSetOfTiltSeries.copyInfo(self.inputSetOfTiltSeries.get())
            outputNormalizedSetOfTiltSeries.setDim(self.inputSetOfTiltSeries.get().getDim())
            if self.binning > 1:
                samplingRate = self.inputSetOfTiltSeries.get().getSamplingRate()
                samplingRate *= self.binning.get()
                outputNormalizedSetOfTiltSeries.setSamplingRate(samplingRate)
            outputNormalizedSetOfTiltSeries.setStreamState(Set.STREAM_OPEN)
            self._defineOutputs(outputNormalizedSetOfTiltSeries=outputNormalizedSetOfTiltSeries)
            self._defineSourceRelation(self.inputSetOfTiltSeries, outputNormalizedSetOfTiltSeries)
        return self.outputNormalizedSetOfTiltSeries

    def getRotationAxis(self):
        parseParamsOutputMode = {
            self.AXIS_X: 'X',
            self.AXIS_Y: 'Y',
            self.AXIS_Z: 'Z',
        }
        return parseParamsOutputMode[self.modeToOutput.get()]

    # --------------------------- INFO functions ----------------------------
    def _validate(self):
        validateMsgs = []

        if self.minAngle.get() > self.maxAngle.get():
            validateMsgs = "ERROR: Maximum angle of rotation bigger than minimum"

        if (self.maxAngle.get() - self.minAngle.get()) <self.stepAngle.get():
            validateMsgs = "ERROR: Angle step of rotation bigger than range"

        return validateMsgs

    def _summary(self):
        summary = []
        if hasattr(self, 'outputNormalizedSetOfTiltSeries'):
            summary.append("Input Tilt-Series: %d.\nInterpolations applied: %d.\n"
                           % (self.inputSetOfTiltSeries.get().getSize(),
                              self.outputNormalizedSetOfTiltSeries.getSize()))
        else:
            summary.append("Output classes not ready yet.")
        return summary

    def _methods(self):
        methods = []
        if hasattr(self, 'outputNormalizedSetOfTiltSeries'):
            methods.append("%d tilt-series have been normalized using the IMOD newstack program.\n"
                           % (self.outputNormalizedSetOfTiltSeries.getSize()))
        else:
            methods.append("Output classes not ready yet.")
        return methods
