depends = ('ITKPyBase', 'ITKMesh', 'ITKIOImageBase', 'ITKCommon', )
templates = (
  ('GaussianDistanceKernel', 'itk::GaussianDistanceKernel', 'itkGaussianDistanceKernelF', False, 'float'),
  ('GaussianDistanceKernel', 'itk::GaussianDistanceKernel', 'itkGaussianDistanceKernelD', False, 'double'),
)
snake_case_functions = ()
