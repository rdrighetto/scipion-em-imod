# **************************************************************************
# *
# * Authors:     Federico P. de Isidro Gomez (fp.deisidro@cnb.csic.es) [1]
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

from pyworkflow.tests import *
from imod.protocols import *
from pwem.emlib.image import ImageHandler
import tomo


class TestImodBase(BaseTest):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)

    @classmethod
    def _runImportTiltSeries(cls, filesPath, pattern, voltage, magnification, sphericalAberration, amplitudeContrast,
                             samplingRate, doseInitial, dosePerFrame, anglesFrom=0, minAngle=0.0, maxAngle=0.0,
                             stepAngle=1.0):
        cls.protImportTS = cls.newProtocol(tomo.protocols.ProtImportTs,
                                           filesPath=filesPath,
                                           filesPattern=pattern,
                                           voltage=voltage,
                                           anglesFrom=anglesFrom,
                                           magnification=magnification,
                                           sphericalAberration=sphericalAberration,
                                           amplitudeContrast=amplitudeContrast,
                                           samplingRate=samplingRate,
                                           doseInitial=doseInitial,
                                           dosePerFrame=dosePerFrame,
                                           minAngle=minAngle,
                                           maxAngle=maxAngle,
                                           stepAngle=stepAngle)
        cls.launchProtocol(cls.protImportTS)
        return cls.protImportTS

    @classmethod
    def _runImportTransformationMatrix(cls, filesPath, pattern, exclusionWords, inputSetOfTiltSeries):
        cls.protImportTM = cls.newProtocol(ProtImodImportTransformationMatrix,
                                           filesPath=filesPath,
                                           filesPattern=pattern,
                                           exclusionWords=exclusionWords,
                                           inputSetOfTiltSeries=inputSetOfTiltSeries,)
        cls.launchProtocol(cls.protImportTM)
        return cls.protImportTM

    @classmethod
    def _runXRaysEraser(cls, inputSoTS, peakCriterion, diffCriterion, maximumRadius, bigDiffCriterion):
        cls.protXRaysEraser = cls.newProtocol(ProtImodXraysEraser,
                                              inputSetOfTiltSeries=inputSoTS,
                                              peakCriterion=peakCriterion,
                                              diffCriterion=diffCriterion,
                                              maximumRadius=maximumRadius,
                                              bigDiffCriterion=bigDiffCriterion)
        cls.launchProtocol(cls.protXRaysEraser)
        return cls.protXRaysEraser

    @classmethod
    def _runDoseFilter(cls, inputSoTS, initialDose, inputDoseType, fixedImageDose):
        cls.protDoseFilter = cls.newProtocol(ProtImodDoseFilter,
                                            inputSetOfTiltSeries=inputSoTS,
                                            initialDose=initialDose,
                                            inputDoseType=inputDoseType,
                                            fixedImageDose=fixedImageDose)
        cls.launchProtocol(cls.protDoseFilter)
        return cls.protDoseFilter

    @classmethod
    def _runExcludeViews(cls, inputSoTS, excludeViewsFile):
        cls.protExcludeViews = cls.newProtocol(ProtImodExcludeViews,
                                               inputSetOfTiltSeries=inputSoTS,
                                               excludeViewsFile=excludeViewsFile)
        cls.launchProtocol(cls.protExcludeViews)
        return cls.protExcludeViews

    @classmethod
    def _runTSNormalization(cls, inputSoTS, binning, floatDensities, modeToOutput, scaleRangeToggle, scaleRangeMax,
                            scaleRangeMin, meanSdToggle, scaleMean, scaleSd, scaleMax, scaleMin):
        cls.protTSNormalization = cls.newProtocol(ProtImodTSNormalization,
                                                  inputSetOfTiltSeries=inputSoTS,
                                                  binning=binning,
                                                  floatDensities=floatDensities,
                                                  modeToOutput=modeToOutput,
                                                  scaleRangeToggle=scaleRangeToggle,
                                                  scaleRangeMax=scaleRangeMax,
                                                  scaleRangeMin=scaleRangeMin,
                                                  meanSdToggle=meanSdToggle,
                                                  scaleMean=scaleMean,
                                                  scaleSd=scaleSd,
                                                  scaleMax=scaleMax,
                                                  scaleMin=scaleMin)
        cls.launchProtocol(cls.protTSNormalization)
        return cls.protTSNormalization

    @classmethod
    def _runXcorrPrealignment(cls, inputSoTS, computeAlignmentToggle, binning, rotationAngle):
        cls.protXcorr = cls.newProtocol(ProtImodXcorrPrealignment,
                                        inputSetOfTiltSeries=inputSoTS,
                                        computeAlignment=computeAlignmentToggle,
                                        binning=binning,
                                        rotationAngle=rotationAngle)
        cls.launchProtocol(cls.protXcorr)
        return cls.protXcorr

    @classmethod
    def _runFiducialAlignemnt(cls, inputSoTS, twoSurfaces, fiducialDiameter, numberFiducial, rotationAngle,
                              computeAlignment, binning):
        cls.protFiducialAlignment = cls.newProtocol(ProtImodFiducialAlignment,
                                                    inputSetOfTiltSeries=inputSoTS,
                                                    twoSurfaces=twoSurfaces,
                                                    fiducialDiameter=fiducialDiameter,
                                                    numberFiducial=numberFiducial,
                                                    rotationAngle=rotationAngle,
                                                    computeAlignment=computeAlignment,
                                                    binning=binning)
        cls.launchProtocol(cls.protFiducialAlignment)
        return cls.protFiducialAlignment

    @classmethod
    def _runApplyTransformationMatrix(cls, inputSoTS, binning):
        cls.protApplyTransformationMatrix = cls.newProtocol(ProtImodApplyTransformationMatrix,
                                                            inputSetOfTiltSeries=inputSoTS,
                                                            binning=binning)
        cls.launchProtocol(cls.protApplyTransformationMatrix)
        return cls.protApplyTransformationMatrix

    @classmethod
    def _runTomoReconstruction(cls, inputSoTS, tomoThickness, tomoShiftX, tomoShiftZ, angleOffset, tiltAxisOffset,
                               fakeInteractionsSIRT, radialFirstParameter, radialSecondParameter):
        cls.protTomoReconstruction = cls.newProtocol(ProtImodTomoReconstruction,
                                                     inputSetOfTiltSeries=inputSoTS,
                                                     tomoThickness=tomoThickness,
                                                     tomoShiftX=tomoShiftX,
                                                     tomoShiftZ=tomoShiftZ,
                                                     angleOffset=angleOffset,
                                                     tiltAxisOffset=tiltAxisOffset,
                                                     fakeInteractionsSIRT=fakeInteractionsSIRT,
                                                     radialFirstParameter=radialFirstParameter,
                                                     radialSecondParameter=radialSecondParameter)
        cls.launchProtocol(cls.protTomoReconstruction)
        return cls.protTomoReconstruction

    @classmethod
    def _runTomoNormalization(cls, inputSetOfTomograms, binning, floatDensities, modeToOutput, scaleRangeToggle,
                              scaleRangeMax, scaleRangeMin, meanSdToggle, scaleMean, scaleSd, scaleMax, scaleMin):
        cls.protTomoNormalization = cls.newProtocol(ProtImodTomoNormalization,
                                                    inputSetOfTomograms=inputSetOfTomograms,
                                                    binning=binning,
                                                    floatDensities=floatDensities,
                                                    modeToOutput=modeToOutput,
                                                    scaleRangeToggle=scaleRangeToggle,
                                                    scaleRangeMax=scaleRangeMax,
                                                    scaleRangeMin=scaleRangeMin,
                                                    meanSdToggle=meanSdToggle,
                                                    scaleMean=scaleMean,
                                                    scaleSd=scaleSd,
                                                    scaleMax=scaleMax,
                                                    scaleMin=scaleMin)
        cls.launchProtocol(cls.protTomoNormalization)
        return cls.protTomoNormalization

    @classmethod
    def _runGoldBeadPeaker3D(cls, inputSetOfTomograms, beadDiameter, beadsColor, minRelativeStrength, minSpacing):
        cls.protGoldBeadPicker3d = cls.newProtocol(ProtImodGoldBeadPicker3d,
                                                   inputSetOfTomograms=inputSetOfTomograms,
                                                   beadDiameter=beadDiameter,
                                                   beadsColor=beadsColor,
                                                   minRelativeStrength=minRelativeStrength,
                                                   minSpacing=minSpacing)
        cls.launchProtocol(cls.protGoldBeadPicker3d)
        return cls.protGoldBeadPicker3d

    @classmethod
    def _runTomoProjection(cls, inputSetOfTomograms, minAngle, maxAngle, stepAngle, rotationAxis):
        cls.protTomoProjection = cls.newProtocol(ProtImodTomoProjection,
                                                 inputSetOfTomograms=inputSetOfTomograms,
                                                 minAngle=minAngle,
                                                 maxAngle=maxAngle,
                                                 stepAngle=stepAngle,
                                                 rotationAxis=rotationAxis)
        cls.launchProtocol(cls.protTomoProjection)
        return cls.protTomoProjection

    @classmethod
    def _runCTFEstimation(cls, inputSoTS, defocusTol, expectedDefocusOrigin, expectedDefocusValue, expectedDefocusFile,
                          axisAngle, interactiveMode, leftDefTol, rightDefTol, tileSize, angleStep, angleRange,
                          startFreq, endFreq, extraZerosToFit, skipAstigmaticViews, searchAstigmatism,
                          findAstigPhaseCutonToggle, phaseShiftAstigmatism, cutOnFrequencyAstigmatism,
                          minimumViewsAstigmatism, minimumViewsPhaseShift, numberSectorsAstigmatism,
                          maximumAstigmatism):
        cls.protCTFEstimation = cls.newProtocol(ProtImodAutomaticCtfEstimation,
                                                inputSet=inputSoTS,
                                                defocusTol=defocusTol,
                                                expectedDefocusOrigin=expectedDefocusOrigin,
                                                expectedDefocusValue=expectedDefocusValue,
                                                expectedDefocusFile=expectedDefocusFile,
                                                axisAngle=axisAngle,
                                                interactiveMode=interactiveMode,
                                                leftDefTol=leftDefTol,
                                                rightDefTol=rightDefTol,
                                                tileSize=tileSize,
                                                angleStep=angleStep,
                                                angleRange=angleRange,
                                                startFreq=startFreq,
                                                endFreq=endFreq,
                                                extraZerosToFit=extraZerosToFit,
                                                skipAstigmaticViews=skipAstigmaticViews,
                                                searchAstigmatism=searchAstigmatism,
                                                findAstigPhaseCutonToggle=findAstigPhaseCutonToggle,
                                                phaseShiftAstigmatism=phaseShiftAstigmatism,
                                                cutOnFrequencyAstigmatism=cutOnFrequencyAstigmatism,
                                                minimumViewsAstigmatism=minimumViewsAstigmatism,
                                                minimumViewsPhaseShift=minimumViewsPhaseShift,
                                                numberSectorsAstigmatism=numberSectorsAstigmatism,
                                                maximumAstigmatism=maximumAstigmatism)
        cls.launchProtocol(cls.protCTFEstimation)
        return cls.protCTFEstimation

    @classmethod
    def _runCTFCorrection(cls, inputSetOfTiltSeries, inputSetOfCtfTomoSeries, defocusTol, interpolationWidth):
        cls.protCTFCorrection = cls.newProtocol(ProtImodCtfCorrection,
                                                inputSetOfTiltSeries=inputSetOfTiltSeries,
                                                inputSetOfCtfTomoSeries=inputSetOfCtfTomoSeries,
                                                defocusTol=defocusTol,
                                                interpolationWidth=interpolationWidth)
        cls.launchProtocol(cls.protCTFCorrection)
        return cls.protCTFCorrection


