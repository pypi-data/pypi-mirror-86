depends = ('ITKPyBase', 'ITKSmoothing', 'ITKImageFilterBase', 'ITKIOImageBase', 'ITKCommon', )
templates = (
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterID2ID2', True, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('SmoothingRecursiveYvvGaussianImageFilter', 'itk::SmoothingRecursiveYvvGaussianImageFilter', 'itkSmoothingRecursiveYvvGaussianImageFilterID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
)
snake_case_functions = ('smoothing_recursive_yvv_gaussian_image_filter', )
