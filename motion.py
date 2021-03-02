import os
import SimpleITK as sitk
import sys

pdir = os.getcwd()
filedir = 'resp_motion'
indir = f'{pdir}/{filedir}'
os.chdir(indir)
# image = sitk.ReadImage(f'{indir}/resp_motion1.nii')
# sitk.WriteImage(image, 'testITK.nii')


def command_iteration(filter):
    print(f"{filter.GetElapsedIterations():3} = {filter.GetMetric():10.5f}")


# if len(sys.argv) < 4:
#     print(
#         f"Usage: {sys.argv[0]} <fixedImageFilter> <movingImageFile> <outputTransformFile>")
#     sys.exit(1)

print('attempts to open nii files')
fixed = sitk.ReadImage(f'{indir}/resp_motion1.nii')
moving = sitk.ReadImage(f'{indir}/resp_motion2.nii')

print('attempts to perform a histogram matching algorithm')
matcher = sitk.HistogramMatchingImageFilter()
matcher.SetNumberOfHistogramLevels(1024)
matcher.SetNumberOfMatchPoints(7)  ## bigger number - TODO
matcher.ThresholdAtMeanIntensityOn()
moving = matcher.Execute(moving, fixed)

# The basic Demons Registration Filter
# Note there is a whole family of Demons Registration algorithms included in
# SimpleITK
print('attempts to perform a demons registration filter')
demons = sitk.DemonsRegistrationFilter()
demons.SetNumberOfIterations(100)
# Standard deviation for Gaussian smoothing of displacement field
demons.SetStandardDeviations(1.0)
demons.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(demons))
displacementField = demons.Execute(fixed, moving)

sitk.WriteImage(displacementField, 'disp.nii')

print("-------")
print(f"Number Of Iterations: {demons.GetElapsedIterations()}")
print(f" RMS: {demons.GetRMSChange()}")

outTx = sitk.DisplacementFieldTransform(displacementField)

# sitk.WriteTransform(outTx, 'transform.nii')

resampler = sitk.ResampleImageFilter()
resampler.SetReferenceImage(moving)
# resampler.SetInterpolator(sitk.sitkLinear) # check that later - linear??
resampler.SetInterpolator(sitk.sitkBSplineResampler) # check that later - linear??
# resampler.SetInterpolator(sitk.sitkNearestNeighbor) # check that later - linear??
resampler.SetDefaultPixelValue(1)  # ? should be smaller like 1
resampler.SetTransform(outTx)

out = resampler.Execute(moving)
# out = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)

sitk.WriteImage(out, 'out.nii')

simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
# Use the // floor division operator so that the pixel type is
# the same for all three images which is the expectation for
# the compose filter.
cimg = sitk.Compose(simg1, simg2, simg1 // 2. + simg2 // 2.)
sitk.WriteImage(cimg, 'cimg.nii')