class TestImodReconstructionWorkflow(TestImodBase):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)

        cls.inputDataSet = DataSet.getDataSet('tomo-em')
        cls.inputSoTS = cls.inputDataSet.getFile('ts1')

        cls.excludeViewsFile = cls.inputDataSet.getFile('excludeViewsFile')

        cls.excludeViewsOutputSizes = [57, 56]

        cls.binningTsNormalization = 2

        cls.binningPrealignment = 2

        cls.binningFiducialAlignment = 2

        cls.binningApplyTransformMatrix = 2

        cls.thicknessTomo = 100

        cls.binningTomoNormalization = 2

        cls.protImportTS = cls._runImportTiltSeries(filesPath=os.path.split(cls.inputSoTS)[0],
                                                    pattern="BB{TS}.st",
                                                    anglesFrom=0,
                                                    voltage=300,
                                                    magnification=105000,
                                                    sphericalAberration=2.7,
                                                    amplitudeContrast=0.1,
                                                    samplingRate=20.2,
                                                    doseInitial=0,
                                                    dosePerFrame=0.3,
                                                    minAngle=-55,
                                                    maxAngle=65.0,
                                                    stepAngle=2.0)

        cls.protXRaysEraser = cls._runXRaysEraser(inputSoTS=cls.protImportTS.outputTiltSeries,
                                                  peakCriterion=8.0,
                                                  diffCriterion=6.0,
                                                  maximumRadius=4.2,
                                                  bigDiffCriterion=19)

        cls.protDoseFilter = cls._runDoseFilter(inputSoTS=cls.protXRaysEraser.outputSetOfTiltSeries,
                                                initialDose=0,
                                                inputDoseType=1,
                                                fixedImageDose=0.2)

        cls.protExcludeViews = cls._runExcludeViews(inputSoTS=cls.protXRaysEraser.outputSetOfTiltSeries,
                                                    excludeViewsFile=cls.excludeViewsFile)

        cls.protTSNormalization = cls._runTSNormalization(inputSoTS=cls.protDoseFilter.outputSetOfTiltSeries,
                                                          binning=cls.binningTsNormalization,
                                                          floatDensities=0,
                                                          modeToOutput=0,
                                                          scaleRangeToggle=1,
                                                          scaleRangeMax=255,
                                                          scaleRangeMin=0,
                                                          meanSdToggle=1,
                                                          scaleMean=0,
                                                          scaleSd=1,
                                                          scaleMax=255,
                                                          scaleMin=0)

        cls.protXcorr = cls._runXcorrPrealignment(inputSoTS=cls.protDoseFilter.outputSetOfTiltSeries,
                                                  computeAlignmentToggle=0,
                                                  binning=cls.binningPrealignment,
                                                  rotationAngle=-12.5)

        cls.protFiducialAlignment = cls._runFiducialAlignemnt(inputSoTS=cls.protXcorr.outputSetOfTiltSeries,
                                                              twoSurfaces=0,
                                                              fiducialDiameter=4.95,
                                                              numberFiducial=25,
                                                              rotationAngle=0,
                                                              computeAlignment=0,
                                                              binning=cls.binningFiducialAlignment)

        cls.protApplyTransformationMatrix = \
            cls._runApplyTransformationMatrix(inputSoTS=cls.protFiducialAlignment.outputSetOfTiltSeries,
                                              binning=cls.binningApplyTransformMatrix)

        cls.protTomoReconstruction = \
            cls._runTomoReconstruction(inputSoTS=cls.protFiducialAlignment.outputSetOfTiltSeries,
                                       tomoThickness=cls.thicknessTomo,
                                       tomoShiftX=0.0,
                                       tomoShiftZ=0.0,
                                       angleOffset=0.0,
                                       tiltAxisOffset=0.0,
                                       fakeInteractionsSIRT=0,
                                       radialFirstParameter=0.35,
                                       radialSecondParameter=0.035)

        cls.protTomoNormalization = \
            cls._runTomoNormalization(inputSetOfTomograms=cls.protTomoReconstruction.outputSetOfTomograms,
                                      binning=cls.binningTomoNormalization,
                                      floatDensities=0,
                                      modeToOutput=0,
                                      scaleRangeToggle=1,
                                      scaleRangeMax=255,
                                      scaleRangeMin=0,
                                      meanSdToggle=1,
                                      scaleMean=0,
                                      scaleSd=1,
                                      scaleMax=255,
                                      scaleMin=0)

        cls.protGoldBeadPicker3D = \
            cls._runGoldBeadPeaker3D(inputSetOfTomograms=cls.protTomoReconstruction.outputSetOfTomograms,
                                     beadDiameter=10,
                                     beadsColor=0,
                                     minRelativeStrength=0.05,
                                     minSpacing=0.9)

        cls.protTomoProjection = \
            cls._runTomoProjection(inputSetOfTomograms=cls.protTomoNormalization.outputNormalizedSetOfTomograms,
                                   minAngle=-60.0,
                                   maxAngle=60.0,
                                   stepAngle=2.0,
                                   rotationAxis=1)

    def test_doseFitlerOutputTS(self):
        self.assertIsNotNone(self.protDoseFilter.outputSetOfTiltSeries)

        tsId = self.protDoseFilter.outputSetOfTiltSeries.getFirstItem().getTsId()

        self.assertTrue(os.path.exists(os.path.join(self.protDoseFilter._getExtraPath(tsId), "BB" + tsId + ".st")))

    def test_xRaysEraserOutputTS(self):
        self.assertIsNotNone(self.protXRaysEraser.outputSetOfTiltSeries)

        tsId = self.protXRaysEraser.outputSetOfTiltSeries.getFirstItem().getTsId()

        self.assertTrue(os.path.exists(os.path.join(self.protXRaysEraser._getExtraPath(tsId), "BB" + tsId + ".st")))

    def test_excludeViewsOutputTS(self):
        self.assertIsNotNone(self.protExcludeViews.outputSetOfTiltSeries)

        tsId = self.protExcludeViews.outputSetOfTiltSeries.getFirstItem().getTsId()

        self.assertTrue(os.path.exists(os.path.join(self.protExcludeViews._getExtraPath(tsId), "BB" + tsId + ".st")))

    def test_excludeViewsOutputTSSize(self):
        for index, tsOut in enumerate(self.protExcludeViews.outputSetOfTiltSeries):
            self.assertTrue(tsOut.getSize() == self.excludeViewsOutputSizes[index])

    def test_normalizationOutputTS(self):
        self.assertIsNotNone(self.protTSNormalization.outputNormalizedSetOfTiltSeries)

        tsId = self.protTSNormalization.outputNormalizedSetOfTiltSeries.getFirstItem().getTsId()

        self.assertTrue(os.path.exists(os.path.join(self.protTSNormalization._getExtraPath(tsId), "BB" + tsId + ".st")))

    def test_normalizationOutputTSSamplingRate(self):
        inSamplingRate = self.protTSNormalization.inputSetOfTiltSeries.get().getSamplingRate()
        outSamplingRate = self.protTSNormalization.outputNormalizedSetOfTiltSeries.getSamplingRate()

        self.assertTrue(inSamplingRate * self.binningTsNormalization == outSamplingRate)

    def test_prealignmentOutputTS(self):
        self.assertIsNotNone(self.protXcorr.outputSetOfTiltSeries)

        tsId = self.protXcorr.outputSetOfTiltSeries.getFirstItem().getTsId()
        outputLocation = os.path.join(self.protXcorr._getExtraPath(tsId), "BB" + tsId + ".st")

        self.assertTrue(os.path.exists(outputLocation))

    def test_prealignmentTransformMatrixOutputTS(self):
        self.assertIsNotNone(self.protXcorr.outputSetOfTiltSeries.getFirstItem().getFirstItem().getTransform())

    def test_prealignmentOutputInterpolatedTS(self):
        self.assertIsNotNone(self.protXcorr.outputInterpolatedSetOfTiltSeries)

        tsId = self.protXcorr.outputInterpolatedSetOfTiltSeries.getFirstItem().getTsId()
        outputLocation = os.path.join(self.protXcorr._getExtraPath(tsId), "BB" + tsId + ".st")

        self.assertTrue(os.path.exists(outputLocation))

    def test_prealignmentOutputInterpolatedTSSamplingRate(self):
        inSamplingRate = self.protXcorr.inputSetOfTiltSeries.get().getSamplingRate()
        outSamplingRate = self.protXcorr.outputInterpolatedSetOfTiltSeries.getSamplingRate()

        self.assertTrue(inSamplingRate * self.binningPrealignment == outSamplingRate)

    def test_fiducialAlignmentOutputTS(self):
        self.assertIsNotNone(self.protFiducialAlignment.outputSetOfTiltSeries)

        tsId = self.protFiducialAlignment.outputSetOfTiltSeries.getFirstItem().getTsId()
        outputLocation = os.path.join(self.protFiducialAlignment._getExtraPath(tsId), "BB" + tsId + ".st")

        self.assertTrue(os.path.exists(outputLocation))

    def test_fiducialAlignmentTransformMatrixOutputTS(self):
        self.assertIsNotNone(
            self.protFiducialAlignment.outputSetOfTiltSeries.getFirstItem().getFirstItem().getTransform())

    def test_fiducialAlignmentOutputInterpolatedTS(self):
        self.assertIsNotNone(self.protFiducialAlignment.outputInterpolatedSetOfTiltSeries)

        tsId = self.protFiducialAlignment.outputInterpolatedSetOfTiltSeries.getFirstItem().getTsId()
        outputLocation = os.path.join(self.protFiducialAlignment._getExtraPath(tsId), "BB" + tsId + ".st")

        self.assertTrue(os.path.exists(outputLocation))

    def test_fiducialAlignmentOutputInterpolatedTSSamplingRate(self):
        inSamplingRate = self.protFiducialAlignment.inputSetOfTiltSeries.get().getSamplingRate()
        outSamplingRate = self.protFiducialAlignment.outputInterpolatedSetOfTiltSeries.getSamplingRate()

        self.assertTrue(inSamplingRate * self.binningFiducialAlignment == outSamplingRate)

    # def test_fiducialAlignmentOutputFiducialModelGaps(self):
    #     self.assertIsNotNone(self.protFiducialAlignment.outputFiducialModelGaps)
    #
    #     tsId = self.protFiducialAlignment.outputInterpolatedSetOfTiltSeries.getFirstItem().getTsId()
    #     outputLocation = os.path.join(self.protFiducialAlignment._getExtraPath(tsId), "BB" + tsId + "_resid.txt")
    #
    #     self.assertTrue(os.path.exists(outputLocation))
    #
    # def test_fiducialAlignmentOutputFiducialModelGapsSize(self):
    #     self.assertTrue(self.protFiducialAlignment.outputFiducialModelGaps.getSize() == 2)

    def test_fiducialAlignmentOutputFiducialModelNoGaps(self):
        self.assertIsNotNone(self.protFiducialAlignment.outputFiducialModelNoGaps)

        tsId = self.protFiducialAlignment.outputInterpolatedSetOfTiltSeries.getFirstItem().getTsId()
        outputLocation = os.path.join(self.protFiducialAlignment._getExtraPath(tsId), "BB" + tsId + "_noGaps.sfid")

        self.assertTrue(os.path.exists(outputLocation))

    def test_fiducialAlignmentOutputFiducialModelNoGapsSize(self):
        self.assertTrue(self.protFiducialAlignment.outputFiducialModelNoGaps.getSize() == 2)

    def test_fiducialAlignmentOutputCoordinates3D(self):
        self.assertIsNotNone(self.protFiducialAlignment.outputSetOfCoordinates3D)

        tsId = self.protFiducialAlignment.outputInterpolatedSetOfTiltSeries.getFirstItem().getTsId()
        outputLocation = os.path.join(self.protFiducialAlignment._getExtraPath(tsId), "BB" + tsId + "_fid.xyz")

        self.assertTrue(os.path.exists(outputLocation))

    def test_fiducialAlignmentOutputCoordinates3DSize(self):
        tolerance = 2
        expectedSize = 34

        self.assertTrue(
            abs(self.protFiducialAlignment.outputSetOfCoordinates3D.getSize() - expectedSize) <= tolerance)

    def test_applyTransformationMatrixOutputInterpolatedTS(self):
        self.assertIsNotNone(self.protApplyTransformationMatrix.outputInterpolatedSetOfTiltSeries)

        tsId = self.protFiducialAlignment.outputInterpolatedSetOfTiltSeries.getFirstItem().getTsId()
        outputLocation = os.path.join(self.protApplyTransformationMatrix._getExtraPath(tsId), "BB" + tsId + ".st")

        self.assertTrue(os.path.exists(outputLocation))

    def test_applyTransformationMatrixOutputInterpolatedTSSamplingRate(self):
        inSamplingRate = self.protApplyTransformationMatrix.inputSetOfTiltSeries.get().getSamplingRate()
        outSamplingRate = self.protApplyTransformationMatrix.outputInterpolatedSetOfTiltSeries.getSamplingRate()

        self.assertTrue(inSamplingRate * self.binningApplyTransformMatrix == outSamplingRate)

    def test_tomoReconstructionOutputTomogram(self):
        self.assertIsNotNone(self.protTomoReconstruction.outputSetOfTomograms)

        tomoId = self.protTomoReconstruction.inputSetOfTiltSeries.get().getFirstItem().getTsId()
        outputLocation = os.path.join(self.protTomoReconstruction._getExtraPath(tomoId), "BB" + tomoId + ".mrc")

        self.assertTrue(os.path.exists(outputLocation))

    def test_tomoReconstructionOutputTomogramSize(self):
        self.assertEqual(self.protTomoReconstruction.outputSetOfTomograms.getSize(), 2)

    def test_tomoReconstructionOutputTomogramDimensions(self):
        ih = ImageHandler()
        outputDimensions = ih.getDimensions(self.protTomoReconstruction.outputSetOfTomograms.getFirstItem())

        self.assertTrue(outputDimensions == (512, 512, self.thicknessTomo, 1))

    def test_goldBeadPeaker3DOutput(self):
        self.assertIsNotNone(self.protGoldBeadPicker3D.outputSetOfCoordinates3D)

        tomoId = self.protGoldBeadPicker3D.inputSetOfTomograms.get().getFirstItem().getTsId()
        location = self.protGoldBeadPicker3D._getExtraPath("BB" + tomoId)

        self.assertTrue(os.path.exists(os.path.join(location, "BB" + tomoId + ".mod")))

    def test_goldBeadPeaker3DOutputCoordinates3DSize(self):
        tolerance = 1
        expectedSize = 14

        self.assertTrue(
            abs(self.protGoldBeadPicker3D.outputSetOfCoordinates3D.getSize() - expectedSize) <= tolerance)

    def test_tomoNormalizationOutput(self):
        self.assertIsNotNone(self.protTomoNormalization.outputNormalizedSetOfTomograms)

        location = self.protTomoNormalization.inputSetOfTomograms.get().getFirstItem().getLocation()[1]
        fileName, _ = os.path.splitext(location)
        tomoId = os.path.basename(fileName)

        self.assertTrue(os.path.exists(os.path.join(self.protTomoNormalization._getExtraPath(tomoId), tomoId + ".mrc")))

    def test_tomoNormalizationOutputSize(self):
        self.assertTrue(self.protTomoNormalization.outputNormalizedSetOfTomograms.getSize() == 2)

    def test_tomoNormalizationOutputSamplingRate(self):
        inSamplingRate = self.protTomoNormalization.inputSetOfTomograms.get().getSamplingRate()
        outSamplingRate = self.protTomoNormalization.outputNormalizedSetOfTomograms.getSamplingRate()

        self.assertTrue(inSamplingRate * self.binningTomoNormalization == outSamplingRate)

    def test_tomoProjectionOutputTiltSeriesSize(self):
        self.assertTrue(self.protTomoProjection.outputProjectedSetOfTiltSeries.getSize() == 2)

    def test_tomoProjectionOutputTiltSeriesDimension(self):
        ih = ImageHandler()
        outputDimensions = ih.getDimensions(
            self.protTomoProjection.outputProjectedSetOfTiltSeries.getFirstItem().getFirstItem().getFileName())

        self.assertTrue(outputDimensions == (256, 256, 61, 1))

    def test_tomoProjectionOutputTiltSeriesSamplingRate(self):
        inSamplingRate = self.protTomoProjection.inputSetOfTomograms.get().getSamplingRate()
        outSamplingRate = self.protTomoProjection.outputProjectedSetOfTiltSeries.getSamplingRate()

        self.assertTrue(inSamplingRate == outSamplingRate)


class TestImodCTFCorrectionWorkflow(TestImodBase):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)

        cls.inputDataSet = DataSet.getDataSet('tutorialDataImodCTF')
        cls.inputSoTS = cls.inputDataSet.getFile('tsCtf1')

        cls.protImportTS = cls._runImportTiltSeries(filesPath=os.path.split(cls.inputSoTS)[0],
                                                    pattern="*.mdoc",
                                                    anglesFrom=0,
                                                    voltage=300,
                                                    magnification=50000,
                                                    sphericalAberration=0.0,
                                                    amplitudeContrast=0.07,
                                                    samplingRate=6.73981,
                                                    doseInitial=0,
                                                    dosePerFrame=0.3)

        cls.protCTFEstimation = cls._runCTFEstimation(inputSoTS=cls.protImportTS.outputTiltSeries,
                                                      defocusTol=200.0,
                                                      expectedDefocusOrigin=0,
                                                      expectedDefocusValue=6000,
                                                      expectedDefocusFile="",
                                                      axisAngle=0.0,
                                                      interactiveMode=1,
                                                      leftDefTol=2000.0,
                                                      rightDefTol=2000.0,
                                                      tileSize=256,
                                                      angleStep=2.0,
                                                      angleRange=20.0,
                                                      startFreq=0.0,
                                                      endFreq=0.0,
                                                      extraZerosToFit=0.0,
                                                      skipAstigmaticViews=1,
                                                      searchAstigmatism=1,
                                                      findAstigPhaseCutonToggle=1,
                                                      phaseShiftAstigmatism=0,
                                                      cutOnFrequencyAstigmatism=0,
                                                      minimumViewsAstigmatism=3,
                                                      minimumViewsPhaseShift=1,
                                                      numberSectorsAstigmatism=36,
                                                      maximumAstigmatism=1.2)

        cls.protCTFCorrection = cls._runCTFCorrection(inputSetOfTiltSeries=cls.protImportTS.outputTiltSeries,
                                                      inputSetOfCtfTomoSeries=cls.protCTFEstimation.outputSetOfCTFTomoSeries,
                                                      defocusTol=200,
                                                      interpolationWidth=15)

    def test_ctfEstimationOutputSize(self):
        self.assertIsNotNone(self.protCTFEstimation.outputSetOfCTFTomoSeries)

        self.assertTrue(self.protCTFEstimation.outputSetOfCTFTomoSeries.getSize() == 1)

    def test_ctfEstimationOutputDefocusFile(self):
        tsId = self.protCTFEstimation.inputSet.get().getFirstItem().getTsId()
        defocusFile = os.path.join(self.protCTFEstimation._getExtraPath(tsId), '%s.defocus' % tsId)

        self.assertTrue(os.path.exists(defocusFile))

    def test_ctfCorrectionOutput(self):
        self.assertIsNotNone(self.protCTFCorrection.outputCtfCorrectedSetOfTiltSeries)

        tsId = self.protCTFCorrection.outputCtfCorrectedSetOfTiltSeries.getFirstItem().getTsId()
        outputLocation = os.path.join(self.protCTFCorrection._getExtraPath(tsId), "WTI042413_1series4.st")

        self.assertTrue(os.path.exists(outputLocation))
